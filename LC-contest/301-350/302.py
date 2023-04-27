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
https://leetcode.cn/contest/weekly-contest-302
@2022 """
class Solution:
    """ 6120. 数组能形成多少数对 """
    def numberOfPairs(self, nums: List[int]) -> List[int]:
        cnt = Counter(nums)
        ans = [0, 0]
        for _,v in cnt.items():
            a,b = divmod(v, 2)
            ans[0] += a
            ans[1] += b
        return ans
    
    """ 6164. 数位和相等数对的最大和 """
    def maximumSum(self, nums: List[int]) -> int:
        s2nums = defaultdict(list)
        for num in nums:
            aa = num
            acc = 0
            while num:
                num,a = divmod(num, 10)
                acc += a
            s2nums[acc].append(aa)
        ans = -1
        for s,arr in s2nums.items():
            if len(arr)<2: continue
            arr.sort()
            ans = max(ans, sum(arr[-2:]))
        return ans

    """ 6121. 裁剪数字后查询第 K 小的数字 #medium #排序 """
    def smallestTrimmedNumbers(self, nums: List[str], queries: List[List[int]]) -> List[int]:
        ans = []
        for k, trim in queries:
            trimed = [(num[-trim:], i) for i,num in enumerate(nums)]
            trimed.sort()
            ans.append(trimed[k-1][1])
        return ans
    
    """ 6122. 使数组可以被整除的最少删除次数 #共约束 #hard
给定两个数组, 要求找到nums中最小的, 能否整除numsDivide中所有数字的数字.
思路1: 计算numsDivide所有数字的 #最大公约数 g. 然后nums从小到大遍历, 若当前数字可以整除g, 就找到了.
"""
    def minOperations(self, nums: List[int], numsDivide: List[int]) -> int:
        nums.sort()
        g = reduce(math.gcd, numsDivide)
        target = -1
        for a in sorted(set(nums)):
            if g % a==0:
                target = a
                break
        if target==-1: return -1
        return nums.index(target)
    
sol = Solution()
result = [
    # sol.numberOfPairs(nums = [1,3,2,1,3,2,2]),
    # sol.numberOfPairs(nums = [0]),
    # sol.maximumSum(nums = [18,43,36,13,7]),
    # sol.maximumSum(nums = [10,12,19,14]),
    # sol.smallestTrimmedNumbers(nums = ["102","473","251","814"], queries = [[1,1],[2,3],[4,2],[1,2]]),
    # sol.smallestTrimmedNumbers(nums = ["24","37","96","04"], queries = [[2,1],[2,2]]),
    sol.minOperations(nums = [2,3,2,4,3], numsDivide = [9,6,9,3,15]),
    sol.minOperations(nums = [4,3,6], numsDivide = [8,2,6,10]),
]
for r in result:
    print(r)
