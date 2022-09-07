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
[排序](https://leetcode.cn/leetbook/detail/sort-algorithms/)


@2022 """
class Solution:
    """ 剑指 Offer 45. 把数组排成最小的数 #medium
给定一组数组, 重新排列形成最小的数字. 可以有前置零.
思路1: 显然是一个 #排序问题. 关键是如何定义排序规则?
    提示: 对于 x,y 两个数字/字符串, 直接比较 x+y, y+x (拼接)的大小即可.
    技巧: 在Python中, 定义 comp(x,y) 返回两个数字的大小关系定义, 然后可以通过 `functools.cmp_to_key(comp)` 进行包装, 从而作为 key 传入sort函数.
"""
    def minNumber(self, nums: List[int]) -> str:
        def comp(x:str, y:str):
            # 定义比较函数
            return 1 if x+y > y+x else -1
        nums = [str(i) for i in nums]
        nums.sort(key=functools.cmp_to_key(comp))
        return ''.join(nums)
    
    
    
    

    
sol = Solution()
result = [
    sol.minNumber([10,2]),
]
for r in result:
    print(r)
