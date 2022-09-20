from tkinter import N
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
https://leetcode.cn/contest/weekly-contest-193
@2022 """
class Solution:
    """ 1480. 一维数组的动态和 """
    """ 1481. 不同整数的最少数目 """
    def findLeastNumOfUniqueInts(self, arr: List[int], k: int) -> int:
        cnt = Counter(arr)
        nums = sorted(cnt.values())
        acc = 0
        for a in nums:
            if a>k: break
            else: acc += 1; k -= a
        return len(nums) - acc
    
    """ 1482. 制作 m 束花所需的最少天数 #medium #题型
给一个 bloomDay 数组表示每朵花开的时间. 要求制作 m束花, 每朵消耗连续的 k朵花. 问最少满足时间. 限制: n 1e5; 花开时间 m 1e9
思路1: #二分. 下面基本是 #copilot 自动补全的, 恐怖.
    复杂度: O(n log(mx-mn)). 每次检查的复杂度为 O(n)
思路2: 强行 #并查集. 但没必要?
    按照开花的顺序依次将花朵加入连续的组. 具体逻辑比较多 #细节. 没必要.
    复杂度: O(n (a(n)+logn)). 主要是排序的复杂度.
"""
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        # 思路1: #二分.
        if m*k > len(bloomDay): return -1
        def check(day, m):
            acc = 0
            for i in range(len(bloomDay)):
                if bloomDay[i] <= day:
                    acc += 1
                    if acc == k: acc = 0; m -= 1
                else: acc = 0
            return m <= 0
        l, r = min(bloomDay), max(bloomDay)
        while l<r:
            mid = (l+r)//2
            if check(mid, m): r = mid
            else: l = mid + 1
        return l
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        # 思路2: 强行 #并查集. 但没必要
        n = len(bloomDay)
        # 快速返回 -1
        if m*k > n: return -1
        days = sorted(zip(bloomDay, range(n)))
        # 边界: k=1时, 特殊判断.
        if k==1: return days[m-1][0]
        fa = list(range(n))
        sz = [1] * n
        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        def merge(x,y):
            fx,fy = find(x),find(y)
            if fx==fy: return
            if fx>fy: fx,fy = fy,fx
            fa[fx] = fy
            sz[fy] += sz[fx]
            # 返回原本的两个区间的大小.
            return sz[fx], sz[fy]-sz[fx]
        acc = 0
        for d,i in days:
            # 用 -1 标记这朵花已经开放.
            bloomDay[i] = -1
            if i>0 and bloomDay[i-1]==-1:
                sx,sy = merge(i,i-1)
                # 上面判断了 k!=1, 因此不必担心 当前组大小为1的点产生误差.
                acc += (sx+sy)//k - sx//k - sy//k
            if i<n-1 and bloomDay[i+1]==-1:
                sx,sy = merge(i,i+1)
                acc += (sx+sy)//k - sx//k - sy//k
            if acc>=m: return d
        
""" 1483. 树节点的第 K 个祖先 #hard #倍增 #题型 #hardhard
给定一棵树, 要求快速查询节点的 k级祖先. 限制: k<=n 5e4; 查询 5e4
思路1: #倍增 法 Binary Lifting
    直觉思想是建立指数级别的索引. 也即 1,2,4,8... 级祖先节点.
    定义 `f[i][j]` 是节点 i 的 `2^j` 祖先节点. 则 `f[i][j] = f[f[i][j-1]][j-1]`.
    于是, 问题转化为 DP 形式. 我们在初始化的时候构建这样转移表. 复杂度 O(n logd)
    如何查询? 对于查询的级别k, 根据其二进制形式搜索. 每次查询的复杂度 O(d).
    see [here](https://leetcode.cn/problems/kth-ancestor-of-a-tree-node/solution/dfsceng-ci-bian-li-er-fen-cha-zhao-bei-zeng-shi-ya/)
思路2: 利用 #DFS 给每个节点打编号, 并记录每个节点的深度信息. 查询的时候根据所在层找到对应的祖先节点.
    提示: **由DFS的访问顺序可知, 节点的祖先的序号一定小于该节点的序号**. 我们在对应的层上找到「小于该节点序号的最大序号」即可.
    [here](https://leetcode.cn/problems/kth-ancestor-of-a-tree-node/solution/er-xu-cheng-ming-jiu-xu-zui-python3shen-orrck/)
"""
# 思路1: 倍增思想
class TreeAncestor:
    def __init__(self, n: int, parent: List[int]):
        f = [[parent[i]] for i in range(n)]
        for j in range(1, n):
            flag = False        # 标记是否还有节点需要更新.
            for i in range(n):
                if f[i][j-1]==-1: 
                    f[i].append(-1) # -1 标记不存在.
                    continue
                t = f[f[i][j-1]][j-1]
                f[i].append(t)
                flag = True
            # 所有的节点的 2^j 的祖先都是 -1 了，就不用再计算了
            if not flag: break
        self.f = f

    def getKthAncestor(self, node: int, k: int) -> int:
        # 1) 递归形式
        # 返回 node 的第 k 级祖先节点.
        # -1 标记为不存在.
        if node==-1: return -1
        if k==0: return node
        # 最高位所在的位置.
        j = k.bit_length()
        # 放置越界
        if j>len(self.f[node]): return -1
        return self.getKthAncestor(self.f[node][j-1], k-(1<<j-1))
    
    def getKthAncestor(self, node:int, k: int) -> int:
        # 2) 迭代形式
        j = 0
        while k!=0 and node != -1:
            if j > len(self.f[node]): return -1
            if k&1: node = self.f[node][j]
            k>>=1
            j += 1
        return node

# 思路2: 利用DFS的访问顺序.
class TreeAncestor:
    def __init__(self, n: int, parent: List[int]):
        son = defaultdict(list)
        for i in range(n):
            son[parent[i]].append(i)

        # 深搜顺序
        self.order_num = [-1]*n
        self.num_order = [-1]*n
        # 层次遍历
        self.num_level = [-1]*n         # 层级信息
        self.dct = defaultdict(list)    # 某一层汇总包含的节点 (order)
        order = 0
        def dfs(num, level):
            nonlocal order
            self.num_order[num] = order
            self.order_num[order] = num
            self.num_level[num] = level
            self.dct[level].append(order)
            order += 1
            for node in son[num]:
                dfs(node, level+1)
            return
        dfs(0, 0)

    def getKthAncestor(self, node: int, k: int) -> int:
        level = self.num_level[node]
        if level < k:
            return -1
        # 二分查找
        # 性质: 由DFS的访问顺序可知, 节点的祖先的序号一定小于该节点的序号
        # 在对应的层上找到「小于该节点序号的最大序号」
        i = bisect.bisect_left(self.dct[level-k], self.num_order[node]) - 1
        order = self.dct[level-k][i]
        return self.order_num[order]


sol = Solution()
result = [
    # sol.findLeastNumOfUniqueInts(arr = [5,5,4], k = 1),
    # sol.minDays(bloomDay = [1,10,3,10,2], m = 3, k = 1),
    # sol.minDays(bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3),
    testClass("""["TreeAncestor","getKthAncestor","getKthAncestor","getKthAncestor"]
[[7,[-1,0,0,1,1,2,2]],[3,1],[5,2],[6,3]]""")
]
for r in result:
    print(r)
