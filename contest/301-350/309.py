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
https://leetcode.cn/contest/weekly-contest-309

T2 考虑了好久, 但本质上就是一个简单的数学模型...T4 题型还不错.

@2022 """
class Solution:
    """ 6167. 检查相同字母间的距离 """
    def checkDistances(self, s: str, distance: List[int]) -> bool:
        ch2idx = defaultdict(list)
        for i,ch in enumerate(s):
            ch2idx[ord(ch)-ord('a')].append(i)
        for i,d in enumerate(distance):
            if i in ch2idx:
                if ch2idx[i][1] - ch2idx[i][0] != d+1: return False
        return True
    
    """ 2400. 恰好移动 k 步到达某一位置的方法数目 #medium
走k步向右移动x单位, 问有多少种方式, 对结果取模. 限制: start,end,k 都在 1e3 范围内
思路1: #数学 
    本质上就是 Comb(x, (k-x)//2)
思路2: #DP 或者 #记忆化
    例如定义 f(x， left) 表示剩余left步骤从x位置出发, 到达终点的方法数.
[灵神](https://leetcode.cn/problems/number-of-ways-to-reach-a-position-after-exactly-k-steps/solution/by-endlesscheng-6yvy/)
"""
    def numberOfWays(self, startPos: int, endPos: int, k: int) -> int:
        mod = 10**9 + 7
        d = abs(startPos-endPos)
        if k<d or (k-d)&1: return 0
        xx = (k-d)//2
        return math.comb(k, xx) % mod
    
    """ 6169. 最长优雅子数组 #medium 找到数组中的最长子数组, 其所有元素的AND结果都为0.
思路1: 基本的 #滑动窗口
"""
    def longestNiceSubarray(self, nums: List[int]) -> int:
        l = 0
        ans = 0
        xorr = 0
        for r,num in enumerate(nums):
            while xorr & num:
                xorr ^= nums[l]
                l += 1
            xorr |= num
            ans = max(ans, r-l+1)
        return ans
    
    
    """ 6170. 会议室 III #hard #题型
有一组 [s,e) 的会议 和 n个会议室. 安排会议的逻辑是: 优先选此时空闲的最小会议室; 若没有空闲则延期, 会议的优先级为开始时间.
思路1: 维护两个 #最小堆, 分别记录「空闲的会议室」和「使用中的会议室」, 分别根据会议室序号, 和结束时间排序.
    从小到大遍历会议时, 将此时已经结束的会议室放到 spared中.
"""
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort()
        spared = list(range(n))
        heapify(spared)
        used = []
        cnt = [0] * n
        for s,e in meetings:
            while used and used[0][0] <= s:
                _,idx = heappop(used)
                heappush(spared, idx)
            if spared:
                idx = heappop(spared)
                heappush(used, (e, idx))
                cnt[idx] += 1
            else:
                end,i = heappop(used)
                cnt[i] += 1
                heappush(used, (end + e-s, i))
        return cnt.index(max(cnt))
    
sol = Solution()
result = [
    # sol.checkDistances(s = "abaccb", distance = [1,3,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    # sol.checkDistances(s = "aa", distance = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    # sol.longestNiceSubarray(nums = [1,3,8,48,10]),
    # sol.longestNiceSubarray([3,1,5,11]),
    sol.mostBooked(n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]),
    sol.mostBooked(n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]),
    sol.mostBooked(4, [[18,19],[3,12],[17,19],[2,13],[7,10]]),
    # sol.numberOfWays(startPos = 1, endPos = 2, k = 3),
    # sol.numberOfWays(startPos = 2, endPos = 5, k = 10),
]
for r in result:
    print(r)
