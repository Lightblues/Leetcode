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
https://leetcode.cn/contest/weekly-contest-214
@2022 """
class Solution:
    """ 1646. 获取生成数组中的最大值 """
    def getMaximumGenerated(self, n: int) -> int:
        if n==0: return 0
        arr = [0,1]; mx = 1
        for i in range(2, n+1):
            if i%2==0:
                arr.append(arr[i//2])
            else:
                tgt = arr[i//2] + arr[i//2+1]
                mx = max(mx, tgt)
                arr.append(tgt)
        return mx
    """ 1647. 字符频次唯一的最小删除次数 """
    def minDeletions(self, s: str) -> int:
        cnts = list(Counter(s).values())
        cnts.sort()
        mn = inf; ans = 0
        for c in cnts[::-1]:
            if mn==0: ans += c
            elif c<mn: mn = c
            else:
                ans += c-mn+1
                mn -= 1
        return ans
    
    """ 1648. 销售价值减少的颜色球 #medium 类似阶梯蓄水 """
    def maxProfit(self, inventory: List[int], orders: int) -> int:
        mod = 10**9+7
        def f(mx,mn):   # 依次取这些数字的分数
            return (mx+mn) * (mx-mn+1) // 2
        inventory.sort()
        inventory = [0] + inventory
        n = len(inventory)
        ans = 0
        for idx in range(n-1, 0, -1):
            if (n-idx) * (inventory[idx]-inventory[idx-1]) >= orders:
                d, r = divmod(orders, n-idx)
                ans += f(inventory[idx], inventory[idx]-d+1) * (n-idx) + (inventory[idx]-d) * r
                ans %= mod
                return ans
            else:
                ans += f(inventory[idx], inventory[idx-1]+1) * (n-idx)
                ans %= mod
                orders -= (n-idx) * (inventory[idx]-inventory[idx-1])
        return ans
    
    """ 1649. 通过指令创建有序数组 #hard
需要一个DS满足: 1. 添加一个元素x; 2. 给定元素x查询DS中在 [1...x-1] 范围的数量; 3. 查询 [x+1...UB] 范围的数量. 见 [zero](https://leetcode.cn/problems/create-sorted-array-through-instructions/solution/tong-guo-zhi-ling-chuang-jian-you-xu-shu-zu-by-zer/)
因此, 可以通过 线段树、树状数组、平衡树 等方式来解决.
思路1: 直接调用了 SortedList.
"""
    
    def createSortedArray(self, instructions: List[int]) -> int:
        from sortedcontainers import SortedList
        nums = SortedList()
        mod = 10**9+7
        ans = 0
        for i in instructions:
            idxL = nums.bisect_left(i)
            idxR = nums.bisect_right(i)
            ans += min(idxL, len(nums)-idxR)
            nums.add(i)
        return ans%mod
    
sol = Solution()
result = [
    # sol.getMaximumGenerated(n = 7),
    # sol.maxProfit(inventory = [2,5], orders = 4),
    # sol.maxProfit(inventory = [3,5], orders = 6),
    
    sol.createSortedArray(instructions = [1,5,6,2]),
    sol.createSortedArray(instructions = [1,2,3,6,5,4]),
]
for r in result:
    print(r)
