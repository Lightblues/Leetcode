import tty
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

""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-57
@2022 """
class Solution:
    """ 1941. 检查是否所有字符出现次数相同 """
    def areOccurrencesEqual(self, s: str) -> bool:
        c = Counter(s)
        cc = list(c.values())
        return all(cc[i]==cc[i-1] for i in range(1, len(cc)))
    
    """ 1942. 最小未被占据椅子的编号 """
    def smallestChair(self, times: List[List[int]], targetFriend: int) -> int:
        # 展开 arrival 和 leaving 时间
        allTimes = []
        for f, (a,l) in enumerate(times):
            # 需要先处理离开的人
            allTimes.append((a,1,f))
            allTimes.append((l,0,f))
        allTimes.sort()
        # 模拟
        available = SortedList(range(len(times)))
        f2idx = {}
        for t,ttype, f in allTimes:
            if ttype == 1:
                idx = available.pop(0)
                if f==targetFriend: return idx
                # available.remove(f)
                f2idx[f] = idx
            elif ttype == 0:
                available.add(f2idx[f])
        return -1
    
    
    """ 1943. 描述绘画结果 """
    def splitPainting(self, segments: List[List[int]]) -> List[List[int]]:
        maxn = max(s[1] for s in segments)
        pivots = set()
        acc = [0] * (maxn+1)
        for s,e,c in segments:
            pivots.add(s)
            pivots.add(e)
            acc[s] += c
            acc[e] -= c
        for i in range(1, maxn+1):
            acc[i] += acc[i-1]
        pivots = sorted(pivots)
        ans = []
        for s,e in zip(pivots, pivots[1:]):
            # 注意需要排除空的部分!!!
            if acc[s]==0: continue
            ans.append([s,e,acc[s]])
        return ans
    
    """ 1944. 队列中可以看到的人数 #hard #单调栈
思路1: #单调栈
    
"""
    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        ans = [0] * n
        stack = []
        # stack.append(heights[-1])
        for i in range(n-1, -1, -1):
            h = heights[i]
            c = 0
            while stack and stack[-1] < h:
                stack.pop()
                c += 1
            ans[i] = c + (len(stack)>0)
            stack.append(h)
        return ans
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [
    # sol.smallestChair(times = [[1,4],[2,3],[4,6]], targetFriend = 1),
    # sol.smallestChair(times = [[3,10],[1,5],[2,6]], targetFriend = 0),
    # sol.smallestChair([[4,5],[12,13],[5,6],[1,2],[8,9],[9,10],[6,7],[3,4],[7,8],[13,14],[15,16],[14,15],[10,11],[11,12],[2,3],[16,17]],15),
    
    # sol.splitPainting(segments = [[1,4,5],[4,7,7],[1,7,9]]),
    # sol.splitPainting(segments = [[1,4,5],[1,4,7],[4,7,1],[4,7,11]]),
    
    sol.canSeePersonsCount(heights = [10,6,8,5,11,9]),
    sol.canSeePersonsCount(heights = [5,1,2,3,10]),
]
for r in result:
    print(r)
