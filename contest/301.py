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

题解: https://leetcode.cn/circle/discuss/5t4W96/view/kJ2FEW/
@2022 """

""" 6113. 无限集中的最小数字 """
class SmallestInfiniteSet:
    def __init__(self):
        self.ava = SortedList(range(1, 10000))

    def popSmallest(self) -> int:
        return self.ava.pop(0)

    def addBack(self, num: int) -> None:
        if num not in self.ava:
            self.ava.add(num)

class Solution:
    """ 6112. 装满杯子需要的最短总时长 #easy
有三种类型的物品, 各需要一定数量, 每次操作可以 1) 获得两种物品各一; 或 2) 或者一种物品. 问最少需要多少次操作才能得到所有的物品?
思路: #归纳 分析
"""
    def fillCups(self, amount: List[int]) -> int:
        amount.sort()
        a,b,c = amount
        if a+b>=c:
            return c+ ceil((a+b-c)/2)
        return a+b + (c-a-b)
    
    """ 6114. 移动片段得到字符串 #medium
两个字符串包括了 `L,R,_` 类别, L只能向左, R只能向右, 不能交替. 问start能否变为target.
限制: 两字符串等长, 1e5
思路1: 字符之间存在一一对应关系, #模拟 检查即可.
    由于LR不能交错, 因此要求S,T中, 非空字符的顺序相同. 并且要求: 对应字符中, L的位置满足 `idxS>=idxT`, R的位置 `idxS<=idxT`
"""
    def canChange(self, start: str, target: str) -> bool:
        s = [ch for ch in start if ch!="_"]
        t = [ch for ch in target if ch!="_"]
        if s!=t: return False
        idxS = [i for i,ch in enumerate(start) if ch!="_"]
        idxT = [i for i,ch in enumerate(target) if ch!="_"]
        for ch,idxs,idxt in zip(s,idxS,idxT):
            if ch=="L":
                if idxs<idxt: return False
            elif ch=='R':
                if idxs>idxt: return False
        return True
    
    """ 6115. 统计理想数组的数目 #hard
定义「理想数组」: 所有元素都在 `[1...maxValue]`, `arr[i]` 都是` arr[i-1]` 的倍数 (1,2,3...倍)
限制: n,maxVal 1e4
思路0: #DP
    定义 `f[i][j]` 为长度为i的数组, 最后一个值为j的理想数组的数量.则有递推 `f[i][j] = sum{ f[i-1][k] }`, 其中k为j的因子.
    但显然复杂度不够, 需要 O(n^3).
"""
    def idealArrays(self, n: int, maxValue: int) -> int:
        mod = 10**9 + 7
    

def matrix_multiply(matrix_a, matrix_b):
    n_row = len(matrix_a)
    n_col = len(matrix_b[0])
    n_tmp = len(matrix_a[0])
    matrix_c = [[0 for _ in range(n_col)] for _ in range(n_row)]
    for i in range(n_row):
        for j in range(n_col):
            for k in range(n_tmp):
                matrix_c[i][j] += matrix_a[i][k] * matrix_b[k][j]
    return matrix_c

def get_unit_matrix(n):
    # matrix I 生成单位矩阵
    unit_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for _ in range(n):
        unit_matrix[_][_] = 1
    return unit_matrix

def quick_matrix_pow(matrix_a, n):
    # A ^ n
    l = len(matrix_a)
    res = get_unit_matrix(l)
    while n:
        if n & 1:
            # 调用矩阵乘法
            res = matrix_multiply(res, matrix_a)
        matrix_a = matrix_multiply(matrix_a, matrix_a)
        n >>= 1
    return res

    
sol = Solution()
result = [
    # sol.fillCups(amount = [1,4,2]),
    # sol.fillCups(amount = [5,4,4]),
#     testClass("""["SmallestInfiniteSet", "addBack", "popSmallest", "popSmallest", "popSmallest", "addBack", "popSmallest", "popSmallest", "popSmallest"]
# [[], [2], [], [], [], [1], [], [], []]"""),
    # sol.canChange(start = "_L__R__R_", target = "L______RR"),
    # sol.canChange(start = "R_L_", target = "__LR"),
    # sol.canChange(start = "_R", target = "R_"),
    quick_matrix_pow([[1,1],[1,0]], 3)
]
for r in result:
    print(r)
