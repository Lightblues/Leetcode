from turtle import st
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
https://leetcode.cn/contest/weekly-contest-246
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1903. 字符串中的最大奇数 """
    def largestOddNumber(self, num: str) -> str:
        for i in range(len(num)-1, -1, -1):
            if int(num[i]) & 1:
                return num[:i+1]
        return ""
    
    """ 1904. 你完成的完整对局数 #medium #题型
一个完整的棋局时长15分钟, 都是整点, 也即 HH:00, HH:15, HH:30, HH:45 之间的. 现在给定开始结束时间, 问其中包含多少个完整时间.
思路1: 转为 #整数 #取整.
    小时的权重为60转为整数, 然后除以15算差值, 注意分别上下取整.
    注意边界: "00:47" "00:57" 这种情况可能产生 -1, 需要特别判断为 0.
"""
    def numberOfRounds(self, startTime: str, finishTime: str) -> int:
        startTime = [int(t) for t in startTime.split(':')]
        finishTime = [int(t) for t in finishTime.split(':')]
        if startTime[0]*60 + startTime[1] > finishTime[0]*60 + finishTime[1]:
            finishTime[0] += 24
        startTime = startTime[0]*60 + startTime[1]
        finishTime = finishTime[0]*60 + finishTime[1]
        finishTime = finishTime // 15
        startTime = math.ceil(startTime / 15)
        # 边界: "00:47" "00:57" 这种情况可能产生 -1
        return finishTime - startTime if finishTime - startTime >= 0 else 0

    def numberOfRounds(self, startTime: str, finishTime: str) -> int:
        """ [官答](https://leetcode.cn/problems/the-number-of-full-rounds-you-have-played/solution/ni-wan-cheng-de-wan-zheng-dui-ju-shu-by-df44r/)
        更为简洁"""
        # 转化为分钟
        t0 = 60 * int(startTime[:2]) + int(startTime[3:])
        t1 = 60 * int(finishTime[:2]) + int(finishTime[3:])
        if t1 < t0:
            # 此时 finishTime 为第二天
            t1 += 1440
        # 第一个小于等于 finishTime 的完整对局的结束时间
        t1 = t1 // 15 * 15
        return max(0, (t1 - t0)) // 15


    """ 1905. 统计子岛屿 #medium #题型
有两个大小为 (m,n) 的0/1 grid表示地图, 1相连的部分表示岛屿. 对于B中的某个岛屿, 若其所有点都在A的某个岛屿上, 则称其为A的子岛屿. 现要求返回B的所有子岛屿的个数.
限制: m,n 500; 
提示: 注意到, 只需要求出B中的所有岛屿 (联通分量), 检查该岛屿覆盖的点在A上是否均为陆地即可.
思路1: 利用 #并查集 得到B中所有的岛屿
    一开始不知道怎么求所有的岛屿, 写了个并查集, 比较繁琐.
    注意到, 并查集「并查集」也可以实现返回当前某集合/联通分量的大小. (但这里还是要遍历所有的节点)
思路2: 直接用 #BFS 得到B中所有的岛屿
    参见 题中的 [官答](https://leetcode.cn/problems/number-of-islands/solution/dao-yu-shu-liang-by-leetcode/)
复杂度: 均为 O(MN)
"""
    def countSubIslands(self, grid1: List[List[int]], grid2: List[List[int]]) -> int:
        m, n = len(grid1), len(grid1[0])
        idx2node = {}; node2idx = {}    # 两个哈希表
        # 并查集
        for i in range(m):
            for j in range(n):
                if grid2[i][j] == 1:
                    node2idx[(i,j)] = len(idx2node)
                    idx2node[len(idx2node)] = (i, j)
        fa = [i for i in range(len(idx2node))]
        def find(x):
            path = []
            while fa[x] != x:
                path.append(x)
                x = fa[x]
            for i in path:
                fa[i] = fa[x]
            return x
        def merge(x, y):
            fa[find(x)] = find(y)
        # 对每个节点进行合并
        for node in node2idx:
            i, j = node
            if i > 0 and grid2[i-1][j] == 1:
                merge(node2idx[(i-1,j)], node2idx[node])
            if i < m-1 and grid2[i+1][j] == 1:
                merge(node2idx[(i+1,j)], node2idx[node])
            if j > 0 and grid2[i][j-1] == 1:
                merge(node2idx[(i,j-1)], node2idx[node])
            if j < n-1 and grid2[i][j+1] == 1:
                merge(node2idx[(i,j+1)], node2idx[node])
        # 找到所有的联通分量, 检查
        groups = defaultdict(list)
        for i in range(len(idx2node)):
            groups[find(i)].append(idx2node[i])
        ans = 0
        for i,nodes in groups.items():
            if all(grid1[node[0]][node[1]] == 1 for node in nodes):
                ans += 1
        return ans
    
    def countSubIslands(self, grid1: List[List[int]], grid2: List[List[int]]) -> int:
        # https://leetcode.cn/problems/count-sub-islands/solution/tong-ji-zi-dao-yu-by-leetcode-solution-x32x/
        m, n = len(grid1), len(grid1[0])

        def bfs(sx: int, sy: int) -> int:
            q = deque([(sx, sy)])
            grid2[sx][sy] = 0
            # 判断岛屿包含的每一个格子是否都在 grid1 中出现了
            check = (grid1[sx][sy] == 1)
            while q:
                x, y = q.popleft()
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < m and 0 <= ny < n and grid2[nx][ny] == 1:
                        q.append((nx, ny))
                        grid2[nx][ny] = 0
                        if grid1[nx][ny] != 1:
                            check = False
            return int(check)

        ans = 0
        for i in range(m):
            for j in range(n):
                if grid2[i][j] == 1:
                    ans += bfs(i, j)
        return ans

    """ 1906. 查询差绝对值的最小值 #medium #题型
定义查询为: 给定 [start, end], 返回这一子数组中元素的「差绝对值的最小值」 注意如果范围内所有元素都相同, 则返回-1 (也即不能为0). 现给定一个数组和一组查询, 返回所有查询的结果.
限制: 数组长度 1e5, 查询数量 2e4; 数组中每个元素范围 [1,100]
思路1: #前缀和 
    注意, 这里元素的范围较小 (100) , 考虑用前缀和记录每一个前缀中所包含的元素数量
    这样, 对于任意的区间 (i,j) 都可以在O(100)的时间内查询出其中包含的元素数量. 对于每个查询计算即可.
    复杂度: (n+q)100
拓展: [这里](https://codeforces.com/problemset/problem/765/F) 将元素范围拓展到了 1e9, 只能采用离线方案了.
"""
    def minDifference(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        # 计算前缀和矩阵 numsMasks
        numsMasks = [None] * (n+1)
        mask = [0] * 101
        numsMasks[0] = mask[:]
        for i, num in enumerate(nums):
            mask[num] += 1
            numsMasks[i+1] = mask[:]
        # 计算每一个查询的结果
        ans = [101] * len(queries)
        def f(start, end):
            """ 计算最小差绝对值 """
            ans = 101; pre = None   # ans = inf
            for i in range(1, 101):
                if numsMasks[end][i] - numsMasks[start][i] > 0:
                    if pre is None:
                        pre = i
                        continue
                    ans = min(ans, i-pre)
                    pre = i
            return ans if ans!=101 else -1
        for i, (s,e) in enumerate(queries):
            ans[i] = f(s, e+1)
        return ans
    
    
    """ 0200. 岛屿数量 #medium
给定一张土地, 相互邻接的土地构成岛屿, 问图上的岛屿数量. 等价于, 联通分量的数量.
思路1: 直接 #BFS
    注意: 为了避免重复, 可以直接到grid上修改, 将访问过的点置为0.
思路2: #并查集
    [官答](https://leetcode.cn/problems/number-of-islands/solution/dao-yu-shu-liang-by-leetcode/) 给出了采用并查集, 得到联通分量数量的方法.
"""
    def numIslands(self, grid: List[List[str]]) -> int:
        # 思路1: 直接 #BFS
        m, n = len(grid), len(grid[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0,1)]
        def bfs(i,j):
            q = deque([(i,j)])
            while q:
                i,j = q.popleft()
                for di,dj in directions:
                    ni,nj = i+di, j+dj
                    if 0<=ni<m and 0<=nj<n and grid[ni][nj]=='1':
                        grid[ni][nj] = '0'
                        q.append((ni,nj))
        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j]=='1':
                    bfs(i,j)
                    ans += 1
        return ans
    
    def numIslands(self, grid: List[List[str]]) -> int:
        # 采用并查集 https://leetcode.cn/problems/number-of-islands/solution/dao-yu-shu-liang-by-leetcode/
        nr = len(grid)
        if nr == 0:
            return 0
        nc = len(grid[0])

        uf = UnionFind(grid)
        for r in range(nr):
            for c in range(nc):
                if grid[r][c] == "1":
                    grid[r][c] = "0"
                    for x, y in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                        if 0 <= x < nr and 0 <= y < nc and grid[x][y] == "1":
                            uf.union(r * nc + c, x * nc + y)
        
        return uf.getCount()
    
class UnionFind:
    def __init__(self, grid):
        m, n = len(grid), len(grid[0])
        self.count = 0
        self.parent = [-1] * (m * n)
        self.rank = [0] * (m * n)
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "1":
                    self.parent[i * n + j] = i * n + j
                    self.count += 1
    
    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, x, y):
        rootx = self.find(x)
        rooty = self.find(y)
        if rootx != rooty:
            if self.rank[rootx] < self.rank[rooty]:
                rootx, rooty = rooty, rootx
            self.parent[rooty] = rootx
            if self.rank[rootx] == self.rank[rooty]:
                self.rank[rootx] += 1
            self.count -= 1
    
    def getCount(self):
        return self.count

sol = Solution()
result = [
    # sol.largestOddNumber(num = "52"),
    # sol.largestOddNumber(num = "4206"),
    # sol.numberOfRounds(startTime = "12:01", finishTime = "12:44"),
    # sol.numberOfRounds(startTime = "20:00", finishTime = "06:00"),
    # sol.numberOfRounds(startTime = "00:00", finishTime = "23:59"),
    # sol.numberOfRounds(startTime = "6:00", finishTime = "20:00"),
    
    # sol.countSubIslands(grid1 = [[1,1,1,0,0],[0,1,1,1,1],[0,0,0,0,0],[1,0,0,0,0],[1,1,0,1,1]], grid2 = [[1,1,1,0,0],[0,0,1,1,1],[0,1,0,0,0],[1,0,1,1,0],[0,1,0,1,0]]),
    # sol.countSubIslands(grid1 = [[1,0,1,0,1],[1,1,1,1,1],[0,0,0,0,0],[1,1,1,1,1],[1,0,1,0,1]], grid2 = [[0,0,0,0,0],[1,1,1,1,1],[0,1,0,1,0],[0,1,0,1,0],[1,0,0,0,1]]),
    # sol.minDifference(nums = [1,3,4,8], queries = [[0,1],[1,2],[2,3],[0,3]]),
    # sol.minDifference(nums = [4,5,2,2,7,10], queries = [[2,3],[0,2],[0,5],[3,5]]),
    sol.numIslands(grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]),
]
for r in result:
    print(r)
