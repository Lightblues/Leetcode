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
https://leetcode.cn/contest/weekly-contest-210
@2022 """
class Solution:
    """ 1614. 括号的最大嵌套深度 """
    def maxDepth(self, s: str) -> int:
        depth = 0
        ans = 0
        for ch in s:
            if ch=='(':
                depth += 1
                ans = max(ans, depth)
            elif ch==')': depth -= 1
        return ans
    
    """ 1615. 最大网络秩 """
    def maximalNetworkRank(self, n: int, roads: List[List[int]]) -> int:
        degree = [0] * n
        g = set()
        for a,b in roads:
            degree[a]+=1
            degree[b]+=1
            g.add((a,b)); g.add((b,a))
        ans = 0
        for i in range(n):
            for j in range(i+1,n):
                ans = max(ans, degree[i] + degree[j] - ((i,j) in g))
        return ans
    
    """ 1616. 分割两个字符串得到回文串 #medium 两个等长字符串a,b, 问能否在某处分割, 使得交叉后的某一字符串为回文串 """
    def checkPalindromeFormation(self, a: str, b: str) -> bool:
        def check(s):
            return s[::-1]==s
        n = len(a)
        i = 0
        while i<n-i-1 and a[i]==b[n-i-1]: i+=1
        if check(a[i:n-i]) or check(b[i:n-i]): return True
        i = 0
        while i<n-i-1 and b[i]==a[n-i-1]: i+= 1
        if check(a[i:n-i]) or check(b[i:n-i]): return True
        return False
    
    """ 1617. 统计子树中城市之间最大距离 #hard
n个城市之间的联通关系恰好构成一棵树. 要求返回这棵树的子树中, 节点之间最大距离(直径)分别为 1...n-1 的数量.
限制 n<=15
思路1: 子集遍历, 对于每一个子集检查是否为子树及其直径.
    复杂度: 2^n * n
    如何 **查询一棵树上的直径**? 采用 #树形 DP
        任取一个点作为root, 在遍历孩子的过程中记录经过这个点的 `max_depth, max_dist`. 采用递归的形式计算. 假设当前值为 `max_depth, max_dist`, 遍历下一个孩子节点返回了 `mdepth, mdist`, 进行更新: `max_depth = max(max_depth, mdepth+1), max_dist = max(max_dist, mdist, max_depth+mdepth+1)`.
思路2: 与其用上面的形式来找所有可能的子集/树, 我们一开始就固定树的结构 (单向图). 然后, 对于每一个树节点, 我们统计 **经过该节点的子树的所有统计结果(子问题)**. 注意到, 因为我们一开始固定了树结构, 所以不会产生重复计数, 所以答案就是子问题之和.
    如何在上面的 #树形 DP 的框架下实现结果的统计? 用 `count{dist:cnt}` 表示当前遍历中的结果, `subcount` 表示下一个孩子节点的统计结果, 对于这两个结果进行交叉即可.
"""
    def countSubgraphsForEachDiameter(self, n: int, edges: List[List[int]]) -> List[int]:
        # 思路1 see https://leetcode.cn/problems/count-subtrees-with-max-distance-between-cities/solution/mei-ju-zi-ji-shu-xing-dp-by-lucifer1004/
        # build the graph
        g = [[] for _ in range(n)]
        for u,v in edges:
            u,v = u-1,v-1
            g[u].append(v); g[v].append(u)
        
        # tree dp.
        def dfs(root, ava) -> List[int]:
            # 参数传递形式: 当前遍历的跟节点; 可用节点;
            # 返回 max_depth, max_dist, nnodes为root子树上的节点数目
            ava.remove(root)    # remove the root from ava
            nnodes = 1          # count the nodes in the subtree rooted at root
            max_depth, max_dist = 0, 0  # initialize the max_depth and max_dist
            for child in g[root]:
                if child not in ava: continue
                mdepth, mdist, nn = dfs(child, ava)
                nnodes += nn
                max_dist = max(max_dist, mdist, max_depth+mdepth+1)
                max_depth = max(max_depth, mdepth+1)
            return max_depth, max_dist, nnodes
        
        ans = [0]*(n-1)
        for mask in range(1, 1<<n):
            nodes = set(i for i in range(n) if (mask>>i)&1)
            root = next(iter(nodes))    # 取一个集合中的元素
            max_depth, max_dist, nnodes = dfs(root, nodes)
            if max_depth==0: continue
            if nnodes==mask.bit_count():
                ans[max_dist-1]+=1
        return ans

    def countSubgraphsForEachDiameter(self, n: int, edges: List[List[int]]) -> List[int]:
        # 树形DP , from https://leetcode.cn/problems/count-subtrees-with-max-distance-between-cities/solution/python3-shu-xing-dp-by-simpleson/
        # d[maxDepth][maxDist] 统计最大深度为maxDepth的最大距离为maxDist的子树数目
        # 数据结构：
        dict2d = lambda:collections.defaultdict(collections.Counter)
        def dict2d_iter(mat: dict2d):
            for L,row in mat.items():
                for R,val in row.items():
                    yield L,R,val
        
        # 建树：
        links = dict2d()
        for L,R in edges:   # 先构建双向图
            links[L][R]=1
            links[R][L]=1
        BFS = [1]           # 转为以节点1为根的树, 有向边
        for L in BFS:
            for R in links[L]:
                BFS.append(R)
                links[R].pop(L)
        
        # 动态规划：
        # 统计所有以L为根节点的子树数目，按"最大深度"和"最大节点间距离"分类
        @lru_cache(None)
        def subcount(L:int) -> dict2d:
            # 状态初始化
            count = dict2d()        # count[maxDepth][maxDist] 统计最大深度为maxDepth的最大距离为maxDist的子树数目
            count[0][0]=1
            if not links[L]:
                return count
            # 状态转移
            for R in links[L]:
                # count实时记录; 在遍历L节点的子节点的过程中, 将R子树和L节点已统计过的子树进行合并.
                upd = dict2d()
                for depthR,distR,cntR in dict2d_iter(subcount(R)):
                    for depth,dist,cnt in dict2d_iter(count):       # 此时count不包含R子树.
                        upd[max(depth,depthR+1)][max(dist,distR,depth+depthR+1)]+=cnt*cntR
                for d in upd:
                    count[d]+=upd[d]
            return count
        # 将所有节点的子树信息加起来
        total = collections.Counter()
        for node in range(1,n+1):
            for dist_cnt in subcount(node).values():
                total += dist_cnt       # Counter 可以应用加法
        return [total[i] for i in range(1,n)]


    
sol = Solution()
result = [
    sol.countSubgraphsForEachDiameter(n = 4, edges = [[1,2],[2,3],[2,4]]),
]
for r in result:
    print(r)
