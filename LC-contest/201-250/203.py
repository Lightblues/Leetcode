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
https://leetcode.cn/contest/weekly-contest-203
@2022 """
class Solution:
    """ 1560. 圆形赛道上经过次数最多的扇区 """
    def mostVisited(self, n: int, rounds: List[int]) -> List[int]:
        if rounds[0] == rounds[-1]: return rounds[:1]
        s,e = rounds[0], rounds[-1]
        if s<e: return list(range(s, e+1))
        else: return list(range(1, e+1)) + list(range(s, n+1))
    
    """ 1561. 你可以获得的最大硬币数目 """
    def maxCoins(self, piles: List[int]) -> int:
        piles.sort()
        n = len(piles)//3
        ans = 0
        for i in range(2, 2*n+1, 2):
            ans += piles[-i]
        return ans
    
    """ 1562. 查找大小为 M 的最新分组 #medium #题型 #并查集
给定一个排列表示按照一定顺序将某些位置从0变为1. 要求记录这一过程中数字1所组成的序列的各个长度(两侧为0). 问这一序列中, 长度为m的全1序列最后出现的时刻.
思路1: 采用 #并查集 来记录相邻元素的连接关系, 并记录每一个组的大小.
    在模拟这一排列的操作的过程中, 用一个全局 szCnt 记录当前所有组的大小计数.
"""
    def findLatestStep(self, arr: List[int], m: int) -> int:
        n = len(arr)
        fa = list(range(n+2))       # 左右哨兵
        sz = [0] * (n+2)
        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        def getSz(x):
            return sz[find(x)]
        def union(x,y):
            fx,fy = find(x), find(y)
            if fx==fy: return
            fa[fx] = fy
            sz[fy] += sz[fx]
        def addSz(x):
            fx = find(x)
            sz[fx] += 1
            return sz[fx]
        
        ans = -1
        szCnt = Counter()
        for i,x in enumerate(arr):
            sm = szCnt[m]
            sl,sr = getSz(x-1), getSz(x+1)
            if sl>0:
                szCnt[sl] -= 1
                union(x-1, x)
            if sr>0:
                szCnt[sr] -= 1
                union(x+1, x)
            szCnt[sl+sr+1] += 1
            if szCnt[m]>0:  # 符合要求
                ans = i+1
            addSz(x)
        return ans


    """ 1563. 石子游戏 V #hard
有一系列的石子, A每次将其分成左右两部分, B丢弃总和较大的那部分, A得到剩余部分的分数. 然后A再次划分剩余部分... 问A能得到的最大分数.
限制: 石子数量 500
思路1: DP 需要用到 #前缀和
    记 `f(l,r)` 表示A从该子数组得到的最大分数. 边界l==r. 否则 `f(l,r) = max{ s[l:i]+f(l,i), s[j:r]+f(j:r) }` 其中i/j的划分依据是左右两则的分数和更小者.
    复杂度: 注意状态转移的复杂度为n, 因此总体复杂度为 `O(n^3)` 用Python写会超时! #TLE
思路2: 对于上述DP过程优化 #hardhard
    观察上面的递推 `f(l,r) = max{ s[l:i]+f(l,i), s[j:r]+f(j:r) }`. 这里i/j的范围由约束, **取左还是右半部分的依据是左右两侧的分数和哪个更小**. 我们不妨记 `maxl(l,r) = max{ s[l:i]+f(l,i) }; maxr(l,r) = max{ s[j:r]+f(j:r) }`.
    这样, 假设l/r的「均衡分割点」为i0, 则 `f(l,r) = max{ maxl(l,i0)+maxr(i0+2,r) }` (这里「均衡」的定义见官答, 参见下面的代码, 还有边界条件).
    另外, 这里 maxl,maxr 的表达式中还包含f, 因此需要按照一定的顺序来计算. 下面双重循环中, 外层l从左到右, 内层r从右到左, 在此过程中维护分割点.
    复杂度: 这样f的计算就是O(1), 而分割点的维护平均也是O(1), 因此整体 `O(n^2)` [官答](https://leetcode.cn/problems/stone-game-v/solution/shi-zi-you-xi-v-by-leetcode-solution/)
"""
    def stoneGameV(self, stoneValue: List[int]) -> int:
        # 思路1: DP 但是 TLE
        n = len(stoneValue)
        acc = list(accumulate(stoneValue, initial=0))
        @lru_cache(None)
        def f(l,r):
            if l==r: return 0
            ans = 0
            for i in range(l, r):
                sl,sr = acc[i+1]-acc[l], acc[r+1]-acc[i+1]
                if sl<=sr:
                    ans = max(ans, sl+f(l,i))
                if sl>=sr:      # 注意, 两侧相等时, 取较大值
                    ans = max(ans, sr+f(i+1,r))
            return ans
        return f(0,n-1)
        
    def stoneGameV(self, stoneValue: List[int]) -> int:
        # 思路2: 对于上述DP过程优化
        n = len(stoneValue)
        f = [[0] * n for _ in range(n)]
        maxl = [[0] * n for _ in range(n)]
        maxr = [[0] * n for _ in range(n)]

        for left in range(n - 1, -1, -1):
            maxl[left][left] = maxr[left][left] = stoneValue[left]
            total = stoneValue[left]
            suml = 0
            i = left - 1
            for right in range(left + 1, n):        # 确保 l<r
                total += stoneValue[right]
                # 维护「均衡」点. 要求 s[l:i] <= s[i+1:r]
                while i + 1 < right and (suml + stoneValue[i + 1]) * 2 <= total:
                    suml += stoneValue[i + 1]
                    i += 1
                # 更新 f[left][right]
                if left <= i:
                    f[left][right] = max(f[left][right], maxl[left][i])
                if i + 1 < right:
                    f[left][right] = max(f[left][right], maxr[i + 2][right])
                if suml * 2 == total:       # 边界: 均衡点平均分割
                    f[left][right] = max(f[left][right], maxr[i + 1][right])
                # 更新 maxl, maxr
                maxl[left][right] = max(maxl[left][right - 1], total + f[left][right])
                maxr[left][right] = max(maxr[left + 1][right], total + f[left][right])
        
        return f[0][n - 1]

sol = Solution()
result = [
    # sol.findLatestStep(arr = [3,5,1,2,4], m = 1),
    # sol.findLatestStep(arr = [3,1,5,4,2], m = 2),
    sol.stoneGameV(stoneValue = [6,2,3,4,5,5]),
    sol.stoneGameV(stoneValue = [7,7,7,7,7,7,7]),
    sol.stoneGameV(stoneValue = [4]),
]
for r in result:
    print(r)
