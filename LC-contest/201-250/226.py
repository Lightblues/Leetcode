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
https://leetcode.cn/contest/weekly-contest-226
@2022 """
class Solution:
    """ 1742. 盒子中小球的最大数量 """
    def countBalls(self, lowLimit: int, highLimit: int) -> int:
        cnt = Counter()
        for i in range(lowLimit, highLimit+1):
            c = 0
            while i:
                c += i%10
                i //=10
            cnt[c] += 1
        return max(cnt.values())
    
    """ 1743. 从相邻元素对还原数组 #medium #题型
对于原本的长n的各个元素都不同的数组, 只剩下了n-1组相邻元素. 要求根据这些重构原数组 (一种即可).
提示: 由于元素各不相同, 因此很容易判断头尾元素 (仅与一个相连).
"""
    def restoreArray(self, adjacentPairs: List[List[int]]) -> List[int]:
        g = defaultdict(list)
        for u,v in adjacentPairs:
            g[u].append(v)
            g[v].append(u)
        heads = [a for a,b in g.items() if len(b)==1]
        s,e = heads
        used = set([s])
        ans = [s]
        while s!=e:
            for a in g[s]:
                if a not in used:
                    ans.append(a)
                    used.add(a)
                    s = a
                    break
        return ans
    
    """ 1744. 你能在你最喜欢的那天吃到你最喜欢的糖果吗？ #medium
题目其实比较简单, 用一个 accumulate 即可. 但写得很烦躁, 因为使用在线编辑的原因吗?
"""
    def canEat(self, candiesCount: List[int], queries: List[List[int]]) -> List[bool]:
        acc = list(accumulate(candiesCount, initial=0))
        ans = [False] * len(queries)
        for i,(t,d,c) in enumerate(queries):
            if acc[t] >= c*(d+1): continue
            if acc[t+1] < (d+1): continue
            ans[i] = True
        return ans
    
    """ 1745. 回文串分割 IV #hard
给定一个字符串, 问能否将其分割成三个非空的回文串. 限制: 长度 [3, 2000]
思路1: 遍历两个分割点, 这样就要求在 O(1) 的时间内判断 s[i,j] 是否为回文串. 考虑进行预处理
    记 `f[i][j]` 为 s[i...j] 是否为回文串. 递推: 1) s[i]==s[j] 的话, 递推到 f[i+1][j-1], 否则 False; 2) 边界: i==j 的话, True.
"""
    def checkPartitioning(self, s: str) -> bool:
        n = len(s)
        f = [[False]*n for _ in range(n)]
        for i in range(n-1, -1, -1):
            f[i][i] = True
            for j in range(i+1, n):
                if s[i]==s[j]:
                    if j-i==1: f[i][j] = True
                    else: f[i][j] = f[i+1][j-1]
        # [0...i][i+1...j][j+1...n-1]
        for i in range(0, n):
            if not f[0][i]: continue
            for j in range(i+1,n-1):    # j 最大为 n-2
                if f[i+1][j] and f[j+1][n-1]: return True
        return False
    
    
sol = Solution()
result = [
    # sol.restoreArray([[4,-2],[1,4],[-3,1]]),
    # sol.checkPartitioning(s = "abcbdd"),
    # sol.checkPartitioning(s = "bcbddxy"),
    sol.checkPartitioning("bbab"),
]
for r in result:
    print(r)
