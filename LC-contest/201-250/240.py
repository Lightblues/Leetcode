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
https://leetcode.cn/contest/weekly-contest-240
@2022 """
class Solution:
    """ 1854. 人口最多的年份 """
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        cnt = Counter()
        for s,e in logs:
            for a in range(s,e):
                cnt[a] += 1
        mx, year = 0, 0
        for y,c in sorted(cnt.items()):
            if c>mx:
                year = y; mx = c
        return year
    
    """ 1855. 下标对中的最大距离 #medium #双指针 """
    def maxDistance(self, nums1: List[int], nums2: List[int]) -> int:
        mx = 0
        j = 0; m = len(nums2)
        for i,a in enumerate(nums1):
            j = max(j, i)
            while j<m-1 and nums2[j+1]>=a: j+= 1
            mx = max(mx, j-i)
        return mx
    
    """ 1856. 子数组最小乘积的最大值 #medium 见 stack """
    
    """ 1857. 有向图中最大颜色值 #hard 见 topological """
    

    
sol = Solution()
result = [
    # sol.maximumPopulation(logs = [[1993,1999],[2000,2010]]),
    # sol.maximumPopulation(logs = [[1950,1961],[1960,1971],[1970,1981]]),
    sol.maxDistance(nums1 = [55,30,5,4,2], nums2 = [100,20,10,10,5]),
    sol.maxDistance(nums1 = [2,2,2], nums2 = [10,10,1]),
]
for r in result:
    print(r)
