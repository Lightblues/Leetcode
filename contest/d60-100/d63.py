from typing import List, Optional
import collections
import math
import bisect
import heapq
import functools, itertools

from torch import seed
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
# from utils_leetcode import testClass
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 2037. 使每位学生都有座位的最少移动次数
给定一组座位的位置和一组学生当前的位置, 要求对每个人匹配到合适的位置所需最少移动次数
"""
    def minMovesToSeat(self, seats: List[int], students: List[int]) -> int:
        seats.sort()
        students.sort()
        ans = 0
        for a,b in zip(seats, students):
            ans += abs(a-b)
        return ans

    """ 2038. 如果相邻两个颜色均相同则删除当前颜色 """
    def winnerOfGame(self, colors: str) -> bool:
        # 统计colors 出现的 A/B 连续个数
        countsA, countsB = [], []
        # 注意添加首尾哨兵
        lastCh = " "
        count = 0
        for ch in colors+" ":
            if ch in lastCh:
                count += 1
                continue
            if lastCh == "A":
                countsA.append(count)
            elif lastCh == "B":
                countsB.append(count)
            count = 1
            lastCh = ch
        a = sum(i-2 if i>2 else 0 for i in countsA )
        b = sum(i-2 if i>2 else 0 for i in countsB )
        return a>b
    
    """ 2039. 网络空闲的时刻
有 n 个节点, 0 号为服务器, 其他为数据节点. 节点之间通过网络连接, 经过一个时间段信息传递一条边.
现所有的数据节点需要向服务器发送信息, 服务器收到后发送反馈. 每个数据节点还有一个 patience[i], 表示在经历这么长时间没有收到回复则重发消息.
要求计算经过多少时刻后, 网络上没有数据包 (空闲).

输入：edges = [[0,1],[1,2]], patience = [0,2,1]
输出：8
参见 图 https://leetcode-cn.com/problems/the-time-when-the-network-becomes-idle/

思路: BFS+遍历
每个数据节点和服务器的关系是独立的, 因此, 分别计算每个数据节点到服务器的距离, 遍历计算即可.
对于数据节点 i 来说, 其距离和等待时间为 distance[i], patience[i], 则收到最后一个数据包的时间为: `2*distance[i] + 1 + 2*distance[i]//patience[i]*patience[i]`
其中, `2*distance[i] + 1` 是第一个数据包发送到收到回复的时间, `2*distance[i]//patience[i]*patience[i]` 是可能有的接受不了重发数据包所需的额外时间.
"""
    def networkBecomesIdle(self, edges: List[List[int]], patience: List[int]) -> int:
        # 构建图
        n = len(patience)
        edgeList = [[] for _ in range(n)]
        for u,v in edges:
            edgeList[u].append(v)
            edgeList[v].append(u)
        
        # 计算每个数据节点到服务器的距离
        distances = [math.inf]*n
        q = collections.deque([(0, 0)])
        distances[0] = 0
        visited = set([0])
        while q:
            u, d = q.popleft()
            # visited.append(u)
            # distances[u] = min(distances[u], d)
            for v in edgeList[u]:
                if v not in visited:
                    q.append((v, d+1))
                    visited.add(v)
                    distances[v] = min(distances[v], d+1)
        
        ans = 0
        for dist, pat in zip(distances[1:], patience[1:]):
            d = dist*2
            t = d + (d-1)//pat * pat + 1
            ans = max(ans, t)
        return ans


    """ 2040. 两个有序数组的第 K 小乘积
对于两个有序数组 nums1 和 nums2, 定义它们之间的交互乘积 `nums1[i] * nums2[j]`, 要求返回这些数中第 k 小的 (从1开始).
复杂度: 两数组的长度为 5e4, 数字范围为 -1e5~1e5.

输入：nums1 = [-2,-1,0,1,2], nums2 = [-3,-1,2,4,5], k = 3
输出：-6
解释：第 3 小的乘积计算如下：
- nums1[0] * nums2[4] = (-2) * 5 = -10
- nums1[0] * nums2[3] = (-2) * 4 = -8
- nums1[4] * nums2[0] = 2 * (-3) = -6
第 3 小的乘积为 -6 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/kth-smallest-product-of-two-sorted-arrays
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

思路 1: #二分查找 + #双指针 + #分类讨论
基本的思路是二分查找可能的范围 [-1e10, 1e10]
根据零将两个数组分别分为负数和非负数两部分, 然后分类统计两两组合之下, <= 待搜索的 m 的组合的数量; 由于采用双指针形式, 二分判断的复杂度为 O(L), 因此总复杂度为 O(Llog(N)), 这里 L为数组长度N为搜索空间大小.
[解答](https://leetcode-cn.com/problems/kth-smallest-product-of-two-sorted-arrays/solution/yi-ti-san-jie-shuang-zhi-zhen-jie-bu-den-sqsu/) 还可以对于四种条件进行合并讨论

思路 2: 也是二分查找框架, 不过在组合 nums1, nums2 的时候, 直接利用不等式条件, 内部进行一次二分搜索. 
这样, 内部二分的复杂度为 O(LlogL), 整体的复杂度为 O(NLlogL).
具体而言, 对于 nums1[i], 要求 nums1[i] * nums2[j] <= m, 根据 nums1[i] 与0 的关系, 可以直接计算出如 nums2[j]<=m/nums1[i], 基于这个条件进行二分搜索.

思路 3: 在上一种解法中, 复杂度增加了, 实际上我们可以通过 #前缀和 来避免内部的二分. 注意到 nums 的元素范围为 [-1e5, 1e5], 我们可以利用前缀和得到 cumsum[m] 表示数组中包括多少个小于等于 m 的元素.
"""
    def kthSmallestProduct_1(self, nums1: List[int], nums2: List[int], k: int) -> int:
        idx = bisect.bisect_left(nums1, 0)
        neg1, pos1 = nums1[:idx], nums1[idx:]
        idx = bisect.bisect_left(nums2, 0)
        neg2, pos2 = nums2[:idx], nums2[idx:]
        
        l, r = int(-1e10), int(1e10)
        while l<r:
            m = (l+r)>>1
            # 统计 num1[i]*num2[j] <=m 的pair的数量.
            """ 重点看这里的图 https://leetcode-cn.com/problems/kth-smallest-product-of-two-sorted-arrays/solution/yi-ti-san-jie-shuang-zhi-zhen-jie-bu-den-sqsu/ 
            注意下面前两种情况 j 范围为 [-1, len(num)-1], 后两种情况 j 范围 [0, len(num)]
            """
            cur = 0
            # pos1, pos2
            j = len(pos2)-1
            for i in range(len(pos1)):
                # 随着 i增大, pos1[i]正数增大; pos2[j] 的阈值应当减小, j减小. (看曲线的变化情况也行)
                # 合法区间位于曲线下方, 因此用 > 比较.
                while j>= 0 and pos2[j] * pos1[i] > m: j-= 1
                # j 的范围为 [-1, len(pos2)-1]
                cur += j+1
            # neg1, neg2
            j = len(neg2)-1
            for i in range(len(neg1)):
                # 随着 i增大, neg1[i]负数绝对值减小; neg2[j] 的绝对值阈值应当增大, j减小.
                # 合法区间位于曲线上方, 因此 <= 比较
                while j>=0 and neg2[j] * neg1[i] <= m: j-= 1
                cur += len(neg2)-(j+1)
            
            # neg1, pos2
            # j = len(pos2)-1
            # for i in range(len(neg1)-1, -1, -1):
            #     while j>=0 and pos2[j] * neg1[i] > m: j-= 1
            #     cur += len(pos2)-(j+1)
            j = 0
            for i in range(len(neg1)):
                while j<len(pos2) and pos2[j] * neg1[i] > m: j+= 1
                cur += len(pos2) - j
            # pos1, neg2
            # j = len(neg2)-1
            # for i in range(len(pos1)-1, -1, -1):
            #     while j>=0 and neg2[j] * pos1[i] > m: j-= 1
            #     cur += j+1
            j = 0
            for i in range(len(pos1)):
                while j<len(neg2) and neg2[j] * pos1[i] <= m: j+= 1
                cur += j
            
            if cur < k: l = m+1
            else: r = m
        return l

    def kthSmallestProduct2(self, nums1: List[int], nums2: List[int], k: int) -> int:
        l, r = int(-1e10), int(1e10)
        while l<r:
            m = (l+r)>>1
            cur = 0
            for a in nums1:
                if a > 0:
                    cur += bisect.bisect_right(nums2, m/a)
                elif a==0:
                    cur += len(nums2) if m>=0 else 0
                elif a<0:
                    cur += len(nums2) - bisect.bisect_left(nums2, m/a)
            if cur < k: l = m+1
            else: r = m
        return l

    def kthSmallestProduct(self, nums1: List[int], nums2: List[int], k: int) -> int:
        limit = int(1e5)
        # 计算 nums2 的前缀和: 注意到 nums 的元素范围为 [-1e5, 1e5]
        cumsum = [0] * (2*limit+1)
        for a in nums2: cumsum[a+limit] += 1
        for a in range(1, 2*limit+1): cumsum[a] += cumsum[a-1]
        def get_count(a):
            """ 返回 nums2 中小于等于 a 的数量 """
            if a < -limit: return 0
            if a >= limit: return cumsum[-1]
            return cumsum[a+limit]
        
        l, r = int(-1e10), int(1e10)
        while l<r:
            m = (l+r)>>1
            cur = 0
            for a in nums1:
                if a > 0:
                    cur += get_count(m//a)  # 求数组中 <= m/a 的数量
                elif a==0:
                    cur += len(nums2) if m>=0 else 0
                elif a < 0:
                    cur += len(nums2) - get_count(math.ceil(m/a)-1) # 求数组中 >= m/a 的数量
            if cur < k: l = m+1
            else: r = m
        return l

sol = Solution()
result = [
    # sol.minMovesToSeat(seats = [2,2,6,6], students = [1,3,2,6]),
    
    # sol.winnerOfGame(colors = "AAABABB"),
    # sol.winnerOfGame(colors = "ABBBBBBBAAA"),
    
    # sol.networkBecomesIdle(edges = [[0,1],[1,2]], patience = [0,2,1]),
    # sol.networkBecomesIdle(edges = [[0,1],[0,2],[1,2]], patience = [0,10,10]),
    
    # 8, 0, -6
    sol.kthSmallestProduct(nums1 = [2,5], nums2 = [3,4], k = 2),
    sol.kthSmallestProduct(nums1 = [-4,-2,0,3], nums2 = [2,4], k = 6),
    sol.kthSmallestProduct(nums1 = [-2,-1,0,1,2], nums2 = [-3,-1,2,4,5], k = 3),
    sol.kthSmallestProduct([-6],[-9],1),
]
for r in result:
    print(r)
