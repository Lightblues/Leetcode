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
from more_itertools import tail

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
https://leetcode.cn/contest/weekly-contest-222
@2022 """
class Solution:
    """ 1712. 将数组分成三个子数组的方案数 #medium
要将一个数组分成三部分, 使得三部分的和依次满足 a<=b<=c, 求分割数.
思路: 利用 #前缀和 加速, 用 #二分 搜索.
    假设数组和为 s, 给定a, 则a+b需要满足 2*a<=a+b<=(s+a)/2
"""
    def waysToSplit(self, nums: List[int]) -> int:
        mod = 10**9+7
        s = sum(nums)
        acc = list(accumulate(nums, initial=0))
        ans = 0
        for i in range(1, len(nums)):
            a = acc[i+1]
            if a>=s/3: break
            l = bisect_left(acc, 2*a)
            r = bisect_left(acc, (s+a)//2)
            ans = (ans +r-l) % mod
        return ans
    
    
    
    

    
sol = Solution()
result = [
    sol.waysToSplit(nums = [1,1,1]),
    sol.waysToSplit(nums = [1,2,2,2,5,0]),
    
]
for r in result:
    print(r)
