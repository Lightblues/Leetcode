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

    """ 1467. 两个盒子中球的颜色数相同的概率 #hard  """
    def getProbability(self, balls: List[int]) -> float:

sol = Solution()
result = [
    # sol.minReorder(n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]),
    sol.minReorder(5, [[4,3],[2,3],[1,2],[1,0]]),
]
for r in result:
    print(r)
