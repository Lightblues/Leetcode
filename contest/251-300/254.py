import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, cache, reduce, partial
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-254
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1967. 作为子字符串出现在单词中的字符串数目 """
    def numOfStrings(self, patterns: List[str], word: str) -> int:
        return sum(p in word for p in patterns)
    
    """ 1968. 构造元素不等于两相邻元素平均值的数组
要求重拍之后的每一个元素, 其不等于左右元素的均值
"""
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        nums.sort()
        ans = []
        i,j = 0, len(nums)-1
        while i<j:
            ans.extend([nums[i], nums[j]])
            i,j = i+1, j-1
        if i==j:
            ans.append(nums[i])
        return ans
    
    """ 1969. 数组元素的最小非零乘积 #medium
给定一个位数p, 对于从1到(2^p)-1一共 `(2^p)-1` 个数字, 我们可以对其中的两个数字进行同位交换的操作(不允许使得数字变为0); 要求最后所有数字的乘积最小
同位交换操作: 例如 x = 1101 且 y = 0011, 我们交换右起第二位后得到 x = 1111 和 y = 0001
约束: p最大到60
思路1: 观察 #归纳 #快速幂
    观察p=3时的情况, 事实上我们比较容易有猜想, 公式也容易得到 $\left(2^{p}-1\right) \cdot\left(2^{p}-2\right)^{2^{p-1}-1}$ .
    注意到, 在 `(2^p)-1` 个数字中, 每一位上出现1的个数为 `2^(p-1) - 1` 次.
    要让乘积尽可能小, 猜想是尽可能将1集中到大数字上. 因此, 分配这些1到各个位上, 可以得到 `(2^(p-1))-1` 个 11..110, `(2^(p-1))-1` 个 00..001, 还有一个 11..111 (因为多了一个最低位1)
    证明见 [灵神](https://leetcode.cn/problems/minimum-non-zero-product-of-the-array-elements/solution/tan-xin-ji-qi-shu-xue-zheng-ming-by-endl-uumv/)
快速幂: `2^p` 可能非常大, 如果直接用 `x**n` 会超时, 应该采用Python的快速幂函数 `pow(x,n,MOD)`. 参见 0050 题.

输入：p = 3
输出：1512
解释：nums = [001, 010, 011, 100, 101, 110, 111]
- 第一次操作中，我们交换第二个和第五个元素最左边的数位。
    - 结果数组为 [001, 110, 011, 100, 001, 110, 111] 。
- 第二次操作中，我们交换第三个和第四个元素中间的数位。
    - 结果数组为 [001, 110, 001, 110, 001, 110, 111] 。
数组乘积 1 * 6 * 1 * 6 * 1 * 6 * 7 = 1512 是最小乘积。
"""
    def minNonZeroProduct(self, p: int) -> int:
        MOD = 10**9+7
        if p==1: return 1
        if p==2: return 6
        n = (2**(p - 1) - 1)
        a = ((2**p) - 2)
        # ans = (a**n * (a+1)) % MOD
        # ans = a+1
        # for i in range(n):
        #     ans = (ans*a) % MOD
        ans = pow(a, n, MOD)
        ans = (ans*(a+1)) % MOD
        return ans
    
    """ 1970. 你能穿过矩阵的最后一天 #hard #题型 #可达性
对于一个 (row, col) 的gird, 目标是从第一行的任意位置到达最后一行的任意位置. 最开始所有单元都是陆地, 给定一个序列, 每一天会淹没一块陆地, 要求能达到最后一行的最大天数.
思路1: 反向 #BFS
    我们从最后的状态反向往前推: 哪一天可以找到一条路径了, 就找到了答案.
    如何避免重复的路径搜索? 用visited记录已经访问的节点. 同时用一个set来记录可以抵达的被淹没节点 —— 这样, 当某一天刚被淹没的单元出现在set中时, 我们即可将它加回queue中继续搜索.
    总结: 本题是可达性判断的变种, 还挺有意思的.
思路2: 二分搜索
    官答给出的一种解法, 复杂度 r*c* log(r*c), 其中对数项为二分.
思路3: #并查集
    也是从后往前考虑: 如果最后一行和第一行属于同一个集合, 则存在路径.
    为此, 定义两个超级节点, 分别连接第一行和最后一行的所有单元. 在从后往前的过程中, 每新增一块陆地, 就将其和相邻陆地连接, 然后检查这两个超级节点是否连接.
[here](https://leetcode.cn/problems/last-day-where-you-can-still-cross/solution/ni-neng-chuan-guo-ju-zhen-de-zui-hou-yi-9j20y/)
"""
    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        # 思路1: BFS
        grid = [[0]*(col+1) for _ in range(row+1)]
        for i,j in cells:
            grid[i][j] = 1
        q = deque()
        frontier = set()    # 
        for j in range(1, col+1):
            if grid[1][j]==0:
                q.append((1,j))
                grid[1][j] = 2
            else:
                frontier.add((1,j))
        
        def getNext(i,j):
            for di,dj in [(0,1),(0,-1),(1,0),(-1,0)]:
                if 0<i+di<=row and 0<j+dj<=col:
                    yield (i+di,j+dj)
        def search(q):
            while q:
                i,j = q.popleft()
                # 在pop的时候检查条件
                if i==row: return True
                for ni,nj in getNext(i,j):
                    if grid[ni][nj]==0:
                        if ni==row:
                            return True
                        q.append((ni,nj))
                        grid[ni][nj] = 2
                    elif grid[ni][nj]==1:
                        frontier.add((ni,nj))
            return False
        r = search(q)
        if r: return len(cells)
        for day in range(len(cells),0,-1):
            i,j = cells[day-1]
            if (i,j) in frontier:
                grid[i][j] = 2
                q.append((i,j))
                r = search(q)
                if r: return day-1
            else:
                grid[i][j] = 0
        return -1

    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        """ 思路2: 并查集 """
        # 编号为 n 的节点是超级节点 s
        # 编号为 n+1 的节点是超级节点 t
        n = row * col
        uf = UnionFind(n + 2)

        valid = [[0] * col for _ in range(row)]
        ans = 0
        for i in range(n - 1, -1, -1):
            x, y = cells[i][0] - 1, cells[i][1] - 1
            valid[x][y] = 1
            # 并查集是一维的，(x, y) 坐标是二维的，需要进行转换
            idx = x * col + y
            if x - 1 >= 0 and valid[x - 1][y]:
                uf.unite(idx, idx - col)
            if x + 1 < row and valid[x + 1][y]:
                uf.unite(idx, idx + col)
            if y - 1 >= 0 and valid[x][y - 1]:
                uf.unite(idx, idx - 1)
            if y + 1 < col and valid[x][y + 1]:
                uf.unite(idx, idx + 1)
            if x == 0:
                uf.unite(idx, n)
            if x == row - 1:
                uf.unite(idx, n + 1)
            if uf.connected(n, n + 1):
                ans = i
                break
        
        return ans


# 并查集模板
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.n = n
        # 当前连通分量数目
        self.setCount = n
    
    def findset(self, x: int) -> int:
        if self.parent[x] == x:
            return x
        self.parent[x] = self.findset(self.parent[x])
        return self.parent[x]
    
    def unite(self, x: int, y: int) -> bool:
        x, y = self.findset(x), self.findset(y)
        if x == y:
            return False
        if self.size[x] < self.size[y]:
            x, y = y, x
        self.parent[y] = x
        self.size[x] += self.size[y]
        self.setCount -= 1
        return True
    
    def connected(self, x: int, y: int) -> bool:
        x, y = self.findset(x), self.findset(y)
        return x == y


sol = Solution()
result = [
    # sol.minNonZeroProduct(28),
    # [sol.minNonZeroProduct(i) for i in range(1,10)],
    
    # sol.latestDayToCross(row = 2, col = 2, cells = [[1,1],[2,1],[1,2],[2,2]]),
    # sol.latestDayToCross(row = 2, col = 2, cells = [[1,1],[1,2],[2,1],[2,2]]),
    # sol.latestDayToCross(row = 3, col = 3, cells = [[1,2],[2,1],[3,3],[2,2],[1,1],[1,3],[2,3],[3,2],[3,1]]),
    # sol.latestDayToCross(2,6,[[1,2],[2,5],[2,3],[1,1],[1,3],[1,5],[2,1],[1,6],[2,4],[2,2],[2,6],[1,4]]),
    
]
for r in result:
    print(r)
