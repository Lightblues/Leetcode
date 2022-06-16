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

""" 
https://leetcode-cn.com/contest/biweekly-contest-59
@2022 """
class Solution:
    """ 1974. 使用特殊打字机键入单词的最少时间 """
    def minTimeToType(self, word: str) -> int:
        p = 0
        word = [ord(i)-ord('a') for i in word]
        ans = 0
        for ch in word:
            move = min(abs(ch-p), 26-abs(ch-p))
            ans += move + 1
            p = ch
        return ans
    
    """ 1975. 最大方阵和 """
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        # m, n = len(matrix), len(matrix[0])
        nums = list(itertools.chain(*matrix))
        cnt = sum(i<0 for i in nums)
        abss = [abs(i) for i in nums]
        return sum(abss) if cnt%2==0 else sum(abss)-2*min(abss)
    
    """ 1976. 到达目的地的方案数 #medium #题型 #最短路径
求出从s到e的最短路径的数量.
约束: 节点数量 n为200, 题目确保了是连通图; 需要对答案取 MOD
思路1: #BFS
    题目中提示了要对答案取模, 说明了等长的路径数量可能很多, 不能暴力累计所有路径.
    因此, 在BFS过程中维护一张哈希表 `cnt` 记录每个节点的最短路径数, 然后在到达v的时候增加计数 `cnt[v] + cnt[u]`
    如何保证每次增加的计数都是正确/最短的? PQ中的元素为到达节点v的 cost 以及 (u,v) 信息. 也即, 每次取出的一定是到v的最短路径.
    需要注意的是, 一个节点可能会被多次加入 PQ, 如何保证不会出现重复? 仅第一次拓展的时候入 PQ即可.
思路2: 先计算所有节点的最短路径, 然后在构造的 #DAG 上 #DP 求解路径数量.
    具体而言, 在计算到每个点的距离之后,构建一个DAG仅包含最短路径上的边, $\operatorname{dist}[v]-\operatorname{dist}[u]=\operatorname{length}(u \rightarrow v)$
    然后在这张图上DP就比较直观了.
    [官答](https://leetcode.cn/problems/number-of-ways-to-arrive-at-destination/solution/dao-da-mu-de-di-de-fang-an-shu-by-leetco-5ptp/)
总结: 是计算「最短路径数量」的题型
"""
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        # 思路1.1: used 记录已经计算过的边 (u,v); 相较于下面的优化有冗余的部分
        MOD = 10**9+7
        g = [list() for _ in range(n)]
        for u,v,c in roads:
            g[u].append((c,v))
            g[v].append((c,u))
        minCost = [inf] * n
        cnt = [0] * n
        minCost[0] = 0
        cnt[0] = 1
        used = set()    # used 记录已经计算过的边 (u,v). 因为两点之间可能由多条路径相连, 但由于采用了cnt每条边只应该计算一次.
        # (cost, v, u) 确保第一次更新的就是最短路径
        # pq = [(c,u,0) for c,u in g[0]]
        # heapify(pq)
        pq = [(0,0,-1)]
        while pq:
            c, v, u = heappop(pq)
            if c > minCost[v]: continue
            if (u,v) in used: continue
            used.add((u,v))
            minCost[v] = c
            cnt[v] = (cnt[v] + cnt[u]) % MOD
            for c,w in g[v]:
                if c+minCost[v] < minCost[w]:
                    heappush(pq, (c+minCost[v], w, v))
        return cnt[-1] % MOD
    
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        # 思路1.2: 仅第一次拓展的时候入 PQ
        MOD = 10**9+7
        g = [list() for _ in range(n)]
        for u,v,c in roads:
            g[u].append((c,v))
            g[v].append((c,u))
        minCost = [inf] * n
        cnt = [0] * n
        minCost[0] = 0
        cnt[0] = 1
        visited = set() # 记录所有拓展过的节点
        # (cost, v, u) 确保第一次更新的就是最短路径
        # pq = [(c,u,0) for c,u in g[0]]
        # heapify(pq)
        pq = [(0,0,-1)]
        while pq:
            c, v, u = heappop(pq)
            if c > minCost[v]: continue
            minCost[v] = c
            if u!=-1:   # 根节点
                cnt[v] = (cnt[v] + cnt[u]) % MOD
            # 仅第一次遍历到时拓展
            if v in visited: continue
            for c,w in g[v]:
                if c+minCost[v] < minCost[w]:
                    heappush(pq, (c+minCost[v], w, v))
            visited.add(v)
        return cnt[-1] % MOD
    
    """ 1977. 划分数字的方案数 #hard #题型
给定一个数字串, 问有多少种分割方式, 使其变为非递减的正数序列, 要求数字没有前导零.
约束: 数字长度 n<=3500. 注意最多支持 O(n^2) 复杂度.
思路1:
    DP框架
        形式: `f[i][j]` 表示对于序列nums[0...j]的分割方案中, 最后一个数字为 nums[i...j] 的方案数.
        迭代: 既然最有一个数字为 nums[i...j] 其要满足条件要求上一个数字 nums[k...i-1] 更小, 因此迭代公式为 `f[i][j] = sum{ f[k][i-1] }` 这里的k的范围为上面的约束
            注意数字不包含前导零, 因此若 `j-i > i-1 - k` 则一定满足, 反之则不满足. 两者相等时的情况需要另外讨论 (见下).
            因此, 求和范围为 `2i-j(or -1) ... i-1`.
        边界: f[0][...] = 1; 要求的答案为 sum{f[...][n-1]}
        前缀和优化: 直接求和复杂度 O(n^3) 不够. 可以采用前缀和计算. 记 pre[k][i-1] 为上一迭代中的前缀和, 则有 `f[i][j] = pre[i][i-1] - pre[2i-j(or -1)]` 其实是否有 2i-j-1 项根据 nums[2i-j-1...i-1] <=nums[i...j] 判断.
            观察: 实际上不用前缀和利用迭代也可. 假如我们按照 i,j 的前后顺序来进行两次枚举, 根据 j, j+1 两个相邻状态的元素, 发现后者只多了1/2项, 因此用一个idx记录累计的元素即可.
        LCP: 预计算 #最长公共前缀, 快速比较两个数的大小
            上述过程中, 还需要比较 `nums[2i-j-1...i-1], nums[i...j]` 两个数字的大小, 但直接算的复杂度为 O(k), 会超时
            用 DP 预计算LCP, 形式为: lcp[i][j] 表示分别从 i,j 位置出发向右的最长公共串长度.
            显然有递推公式: 若num[i]==num[j] 则有 `lcp[i][j] = lcp[i+1][j+1] + 1`, 否则为 0.
            在此基础上, 比较 `nums[2i-j-1...i-1], nums[i...j]` 的大小就很简单: 若 lcp[i][2i-j-1] >= j-i+1, 说明公共部分比比较的部分更长, 满足大于等于; 否则, 直接比较 num[i+ll], num[2i-j-1+ll] 即可.
[官答](https://leetcode.cn/problems/number-of-ways-to-separate-numbers/solution/hua-fen-shu-zi-de-fang-an-shu-by-leetcod-env6/)
总结: 想到DP迭代公式就挺难的; 更为复杂的是之后的LCP等技巧. 本题比较综合.
"""
    def numberOfCombinations(self, num: str) -> int:
        """ 没有用LCP, 超时了 """
        # 边界: 第一个数字为0
        if num[0] == '0': return 0
        
        def compare(a,b, c,d):
            # test num[c...d] >= num[a...b]
            assert b-a == d-c
            for i in range(a, b+1):
                if num[i] > num[c+i-a]: return False
                elif num[i] < num[c+i-a]: return True
            return True
        
        n = len(num)
        # f = [0] * n
        f = [[0] * n for _ in range(n)]
        for j in range(n):
            f[0][j] = 1
        # ans = 1
        for i in range(1, n):
            s = 0
            # 边界情况: 不能有前缀 0
            if num[i]=='0': continue
            left = i
            # range of sum: 2i-j(or -1) ... i-1
            for j in range(i, n):
                newLeft = max(2*i-j, 0)
                if newLeft > 0:
                    if compare(2*i-j-1,i-1, i,j):
                        newLeft -= 1
                for ii in range(newLeft, left):
                    s += f[ii][i-1]
                left = newLeft
                f[i][j] = s
        return sum(l[-1] for l in f)

    def numberOfCombinations(self, num: str) -> int:
        """ [官答](https://leetcode.cn/problems/number-of-ways-to-separate-numbers/solution/hua-fen-shu-zi-de-fang-an-shu-by-leetcod-env6/) """
        MOD = 10**9 + 7
        # 边界: 第一个数字为0
        if num[0] == '0': return 0
        n = len(num)
        
        # DP计算 LCP矩阵
        lcp = [[0]*n for _ in range(n)]
        # 仅计算 i>j 的下三角部分
        for j in range(n-1):
            if num[j]==num[n-1]: lcp[n-1][j] = 1
        for i in range(n-2, -1, -1):
            for j in range(i):
                if num[i]==num[j]:
                    lcp[i][j] = lcp[i+1][j+1] + 1
        # 封装比较 nums[2i-j-1...i-1], nums[i...j] 两数字大小的函数
        def compare(a,b, c,d):
            # test num[c...d] >= num[a...b]
            assert b-a == d-c
            ll = lcp[c][a]
            if ll>=b-a+1: return True
            return num[c+ll] >= num[a+ll]
        
        f = [[0] * n for _ in range(n)]
        for j in range(n):
            f[0][j] = 1
        for i in range(1, n):
            s = 0
            # 边界情况: 不能有前缀 0
            if num[i]=='0': continue
            left = i
            # range of sum: 2i-j(or -1) ... i-1
            for j in range(i, n):
                newLeft = max(2*i-j, 0)
                if newLeft > 0:
                    if compare(2*i-j-1,i-1, i,j):
                        newLeft -= 1
                for ii in range(newLeft, left):
                    s += f[ii][i-1]
                    s %= MOD
                left = newLeft
                f[i][j] = s
        return sum(l[-1] for l in f) % MOD


    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [
    # sol.minTimeToType(word = "bza"),
    # sol.minTimeToType(word = "zjpc"),
    # sol.maxMatrixSum(matrix = [[1,-1],[-1,1]]),
    # sol.maxMatrixSum(matrix = [[1,2,3],[-1,-2,-3],[1,2,3]]),
    # sol.countPaths(n = 7, roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],[3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]),
    sol.numberOfCombinations(num = "327"),
    sol.numberOfCombinations(num = "094"),
    sol.numberOfCombinations(num = "9999999999999"),
    sol.numberOfCombinations("1203"),
    
]
for r in result:
    print(r)
