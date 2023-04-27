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
https://leetcode.cn/contest/weekly-contest-237
@2022 """
class Solution:
    """ 1832. 判断句子是否为全字母句 """
    def checkIfPangram(self, sentence: str) -> bool:
        return len(Counter(sentence.lower()).keys()) == 26
    
    """ 1833. 雪糕的最大数量 """
    def maxIceCream(self, costs: List[int], coins: int) -> int:
        costs.sort()
        cnt = 0; sum = 0
        for c in costs:
            sum += c
            if sum > coins: break
            cnt += 1
        return cnt
    
    """ 1834. 单线程 CPU """
    
    """ 1835. 所有数对按位与结果的异或和 #medium #异或
给定两个长度为 m,n 数组, 通过两两组合区AND操作, 得到一个长度为 mn 的数组, 返回该数组所有元素依次 XOR 的结果.
思路1: 笨方法 #推导 异或和与运算之间的结合律
    最后的结果为 `XOR_i{ ai&b1 ^ ai&b2 ^ ... ^ ai&bm }`, 对于任意一个ai而言, 内部要求其与arr2中的所有元素取AND之后再依次异或.
        那么? ai的每一位会保留多少次? (奇数次的异或结果保留, 偶数次则消失). 显然, **保留的次数 = bj该位为1**. 因此, 可以先对所有的bj取 XOR, 然后将结果与ai取AND.
        简言之, 我们证明了 `a&b ^ a&c = a & (b^c)`
    因此, 上式变为 `XOR_i{ ai & XOR_j{bj} }`. 复杂度为 O(m+n)
思路2: 事实上, 我们可以再次利用上述定理, 进一步化为 `XOR_i{ai} & XOR_J{bj}` 参见 [here](https://leetcode.cn/problems/find-xor-sum-of-all-pairs-bitwise-and/solution/yi-xing-python-by-r4c12-p4bv/)
    [官答](https://leetcode.cn/problems/find-xor-sum-of-all-pairs-bitwise-and/solution/find-xor-sum-of-all-pairs-bitwise-and-by-sok6/).
"""
    def getXORSum(self, arr1: List[int], arr2: List[int]) -> int:
        xor2 = 0
        for b in arr2:
            xor2 ^= b
        ans = 0
        for a in arr1:
            ans ^= a&xor2
        return ans
    def getXORSum(self, arr1: List[int], arr2: List[int]) -> int:
        # 思路2
        # 下面两行都行
        # return reduce(lambda x, y: x ^ y, arr1) & reduce(lambda x, y: x ^ y, arr2)
        return reduce(xor, arr1) & reduce(xor, arr2)

    
sol = Solution()
result = [
    sol.getXORSum(arr1 = [1,2,3], arr2 = [6,5]),
    sol.getXORSum([12], [4]),
]
for r in result:
    print(r)
