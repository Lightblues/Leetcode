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
https://leetcode-cn.com/contest/biweekly-contest-86

T2 不知道是否有数学解法; T3 复杂度分析一开始没想好; T4 的题目描述也有点奇怪, 虽然最后实现比较简单就是...

@2022 """
class Solution:
    """ 6171. 和相等的子数组 """
    def findSubarrays(self, nums: List[int]) -> bool:
        s = set()
        for i in range(1,len(nums)):
            ss = nums[i]+nums[i-1]
            if ss in s: return True
            s.add(ss)
        return False
    
    """ 6172. 严格回文的数字
给定一个数字 n, 判断其是否在 2...n-2 进制下都是回文的.
思路0: 暴力检查
"""
    def isStrictlyPalindromic(self, n: int) -> bool:
        def check(n,k):
            arr = []
            while n:
                n,a = divmod(n,k)
                arr.append(a)
            return arr==arr[::-1]
        for i in range(2,n-1):
            if not check(n,i): return False
        return True
    
    """ 6173. 被列覆盖的最多行数 #medium
有一个0/1矩阵, 可以选择其中cols列, 对于每一行, 若其所有的非0列都被覆盖, 则满足要求, 问最多能覆盖多少行. 限制: 行列 n 12
思路1: 暴力枚举所有的可能. 按照 #二进制 压缩.
    通过位压缩可以在 O(n) 的时间计算满足要求的行有多少.
    由于列较少, 可以直接枚举所有列组合, 因此复杂度 `O(n 2^n)` 也是够的.
    1.2 尝试用 `combinations(range(n),cols)` 但其实复杂度没有影响.
"""
    def maximumRows(self, mat: List[List[int]], cols: int) -> int:
        m,n = len(mat), len(mat[0])
        rows = []
        for i in range(m):
            s = 0
            for j in range(n):
                s += mat[i][n-j-1] * 2**j
            rows.append(s)
        # 
        def check(mask):
            return sum([1 for row in rows if row | mask == mask])
        ans = 0
        for comb in combinations(range(n),cols):
            mask = 0
            for i in comb: mask += 1<<i
            ans = max(ans, check(mask))
        return ans
            
    """ 6143. 预算内的最多机器人数目 #hard 
题目定义有点奇怪. 总言之, 有等长的 arr1, arr2, 选择连续长为k的区间的代价为 max(arr1[i:i+k]) + k * sum(arr2[i:i+k]), 问在给定 budget 能得到的最大k.
限制: n 5e4
思路1: #二分 范围 [0,n].
    如何check? 需要得到长k子数组中的最大值, 可以维护一个 #最大堆 (结合时间戳限制长度). 这样检查的复杂度 `O(n log k)`.
    总体复杂度 O(n log(n) log(k))
"""
    def maximumRobots(self, chargeTimes: List[int], runningCosts: List[int], budget: int) -> int:
        def check(k):
            if k==0: return True
            # 最大堆, 利用时间戳限制长度
            ct = [(-c,i) for i,c in enumerate(chargeTimes[:k])]
            heapify(ct)
            csum = sum(runningCosts[:k])
            if csum * k - ct[0][0] <= budget: return True
            for i in range(k,n):
                csum += runningCosts[i] - runningCosts[i-k]
                heappush(ct, (-chargeTimes[i], i))
                while ct[0][1] <= i-k: heappop(ct)
                if csum * k - ct[0][0] <= budget: return True
            return False
        ans = 0
        n = len(chargeTimes)
        l,r = 0, n
        while l<=r:
            m = (l+r)//2
            if check(m): ans = m; l = m+1
            else: r = m-1
        return ans

    
sol = Solution()
result = [
    # sol.findSubarrays([1,2,3,4]),
    # sol.findSubarrays([1,2,1]),
    # sol.findSubarrays([1,3,2,2]),
    # sol.isStrictlyPalindromic(10),
    # sol.isStrictlyPalindromic(4),
    # sol.isStrictlyPalindromic(9),
    # sol.maximumRows(mat = [[0,0,0],[1,0,1],[0,1,1],[0,0,1]], cols = 2),
    # sol.maximumRows([[1],[0]], 1),
    # sol.maximumRows([[1,0,0,0,0,0,0],[0,1,0,1,1,1,1],[0,0,0,1,0,0,1]],5),
    sol.maximumRobots(chargeTimes = [3,6,1,3,4], runningCosts = [2,1,3,4,5], budget = 25),
    sol.maximumRobots(chargeTimes = [11,12,19], runningCosts = [10,8,7], budget = 19),
]
for r in result:
    print(r)
