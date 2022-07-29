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
https://leetcode.cn/contest/weekly-contest-219
@2022 """
class Solution:
    """ 1690. 石子游戏 VII #medium
有一排石子表示不同的分数, AB轮流选择从左右两侧取石子, 得到的分数为剩余石子的分数之和. 可知A总会获胜. 会两者都在最优决策下分数差值.
提示: AB两人是「对称」的, 因此对于 stones[i...j], 我们可以用 f[i,j] 表示最优分数即可
思路1: 推导分数递归关系, 采用 #DP
    根据上述f的定义, 考虑递推式: `f[i,j] = max{ s[i,j-1] - f[i,j-1], s[i+1,j] - f[i+1,j] }` 分表表示取左右石子的情况. 边界: i==j 时分数为0.
    复杂度: O(n^2)
"""
    def stoneGameVII(self, stones: List[int]) -> int:
        n = len(stones)
        acc = list(accumulate(stones, initial=0))
        f = [[0] * n for _ in range(n)]
        for i in range(n-1, -1, -1):
            for j in range(i+1, n):
                f[i][j] = max(
                    acc[j]-acc[i] - f[i][j-1],
                    acc[j+1]-acc[i+1] - f[i+1][j]
                )
        return f[0][n-1]
    
    
    """ 1691. 堆叠长方体的最大高度 #hard
有一组长方体 `(w,l,h)` 要进行堆叠. 当i的三个长度都小于j时, 可以将其叠在上面. 问最大堆叠高度. 长方体可以旋转.
限制: 数量 100.
提示: 根据提示可以推测, 最优的方案时把高度为度用最长的一组. 证明: 假设有一种最优排列每个块表示为 `(wi,li,hi)`, 我们对于这些纬度按照从小到大顺序重排列得到 `(wi',lj',hi')`, 可以证明对于任意的 i,j, 重排列后的三元组仍然符合要求. 而重排列之后的高度显然不会减少.
    核心证明: 对于任意一组 `(wi,li,hi)<(wj,lj,hj)` 都可以证明重排列之后也是成立的. 任取一种情况, 不妨假设i的内部顺序为 hi<wi<li, j的顺序为 lj<hj<wj. 则重排列之后, `hi<li<lj, wi<li <lj<hj, li<lj<wj`. 因此调换之后的三元组也成立
思路1: 根据上述提示, 可以确定长方体的方向. 然后 #DP 来求 f[i] 表示第i个长方体作为底的最大高度
    则有递推关系 `f[i] = max{ f[j] } + hi` 其中j是所有满足可堆叠条件 `(wi,li,hi)>(wj,lj,hj)` 的长方体.
    如何保证顺序? 可以对于 (w,l,h) 进行排序. 也可以 (w+l,h) 等. 只需要「保证枚举关系的拓扑性即可」.
    见 [zero](https://leetcode.cn/problems/maximum-height-by-stacking-cuboids/solution/dui-die-chang-fang-ti-de-zui-da-gao-du-b-qzgy/)
"""
    def maxHeight(self, cuboids: List[List[int]]) -> int:
        n = len(cuboids)
        for i in range(n): cuboids[i].sort()
        cuboids.sort()
        f = [a[2] for a in cuboids]
        for i in range(n):
            for j in range(i):
            # 注意下面无脑遍历是错的! 考虑所有的长方体都相同, 则j=i+1可以堆叠到i上, 造成重复计算.
            # for j in range(n):
            #     if i==j: continue
                if cuboids[i][0]>=cuboids[j][0] and cuboids[i][1]>=cuboids[j][1] and cuboids[i][2]>=cuboids[j][2]:
                    f[i] = max(f[i], cuboids[i][2]+f[j])
        return max(f)

    
sol = Solution()
result = [
    # sol.stoneGameVII(stones = [5,3,1,4,2]),
    # sol.stoneGameVII(stones = [7,90,5,1,100,10,10,2]),
    sol.maxHeight(cuboids = [[50,45,20],[95,37,53],[45,23,12]]),
    sol.maxHeight(cuboids = [[38,25,45],[76,35,3]]),
]
for r in result:
    print(r)
