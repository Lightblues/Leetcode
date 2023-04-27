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
from numpy import sort

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
https://leetcode.cn/contest/weekly-contest-221
@2022 """
class Solution:
    """ 1704. 判断字符串的两半是否相似 """
    def halvesAreAlike(self, s: str) -> bool:
        l,r = s[:len(s)//2], s[len(s)//2:]
        lc, rc = Counter(l), Counter(r)
        lcc = sum(v for k,v in lc.items() if k in 'aeiouAEIOU')
        rcc = sum(v for k,v in rc.items() if k in 'aeiouAEIOU')
        return lcc==rcc
    
    """ 1705. 吃苹果的最大数目 #medium #题型
有一棵苹果树, 第i天长出 apples[i] 个苹果, 它们在 days[i] 后腐烂. 你每天最多吃一个, 问最多能吃几颗.
限制: 天数i 2e4, 苹果和腐烂天数 2e4
思路0: 暴力 #TLE
    一开始的贪心策略是, 从后往前遍历, 对于每一颗苹果, 尽量在最晚的时间吃. 但这样的复杂度为 O(n^2), 超时了.
思路1: 也是 #贪心, 用一个 #最小堆 记录所有苹果的腐烂日期, 每次选择腐烂日期最近的苹果吃 (数量 -1)
    堆元素: `(day, cnt)`. 注意需要分n天之内树上长苹果, 和n天之外剩余的苹果两部分.
"""
    def eatenApples(self, apples: List[int], days: List[int]) -> int:
        # 暴力, 超时
        ava = [False] * 5*10**4
        n = len(apples)
        for i in range(n-1, -1, -1):
            a,d = apples[i], days[i]
            idx = i+d-1
            while a>0 and idx>=i:
                if ava[idx]==False:
                    ava[idx] = True
                    a-=1
                idx -= 1
        return sum(ava)
    
    def eatenApples(self, apples: List[int], days: List[int]) -> int:
        # 思路1
        h = []
        ans = 0
        for i,(a,d) in enumerate(zip(apples, days)):
            while h and h[0][0]<=i:
                heappop(h)
            if a>0:
                heappush(h, [i+d, a])
            if h:
                ans += 1
                h[0][1]-=1
                if h[0][1]==0: heappop(h)
        # 还剩余的苹果
        d = len(apples)
        while h:
            while h and h[0][0]<=d: heappop(h)
            if h:
                ans += 1
                h[0][1]-=1
                if h[0][1]==0: heappop(h)
            d += 1
        return ans
        
    """ 1706. 球会落何处
用一个grid表示该位置挡板的方向 (`/\`), 从最上边的每一个位置放小球, 返回小球最后落在的位置, 若无法掉出来 (挡板呈现V字形) 则返回 -1.
提示: 注意球无法掉下来的条件: 1) 出现V字形或者 2) 到达边界无法再往边界方向.
    参见 daily2202 写的js版本
"""
    def findBall(self, grid: List[List[int]]) -> List[int]:
        m,n = len(grid), len(grid[0])
        ans = [-1] * n
        for i in range(n):
            col = i
            for r in range(m):
                direction = grid[r][col]
                col += direction
                if col<0 or col>=n or grid[r][col]!=direction:
                    break
            # 注意这里的语法! 当 for 正常退出时执行
            else:
                ans[i] = col
        return ans
    
    
    """ 1707. 与数组中元素的最大异或值 #hard
参见 trie, 这里自己重新写一遍
思路: 离线查询. 根据查询动态插入字典树
"""
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        MX = 30
        class Node:
            def __init__(self) -> None:
                self.left = None
                self.right = None
        def add(root: Node, x:int):
            for i in range(MX, -1, -1):
                b = x & (1<<i)
                if b==0:
                    if root.left is None: root.left = Node()
                    root = root.left
                else:
                    if root.right is None: root.right = Node()
                    root = root.right
        def query(root: Node, x:int):
            # 查询树中值与x的最大值
            if root.left is None and root.right is None: return -1
            mx = 0
            for i in range(MX, -1, -1):
                b = x & (1<<i)
                if b==0:
                    if root.right is not None: mx = (mx<<1)+1; root = root.right
                    else: mx <<= 1; root = root.left
                else:
                    if root.left is not None: mx = (mx<<1)+1; root = root.left
                    else: mx <<=1; root = root.right
            return mx
        
        root = Node()
        nums.sort(); idx = 0
        ans = [-1] * len(queries)
        queries = sorted((m,x,i) for i,(x,m) in enumerate(queries))
        for m,x,i in queries:
            while idx<len(nums) and nums[idx]<=m:
                add(root, nums[idx]); idx += 1
            ans[i] = query(root, x)
        return ans

sol = Solution()
result = [
    # sol.eatenApples(apples = [1,2,3,5,2], days = [3,2,1,4,2]),
    # sol.eatenApples(apples = [3,0,0,0,0,2], days = [3,0,0,0,0,2]),
    # sol.eatenApples([2,1,10],[2,10,1]),
    # sol.findBall(grid = [[1,1,1,-1,-1],[1,1,1,-1,-1],[-1,-1,-1,1,1],[1,1,1,1,-1],[-1,-1,-1,-1,-1]]),
    # sol.findBall(grid = [[1,1,1,1,1,1],[-1,-1,-1,-1,-1,-1],[1,1,1,1,1,1],[-1,-1,-1,-1,-1,-1]]),
    # sol.maximizeXor(nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]),
    sol.maximizeXor([5,2,4,6,6,3],[[12,4],[8,1],[6,3]])
    
    
]
for r in result:
    print(r)
