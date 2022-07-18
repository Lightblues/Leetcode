import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, cache, reduce, partial
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import sys, os
# sys.setrecursionlimit(10000)

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode

""" 
https://leetcode.cn/contest/weekly-contest-294
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 6074. 字母在字符串中的百分比 """
    def percentageLetter(self, s: str, letter: str) -> int:
        return int(s.count(letter) / len(s) * 100)
    
    """ 6075. 装满石头的背包的最大数量 """
    def maximumBags(self, capacity: List[int], rocks: List[int], additionalRocks: int) -> int:
        remains = [a-b for a, b in zip(capacity, rocks)]
        remains.sort()
        ans = 0
        for i, remain in enumerate(remains):
            if additionalRocks >= remain:
                ans += 1
                additionalRocks -= remain
        return ans

    """ 6076. 表示一个折线图的最少线段数
给一组xy坐标上的点, 顺序连起来, 要求计算线段的数量
"""
    def minimumLines(self, stockPrices: List[List[int]]) -> int:
        if len(stockPrices) < 2: return 0
        stockPrices.sort()
        from fractions import Fraction
        ans  = 0
        lastFraction = None
        for i in range(len(stockPrices)-1):
            f = Fraction(stockPrices[i+1][1] - stockPrices[i][1], stockPrices[i+1][0] - stockPrices[i][0])
            if f==lastFraction: continue
            lastFraction = f
            ans += 1
        return ans
    
    """ 6077. 巫师的总力量和 #hard #单调栈
对一个子数组, 定义score为 **最小元素 * 子数组元素和**, 现给定一个数组求所有子数组的score之和.
复杂度: 长度 1e5, 每个元素 1e9
思路1: #单调栈 #前缀和
"""
    def totalStrength(self, strength: List[int]) -> int:
        MOD = 10**9 + 7

sol = Solution()
result = [
    # sol.percentageLetter(s = "foobar", letter = "o"),
    
    # sol.maximumBags(capacity = [2,3,4,5], rocks = [1,2,4,4], additionalRocks = 2),
    # sol.maximumBags(capacity = [10,2,2], rocks = [2,2,0], additionalRocks = 100),
    
    # sol.minimumLines(stockPrices = [[1,7],[2,6],[3,5],[4,4],[5,4],[6,3],[7,2],[8,1]]),
    # sol.minimumLines(stockPrices = [[3,4],[1,2],[7,8],[2,3]]),
    # sol.minimumLines(stockPrices = [[3,4],[1,2]]),
    sol.minimumLines([[72,98],[62,27],[32,7],[71,4],[25,19],[91,30],[52,73],[10,9],[99,71],[47,22],[19,30],[80,63],[18,15],[48,17],[77,16],[46,27],[66,87],[55,84],[65,38],[30,9],[50,42],[100,60],[75,73],[98,53],[22,80],[41,61],[37,47],[95,8],[51,81],[78,79],[57,95]]),
]
for r in result:
    print(r)
