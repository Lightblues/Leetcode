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
https://leetcode.cn/contest/weekly-contest-216
@2022 """
class Solution:
    """ 1662. 检查两个字符串数组是否相等 """
    def arrayStringsAreEqual(self, word1: List[str], word2: List[str]) -> bool:
        return  "".join(word1)=="".join(word2)
    
    """ 1663. 具有给定数值的最小字符串 #medium #题型
16个字母分别赋值 1...26, 现在要求构造长为n所有值之和为k的最小字符串.
思路: 先全填a, 然后从后往前尽量变为z
 """
    def getSmallestString(self, n: int, k: int) -> str:
        ans = [1] * n; k -= n
        idx = n-1
        while k>0:
            a = min(k, 25)
            ans[idx] += a; k -= a; idx -= 1
        return "".join([chr(ord('a')-1+i) for i in ans])
    
    """ 1664. 生成平衡数组的方案数 #medium #题型
给定一个数组, 可以删除任意idx位置的元素. 问删除之后, 奇偶位置元素和相等的情况数. (注意右侧的奇偶性发生了变化)
思路1: 分别暴力求出奇偶位置的前缀和, 然后翻转位置i后面的奇偶性来验证.
思路2: 采用 #交替 #前缀和 
    注意, **交易前缀和天然可以记录奇偶位置元素和的差值**.
    这样, 对于索引i, `dp[i-1]` 表示左边奇偶元素的差值, `dp[n]-dp[i]` 表示右边奇偶元素的差值. **去除位置i之后, 右边元素的奇偶性翻转, 因此 `dp[n]-dp[i]` 恰好表示右边奇偶元素的差值的相反数**. 因此, 判断条件为 `dp[i-1]==dp[n]-dp[i]`.
    [here](https://leetcode.cn/problems/ways-to-make-a-fair-array/solution/shuang-bai-zheng-fu-jiao-ti-qian-zhui-he-by-letian/)
"""
    def waysToMakeFair(self, nums: List[int]) -> int:
        n = len(nums)
        sodd = [0] * n; seven = [0] * n
        for i,num in enumerate(nums):
            if i%2==0:
                if i>0:
                    seven[i] = seven[i-1] + num
                    sodd[i] = sodd[i-1]
                else: seven[i] = num
            else:
                sodd[i] = sodd[i-1] + num
                seven[i] = seven[i-1]
        # 
        ans = 0
        ans += seven[-1]-seven[0] == sodd[-1]
        for i,num in enumerate(nums):
            if i==0: continue
            # if i%2==0:
            #     ans += seven[i-1]+sodd[-1]-sodd[i-1] == sodd[i-1]+seven[-1]-seven[i]
            # else:
            #     ans += seven[i-1]+sodd[-1]-sodd[i-1] == sodd[i-1]+seven[-1]-seven[i]
            ans += seven[i-1]+sodd[-1]-sodd[i] == sodd[i-1]+seven[-1]-seven[i]
        return ans
    def waysToMakeFair(self, nums: List[int]) -> int:
        # 思路2
        n = len(nums)
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i-1] + (nums[i-1] if i % 2 else -nums[i-1])

        ans = 0
        for i in range(1, n + 1):
            if dp[i - 1] == dp[n] - dp[i]:
                ans += 1

        return ans
    
    """ 1665. 完成所有任务的最少初始能量 #hard 但实际上不难
每一项任务 (actual, minimum) 需要在有至少minimum点能量的情况下才能做, 但实际消耗actual. 现给定一组任务, 问开始需要的最少能量.
思路1: 排序之后 #贪心
    注意到, 若没有minimum的限制, 则答案就是actual之和. 因为有了两者的差值, 导致最后可能剩余一些能量. 因为实际消耗的能量就是 `sum(actual)` 因此实际上产生影响的就是 `minimum-actual`. 直接对于该差值从大到小排序, 累积每次需要增加的能量即可.
思路2: 理论的不等式推导见 [zero](https://leetcode.cn/problems/minimum-initial-energy-to-finish-tasks/solution/wan-cheng-suo-you-ren-wu-de-zui-shao-chu-shi-neng-/)
"""
    def minimumEffort(self, tasks: List[List[int]]) -> int:
        tasks.sort(key=lambda x: x[1]-x[0], reverse=True)
        acc = redusal = 0
        for act,mn in tasks:
            a = max(0, mn-redusal)
            acc += a
            redusal += a-act
        return acc

sol = Solution()
result = [
    # sol.waysToMakeFair(nums = [2,1,6,4]),
    # sol.waysToMakeFair([1,1,1]),
    # sol.waysToMakeFair(nums = [1,2,3]),
    sol.minimumEffort(tasks = [[1,2],[2,4],[4,8]]),
    sol.minimumEffort(tasks = [[1,3],[2,4],[10,11],[10,12],[8,9]]),
]
for r in result:
    print(r)
