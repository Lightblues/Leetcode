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
https://leetcode.cn/contest/weekly-contest-192

主要是 T4挺有意思. 在较多限制条件下的 DP求解, 用到了三维DP. 
@2022 """
class Solution:
    """ 1470. 重新排列数组 """
    
    """ 1471. 数组中的 k 个最强值 """
    def getStrongest(self, arr: List[int], k: int) -> List[int]:
        arr.sort(); n = len(arr)
        # 这里 「中位数」的定义为 ((n - 1) / 2) 个元素
        median = arr[(n-1)//2]
        power = []
        for a in arr: 
            power.append((abs(a-median), a))
        power.sort(reverse=True)
        return [i[1] for i in power[:k]]
    
    """ 1473. 粉刷房子 III #hard #题型 要对于一排 m个房子涂色(一部分已经涂好的不能修改), 有 n种颜色, 每个房子涂不同颜色有着不一样的成本. 
相邻的相同颜色的房子视为一个街区. 在要求分成 target个街区的限制下成本最小化. 限制: 1<=m<=100, 1<=n<=20, 1<=target<=m, 1<=cost[i][j]<=10^4
提示: DP方程 `f(i,j,k)` 表示考虑前i个房子分成k个街区, 并且第i个房子为颜色j的最小成本.
思路1: #DP 我们需要通过j个房子本身的颜色和 j-1个房子的颜色来确定状态转移方程.
    若 hours[j] = cj != 0, 已经有了颜色不能修改, 于是 `f(i,j,k)` 只有在j=cj位置才合法, 转移 `f(i,cj,k) = min{ f(i-1, c!=cj, k-1), f(i-1,cj,k) }`
    否则, 我们可以选择涂颜色. `f(i,j,k) = min{ f(i-1, c!=j, k-1), f(i-1,j,k) } + cost[i][j]`
    复杂度: O(m n^2 k). 三维DP的状态空间 mnk, 每次转移的复杂度为 n.
思路2: 优化版本: 考察状态转移中哪些是需要 O(n)? 可以采用额外的变量优化到 O(1), 见官答.
见 [官答](https://leetcode.cn/problems/paint-house-iii/solution/fen-shua-fang-zi-iii-by-leetcode-solutio-powb/)
"""
    def minCost(self, houses: List[int], cost: List[List[int]], m: int, n: int, target: int) -> int:
        # 思路1: #DP DP方程 `f(i,j,k)` 表示考虑前i个房子分成k个街区, 并且第i个房子为颜色j的最小成本.
        f = [[[inf] * (target+1) for _ in range(n+1)] for _ in range(m+1)]
        for i in range(1,m+1):
            cj = houses[i-1]
            # 1) 只有在j=cj位置才合法,
            if cj!=0:
                if i==1:
                    f[i][cj][1] = 0
                else:
                    for k in range(1,target+1):
                        mn = min(f[i-1][jj][k-1] for jj in range(1,n+1) if jj!=cj)
                        mn = min(mn, f[i-1][cj][k])
                        f[i][cj][k] = mn
            # 2) 需要更新每一个 j
            else:
                for j in range(1,n+1):
                    for k in range(1, target+1):
                        if i==1: mn = 0 if k==1 else inf # 注意只有一个房子的时候, k=1才合法
                        else:
                            mn = min(f[i-1][jj][k-1] for jj in range(1,n+1) if jj!=j)
                            mn = min(mn, f[i-1][j][k])
                        f[i][j][k] = mn + cost[i-1][j-1]
        ans = min(f[m][j][target] for j in range(1,n+1))
        return -1 if ans==inf else ans

""" 1472. 设计浏览器历史记录 """
class BrowserHistory:
    def __init__(self, homepage: str):
        self.hist = [homepage]
        self.p = 0
    def visit(self, url: str) -> None:
        self.p += 1
        self.hist[self.p:] = [url]
    def back(self, steps: int) -> str:
        if steps > self.p: self.p = 0
        else: self.p -= steps
        return self.hist[self.p]

    def forward(self, steps: int) -> str:
        if self.p+steps >= len(self.hist)-1: self.p = len(self.hist)-1
        else: self.p += steps
        return self.hist[self.p]

    
sol = Solution()
result = [
    # sol.getStrongest([-7,22,17,3], 2)
#     testClass("""["BrowserHistory","visit","visit","visit","back","back","forward","visit","forward","back","back"]
# [["leetcode.com"],["google.com"],["facebook.com"],["youtube.com"],[1],[1],[1],["linkedin.com"],[2],[2],[7]]"""),
    sol.minCost(houses = [0,0,0,0,0], cost = [[1,10],[10,1],[10,1],[1,10],[5,1]], m = 5, n = 2, target = 3),
    sol.minCost(houses = [0,2,1,2,0], cost = [[1,10],[10,1],[10,1],[1,10],[5,1]], m = 5, n = 2, target = 3),
    sol.minCost([0,0,0,1], [[1,5],[4,1],[1,3],[4,4]],4,2,4)
]
for r in result:
    print(r)
