import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
from bisect import bisect_right, bisect_left
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, reduce, partial # cache
# cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # 注意 pow 与默认环境下的 pow(x,y, MOD) 签名冲突
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
import sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-202
@2022 """
class Solution:
    """ 1550. 存在连续三个奇数的数组 """
    def threeConsecutiveOdds(self, arr: List[int]) -> bool:
        acc = 0
        for a in arr:
            if a%2==0: acc = 0
            else:
                acc+= 1
                if acc>=3: return True
        return False
    """ 1551. 使数组中所有元素相等的最小操作数 """
    def minOperations(self, x: int) -> int:
        if x%2==0: return x * (x//2) // 2
        else: return (x+1) * (x//2) // 2
    
    """ 1552. 两球之间的磁力 #medium #二分
一数轴上有n个位置, 求放m个球, 要求任意相邻球之间的最小距离最大化 (也即「平均放置」).
限制: m,n 1e5, 位置限制 p 1e9.
思路1: #二分
    提示: 如何检查间距x是否可以达到? 注意, 可以贪心放置: 尽量将占据的位置放在左侧. 证明: 若有另一种放置方案, 其不会优于这种.
    因此, 可以在O(n)的时间内检查; 搜索范围为p, 因此复杂度为 O(n logp)
"""
    def maxDistance(self, position: List[int], m: int) -> int:
        pass

    """ 1553. 吃掉 N 个橘子的最少天数 #hard #题型
有n个橘子, 每次可以选择: 1) 吃一个; 2) 若可以被2整除, 吃1/2个; 3) 若可以被3整除, 吃2/3个. 问最少吃完的天数. 限制: n 2e9
注意: 比如 n=10, 则 10-9-3-1-0 的方案要优于 10-5-4-3-1-0.
思路1: 采用 #记忆化 搜索
    直觉: 对于一个数字, 最多进行两次-1操作, 然后进行/2或/3操作.
    证明: 见官答, 核心思想是, 对于-1操作和/2 (或/3操作而言), 先进行后者一定是更优的.
    因此, 采用 #记忆化 搜索, 对于一个数字探索 `min{ 1+x%2+f(x//2), 1+x%3+f(x//3) }`
    复杂度说明: 
        注意到, 若没有记忆化操作, 则复杂度为 `T(n) = T(n/2) + T(n/3) + O(1)`; 我们设 `T(n) = O(n^t)`, 代入, 然后两边同除 `O(n^t)`, 可以算出来 `t~0.788`, 还是会超时!!
        然而, 事实上这里有很多重复的计算. 利用这个论述: 对于正整数, 我们有结论 `⌊⌊n/x⌋/y⌋=⌊n/(xy)⌋=⌊⌊n/y⌋/x⌋`
        因此, 在本问题中, 只有 `i = ⌊n / 2^x3^y⌋` 的数才会被计算, 这里x/y的数量都是对数级别的, 因子整体复杂度控制在 `O(log^2(n))` 级别!!
思路2: 将上述过程建模为图上的 #最短路 问题
    还是思路1, 我们仅考虑其中 `i = ⌊n / 2^x3^y⌋` 的节点, 边权定义为转移成本, 例如 `x` 转移到 `x//2` 的成本为 `1+x%2`. 这样, 就变为从n到1的最短路搜索问题.
    细节: 图应该包含哪些节点? 我们一开始不需要预先找到所有的点, 从n开始往下搜索即可, 动态加入节点之间的边即可. 可以用 #Dijkstra 求解.
    复杂度: `O(log^2(n) loglogn)`, 因为边/节点的数量还是 `O(log^2(n))`, 过程中需要维护一个queue.
思路3: #启发式 搜索 #题型
    对于思路2进行改进, 采用启发式搜索.
    回顾: 启发函数的 **「可接受」（admissible heuristic）** (到终点的代价估计小于真实, 乐观的) 和 **「一致」（consistent heuristic）** (任意两点间的启发距离小于真实距离). 
    说明: 1) 若为可接受的, 则一个节点可能被拓展多次, 因为我们计算的不一定是真实的最短路径. 2) 一致性蕴含了可接受, 并且此时每个节点只会被拓展一次 (直接找到了最短路径)
    可以证明, 在本题中, 一个一致的启发函数为 `H(x) = ceil(x/3) + 1`, 当x=0时取值为0.
[官答](https://leetcode.cn/problems/minimum-number-of-days-to-eat-n-oranges/solution/chi-diao-n-ge-ju-zi-de-zui-shao-tian-shu-by-leetco/)
"""
    @lru_cache(None)
    def minDays(self, n: int) -> int:
        # 思路1: 采用 #记忆化 搜索
        if n==1: return 1
        if n==2: return 2   # 2//3 可能出现 0
        return min(
            1 + n%2 + self.minDays(n//2), 1 + n%3 + self.minDays(n//3)
        )
    
    def minDays(self, n: int) -> int:
        # 思路2: 将上述过程建模为图上的 #最短路 问题
        q = [(0, n)]        # (dist, node)
        visited = set()
        ans = 0
        
        while True:
            days, rest = heapq.heappop(q)
            if rest in visited:
                continue
            visited.add(rest)
            if rest == 1:
                ans = days + 1
                break
            heapq.heappush(q, (days + rest % 2 + 1, rest // 2))
            heapq.heappush(q, (days + rest % 3 + 1, rest // 3))
        return ans
    
    def minDays(self, n: int) -> int:
        # 思路3: #启发式 搜索 #题型
        @lru_cache(None)
        def getHeuristicValue(rest: float) -> int:
            # 启发函数为 `H(x) = ceil(x/3) + 1`, 当x=0时取值为0.
            return 0 if rest == 0 else \
                int(math.log(rest) / math.log(3.0)) + 1
        
        q = [(getHeuristicValue(n), 0, n)]      # (heuristic+cost, dist, node)
        visited = set()
        ans = 0
        
        while True:
            expected, days, rest = heapq.heappop(q)
            if rest in visited:
                continue
            visited.add(rest)
            # 找到答案了
            if rest == 1:
                ans = days + 1
                break
            heapq.heappush(q, (
                days + rest % 2 + 1 + getHeuristicValue(rest // 2),
                days + rest % 2 + 1,
                rest // 2
            ))
            heapq.heappush(q, (
                days + rest % 3 + 1 + getHeuristicValue(rest // 3),
                days + rest % 3 + 1,
                rest // 3
            ))
        return ans


sol = Solution()
result = [
    sol.maxDistance(position = [1,2,3,4,7], m = 3),
    sol.maxDistance(position = [5,4,3,2,1,1000000000], m = 2),
    # sol.minDays(10),
    # sol.minDays(6),
]
for r in result:
    print(r)
