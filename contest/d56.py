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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-56
@2022 """
class Solution:
    """ 1925. 统计平方和三元组的数目 #easy
总计 `1 <= a, b, c <= n` 的三元组, 满足 `a^2 + b^2 = c^2`
naive 的思路是暴力遍历, 复杂度 O(n^2).
[here](https://leetcode.cn/problems/count-square-sum-triples/solution/gei-yi-ge-on23-log-n-de-suan-fa-by-hqztr-p91c/) 给出了 O(n) 乃至更小的方法.
"""
    def countTriples(self, n: int) -> int:
        ans = 0
        for a in range(1, n):
            for b in range(a, n):
                cc = math.sqrt(a**2 + b**2)
                if int(cc) == cc and cc<=n: ans += 2
        return ans
    
    """ 1926. 迷宫中离入口最近的出口 """
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        m,n = len(maze), len(maze[0])
        def test(i,j):
            return 0<=i<m and 0<=j<n and maze[i][j]=='.'
        def testGoal(i,j):
            return i==0 or i==m-1 or j==0 or j==n-1
        q = [(entrance[0], entrance[1], 0)]
        maze[entrance[0]][entrance[1]] = '#'
        directions = ((1,0),(-1,0),(0,1),(0,-1))
        while q:
            x,y,d = q.pop(0)
            for dx,dy in directions:
                nx,ny = x+dx, y+dy
                if not test(nx,ny): continue
                if testGoal(nx,ny): return d+1
                maze[nx][ny] = "#" # mark visited
                q.append((nx,ny,d+1))
        return -1
    
    """ 1927. 求和游戏 #medium #博弈
一道博弈论: 有一个长度为 2n 的数组, 每个位置要么是 0-9, 要么为空. 游戏规则是, AB两人分别在空位填数字, 直到全部填满.
结算: 做数组左半部分之和等于右半部分, 则B获胜, 否则A获胜.
思路1: #归纳
    考虑简化情况: 记 `spaceL, spaceR` 分别为左右空格数, 若两者相等. 则A的一种策略是往和大的部分填9, 这样B只能在另一边填一个9...
        总之, 只有当 `sumL = sumR` 时 B才获胜.
    一般情况下, 不妨令右半部分有更多空格 `spaceL <= spaceR`
        显然, 当差值 `d = sumL - sumR < 0` 左侧空格更少而数值和反而更小, A只要不断在左侧填9即可获胜.
        当空格数为奇数时, A填最后一个, 显然可以获胜.
        如上所述, A的策略是往较大的部分填9, B只能在另一侧补充9; 因此, 两侧都有空格的情况可以最终会变为只有一侧有空格并且差值d不变. 
        在假设下有右侧空格更多, 有 `ava = spaceR - spaceL` 个; 两侧的差值 `d = sumL - sumR >= 0`. 
        考虑B如何应对A的阻挠获胜? 显然是两个数字之和应该为9. 因此, B的获胜条件为 `d == ava//2 * 9`.
另见 [官答](https://leetcode.cn/problems/sum-game/solution/qiu-he-you-xi-by-leetcode-solution-06ti/)
"""
    def sumGame(self, num: str) -> bool:
        n = len(num) // 2
        sumL = sumR = 0
        spaceL = spaceR = 0
        for i in range(n):
            if num[i] == '?': spaceL +=1
            else: sumL += int(num[i])
            if num[2*n-1-i] == '?': spaceR +=1
            else: sumR += int(num[2*n-1-i])
        # s = min(spaceL, spaceR)
        # spaceL, spaceR = spaceL-s, spaceR-s
        if spaceL > spaceR:
            # set spaceR >= spaceL
            spaceL, spaceR = spaceR, spaceL
            sumL, sumR = sumR, sumL
        ava = spaceR - spaceL
        if ava % 2 == 1: return True
        d = sumL - sumR
        if d == ava//2 * 9: return False
        return True
    
    """ 1928. 规定时间内到达终点的最小花费 #hard
给定一张地图, 要从0走到 n-1 号节点. 经过每一个节点需要交fee[i] 的费用. 每条边有距离. 需要在所有长度不超过 maxTime 的路径中, 计算最小的fee.
思路0: 尝试通过UCS来搜索. 但问题是, 需要维护一个visited记录确定的最短路径; 但实际的最小花费路径的长度可能是更大的.
    根本原因在于, 我们 **维护的避免重复访问的值不符合题意**.
- 思路1: 根据fee大小建立 #最小堆.
    - 反思了上面的问题, 这里考虑按照fee来构建最小堆.
        - 注意, 此时不能基于路径超出限制就break循环. 因为一条较长路径的fee可能更小.
    - 那么, 如何避免重复访问? 注意到, 我们第一次到达节点i的时候, fee是最小的. 但是这条路径的距离可能很长无法到达终点.
        - 我们用一个哈希表minDist 来维护遍历过程中每个点的最短路径. 当下一次遍历到时比记录的 minDist[i] 小, 说明这条路径更短, 仍要入队列. 否则, 我们知道新的这条路径比已记录的某条路径fee更高, 距离也更大, 直接舍弃.
    - 终止条件: 注意我们第一次到达终点即可退出循环, 因为第一次到达的fee最小. 若遍历到队列为空时仍为到达终点, 说明没有在距离限制内的路径可以到达终点.
思路2: #dp
    更为暴力的解法: 用 f[t][i] 表示恰好在时刻t到达地点i, 所需要的最小fee.
    则有转移方程 `f[t][i] = min_j{ f[t-weight[j,i]] + fee[i] }` 这里j是所有与i相连的节点 (j,i).
    具体来说, 可以采用两层遍历: 外层循环t 从1到maxWeight, 内层遍历所有的边.
    复杂度: O((n+m) * maxWeight). 其中第一项是初始化dp矩阵的代价, 第二项是遍历过程. 显然要比思路1慢.
    [官答](https://leetcode.cn/problems/minimum-cost-to-reach-destination-in-time/solution/gui-ding-shi-jian-nei-dao-da-zhong-dian-n3ews/)

"""
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        """ 尝试BFS, 但是错的!
        BFS需要采用 visited. 这里的策略是, 基于time最小出栈的时候将点加入visited中, 避免了搜索遇到与加入造成不是最短路径这一问题;
        但是这里要求的是最小fee, 这种策略无法避免该问题
        """
        g = collections.defaultdict(list)
        for u,v,t in edges:
            g[u].append((v,t))
            g[v].append((u,t))
        n = len(g)
        ans = inf
        # (time, fee, node)
        q = [(0, passingFees[0], 0)]    # P.Q
        visited = set([0])
        while q:
            t,f,u = heappop(q)
            # 在出栈的时候才加入 visited, 确保 time 是最小的. —— 但还是错了, 因为没有考虑fee
            visited.add(u)
            if t > maxTime: break
            if u==n-1: ans = min(ans, f)
            for v, dt in g[u]:
                if v in visited: continue
                heappush(q, (t+dt, f+passingFees[v], v))
        return ans if ans<inf else -1
    
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        """ 思路1: 根据fee大小建立最小堆. 关键在于如何避免重复访问? 建立 minDist 哈希表记录访问过的点的最小距离, 若新的访问比原来的访问更近, 则更新.
        参见 https://leetcode.cn/problems/minimum-cost-to-reach-destination-in-time/solution/python-fei-yong-zui-xiao-dui-by-qubenhao-i68u/ """
        n = len(passingFees)
        g = collections.defaultdict(list)
        for u,v,fee in edges:
            g[u].append((v,fee))
            g[v].append((u,fee))
        minDist = defaultdict(lambda: inf)
        minDist[0] = 0
        # (fee, dist, nodeID) 按照fee大小排序.
        q = [(passingFees[0], 0, 0)]
        while q:
            fee,dist,u = heappop(q)
            # if dist>maxTime: break
            for v, d in g[u]:
                # 距离限制: 不考虑超过最大时间的路线
                if dist + d > maxTime: continue
                # 避免重复访问
                if dist + d >= minDist[v]: continue
                # 由于是根据fee大小出栈的, 因此一旦找到target即可返回结果
                if v==n-1:
                    # ans = min(ans, fee+passingFees[v])
                    return fee+passingFees[v]
                minDist[v] = dist + d
                heappush(q, (fee+passingFees[v], dist+d, v))
        return -1

    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        """ DP
        https://leetcode.cn/problems/minimum-cost-to-reach-destination-in-time/solution/gui-ding-shi-jian-nei-dao-da-zhong-dian-n3ews/"""
        n = len(passingFees)
        f = [[float("inf")] * n for _ in range(maxTime + 1)]
        f[0][0] = passingFees[0]
        for t in range(1, maxTime + 1):
            for i, j, cost in edges:
                if cost <= t:
                    f[t][i] = min(f[t][i], f[t - cost][j] + passingFees[i])
                    f[t][j] = min(f[t][j], f[t - cost][i] + passingFees[j])

        ans = min(f[t][n - 1] for t in range(1, maxTime + 1))
        return -1 if ans == float("inf") else ans


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
    # sol.countTriples(n = 10),
    # sol.nearestExit(maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]], entrance = [1,2]),
    # sol.nearestExit(maze = [[".","+"]], entrance = [0,0]),
    # sol.nearestExit(maze = [["+","+","+"],[".",".","."],["+","+","+"]], entrance = [1,0]),
    # sol.sumGame(num = "5023"),
    # sol.sumGame(num = "25??"),
    # sol.sumGame(num = "?3295???"),
    sol.minCost(maxTime = 30, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]),
    sol.minCost(maxTime = 29, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]),
    sol.minCost(maxTime = 25, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]),
]
for r in result:
    print(r)
