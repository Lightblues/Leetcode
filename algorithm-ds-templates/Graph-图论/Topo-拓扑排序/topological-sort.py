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
from itertools import product, permutations, combinations, combinations_with_replacement
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import sys, os
# sys.setrecursionlimit(10000)

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode

""" 拓扑排序

2050. 并行课程 III
1857. 有向图中最大颜色值
    给定一张图 (可认定为是 DAG), 每个节点有一个颜色. 对于每一条路径, 定义其值为相同颜色数量的最大值. 要求计算图上路径分数的最大值.
    如何记录分数? 对于每一个节点记录「以该节点结束的路径中, 各个颜色的最大值」, 根据上一个节点进行状态转移.

6163. 给定条件下构造矩阵 #hard #题型
    给定一个k, 要求构造 k*k 的矩阵, 填充 1~k 共k个数字, 其他位置填0. 要求满足行/列约束. 约束的形式是, 给定一组 (i,j), 要求数字i所在行应该在j所在行的上面. 限制: k 400, 约束数量 n 1e4

5970. 参加会议的最多员工数 #hard #题型 #基环树 #hardhard
    每个人只有一个喜欢的人, 要求安排坐圆桌, 每个人左右要有他喜欢的人, 最大的可安排人数
"""
class Solution:
    """ 2050. 并行课程 III #hard #题型
课程之间存在DAG依赖关系, 每个课程修习需要一定的月份, 前序依赖满足的情况下, 不同课程可以同时修习. 求完成所有可能的最小时间.
复杂度: 节点/边数量 5e4, 
思路1: #拓扑排序 在遍历的过程中记录每个节点的timeLimit, 这样, 遍历每一条边的时候, 可以更新 `timeLimit[v]` 为 max(timeLimit[v], timeLimie[u]+time[v])`
"""
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        degrees = [0] * n   # in degree
        timeLimit  = time[:]
        g = [[] for _ in range(n)]
        for u, v in relations:
            g[u-1].append(v-1)
            degrees[v-1] += 1
        
        # ans = math.inf
        q = collections.deque([i for i,d in enumerate(degrees) if d==0])
        while q:
            u = q.popleft()
            t = timeLimit[u]
            for v in g[u]:
                degrees[v] -= 1
                timeLimit[v] = max(timeLimit[v], t+time[v])
                if degrees[v] == 0:
                    q.append(v)
        return max(timeLimit)
    
    """ 1857. 有向图中最大颜色值 #hard #题型 #DAG #拓扑排序 #DP
给定一张图 (可认定为是 DAG), 每个节点有一个颜色. 对于每一条路径, 定义其值为相同颜色数量的最大值. 要求计算图上路径的最大值.
若图上出现环, 则返回 -1.
思路1: #拓扑排序
    状态转移: 如何记录路径上的(最大)节点数量? 对于每个节点, 用一个数组记录以该节点终止的所有路径上, 各个颜色的最大值.
    更新公式: 对于 (u,v) 边, 其每一个颜色的更新值为 `colorNode[u][color] + (color==colors[v])` 也即上一个邻居点的值, 加上是否为v的颜色.
    如何判断是否有环? 拓扑排序是否遍历了所有节点

输入：colors = "abaca", edges = [[0,1],[0,2],[2,3],[3,4]]
输出：3
解释：路径 0 -> 2 -> 3 -> 4 含有 3 个颜色为 "a" 的节点（上图中的红色节点）。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/largest-color-value-in-a-directed-graph
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        # 边界: 边数为 0 (防止 itertools.chain 报错)
        if len(edges)==0: return 1
        
        # 将字母形式的颜色转为数字
        colors = [ord(c) - ord('a') for c in colors]
        # 节点数量
        n = max(itertools.chain(*edges)) + 1
        degrees = [0] * n # 入度
        colorNode = [[0] * 26 for _ in range(n)]
        g = [[] for _ in range(n)]
        for u,v in edges:
            degrees[v] += 1
            g[u].append(v)
            
        ans = 0
        q = collections.deque([i for i,d in enumerate(degrees) if d==0])
        # visited 记录访问过的节点数量, 若其 != 总的节点数, 说明图上有环!
        visited = len(q)
        for i in q:
            colorNode[i][colors[i]] += 1
        while q:
            u = q.popleft()
            for v in g[u]:
                degrees[v] -= 1
                # colors[v] = max(colors[u], colors[v])
                # colorNode[v] = [max(colorNode[u][i], colorNode[v][i]) for i in range(26)]
                # colorNode[v][colors[v]] += 1
                # colorNode[v] = [a+b+1 if else a+b for a,b in zip(colorNode[u], colorNode[v])]
                for i in range(26):
                    if i==colors[v]:
                        colorNode[v][i] = max(colorNode[u][i]+1, colorNode[v][i])
                        ans = max(ans,colorNode[v][i])
                    else:
                        colorNode[v][i] = max(colorNode[u][i], colorNode[v][i])
                # ans = max(ans, colorNode[v][colors[v]])
                if degrees[v] == 0:
                    q.append(v)
                    visited += 1
        if visited!=n: return -1
        return ans
        
sol = Solution()
result = [
    sol.largestPathValue(colors = "abaca", edges = [[0,1],[0,2],[2,3],[3,4]]),
    sol.largestPathValue(colors = "a", edges = [[0,0]]),
]
for r in result:
    print(r)
