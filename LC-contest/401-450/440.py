from typing import *
import heapq

""" 
https://leetcode.cn/contest/weekly-contest-440
T2 最小堆维护前 k 大
T3 线段树经典题型! 灵神视频详细讲解了一下
T4 一道很有意思的思维题, 图式思维+概念抽象很重要!
Easonsi @2025 """
class Solution:
    """ 3477. 水果成篮 II """
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        ans = 0
        for f in fruits:
            for i,b in enumerate(baskets):
                if b >= f:
                    baskets[i] = -1
                    break
            else:
                ans += 1
        return ans
    
    """ 3478. 选出和最大的 K 个元素 #medium 
思路1: 最小堆维护前 k 大
    """
    def findMaxSum(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        nums = [(a,b,i) for i,(a,b) in enumerate(zip(nums1, nums2))]
        nums.sort(key=lambda x: x[0])
        ans = [None]*len(nums); acc = 0; h = []
        pre = -1; buffer = []
        for a,b,i in nums:
            if a == pre:
                buffer.append(b)
                ans[i] = acc
            else:
                for x in buffer:
                    if len(h) < k:
                        heapq.heappush(h, x)
                        acc += x
                    else:
                        if x > h[0]:
                            acc -= h[0]
                            heapq.heappop(h)
                            heapq.heappush(h, x)
                            acc += x
                buffer = [b]
                pre = a
                ans[i] = acc
        return ans
    
    """ 3479. 水果成篮 III #hard 对于n个fruits和baskets, for i in fruits, 每次从baskets从找到最左侧的未放置的, 满足 >= f 的篮子放置. 问最终未放置的水果数量
限制: n 1e5
思路1: #线段树 二分
    一道标准的线段树题目
    线段树适合哪些问题? 
        - 区间查询!
ling: https://leetcode.cn/problems/fruits-into-baskets-iii/solutions/3603049/xian-duan-shu-er-fen-pythonjavacgo-by-en-ssqf/
    video: https://www.bilibili.com/video/BV15gRaYZE5o/
    """
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        seg = SegementTree(baskets)
        ans = 0; n = len(fruits)
        for f in fruits:
            # op1: 写成一个函数
            # i = seg.find_first_and_update(1, 0, n-1, f)
            # if i == -1:
            #     ans += 1

            # op2: 分开写
            i = seg.find_first(1, 0, n-1, f)
            if i == -1: 
                ans += 1
            else:
                seg.update(1, 0, n-1, i, -1)
        return ans

    """ 3480. 删除一个冲突对后最大子数组数目 #hard 对于数组 [1,2,...n], 有一组冲突对 [(a,b), ...], 要求删掉一个冲突对后, 数组的所有子数组中, 不含冲突对的数量. 
限制: n 1e5
思路1: "枚举左端点，维护最小次小 b"
    考虑枚举左端点1, 它能够构成的子数组数量? (右端点, 不包含)
    例如, 对于 i=2, 相关的限制 (a>=i) 有: (2,6), (3,5), (4,7).
        显然右端点是 5
        总结: i所匹配的右端点是 "所有满足 a>=i 的限制中, 最小的b"! -- 不妨记作 b0
    简化问题: 不考虑删除的情况下, 答案就是 sum{ b0-i }
        如何求出所有的 b0? 
            从右往左遍历, 递增的记录 "所有满足 a>=i 的限制中, 最小的b" 这一信息即可 -- 不妨把所有出现过的 b 放到一个数组 B 中
    允许删除一个? 考虑带来的增量!
        在上面的例子中, 对于i=2, 删掉 (3,5) 后, 新的 b1=6, 增量就是 b1-b0
        又因为上面 "从右往左遍历" 的过程中, 我们记录了数组 B, 可以找到其中最小的两个数字 b0, b1
        如何记录整体带来的增量? 也是从右往左遍历 i, 把增量 b1-b0 记录到 b0!
        Q: 如果两个限制 (2,4), (3,4) 的右端点重复怎么办? 
            在枚举到 i=3 的时候, 假设 b0=4, b1=5, 那么删去 (3,4) 带来的增量可以被记录到!
            在枚举 i=2 的时候, b0=4, b1=4, 没有重复计算!
    复杂度: 不考虑排序 (实际上可以去掉sort操作) 的情况 O(n)
ling: https://leetcode.cn/problems/maximize-subarrays-after-removing-one-conflicting-pair/solutions/3603047/mei-ju-zuo-duan-dian-wei-hu-zui-xiao-ci-4nvu6/
"""
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # 按照右侧分组
        groups = [[] for _ in range(n+1)]
        for a,b in conflictingPairs:
            if a>b:
                a,b = b,a
            groups[a].append(b)
        # 
        acc = 0
        extra = [0] * (n+2)  # 记录删除某一约束之后带来的增量
        b = [n+1, n+1]  # 初始化, 边界为 n+1 (第一个非法位置)
        for i in range(n, 0, -1):
            b = sorted(b + groups[i])[:2]  # 只需要记录最小的两个
            acc += b[0] - i
            extra[b[0]] += b[1] - b[0]
        return acc + max(extra)


class SegementTree:
    # 线段树, 维护最大值
    # 下标使用: 维护大小在 [0, n-1] 范围内的长n的数据; 树结构的根为 1
    def __init__(self, a: list[int]):
        n = len(a)
        self.max = [0] * (4*n)
        self.build(a, 1, 0, n-1)
    def build(self, a: list[int], o: int, l: int, r: int):
        if l==r:
            self.max[o] = a[l]
            return
        m = (l+r) // 2
        self.build(a, o*2, l, m)
        self.build(a, o*2+1, m+1, r)
        self.maintain(o)
    def maintain(self, o: int):
        self.max[o] = max(self.max[o*2], self.max[o*2+1])
    
    # 找到区间内第一个 >= x 的数, 并更新为 -1, 返回下标
    def find_first_and_update(self, o: int, l: int, r: int, x: int) -> int:
        if self.max[o] < x: 
            return -1
        if l==r:
            self.max[o] = -1
            return l
        m = (l+r) // 2
        # NOTE: 这里需要递归调用! 
        i = self.find_first_and_update(o*2, l, m, x)
        if i < 0:
            i = self.find_first_and_update(o*2+1, m+1, r, x)
        self.maintain(o)  # update!
        return i

    # --------- 或者写成两个函数!
    # 找到区间内第一个 >= x 的数, 返回下标
    def find_first(self, o: int, l: int, r: int, x: int) -> int:
        if self.max[o] < x: return -1
        if l==r: return l
        m = (l+r) // 2
        i = self.find_first(o*2, l, m, x)
        if i < 0:
            i = self.find_first(o*2+1, m+1, r, x)
        return i
    # 更新: 把下标 i 的数更新为 x
    def update(self, o: int, l: int, r: int, i: int, x: int) -> None:
        if l==r:
            self.max[o] = x  # NOTE: 更新的一定是 o
            return
        m = (l+r) // 2
        if i <= m:
            self.update(o*2, l, m, i, x)
        else:
            self.update(o*2+1, m+1, r, i, x)
        self.maintain(o)
    
sol = Solution()
result = [
    # sol.findMaxSum(nums1 = [4,2,1,5,3], nums2 = [10,20,30,40,50], k = 2),
    # sol.findMaxSum(nums1 = [2,2,2,2], nums2 = [3,1,2,3], k = 1),
    # sol.numOfUnplacedFruits(fruits = [4,2,5], baskets = [3,5,4]),
    sol.maxSubarrays(n = 4, conflictingPairs = [[2,3],[1,4]]),
]
for r in result:
    print(r)
