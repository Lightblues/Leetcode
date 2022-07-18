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
https://leetcode.cn/contest/weekly-contest-235
@2022 """
class Solution:
    """ 1816. 截断句子 """
    def truncateSentence(self, s: str, k: int) -> str:
        return " ".join(s.split()[:k])
    
    """ 1817. 查找用户活跃分钟数 """
    def findingUsersActiveMinutes(self, logs: List[List[int]], k: int) -> List[int]:
        id2set = defaultdict(set)
        for i,t in logs:
            id2set[i].add(t)
        ans = [0] * k
        for i,s in id2set.items():
            ans[len(s)-1] += 1
        return ans
    
    """ 1818. 绝对差值和 #medium
给两个长度为n的数组, 最多可以用nums1中的i元素替换nums1中另一位置的元素, 目标要求 abs(nums2-nums1) 之和最小化.
思路1: 先将原数组的绝对差值和算出来, 再减去「通过最多可以减小的绝对值」大小即可.
    为了计算最多可以减小的绝对差值, 先对nums1排序, 然而对于目标值muns2的每一个位置, 在排序结果中 #二分 找到最接近的元素, 并且原本相应位置的绝对差比较, 看减小了多少.
"""
    def minAbsoluteSumDiff(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        diff = [abs(a-b) for a,b in zip(nums1, nums2)]
        nums1.sort()
        mx = 0  # 最大减小量
        for i,b in enumerate(nums2):
            # 从 nums1 中找到最接近的两个元素, 从而使得绝对差值最小
            idx = bisect.bisect_right(nums1, b)
            a = abs(nums1[idx-1] - b)
            if idx<n:
                a = min(a, abs(nums1[idx] - b))
            mx = max(mx, diff[i]-a) # diff[i] >= a 因为a是最小可能值
        mod = 10**9 + 7
        ans = (sum(diff) - mx) % mod
        return ans

    """ 1819. 序列中不同最大公约数的数目 #hard #题型 #gcd #公约数
给定一个数组, 对于其所有的子序列 (不要求连续), 问所有子序列的公约数一共有多少中不同的数字.
约束: 数组长度 1e5; 数组大小 C 2e5
提示: **数组中存在gcd为g的子序列, 等价于, 数组中所有g的倍数的gcd为g**. 证明: 否则, 它们的最大公因数一定大于g.
思路1: 因此, 对于每一个可能的公因子 1...C, 从数组中找出其所有倍数, 计算其gcd即可.
    复杂度: 每个g最多的倍数有 `C/1,C/2,...C/C`, 之和渐进为 `ClogC`. 对于gcd, 利用 #辗转相除 法复杂度为 O(logC). 因此整体 `O(C log^2C)`
    事实上, 这个复杂度可以进一步缩紧. 用到的是: **计算m个数字的公约数的复杂度不是 `m logC`, 而是 `m + 2logC`, 也即计算两个数共因子的复杂度logC可以从线性系数中拿出来. 原因在于, 在计算m个数共约数的过程中数字在不断变小. 具体见 [zero](https://leetcode.cn/problems/number-of-different-subsequences-gcds/solution/xu-lie-zhong-bu-tong-zui-da-gong-yue-shu-lrka/) 的评论.
关联: 「AtCoder Beginner Contest 191 F」
"""
    def countDifferentSubsequenceGCDs(self, nums: List[int]) -> int:
        # 思路1, from [zero](https://leetcode.cn/problems/number-of-different-subsequences-gcds/solution/xu-lie-zhong-bu-tong-zui-da-gong-yue-shu-lrka/)
        nums = set(nums)
        mx = max(nums)
        ans = 0
        for g in range(1, mx+1):
            gnow = None
            for y in range(g, mx+1, g):
                if y in nums:
                    if gnow is None: gnow = y
                    else: gnow = math.gcd(gnow, y)
                    if gnow==g:
                        ans += 1
                        break
        return ans
    
sol = Solution()
result = [
    # sol.findingUsersActiveMinutes(logs = [[0,5],[1,2],[0,2],[0,5],[1,3]], k = 5),
    # sol.minAbsoluteSumDiff(nums1 = [1,7,5], nums2 = [2,3,5]),
    # sol.minAbsoluteSumDiff(nums1 = [2,4,6,8,10], nums2 = [2,4,6,8,10]),
    # sol.minAbsoluteSumDiff(nums1 = [1,10,4,4,2,7], nums2 = [9,3,5,1,7,4]),
    sol.countDifferentSubsequenceGCDs(nums = [6,10,3]),
    sol.countDifferentSubsequenceGCDs(nums = [5,15,40,5,6]),
]
for r in result:
    print(r)
