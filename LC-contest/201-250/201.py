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
https://leetcode.cn/contest/weekly-contest-201
@2022 """
class Solution:
    """ 1544. 整理字符串 """
    def makeGood(self, s: str) -> str:
        idx = 0
        diff = ord('a') - ord('A')
        while idx<len(s)-1:
            c1, c2 = s[idx], s[idx+1]
            c1,c2 = ord(c1),ord(c2)
            if c1==c2+diff or c1==c2-diff:
                s = s[:idx] + s[idx+2:]
                # 边界: idx==0
                idx = 0 if idx==0 else idx-1
            else: idx+=1
        return s
    def makeGood(self, s: str) -> str:
        # 官答中更优雅的写法
        ret = list()
        for ch in s:
            if ret and ret[-1].lower() == ch.lower() and ret[-1] != ch:
                ret.pop()
            else:
                ret.append(ch)
        return "".join(ret)

    """ 1545. 找出第 N 个二进制字符串中的第 K 位 #medium #模拟 """
    def findKthBit(self, n: int, k: int) -> str:
        # 思路1: 由于整体的长度有限, 直接构造 1...20 所有的字符串
        n2bin = {}
        v = '0'; n2bin[1] = v
        for i in range(2, 21):
            # 注意这里不能是迭代器, 不然会死循环!!!
            v = v + '1' + ''.join(['1' if c=='0' else '0' for c in v[::-1]])
            n2bin[i] = v
        return n2bin[n][k-1]
    def findKthBit(self, n: int, k: int) -> str:
        # 思路2: #反向 #模拟 构造过程. 注意第n个字符串的长度为 2^n -1, 其中前 2^(n-1)-1 位就是上一轮的字符串, 后 2^(n-1)-1 是上一轮字符串取反翻转的结果.
        if k == 1:
            return "0"
        
        mid = 1 << (n - 1)
        if k == mid:
            return "1"
        elif k < mid:
            return self.findKthBit(n - 1, k)
        else:
            k = mid * 2 - k
            return "0" if self.findKthBit(n - 1, k) == "1" else "1"


    """ 1546. 和为目标值且不重叠的非空子数组的最大数目 #medium #题型 #贪心
给定一个数组 (有正有负), 要求找到最多的 **不重叠子数组, 要求这些子数字的和为target**.
思路1: #贪心 每次尽量考左选择数组
    原因: 「对于某个满足条件的子数组，如果其右端点是所有满足条件的子数组的右端点中最小的那一个，则该子数组一定会被选择」 见[官答](https://leetcode.cn/problems/maximum-number-of-non-overlapping-subarrays-with-sum-equals-target/solution/he-wei-mu-biao-zhi-de-zui-da-shu-mu-bu-zhong-die-f/)
    因此, 每次在左侧子数组中尝试匹配, 利用哈希表来记录 #前缀和 即可
"""
    def maxNonOverlapping(self, nums: List[int], target: int) -> int:
        ans = 0
        acc = 0; prefix = set([0])
        for a in nums:
            acc += a
            if acc-target in prefix:
                ans += 1
                acc = 0; prefix = set([0])
            else:
                prefix.add(acc)
        return ans
            
    """ 1547. 切棍子的最小成本 #hard #题型
对于一个长n的棍子, 需要在m个整数点进行切割, 每次切割的代价为当前切割棍子的长度. 问最小代价.
限制: n 1e6; m 100
思路1: #DP 采用 #记忆化 形式
    记 `f(i,j)` 为ij两个割点的子段切割的最小代价. 则有 `f(i,j) = cost[i,j] + min(f(i,k) + f(k,j))`. 边界: j=i+1
    复杂度: 状态空间 O(m^2), 转移 m, 因此 `O(m^3)`
"""
    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts.sort()
        cuts = [0] + cuts + [n]
        ll = len(cuts)
        @lru_cache(None)
        def f(i,j):
            # if j==i+1: return cuts[j]-cuts[i]
            if j==i+1: return 0
            ans = inf
            for c in range(i+1,j):
                ans = min(ans, f(i,c)+f(c,j))
            # print(i,j, ans + cuts[j]-cuts[i])
            return ans + cuts[j]-cuts[i]
        return f(0,ll-1)
    
    
sol = Solution()
result = [
    # sol.makeGood("abBAcC"),
    # sol.findKthBit(n = 3, k = 1),
    # sol.findKthBit(4,11),
    # sol.findKthBit(2,3),
    # sol.maxNonOverlapping(nums = [-1,3,5,1,4,2,-9], target = 6),
    sol.minCost(n = 7, cuts = [1,3,4,5]),
    sol.minCost(n = 9, cuts = [5,6,1,4,2]),
]
for r in result:
    print(r)
