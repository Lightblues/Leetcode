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
https://leetcode.cn/contest/weekly-contest-207
@2022 """
class Solution:
    """ 1592. 重新排列单词间的空格 """
    def reorderSpaces(self, text: str) -> str:
        nshape = 0
        words = []
        wstart, inword = -1, False
        for i,ch in enumerate(text + ' '):
            if ch==' ':
                if inword:
                    words.append(text[wstart:i])
                    inword = False
                nshape += 1
            else:
                if not inword:
                    inword = True; wstart = i
        nshape -= 1
        # 边界
        if len(words)==1: 
            return words[0] + ' '*nshape
        # 这里要求 len(words) > 1
        s,r = divmod(nshape, len(words)-1)
        return (' '*s).join(words) + " "*r
    def reorderSpaces(self, text: str) -> str:
        # 借助py特性
        sep = ' '
        words = text.split()
        cnt = len(words)
        spaces = text.count(sep)
        sep_num = spaces // (cnt - 1)  if cnt >= 2 else 0
        return (sep * sep_num).join(words) + sep * (spaces - sep_num * (cnt - 1))

    """ 1593. 拆分字符串使唯一子字符串的数目最大 #medium
给定一个字符串, 要求拆分成若干不同的子字符串, 要求拆分数量最大. 限制: 长度 16
思路1: 暴力搜索即可, 用一个全局列表/字典记录当前分割, 采用 #回溯 的方式写.
"""
    def maxUniqueSplit(self, s: str) -> int:
        wds = []
        n = len(s)
        ans = 1
        def f(idx):
            nonlocal ans
            if idx==n:
                ans = max(ans, len(wds)); return
            for nidx in range(idx+1,n+1):
                if s[idx:nidx] not in wds:
                    wds.append(s[idx:nidx]); f(nidx); wds.pop()

        f(0)
        return ans
    
    
    """ 1594. 矩阵的最大非负积 #题型
给定一个grid, 问从左上角到右下角的所有路径中, 最大的非负积是多少?
提示: 应该存储的信息不是「能取到的最大正数/最小负数是多少」, 而应该是以当前点结束的路径值的范围.
思路1: 用DP存储路径中的最大和最小值 (注意, 不是大于/小于零的部分). 
    这是因为, 假设长为l-1的路径可以取到的范围 `[mn,mx]`, 若当前数值x为正, 则不管该区间范围是正是负, 新的范围总是 `[x*mn, x*mx]`, 反之亦然.
    见 [官答](https://leetcode.cn/problems/maximum-non-negative-product-in-a-matrix/solution/ju-zhen-de-zui-da-fei-fu-ji-by-leetcode-solution/)
"""
    def maxProductPath(self, grid: List[List[int]]) -> int:
        mod = 10**9+7
        m,n = len(grid), len(grid[0])
        # 哨兵. 但按照官答中的写法更简便
        mx = [[-1]*(n+1) for _ in range(m+1)]
        mn = [[1]*(n+1) for _ in range(m+1)]
        mx[0][1] = 1    # 初始化
        for i in range(m):
            for j in range(n):
                a = grid[i][j]
                if a>=0:
                    mx[i+1][j+1] = a * max(mx[i][j+1], mx[i+1][j])
                    mn[i+1][j+1] = a * min(mn[i][j+1], mn[i+1][j])
                else:
                    mx[i+1][j+1] = a * min(mn[i][j+1], mn[i+1][j])
                    mn[i+1][j+1] = a * max(mx[i][j+1], mx[i+1][j])
        return mx[-1][-1]%mod if mx[-1][-1]>=0 else -1
    
    """ 1595. 连通两组点的最小成本 #hard #interest #题型
有两组点, 其中 size1>=size2. 两组点之间两两可以连接, 有不同的代价. 要求每个点至少与另一组的一个点连接. 问最小连接代价. 限制: 点数量 12
提示:
    题目是矩阵的形式给了两组点的连接cost. 那就索性用矩阵的角度: 问题等价于从矩阵中选若干点, 要求每一行/每一列至少选择了一个.
思路1: #状压
    采用 #DP #子集枚举 求解. 记 `f(i,mask)` 表示选择了前i行, 已选列的状压表示为mask情况下的最小代价. 
        注意, mask更大反而有可能得到更小的解 `f(i-1, mask) > f(i-1, mask|1<<j)`. 
    递推需要考虑两种情况
        情况1, 第一组中第i个点占用掉第二组中某些点: 子集枚举取最小值 `min{ sum(cost[i,sub]) + f(i-1, mask\sub) }`. 由于第i行至少要选一个, 这里的sub不为空集/全集.
        情况2, 第一组中第i个点和同组至少另外一个点 有共同的第二组中的邻居. 此时不发生独占, 显然前i-1个点已经是的组2中mask点都满足条件了. 因此第i个点只需要需要随便连接一个点即可 `f(i-1,mask) + min{ cost[i,subset(mask)] }`, 这里的subset直接取所有大小为1的子集即可.
    复杂度: 外层for循环 Om, 每一次进行子集枚举 O3^n, 对于mask计算代价需要 On, 因此总体复杂度 `O(mn 3^n)`.
    #TLE: 一开始计算代价的 `m2cost(i,mask)` 没有 #记忆化 结果超时了.
思路2: 拓展
    当最小带权边覆盖问题的权值均为非负数时，可以转换成最大带权匹配问题，后者有多项式时间复杂度的解法（例如 KM 算法、最小费用流等）
    see [zero](https://leetcode.cn/problems/minimum-cost-to-connect-two-groups-of-points/solution/kai-kai-yan-jie-zhuan-huan-cheng-zui-da-dai-quan-p/)
"""
    def connectTwoGroups(self, cost: List[List[int]]) -> int:
        m,n = len(cost), len(cost[0])
        # 一开始没加 cache 过不了, 加了之后 8s+
        @lru_cache(None)
        def m2cost(i,mask):
            idxs = (idx for idx in range(n) if mask&(1<<idx))
            return sum(cost[i][idx] for idx in idxs)
        MX = 1<<n
        f = [m2cost(0,m) for m in range(MX)]
        for i in range(1,m):
            for mask in range(MX-1, 0, -1):
                # 注意, 这里不能初始化为 inf. f[mask] = inf
                # 下面一开始居然瞎猫碰上个死老鼠, 撞对了
                # 2) 第一组中第i个点和同组至少另外一个点 有共同的第二组中的邻居
                idxs = (idx for idx in range(n) if mask&(1<<idx))
                f[mask] += min(cost[i][idx] for idx in idxs)
                # 子集枚举
                # 1) 第一组中第i个点单独和第二组中某个点连接
                sub = (mask-1) & mask
                while sub:
                    f[mask] = min(f[mask-sub] + m2cost(i,sub), f[mask])
                    sub = (sub-1) & mask
        return f[-1]

    
sol = Solution()
result = [
    # sol.maxProductPath(grid = [[-1,-2,-3],
    #          [-2,-3,-3],
    #          [-3,-3,-2]]),
    # sol.maxProductPath(grid = [[1,-2,1],
    #          [1,-2,1],
    #          [3,-4,1]]),
    # sol.maxProductPath(grid = [[1, 3],
    #          [0,-4]]),
    sol.connectTwoGroups(cost = [[15, 96], [36, 2]]),
    sol.connectTwoGroups(cost = [[1, 3, 5], [4, 1, 1], [1, 5, 3]]),
]
for r in result:
    print(r)
