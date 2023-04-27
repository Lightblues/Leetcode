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
https://leetcode.cn/contest/weekly-contest-228
@2022 """
class Solution:
    """ 1758. 生成交替二进制字符串的最少操作数 """
    def minOperations(self, s: str) -> int:
        n = len(s)
        target = "01" * (ceil(n/2)+1)
        ans = min(
            sum(a!=b for a,b in zip(s, target)),
            sum(a!=b for a,b in zip(s, target[1:]))
        )
        return ans
        
    """ 1759. 统计同构子字符串的数目 """
    def countHomogenous(self, s: str) -> int:
        mod = 10**9+7
        last = ""; cnt = 0
        ans = 0
        for ch in s+" ":
            if ch != last:
                ans = (ans + (cnt+1)*cnt//2) % mod
                cnt = 1
            else: cnt += 1
            last = ch
        return ans
    
    """ 1760. 袋子里最少数目的球 #medium 
有一组数, 还有一个最大操作数 maxOperations. 每次操作可以选择将一个数分解成两个整数. 目标是经过 maxOperations 之后, 所有数字的最大值最小化.
限制: 数组长度 1e5; 操作数 1e9
思路1: #二分 
    对于一个目标的最大数. 检查其是否可在maxOperations限制下得到, 复杂度为 O(n). 因此整体复杂度 O(n log(Max))
"""
    def minimumSize(self, nums: List[int], maxOperations: int) -> int:
        def check(mx):
            ans = 0
            for num in nums:
                ans += ceil(num/mx) - 1
                if ans > maxOperations: return False
            return True
        l,r = 1, max(nums)
        ans = inf
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = min(ans, mid)
                r = mid-1
            else: l = mid+1
        return ans
    
    """ 1761. 一个图中连通三元组的最小度数 #hard
给定一张无向图. 问其中所有的联通三角形中 (两两有边相连), 三元组的「度数」的最小值. 度数的定义是, 该三元组与图上其他部分连接的边的数量.
限制: 节点数 n 400
提示: 一种「暴力」的方式是, 直接枚举所有三元组, 若联通的话, 度数即为 `d[a]+d[b]+d[c]-6`
思路0: 假作聪明地尝试遍历两个点, 然后用集合交集来寻找第三个点. 但复杂度同样为 O(n^3).
思路1: 想多了, 直接 #暴力 枚举三个点, 居然就可以过. 当然可以加一些剪枝策略, 但没必要.
不同做法的用时参见 [submission](https://leetcode.cn/problems/minimum-degree-of-a-connected-trio-in-a-graph/submissions/)
"""
    def minTrioDegree(self, n: int, edges: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for u,v in edges:
            u,v = u-1,v-1
            g[u].append(v)
            g[v].append(u)
        degrees = [len(i) for i in g]
        # 思路0. 发现实际上是
        # ans = inf
        # for a in range(n):
        #     # for b in range(a+1, n):
        #     for b in g[a]:
        #         if b<a: continue
        #         cs = set(g[a]).intersection(set(g[b]))
        #         for c in cs:
        #             if c<b: continue
        #             ans = min(ans, degrees[a]+degrees[b]+degrees[c]-6)
        # return ans if ans!=inf else -1
        # 思路1
        ans = inf
        g = [set(i) for i in g]
        for a in range(n):
            for b in range(a,n):
                if b not in g[a]: continue
                for c in range(b,n):
                    if c not in g[a] or c not in g[b]: continue
                    ans = min(ans, degrees[a]+degrees[b]+degrees[c]-6)
        return ans if ans!=inf else -1
sol = Solution()
result = [
    # sol.minimumSize(nums = [2,4,8,2], maxOperations = 4),
    # sol.minimumSize([9], 2),
    sol.minTrioDegree(n = 6, edges = [[1,2],[1,3],[3,2],[4,1],[5,2],[3,6]]),
    sol.minTrioDegree(n = 7, edges = [[1,3],[4,1],[4,3],[2,5],[5,6],[6,7],[7,5],[2,6]]),
    
]
for r in result:
    print(r)
