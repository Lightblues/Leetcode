from tkinter import N
from turtle import up
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
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-250
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1935. 可以输入的最大单词数 """
    def canBeTypedWords(self, text: str, brokenLetters: str) -> int:
        return sum(1 for w in text.split() if not any(ch in brokenLetters for ch in w))

    """ 1936. 新增的最少台阶数 """
    def addRungs(self, rungs: List[int], dist: int) -> int:
        rungs = [0] + rungs
        ans = 0
        for i in range(len(rungs)-1):
            ans += math.ceil((rungs[i+1] - rungs[i]) / dist) - 1
        return ans
    
    """ 1937. 扣分后的最大得分 #medium 
给定一个grid形式的矩阵, 每行选取一个位置的元素, 累计所有分数; 对于相邻的 i, i+1 行, 需要扣除 `abs(c_i - c_i+1)`, 也即相邻行所选两列的位置差值. 要求最大分数
约束: grid大小 1e5
思路1: #DP
    考虑每多一行 row 造成的分数变化? 对于每一列的数字, 都是 `dp[i] = max(dp[j] + row[i] + abs(i-j))` (这里左侧dp是上一行的值).
    也即, 当前行本身的值的大小不会影响j的取值. 上一行的值造成的变化是可以计算的.
    因此, 递归过程中: 每次都 1) 计算上一行的分数影响; 2) 加上当前行每一列的元素值.
    具体而言, 例如上一行的最大值为 `[2,7,4]`, 则下一行每个位置的最优剩余分数为 `[6,7,6]`. 可以看到是较大元素向左右传播. 因此左右两边分别进行一次遍历, 去较大即可.
    see [here](https://leetcode.cn/problems/maximum-number-of-points-with-cost/solution/kou-fen-hou-de-zui-da-de-fen-by-leetcode-60zl/)
"""
    def maxPoints(self, points: List[List[int]]) -> int:
        m,n = len(points), len(points[0])
        
        dp = points[0]
        def update(dp):
            left = dp[:]
            last = 0
            for i in range(n):
                last = max(dp[i], last-1)
                left[i] = last
            right = dp[:]
            last = 0
            for i in range(n-1, -1, -1):
                last = max(dp[i], last-1)
                right[i] = last
            return [max(left[i], right[i]) for i in range(n)]
        for row in points[1:]:
            dp = update(dp)
            dp = [dp[i]+row[i] for i in range(n)]
        return max(dp)
    
    """ 1938. 查询最大基因差 """
    def maxGeneticDifference(self, parents: List[int], queries: List[List[int]]) -> List[int]:
        pass

sol = Solution()
result = [
    # sol.addRungs(rungs = [1,3,5,10], dist = 2),
    
    sol.maxPoints(points = [[1,2,3],[1,5,1],[3,1,1]]),
]
for r in result:
    print(r)
