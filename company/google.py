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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 找出 1...n 数组中重复和缺少的数字 """
    
    """ 1861. 旋转盒子 """
    def rotateTheBox(self, box: List[List[str]]) -> List[List[str]]:
        m,n = len(box),len(box[0])
        ans = [['.'] * m for _ in range(n)]
        for i in range(m):
            nidx = n-1
            for j in range(n-1,-1,-1):
                # if box[i][j]=='.' and : nidx = j
                if box[i][j]=='*': nidx = j-1; ans[j][m-1-i] = '*'
                elif box[i][j]=='#': ans[nidx][m-1-i] = '#'; nidx -= 1
        return ans
    
    """ 
给定一个数字矩阵 (保证了所有元素都不同). 要求替换这些数字, 满足同行列的相对大小保持不变. 并且数字最大值最小化.
关联: 做过可以有相同元素的拓展版本...这里所有数字都distinct的条件使得问题更简单了
思路1: 对于矩阵内元素从小到大赋值. 并且用两个map来分别记录行列中目前的最大值.

e.g.
Input: grid = [[3,1],[2,5]]
Output: [[2,1],[1,2]]
"""
    def minScore(self, grid: List[List[int]]) -> List[List[int]]:
        m,n = len(grid),len(grid[0])
        vals = [(grid[i][j],i,j) for i,j in product(range(m),range(n))]
        vals.sort()
        col2mx = [0] * m
        row2mx = [0] * n
        ans = [[0] * n for _ in range(m)]
        for v,i,j in vals:
            val = max(col2mx[i],row2mx[j]) + 1
            col2mx[i] = val; row2mx[j] = val
            ans[i][j] = val
        return ans

    
sol = Solution()
result = [
    # sol.rotateTheBox([["#",".","#"]]),
    sol.minScore(grid = [[3,1],[2,5]]),
]
for r in result:
    print(r)
