from typing import *
import heapq

""" 
https://leetcode.cn/contest/weekly-contest-440
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
    """
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        seg = SegementTree(baskets)
        ans = 0; n = len(fruits)
        for f in fruits:
            i = seg.find_first_and_update(1, 0, n-1, f)
            if i == -1:
                ans += 1
        return ans

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

    # 找到区间内第一个 >= x 的数, 返回下标
    def find_first(self, o: int, l: int, r: int, x: int) -> int:
        if self.max[o] < x: return -1
        if l==r: return l
        m = (l+r) // 2
        i = self.find_first(o*2, l, m, x)
        if i < 0:
            i = self.find_first(o*2+1, m+1, r, x)
        return i
    # 更新
    def update(self, o: int, l: int, r: int, i: int, x: int) -> None:
        if l==r:
            self.max[l] = x
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
    sol.numOfUnplacedFruits(fruits = [4,2,5], baskets = [3,5,4]),
]
for r in result:
    print(r)
