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
== 检查区间内是否成立
0076. 最小覆盖子串 #hard
    给定字符串s和t, 要求s中长度最小的包含t中所有元素的子串.




"""
class Solution:

    """ 0076. 最小覆盖子串 #hard
给定字符串s和t, 要求s中长度最小的包含t中所有元素的子串.
限制: 长度 1e5
思路1: 滑动窗口仅需要检查当前窗口是否符合要求即可
"""
    def minWindow(self, s: str, t: str) -> str:
        tgt = Counter(t)
        cnt = Counter()
        def check():
            return all(cnt[i]>=tgt[i] for i in tgt)
        n = len(s)
        # 滑动窗口直接 for r in range(n): 即可!!!
        l = 0
        ansLen = inf; ansL = 0
        for r in range(n):
            cnt[s[r]] += 1
            while check():
                if r-l+1 < ansLen:
                    ansLen = r-l+1; ansL = l
                cnt[s[l]] -= 1
                l += 1
        return s[ansL:ansL+ansLen] if ansLen!=inf else ""
    
    
    
    
    
    
    

    
sol = Solution()
result = [
    sol.minWindow(s = "ADOBECODEBANC", t = "ABC"),
    sol.minWindow(s = "a", t = "a"),
    sol.minWindow(s = "a", t = "aa"),
]
for r in result:
    print(r)
