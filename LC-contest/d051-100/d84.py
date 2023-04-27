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
https://leetcode-cn.com/contest/biweekly-contest-84
@2022 """
class Solution:
    """ 6141. 合并相似的物品 """
    def mergeSimilarItems(self, items1: List[List[int]], items2: List[List[int]]) -> List[List[int]]:
        items1, items2 = dict(items1), dict(items2)
        items = []
        for key in set(items1).union(set(items2)):
            items.append([key, items1.get(key, 0)+items2.get(key, 0)])
        items.sort()
        return items
    
    """ 6142. 统计坏数对的数目 #medium
给定一个数组, 对于 (i,j), i<j 假如 `j - i != nums[j] - nums[i]` 则是一个「坏数对」. 统计数组中坏数对数量.
思路1: 对于位置为idx的大小为num的元素, 其对应到位置0的大小应该是 num-idx, 用一个 Counter记录位置0出现各个数字的次数.
"""
    def countBadPairs(self, nums: List[int]) -> int:
        bias = defaultdict(int)
        acc = 0
        for i,num in enumerate(nums):
            acc += bias[num-i]
            bias[num-i] += 1
        n = len(nums)
        return math.comb(n, 2) - acc
    
    """ 6174. 任务调度器 II #medium 贪心即可 """
    def taskSchedulerII(self, tasks: List[int], space: int) -> int:
        cache = defaultdict(int)
        day = 1
        for i,task in enumerate(tasks):
            if task in cache:
                tgt = max(day, cache[task]+space+1)
                cache[task] = tgt
                day = tgt+1
            else:
                cache[task] = day
                day += 1
        return day-1
    
    """ 6144. 将数组排序的最少替换次数 #hard 但完全不难. 对于一个数组, 每个可以将其中的一个数字拆分成两个数字之和. 问最少操作使其变为「非递减」. 
思路1: 逆序, 贪心保留最大的拆分结果.
"""
    def minimumReplacement(self, nums: List[int]) -> int:
        ans = 0
        mn = nums[-1]
        for num in nums[-2::-1]:
            count = ceil(num/mn)
            ans += count-1
            mn = num//count
        return ans
    
sol = Solution()
result = [
    # sol.mergeSimilarItems(items1 = [[1,3],[2,2]], items2 = [[7,1],[2,2],[1,4]]),
    # sol.mergeSimilarItems(items1 = [[1,1],[3,2],[2,3]], items2 = [[2,1],[3,2],[1,3]]),
    # sol.countBadPairs(nums = [1,2,3,4,5]),
    # sol.countBadPairs(nums = [4,1,3,3]),
    # sol.taskSchedulerII(tasks = [1,2,1,2,3,1], space = 3),
    # sol.taskSchedulerII(tasks = [5,8,8,5], space = 2),
    sol.minimumReplacement(nums = [3,9,3]),
    sol.minimumReplacement(nums = [1,2,3,4,5]),
    
    
    
]
for r in result:
    print(r)
