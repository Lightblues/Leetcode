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
@2022 """
class Solution:
    """ 0719. 找出第 K 小的数对距离 #hard #题型 #二分
给定一个数组, 每个数对构成「绝对差值」. 问第k小的差值. 限制: 长度 n 1e4. 数字大小 C 1e6.  
思路0: #二分. 一个比较蠢的实现
    考虑问题「对于给定的d问差值小于d的数对有多少」, 可以通过排序+bisct解决. 每次检查的复杂度为 `O(n log(n))`.
    搜索空间为 [0,C]. 因此可以用二分来查找, 总体复杂度 `O(log(C) * n log(n))`.
    注意: 本题二分的特殊性在于, 搜索的值可能无法取到! 可以通过检查函数返回一个flag来标记数组中是否存在该差值.
"""
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        # 思路0: #二分. 一个比较蠢的实现
        nums.sort(); n = len(nums)
        def f(d):
            # 统计nums中差值 <d 的组数
            # 返回: (cnt, flag) 后者标记是否存在该差值
            cnt = 0; flag = False
            for i,a in enumerate(nums):
                lmt = bisect_left(nums, a+d, i)
                cnt += lmt - i - 1
                if lmt<n and nums[lmt]==a+d: flag=True
            return cnt,flag
        # 二分
        l,r = 0,max(nums) - min(nums)
        ans = 0
        while l<=r:
            m = (l+r)>>1
            cnt,flag = f(m)
            if cnt<k:
                l = m+1
                # 只有存在时才更新
                if flag: ans = m
            else: r = m-1
        return ans


    
sol = Solution()
result = [
    sol.smallestDistancePair([1,3,1], 1),
    sol.smallestDistancePair(nums = [1,1,1], k = 2),
    sol.smallestDistancePair(nums = [1,6,1], k = 3),
    sol.smallestDistancePair([9,10,7,10,6,1,5,4,9,8], 18),
]
for r in result:
    print(r)
