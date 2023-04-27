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
https://leetcode.cn/contest/weekly-contest-191

T4 难炸了... 即使是暴力DFS也需要考虑计数. 果然统计没学好...
@2022 """
class Solution:
    """ 1464. 数组中两元素的最大乘积 """
    
    """ 1465. 切割后面积最大的蛋糕 """
    def maxArea(self, h: int, w: int, horizontalCuts: List[int], verticalCuts: List[int]) -> int:
        horizontalCuts.extend([0, h])
        verticalCuts.extend([0,w])
        horizontalCuts.sort()
        verticalCuts.sort()
        return max([horizontalCuts[i+1]-horizontalCuts[i] for i in range(len(horizontalCuts)-1)]) * \
            max([verticalCuts[i+1]-verticalCuts[i] for i in range(len(verticalCuts)-1)]) % (10**9+7)
    
    """ 1466. 重新规划路线 #medium #题型 对n个节点, 若考虑无向边构成一棵树. 但初始状态是有向的, 问要修改多少条边的方向, 能使得所有节点可达点0
思路1: 维护 正向和反向图, BFS的过程中记录经历的逆向边的数量.
"""
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        g, ng = defaultdict(list), defaultdict(list)
        for u,v in connections:
            g[u].append(v)
            ng[v].append(u)
        ans = 0
        queue = [0]
        seen = set([0])
        while queue:
            u = queue.pop()
            for v in g[u] + ng[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
                    if v in g[u]: ans += 1
        return ans

    """ 1467. 两个盒子中球的颜色数相同的概率 #hard #概率 #题型 给 k种颜色的 2n个球, 随机排列前一半放在第一个盒子中. 问两个盒子中的球的颜色数量相同的概率.
限制: k 8; 每种颜色的球的数量不超过 m 6.
思路1: 暴力 #DFS 求解
    顺序遍历k中颜色, 尝试将 0...balls[i] 个球放在盒子1. 在所有的等分分配中, 计算两个盒子中球的颜色数相同的频数.
    建模: 两个袋子, 不考虑袋内顺序, 依次将 2n个球随机放到两个袋子里.
        关键是如何计数? 假设有四种颜色的球分别有 [1,2,1,2] 个, 若盒子1分配到 [1,2,0,0], 这种情况出现的频次有多少? C(1,1)*C(2,2)*C(1,0)*C(2,0)
    复杂度: `O(m^k)` 级别
    [here](https://leetcode.cn/problems/probability-of-a-two-boxes-having-the-same-number-of-distinct-balls/solution/by-yawn_sean-mg1n/)
思路2: 来自灵神的奇妙 #条件概率 求解.
    原概率(等分情况中, 两盒子颜色数相同的概率) = P(两盒子颜色数相同 & 等分) / P(等分)
    关键是如何求第一个概率? 采用 #DP.
        记 `dp[i][ndiff][diff]` 表示考虑 i...k 这些颜色, 两个盒子球数差值为 ndiff, 颜色数差值 diff 的概率.
        则有转移 `dp[i][ndiff][diff] = sum{ C(balls[i], j) / (2^balls[i]) * dp[i+1][j-k][!!j-!!k] for j+k=balls[i] }` 
            累加的每一项中, 第一个因子是「将balls[i]进行分配, 第一个盒子拿到 j个的概率」; 第二个因子是递归解.
            其实就是考虑对于 balls[i] 考虑分 j = 0...balls[i] 个球给盒子1的转移情况.
            这里的 `!!j-!!k` 就是 `int(j>0)-int(k>0)`
    复杂度: 状态空间 O(m k^2), 每次转移 O(m). 总复杂度 O(m^2 k^2)
    [灵神](https://leetcode.cn/problems/probability-of-a-two-boxes-having-the-same-number-of-distinct-balls/solution/c-dp-si-lu-gai-shu-dai-ma-by-zqy1018/)
思路3: 更加直观的 #DP
    记 `f(T, i,j,u,v)` 表示放完钱T种颜色后, 两个盒子分别有 i,j 个球, u,v 个颜色的方案数.
    则答案就是 `sum_{i}{f(k,n,n,i,i)} / sum_{i,j}f(k,n,n,i,j)`
    [here](https://leetcode.cn/problems/probability-of-a-two-boxes-having-the-same-number-of-distinct-balls/solution/c-dp-si-lu-gai-shu-dai-ma-by-zqy1018/)
"""
    def getProbability(self, balls: List[int]) -> float:
        # 思路1: 暴力 #DFS 求解
        def cnt(bag):
            # 将 balls 所代表的不同颜色的球随机放在两个盒子里, 不考虑盒中球的顺序, 盒子1出现bag所表述的情况的频次.
            ans = 1
            for b,c in zip(bag, balls):
                ans *= math.comb(c, b)
            return ans
        
        k = len(balls)
        n = sum(balls) // 2
        # 分别统计 所有的等分数量, 以及合法的 组合数量
        total = valid = 0
        bag1, bag2 = [],[]
        def dfs(idx=0):
            # DFS 尝试所有的分袋情况. 这里的逻辑比较简单.
            nonlocal total, valid, bag1, bag2
            if idx==k:
                if sum(bag1)!=sum(bag2): return
                # cnt 计算分袋的计数.
                tmp = cnt(bag1)
                total += tmp
                if sum(i>0 for i in bag1) == sum(i>0 for i in bag2): valid += tmp
            else:
                # 尝试将第 i 颜色的球放入两个盒子
                for i in range(balls[idx]+1):
                    bag1.append(i); bag2.append(balls[idx]-i)
                    dfs(idx+1)
                    bag1.pop(); bag2.pop()
        dfs(0)
        return valid / total
                
    def getProbability(self, balls: List[int]) -> float:
        # 思路2: 来自灵神的奇妙 #条件概率 求解.
        colors = len(balls)
        @lru_cache(None)
        def solve(i, ndiff, diff):
            nonlocal colors
            if i==colors: return 1 if ndiff==0 and diff==0 else 0
            ans = 0
            for j in range(balls[i]+1):
                # 分配 j,k 个球到盒子1,2
                k = balls[i]-j
                ddp = solve(i+1, ndiff-j+k, diff+int(j>0)-int(k>0))
                ans += math.comb(balls[i], j) / (2**balls[i]) * ddp
            return ans
        p1 = solve(0,0,0)
        n = sum(balls) // 2
        p2 = math.comb(sum(balls), n) / (2**sum(balls))
        return p1 / p2


sol = Solution()
result = [
    # sol.minReorder(n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]),
    # sol.minReorder(5, [[4,3],[2,3],[1,2],[1,0]]),
    sol.getProbability(balls = [1,2,1,2]),
    sol.getProbability([2,1,1]),
]
for r in result:
    print(r)
