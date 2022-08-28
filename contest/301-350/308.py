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
https://leetcode.cn/contest/weekly-contest-308
@2022 """
class Solution:
    """ 6160. 和有限的最长子序列 """
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        nums.sort()
        acc = list(accumulate(nums))
        ans = []
        for q in queries:
            ans.append(bisect_right(acc, q))
        return ans
    """ 6161. 从字符串中移除星号 """
    def removeStars(self, s: str) -> str:
        st = []
        for ch in s:
            if ch=="*":
                if st: st.pop()
            else: st.append(ch)
        return "".join(st)
    """ 6162. 收集垃圾的最少总时间 无脑模拟题 """
    def garbageCollection(self, garbage: List[str], travel: List[int]) -> int:
        ans = 0
        mx = [0] * 3
        for i,g in enumerate(garbage):
            ans += len(g)
            if 'M' in g: mx[0] = i
            if 'P' in g: mx[1] = i
            if 'G' in g: mx[2] = i
        acc = list(accumulate(travel, initial=0))
        for i in mx:
            ans += acc[i]
        return ans
    
    """ 6163. 给定条件下构造矩阵 #hard #题型
给定一个k, 要求构造 k*k 的矩阵, 填充 1~k 共k个数字, 其他位置填0. 要求满足行/列约束. 约束的形式是, 给定一组 (i,j), 要求数字i所在行应该在j所在行的上面. 限制: k 400, 约束数量 n 1e4
思路0: 一开始看到约束条件想到 #CSP 问题, 但一想约束满足问题的搜索复杂度似乎不够? 没想清楚
思路1: 实际上就是一个 #拓扑排序. 
"""
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def f(conditions):
            # 拓扑排序
            # 构图
            nout = [0] * k
            nins = [[] for _ in range(k)]
            for u,v in conditions:
                u,v = u-1,v-1
                nout[u] += 1
                nins[v].append(u)
            # 拓扑排序
            zero = deque([i for i in range(k) if nout[i]==0])
            ans = list(zero)
            while zero:
                v = zero.popleft()
                for u in nins[v]:
                    nout[u] -= 1
                    if nout[u]==0:
                        zero.append(u)
                        ans.append(u)
            if len(ans)!=k: return []
            return [i+1 for i in ans[::-1]]
        rows, cols = f(rowConditions), f(colConditions)
        if not rows or not cols: return []
        # 综合行列约束
        ans = [[0] * k for _ in range(k)]
        n2row = {rows[i]:i for i in range(k)}
        n2col = {cols[i]:i for i in range(k)}
        for i in range(1, k+1):
            ans[n2row[i]][n2col[i]] = i
        return ans
    
sol = Solution()
result = [
    # sol.answerQueries(nums = [4,5,2,1], queries = [3,10,21]),
    # sol.answerQueries(nums = [2,3,4,5], queries = [1]),
    # sol.removeStars(s = "leet**cod*e"),
    # sol.removeStars(s = "erase*****"),
    # sol.garbageCollection(garbage = ["G","P","GP","GG"], travel = [2,4,3]),
    # sol.garbageCollection(garbage = ["MMM","PGM","GP"], travel = [3,10]),
    sol.buildMatrix(k = 3, rowConditions = [[1,2],[3,2]], colConditions = [[2,1],[3,2]]),
    sol.buildMatrix(k = 3, rowConditions = [[1,2],[2,3],[3,1],[2,3]], colConditions = [[2,1]]),
]
for r in result:
    print(r)
