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
https://leetcode.cn/contest/weekly-contest-263
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """

class Bank:
    """ 2043. 简易银行系统 """
    def __init__(self, balance: List[int]):
        self.balances = [0] + balance
        self.n = len(balance)

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        if account1>self.n or account2>self.n: return False
        if self.balances[account1] >= money:
            self.balances[account1] -= money
            self.balances[account2] += money
            return True
        return False

    def deposit(self, account: int, money: int) -> bool:
        if account>self.n: return False
        self.balances[account] += money
        return True

    def withdraw(self, account: int, money: int) -> bool:
        if account>self.n or self.balances[account] < money: return False
        self.balances[account] -= money
        return True

class Solution:
    """ 2042. 检查句子中的数字是否递增 """
    def areNumbersAscending(self, s: str) -> bool:
        last = -1
        for token in s.strip().split():
            if token[0] in string.digits:
                num = int(token)
                if num <= last: return False
                last = num
        return True
    
    """ 2044. 统计按位或能得到最大值的子集数目 #medium #题型
给定一组数字, 将它们依次 「按位或」 得到一个最大值 maxNum, 现要求 list 的所有子集中, 这些集合中的元素按位或可以得到该 maxNum 的组合数量.
复杂度: 数组长度 n<=16
思路1: 暴力遍历 #二进制枚举. 时间复杂度: O(2^n * n). 第二个因子n是指需要对于数组元素进行按位或操作.
    之前想多了, 考虑到本题的数组长度有限, 暴力枚举所有可能的组合就行
思路2: 通过 #DFS 记录状态, 避免重复枚举
    在上面的思路中, 例如计算 (1,2,3) 位的or 与计算 (1,2,3,4) 位的or 是相互独立的, 因此有重复计算.
    可以采用DFS, 用空间来避免重复计算. `dfs(i, orVal)` 表示枚举第 i 个位置时的状态为 orVal.
思路3: 利用 #DP 来记录状态
    用 dp[mask] 表示利用 mask 所表示的那些数字的 or 和
    如何利用之前的数来帮助计算? 我们可以将 mask 分解成两部分然后对这两个数计算或. 如何划分? 可以利用 **位运算得到一个数字最低位1的位置 lowbit**.
    例如, `6=0b0110` 的最低位为 `lowbit = 6 & -6 = 0b0010`, 因此,
    递推公式: `dp[mask] = dp[mask-lowbit] | nums[lowbitIdx]`
see [here](https://leetcode.cn/problems/count-number-of-maximum-bitwise-or-subsets/solution/by-ac_oier-dos6/)
"""
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        """ 位压缩的枚举, 时间复杂度 O(2^n * n) """
        n = len(nums)
        maxOr = 0
        count = 0
        for i in range(1, 1<<n):
            num = 0
            for j in range(n):
                if i & (1<<j): num |= nums[j]
            if num > maxOr:
                maxOr = num
                count = 1
            elif num == maxOr:
                count += 1
        return count
    
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        """ 通过 DFS 避免了重复枚举, 时间复杂度 O(2^n) """
        maxOr, count = 0, 0
        def dfs(i, orVal):
            if i==len(nums):
                nonlocal maxOr, count
                if orVal > maxOr:
                    maxOr = orVal
                    count = 1
                elif orVal == maxOr:
                    count += 1
                return
            dfs(i+1, orVal | nums[i])
            dfs(i+1, orVal)
        dfs(0, 0)
        return count
    
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        """ dp[mask] 表示利用 mask 所表示的那些数字的 or 和
        如何利用之前的数来帮助计算? 我们可以将 mask 分解成两部分然后对这两个数计算或. 如何划分? 可以利用 **位运算得到一个数字最低位1的位置 lowbit**.
        例如, `6=0b0110` 的最低位为 `lowbit = 6 & -6 = 0b0010`, 因此,
        递推公式: `dp[mask] = dp[mask-lowbit] | nums[lowbitIdx]`
        """
        # 将 lowbit 转为 idx, 例如 0b0100 转为 2
        lowbit2idx = {}
        for i in range(20):
            lowbit2idx[1<<i] = i
        
        dp = [0] * (1<<len(nums))
        maxOr, count = 0,0
        for i in range(1, 1<<len(nums)):
            lowbit = i & -i
            dp[i] = dp[i-lowbit] | nums[lowbit2idx[lowbit]]
            if dp[i] > maxOr:
                maxOr = dp[i]
                count = 1
            elif dp[i] == maxOr: count += 1
        return count
    
sol = Solution()
result = [
    # sol.areNumbersAscending(s = "sunset is at 7 51 pm overnight lows will be in the low 50 and 60 s"),
    # sol.areNumbersAscending(s = "4 5 11 26"),
    
    sol.countMaxOrSubsets(nums = [2,2,2]),
    sol.countMaxOrSubsets(nums = [3,2,1,5]),
    
    
]
for r in result:
    print(r)
