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
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # pow 与基本环境下的 pow 冲突
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



@2022 """
class Solution:
    """ 0050. Pow(x, n) 实现快速幂运算 #题型 #快速幂 #迭代
限制: n的范围在 -2^31 到 2^31 - 1 之间
思路0: 暴力二分, 利用 @cache
思路1: #递归 思路
    对于指数从小到大进行切分. 例如 `x^8` 可以切分为 `x^4 * x^4`, 而 `x^9` 则可以切分为 `x^4 * x^4 * x`
    实现递归函数 `recc(x, k)` 即可
思路2: 将递归展开为 #迭代
    以指数 9 为例, 观察其二进制表示 `1001`, 因此可以将 `x^9` 分解为 `x^(2^3) * x^(2^0)`
    因此, 指数的二进制表示上的每一个数位, 其对应的x的贡献也是一一对应的, 呈指数增长. 因此, 可以采用迭代bit位的方式, 在迭代过程中维护 `x_contribute` 表示每一位的贡献
[官答](https://leetcode.cn/problems/powx-n/solution/powx-n-by-leetcode-solution/)
"""
    @cache
    def myPow(self, x: float, n: int) -> float:
        """ 直接用了cache """
        if n==0: return 1
        elif n<0: return 1/self.myPow(x, -n)
        elif n==1: return x
        else: return self.myPow(x, n//2) * self.myPow(x, n - n//2)
        
    def myPow(self, x: float, n: int) -> float:
        """ 递归 """
        def quickMul(N):
            if N == 0:
                return 1.0
            y = quickMul(N // 2)
            return y * y if N % 2 == 0 else y * y * x
        
        return quickMul(n) if n >= 0 else 1.0 / quickMul(-n)

    def myPow(self, x: float, n: int) -> float:
        """ 迭代 """
        def quickMul(N):
            ans = 1.0
            # 贡献的初始值为 x
            x_contribute = x
            # 在对 N 进行二进制拆分的同时计算答案
            while N > 0:
                if N % 2 == 1:
                    # 如果 N 二进制表示的最低位为 1，那么需要计入贡献
                    ans *= x_contribute
                # 将贡献不断地平方
                x_contribute *= x_contribute
                # 舍弃 N 二进制表示的最低位，这样我们每次只要判断最低位即可
                N //= 2
            return ans
        
        return quickMul(n) if n >= 0 else 1.0 / quickMul(-n)



sol = Solution()
result = [
    sol.myPow(0.00001, 2147483647)
    
]
for r in result:
    print(r)
