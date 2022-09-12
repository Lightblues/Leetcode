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
https://leetcode.cn/contest/weekly-contest-310
@2022 """
class Solution:
    """ 6176. 出现最频繁的偶数元素 """
    
    """ 6177. 子字符串的最优划分 #medium #贪心 """
    
    """ 6178. 将区间分为最少组数 #medium #题型 有一组 [s,e] 区间, 要求划分成数量最少的组, 每一组区间之间不相交.
思路1: 根据开始时间排序. 记录当前所划分的组; 遍历过程中, 每次在合法的组中添加即可 #贪心 思想.
    可以用一个堆来判断是否合法.
"""
    def minGroups(self, intervals: List[List[int]]) -> int:
        intervals.sort()
        ends = []
        cnt = 0; avas = 0
        for s,e in intervals:
            while ends and ends[0] < s:
                heapq.heappop(ends)
                avas += 1
            if avas==0:
                cnt += 1
            else: avas -= 1
            heapq.heappush(ends, e)
        return cnt

    """ 6206. 最长递增子序列 II #hard #题型 对于给定的数组, 找到其中最长的严格递增子序列, 要求相邻元素差值不超过 k.
限制: n 1e5; k 1e5
思路1: 建立 {val: LIS} 的字典, 遍历过程中, 对于val, 在 [val-k,val] 范围内查询最大值.
    考虑到数据范围, 可以采用 #线段树.
"""
    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        
sol = Solution()
result = [
    # sol.minGroups([[5,10],[6,8],[1,5],[2,3],[1,10]]),
    # sol.minGroups([[1,3],[5,6],[8,10],[11,13]]),
]
for r in result:
    print(r)
