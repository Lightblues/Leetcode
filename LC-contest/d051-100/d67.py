from typing import List, Optional, Tuple
import copy
import collections
import math
import bisect
import heapq
import functools, itertools

from regex import F
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
import utils_leetcode
from structures import ListNode, TreeNode
from sortedcontainers import SortedList

""" 
https://leetcode-cn.com/contest/biweekly-contest-67
@20220513 补 """
class Solution:
    """ 2099. 找到和最大的长度为 K 的子序列 #题型 #easy
给定一个序列, 要求返回一个长度为 K 的子序列 (元素可以不连续, 但要求顺序不变), 使其和最大.
思路: 返回最大的 k 的元素, 同时要求保留idx信息.
"""
    def maxSubsequence(self, nums: List[int], k: int) -> List[int]:
        # return bisect.nlargest(k, nums)
        heap = []
        for i, num in enumerate(nums):
            if i<k:
                heapq.heappush(heap, (num, i))
                continue
            if num<=heap[0][0]: continue
            heapq.heappushpop(heap, (num, i))
        idx = sorted([i[1] for i in heap])
        return [nums[i] for i in idx]
    
    
    """ 2100. 适合打劫银行的日子 #medium #题型
求数组中所有满足条件的idx. 条件为: 该元素在 nums[i-k:i+k] 这一区间内为谷底.
思路0: 对于第i个元素, 符合条件意味着左侧长度k的区间非递增, 右侧长度k的区间非递减. 因此考虑滑动窗口: 计算窗口内的增加元素数量.
这样, 对于每个idx, 从左往右和从右往左计算 validL, validR, 汇总所有符合条件的idx即可.
这里具体实现上复杂了: 先用 isUpL, isUpR 记录每个idx是否左/右上升, 然后滑动窗口计算 validL, validR. [here](https://leetcode.cn/problems/find-good-days-to-rob-the-bank/solution/gong-shui-san-xie-qian-zhui-he-yun-yong-gf604/) 指出滑动窗口可以通过前缀和直接得到.
思路1: [官方](https://leetcode.cn/problems/find-good-days-to-rob-the-bank/solution/gua-he-da-jie-yin-xing-de-ri-zi-by-leetc-z6r1/)解答
没有必要限制窗口大小: 对于每个元素, 分别维护左右非递增元素的数量, 只需要判断 `left[i] >= time and right[i] >= time` 即可.
"""
    def goodDaysToRobBank(self, security: List[int], time: int) -> List[int]:
        n = len(security)
        # 注意边界
        if time==0:
            return list(range(n))
        # 分别记录左右是否上升
        isUpL = [False] * n
        isUpR = [False] * n
        for i in range(1, n):
            if security[i] - security[i-1] > 0: isUpL[i] = True
            if security[i-1] - security[i] > 0: isUpR[i-1] = True
        
        validL, validR = [False] * n, [False] * n
        countL = len([i for i in isUpL[:time] if i])
        countR = sum(isUpR[-time:])
        for i in range(time, n):
            countL += isUpL[i] - isUpL[i-time]
            countR += isUpR[-i-1] - isUpR[-i-1+time]
            if countL==0: validL[i] = True
            if countR==0: validR[-i-1] = True
        
        ans = [i for i, (vl,vr) in enumerate(zip(validL, validR)) if vl and vr]
        return ans

    """ 2101. 引爆最多的炸弹
每一个炸弹由 (x,y,r) 所定义, 若另一个炸弹在该炸弹的r范围内, 则可连环引爆. 要求返回最多引燃一个可以引爆的炸弹数量.
思路: 构图后BFS
注意: 这里炸弹之间是有向边! 因此不是 #并查集 ! 思路, 对于炸弹两两构建有向边, (复杂度 n^2), 然后从每个点出发 BFS (整体复杂度n*n^2), 找到最大可引爆数.
"""
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        def testBomb(b1, b2):
            # b1 是否可以引爆 b2
            x1,y1,r1 = b1
            x2,y2,_ = b2
            return r1**2 >= (x1-x2)**2 + (y1-y2)**2
        n = len(bombs)
        g = [[] for _ in range(n)]
        for i, b1 in enumerate(bombs):
            for j,b2 in enumerate(bombs):
                if j==i: continue
                if testBomb(b1, b2): g[i].append(j)
        # BFS
        def bfs(i):
            visited = set()
            ans = 0
            q = collections.deque([i])
            while q:
                b = q.popleft()
                ans += 1
                visited.add(b)
                for j in g[b]:
                    if j in visited: continue
                    q.append(j)
                    visited.add(j)
            return ans
        return max(bfs(i) for i in range(n))
    
    """ 2102. 序列顺序查询 #hard #题型 #优先队列
比较特殊的插入和查询要求: 实现一个数据结构, 支持插入元素, 查询大小为第 k 个元素. 这里的查询有些特殊: 第i次查询需要返回的是第i大的元素.
复杂度: add, get 两种操作的复杂度为 1e4. 元素结构为 (score, name) 要求 score 降序 name 升序. score 范围 1e5.
思路0: #二分 理论的插入复杂度为 O(n), 但这里没有掐直接过了.
思路1: 考虑本题的特殊性: 每次查询的元素是特定的. 具体而言, 我们每次关心的只是查询次数k附近的元素.
因此, 可以分别维护一个最小堆MinHeap 和最大堆MaxHeap: 用最小堆存储前k大的元素, 用最大堆存储其他元素.
每次查询时, 返回最大堆堆顶元素即可
而插入时, 若元素比 MinHeap 堆顶元素大, 则 pushpop, 然后加入到 MaxHeap; 否则直接入 MaxHeap.
Python: 注意heapq只提供了最小堆 (优先队列), 并且需要对于数字和字符串按照不同的方式排序, 因此需要手动写数据结构实现 `__lt__` 或 `__gt__`. 例如对于最小堆而言, 更小的元素优先, 则较小元素的 `__lt__` 函数应该返回 True.
技巧: Python 的 sortedcontainers 还提供了现成的 SortedList 使用. 插入、删除的复杂度约为 O(log n).
"""
    def test_2102(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
        

class MaxNode():
    # 最大堆的节点
    def __init__(self, score, name) -> None:
        super().__init__()
        self.score = score
        self.name = name
    def __lt__(self, other):
        # 注意 Python 中 heapq 只有最小堆, 因此需要取反: 分数越大, 优先级越高
        return (-self.score, self.name) < (-other.score, other.name)
class MinNode():
    def __init__(self, score, name) -> None:
        super().__init__()
        self.score = score
        self.name = name
    def __gt__(self, other):
        # 简单期间, 直接定义 __gt__ 即可
        return (-self.score, self.name) < (-other.score, other.name)

class SORTracker1:
    """ 随着查询次数的增加, 维护 numQuery 个最大元素 (一个大小为 numQuery 的最小堆) """
    def __init__(self):
        self.maxHeap = [] # 记录剩余的较小元素 (每次 get 取 maxHeap 的最大值)
        self.minHeap = [] # 记录最大的 numQuery 个元素
        self.numQuery = 0

    def add(self, name: str, score: int) -> None:
        # 按照 score 降序, 按照 name 升序
        max_node = MaxNode(score, name)
        if self.numQuery == 0:
            heapq.heappush(self.maxHeap, max_node)
            return
        min_node = MinNode(score, name)
        if min_node > self.minHeap[0]:
            mnode = heapq.heappushpop(self.minHeap, min_node)
            heapq.heappush(self.maxHeap, MaxNode(mnode.score, mnode.name))
        else:
            heapq.heappush(self.maxHeap, max_node)

    def get(self) -> str:
        max_node = heapq.heappop(self.maxHeap)
        heapq.heappush(self.minHeap, MinNode(max_node.score, max_node.name))
        self.numQuery += 1
        return max_node.name

class SORTracker:
    """  """
    def __init__(self):
        self.l = []
        self.numQuery = 0

    def add(self, name: str, score: int) -> None:
        node = (-score, name)
        # idx = bisect.bisect_right(self.l, node)
        # self.l.insert(idx, node)
        bisect.insort_left(self.l, node)

    def get(self) -> str:
        self.numQuery += 1
        return self.l[self.numQuery-1][1]



sol = Solution()
result = [
    # sol.maxSubsequence(nums = [2,1,3,3], k = 2),
    # sol.maxSubsequence(nums = [-1,-2,3,4], k = 3),
    
    # sol.goodDaysToRobBank(security = [5,3,3,3,5,6,2], time = 2),
    # sol.goodDaysToRobBank(security = [1,1,1,1,1], time = 0), 
    # sol.goodDaysToRobBank([4,3,2,1], 0),
    
    # sol.maximumDetonation(bombs = [[2,1,3],[6,1,4]]),
    # sol.maximumDetonation(bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]),
    # sol.maximumDetonation([[4,4,3],[4,4,3]]),
    
    sol.test_2102("""["SORTracker", "add", "add", "get", "add", "get", "add", "get", "add", "get", "add", "get", "get"]
[[], ["bradford", 2], ["branford", 3], [], ["alps", 2], [], ["orland", 2], [], ["orlando", 3], [], ["alpine", 2], [], []]""")
]
for r in result:
    print(r)
