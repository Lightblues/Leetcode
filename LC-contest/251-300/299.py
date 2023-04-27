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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 6101. 判断矩阵是否是一个 X 矩阵 """
    def checkXMatrix(self, grid: List[List[int]]) -> bool:
        n = len(grid)
        for i in range(n):
            for j in range(n):
                if i==j or i+j==n-1:
                    if grid[i][j]==0: return False
                else:
                    if grid[i][j]!=0: return False
        return True
    
    """ 6100. 统计放置房子的方式数 #medium
有长为n的空地, 在上面盖房子, 要求不相邻, 问有多少种方式. 本题设置了河的两岸各有空地, 结果 ^2 即可
思路: #DP
    用 f[i][0/1] 分别表示长度为i的空地, 最后一个上有无房子的方案数量.
    递推: `f[i+1][0] = f[i][0] + f[i][1]; f[i+1][1] = f[i][0]`
"""
    def countHousePlacements(self, n: int) -> int:
        MOD = 10**9 + 7
        f = (1,1)
        for _ in range(n-1):
            f = (f[1]%MOD, (f[0]+f[1])%MOD)
        return sum(f)**2 % MOD
    
    """ 5229. 拼接数组的最大分数 #medium #题型
给定两个长度均为n的数组 nums1 和 nums2, 可以将某一数组的 [left...right] 段置换到另一个数组, 问最大可能得到的数组的和.
提示: 假设是nums2中的一段置换到nums1上, 我们计算 diff = nums1-nums2, 则问题等价于, 求diff数组上的一个连续子序列, 使其和为非正的最小值.
思路1: 问题等价于求连续子序列的最小值. #贪心 即可
    贪心: 若当前的段落的和 >0, 则这一段没有用, 直接跳过.
    遍历过程中记录curr为当前最小和, 每遍历到一个数字, curr += diff[i]; 如果计算的 curr>=0, 我们将curr重制为0即可.
"""
    def maximumsSplicedArray(self, nums1: List[int], nums2: List[int]) -> int:
        def f(nums1, nums2):
            diff = list(i-j for i, j in zip(nums1, nums2))
            minn = 0
            curr = 0
            for i in diff:
                curr += i
                minn = min(minn, curr)
                curr = min(curr, 0)
            return minn
        return max(
            sum(nums1) - f(nums1, nums2),
            sum(nums2) - f(nums2, nums1)
        )

    """ 6103. 从树中删除边的最小分数 #hard #异或
定义树的分数为, 所有节点的值的异或和. 现在给定一棵树, 可以从中删除两条边, 得到三个联通分量, 要求三个分数的最大最小值之差最小化.
约束: 节点数量 1e3
提示
    简单情况, 仅删除一条边, 对于原本树可以预计算每个节点对应子树的异或和, 这样, 假如分割掉了点node, 则两个分量的异或和分别为 `xors[node], xors[root]^xors[node]`
    问题等价于, 删除两条边将树分成三个联通分支, 要求枚举所有的可能.
思路1: 枚举所有的边, 分割成两个部分a,a', 然后再枚举a'部分的所有边, 得到 b,c, 于是枚举得到所有的三成分 a,b,c
    问题是如何枚举两条分割的边, 然后得到三个分支?
    一个基本的思路是, 递归枚举两条可能的边. 固定其第一个分支, 对于第二分支, 再枚举所有的分割边.
思路2: 直接枚举分割的两条边对, 这样就需要分类讨论分割的情况, 两种:
    若两个节点没有祖先关系, 则三个分支的异或和为 `xors[root]^xors[node1]^xors[node2], xors[node1], xors[node2]`
    若有祖先关系, 不妨设 node1 为 node2 的祖先, 则三个异或和分别为 `xors[root]^xors[node1], xors[node1]^xors[node2], xors[node2]`
    如何判断树上两个节点之间的祖先关系? **利用DFS的时间戳**
    见 [灵神](https://leetcode.cn/problems/minimum-score-after-removals-on-a-tree/solution/dfs-shi-jian-chuo-chu-li-shu-shang-wen-t-x1kk/).
复杂度: 均为 O(n^2)
总结: 注意不要采用class, 这里若用了class, 两种方案都会超时


下面前三个都超时了!
"""
    def minimumScore(self, nums: List[int], edges: List[List[int]]) -> int:
        """ 思路0: 先枚举一条边, 保留节点值较小的那棵树, 然后在节点值较大的那棵树上枚举边
        因为用了class超时了 """
        g = [[] for _ in range(len(nums))]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        class Node:
            def __init__(self, idx) -> None:
                self.idx = idx
                self.children = []
        def build(u, ban:list = []):
            # 构建树
            root = Node(u)
            q = deque([root])
            visited = set([u])
            while q:
                node = q.popleft()
                for v in g[node.idx]:
                    if v not in ban and v not in visited:
                        node.children.append(Node(v))
                        visited.add(v)
                    q.extend(node.children)
            return root
        def calc(root: Node) -> int:
            xor = 0
            for c in root.children:
                xor ^= calc(c)
            xor ^= nums[root.idx]
            root.xor = xor
            return xor
        def dfs(root: Node):
            # 根节点较小的树的xor值为 xor1. 遍历tree2上的所有边
            nonlocal xor1, ans, s
            for child in root.children:
                dfs(child)
                xor2 = child.xor
                xor3 = s^xor2
                mi,ma = min(xor1, xor2, xor3), max(xor1, xor2, xor3)
                ans = min(ans, ma-mi)
        edges = map(lambda x: sorted(x), edges)
        ans = inf
        for a in range(len(nums)):
            for b in g[a]:
                tree1 = build(a, [b])
                xor1 = calc(tree1)
                tree2 = build(b, [a])
                calc(tree2)
                xor1,s = tree1.xor, tree2.xor
                dfs(tree2)
        return ans
    
    def minimumScore(self, nums: List[int], edges: List[List[int]]) -> int:
        """ 尝试2: 暴力枚举两条边, 利用parent关系更新, 得到三个root
        但想了一下, 利用parent来更新祖先路径上的xor需要 O(n) 的时间, 整体复杂度就是 O(n^3) 肯定超时 """
        g = [[] for _ in range(len(nums))]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        class Node:
            def __init__(self, idx) -> None:
                self.idx = idx
                self.children = []
                self.parent = None
                self.xor = 0
        def build(u):
            root = Node(u)
            num2node[u] = root
            q = deque([root])
            visited = set([u])
            while q:
                node = q.popleft()
                for v in g[node.idx]:
                    if v not in visited:
                        c = Node(v)
                        c.parent = node
                        node.children.append(c)
                        visited.add(v)
                    q.extend(node.children)
            return root
        def calc(root: Node) -> int:
            xor = 0
            for c in root.children:
                xor ^= calc(c)
            xor ^= nums[root.idx]
            root.xor = xor
            return xor
        
        num2node = {}
        root = build(0)
        calc(root)
        
        nn = len(edges)
        edges = map(lambda x: sorted(x), edges)
        
        ans = inf
        roots = [root]
        for i in range(nn):
            a,b = edges[i]
            a,b = num2node[a], num2node[b]
            
            if a.parent == b:
                a,b = b,a
            roots.append(b)
            b.parent = None
            v = a.xor
            while a:
                a.xor ^= nums[a.idx]
                a = a.parent
            for j in range(i+1, nn):
                c,d = edges[j]
                c,d = num2node[c], num2node[d]
                if c.parent == d:
                    c,d = d,c
                
        
    def minimumScore(self, nums: List[int], edges: List[List[int]]) -> int:
        """ 灵神的思路, 写成class就超时了 """
        g = [[] for _ in range(len(nums))]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        class Node:
            __slots__ = ['idx', 'children', 'xor', 'time']
            def __init__(self, idx) -> None:
                self.idx = idx
                self.children = []
                self.xor = 0
                self.time = [None, None]
        def build(u):
            root = Node(u)
            num2node[u] = root
            q = deque([root])
            visited = set([u])
            while q:
                node = q.popleft()
                for v in g[node.idx]:
                    if v not in visited:
                        c = Node(v)
                        num2node[v] = c
                        # c.parent = node
                        node.children.append(c)
                        visited.add(v)
                    q.extend(node.children)
            return root
        def dfs(node: Node):
            nonlocal clock
            clock += 1
            node.time[0] = clock
            xor = 0
            for c in node.children:
                xor ^= dfs(c)
            xor ^= nums[node.idx]
            node.xor = xor
            node.time[1] = clock
            return xor
        
        def isChild(a, b):
            # a是否为b的祖先
            return a.time[0] <= b.time[0] and a.time[1] >= b.time[1]
        num2node = {}
        root = build(0)
        clock = 0
        dfs(root)
        
        ans = inf
        for (a,b), (c,d) in combinations(edges, 2):
            a,b = num2node[a], num2node[b]
            if a.time[0]>=b.time[0] and a.time[1]<=b.time[1]:
                a,b = b,a
            c,d = num2node[c], num2node[d]
            if c.time[0]>=d.time[0] and c.time[1]<=d.time[1]:
                c,d = d,c
            if isChild(b,d):
                x,y,z = root.xor^b.xor, b.xor^d.xor, d.xor
            elif isChild(d,b):
                x,y,z = root.xor^d.xor, d.xor^b.xor, b.xor
            else:
                x,y,z = root.xor^b.xor^d.xor, b.xor, d.xor
            ans = min(ans, max(x,y,z)-min(x,y,z))
        return ans
    
    def minimumScore(self, nums: List[int], edges: List[List[int]]) -> int:
        """ 思路1, 不用class就可以过 """
        g = [[] for _ in range(len(nums))]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)

        def dfs(u):
            nonlocal visited
            xorr = 0
            for v in g[u]:
                if v not in visited:
                    visited.add(v)
                    xorr ^= dfs(v)
            xorr ^= nums[u]
            return xorr
        def dfs2(u):
            nonlocal visited, xor3s
            xorr = 0
            for v in g[u]:
                if v not in visited:
                    visited.add(v)
                    xorr ^= dfs2(v)
            xorr ^= nums[u]
            xor3s.append(xorr)
            return xorr
        ans = inf
        # 这里其实是遍历了所有的边 (双向)
        for a in range(len(nums)):
            for b in g[a]:
                visited = set([b, a])
                xor1 = dfs(a)
                xor3s = []
                visited = set([a, b])
                xor2 = dfs2(b)
                for xor3 in xor3s[:-1]:
                    ans = min(ans, max(xor1, xor2^xor3, xor3)-min(xor1, xor2^xor3, xor3))
        return ans

    def minimumScore(self, nums: List[int], edges: List[List[int]]) -> int:
        """ 思路2 from https://leetcode.cn/problems/minimum-score-after-removals-on-a-tree/solution/dfs-shi-jian-chuo-chu-li-shu-shang-wen-t-x1kk/ """
        n = len(nums)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        xor, in_, out, clock = [0] * n, [0] * n, [0] * n, 0
        def dfs(x: int, fa: int) -> None:
            nonlocal clock
            clock += 1
            in_[x] = clock
            xor[x] = nums[x]
            for y in g[x]:
                if y != fa:
                    dfs(y, x)
                    xor[x] ^= xor[y]
            out[x] = clock
        dfs(0, -1)
        def is_parent(x: int, y: int) -> bool:
            return in_[x] <= in_[y] <= out[x]

        for e in edges:
            if not is_parent(e[0], e[1]):
                e[0], e[1] = e[1], e[0]
        ans = inf
        for (x1, y1), (x2, y2) in combinations(edges, 2):
            if is_parent(y1, x2):  # y1 是 x2 的父节点（或重合）
                x, y, z = xor[y2], xor[y1] ^ xor[y2], xor[0] ^ xor[y1]
            elif is_parent(y2, x1):  # y2 是 x1 的父节点（或重合）
                x, y, z = xor[y1], xor[y2] ^ xor[y1], xor[0] ^ xor[y2]
            else:  # 删除的两条边分别属于两颗不相交的子树
                x, y, z = xor[y1], xor[y2], xor[0] ^ xor[y1] ^ xor[y2]
            ans = min(ans, max(x, y, z) - min(x, y, z))
        return ans



sol = Solution()
result = [
    # sol.checkXMatrix(grid = [[2,0,0,1],[0,3,1,0],[0,5,2,0],[4,0,0,2]]),
    # sol.checkXMatrix(grid = [[5,7,0],[0,3,1],[0,5,0]]),
    # sol.countHousePlacements(n = 5),
    # sol.countHousePlacements(2),
    # sol.countHousePlacements(1),
    # sol.maximumsSplicedArray(nums1 = [60,60,60], nums2 = [10,90,10]),
    # sol.maximumsSplicedArray(nums1 = [20,40,20,70,30], nums2 = [50,20,50,40,20]),
    # sol.maximumsSplicedArray(nums1 = [7,11,13], nums2 = [1,1,1]),
    sol.minimumScore(nums = [1,5,5,4,11], edges = [[0,1],[1,2],[1,3],[3,4]]),
    sol.minimumScore(nums = [5,5,2,4,4,2], edges = [[0,1],[1,2],[5,2],[4,3],[1,3]]),
]
for r in result:
    print(r)
