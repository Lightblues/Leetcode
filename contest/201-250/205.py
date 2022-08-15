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
https://leetcode.cn/contest/weekly-contest-205
@2022 """
class Solution:
    """ 1576. 替换所有的问号 """
    def modifyString(self, s: str) -> str:
        res = list(s)
        n = len(res)
        for i in range(n):
            if res[i] == '?':
                for b in "abc":
                    if not (i > 0 and res[i - 1] == b or i < n - 1 and res[i + 1] == b):
                        res[i] = b
                        break
        return ''.join(res)

    """ 1577. 数的平方等于两数乘积的方法数 #medium """
    def numTriplets(self, nums1: List[int], nums2: List[int]) -> int:
        cnt1, cnt2 = Counter(nums1), Counter(nums2)
        ans = 0
        for i,ci in cnt1.items():
            for j,cj in cnt2.items():
                if i*i % j != 0: continue
                k = i*i // j
                if k not in cnt2 or k<i: continue
                if k==j: ans += ci * math.comb(cj, 2)
                else: ans += ci * cj*cnt2[k]
        for i,ci in cnt2.items():
            for j,cj in cnt1.items():
                if i*i % j !=0: continue
                k = i*i // j
                if k not in cnt1 or k<i: continue
                if k==j: ans += ci * math.comb(cj,2)
                else: ans += ci * cj*cnt1[k]
        return ans
    
    """ 1578. 使绳子变成彩色的最短时间 """
    def minCost(self, colors: str, neededTime: List[int]) -> int:
        pre = " "; mx = 0
        s = 0
        for c,t in zip(colors+" ", neededTime + [0]):
            if c!=pre: s += mx; mx = t
            else: mx = max(mx, t)
            pre = c
        return sum(neededTime) - s
    
    """ 1579. 保证图可完全遍历 #hard see [union-find] """
    
sol = Solution()
result = [
    # sol.numTriplets(nums1 = [1,1], nums2 = [1,1,1]),
    sol.minCost(colors = "aabaa", neededTime = [1,2,3,4,1]),
    sol.minCost(colors = "abaac", neededTime = [1,2,3,4,5]),
]
for r in result:
    print(r)
