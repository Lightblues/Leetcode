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
== 要求数字长度
1673. 找出最具竞争力的子序列 #medium #题型
    从长度为k的子序列中找到字典序最小的.



"""
class Solution:
    """ 1673. 找出最具竞争力的子序列 #medium #题型
从长度为k的子序列中找到字典序最小的.
思路: 采用 #最小堆. 如何保证最后剩余的堆大小至少为k? 对于长n的给定序列, 位置i往后的长度为n-i, 因此堆剩余的大小至少为 `k-(n-i)`
"""
    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        h = []
        n = len(nums)
        for i,num in enumerate(nums):
            # 保证剩余堆的大小至少为k
            while len(h) >= max(1, k-n+i + 1) and num<h[-1]:
                h.pop()
            h.append(num)
        return h[:k]
    
    
    
    
    
    

    
sol = Solution()
result = [
    # sol.mostCompetitive(nums = [3,5,2,6], k = 2),
    # sol.mostCompetitive(nums = [2,4,3,3,5,4,9,6], k = 4),
]
for r in result:
    print(r)
