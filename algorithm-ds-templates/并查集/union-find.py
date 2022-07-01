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
from functools import lru_cache, reduce, partial # cache
cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
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

== 处理连接关系; 计算联通分量数量;
0547. 省份数量 #medium
    给定一个矩阵形式的图结构, 表示节点之间的相连关系, 计算其中的联通分量的个数.
    思路1: 并查集. 每次遇到一条边, 将两个集合 union.
0684. 冗余连接 #medium
    有一个节点数为 n 的仅有一个环的联通图, 给定边序列 (长度也为n), 要求去掉「成环边」(环上的最后一条边) 使得图上没有环 (也即是树).
    提示: 在顺序基于边列表连接的过程中, 将一个个不相连的分量进行了连接. 注意到, 「成环」的那条边, 其两个节点已经在一个联通分量中了! 因此, 仅需要记录每个节点所属分量即可; 可采用并查集.
1319. 连通网络的操作次数 #medium
    修改网络上的边, 使其成为联通图, 问最少需要求改多少条边.
    思路1: 等价于求联通分量大小, 直接 #并查集 即可.
0959. 由斜杠划分区域 #medium #题型
    有一个正方形grid, 每一个单元可能是 ` /\` 三种情况表示三种分割方式. 求这些斜杠所定义的划分方式所分割出来的区域数量.
    思路1: 采用 #并查集 来记录节点之间的联通关系
    注意, 在本题中, 一个 (x,y) 应该被看成两个节点 (如果内部没有斜杠也即为 ` ` 则将两个节点连起来即可)

== 其他: 问题转化; 其他更为匹配的解法等
1631. 最小体力消耗路径 #medium #题型
    给定一个grid每个点有一定高度, 要从grid的左上走到右下(方向可以上下左右), 路径的代价定义为, 相邻两点高度差的最小值. 要求给出最小值.
    思路1: #UCS 应该就是 #Dijkstra. 对于frontier维护一个 #优先队列, 每次拓展代价最小的节点.
    思路3: #并查集 #star 根据边权从小到大排序, 逐渐连边, 每次都检查是否能走到终点(联通), 显然可以用并查集来实现.
0778. 水位上升的泳池中游泳 #hard 和1631题基本相同
    要从正方形的左上移动/游到右下, 每个位置都有一个平台的高度, 时刻t的水位为t, 只有当水位高于两个点的平台高度的时候才能通过. 假设移动速度无限, 问能到达的最小时间.
    问题等价于, 在哪个时刻两个目标节点联通了.
    思路1: 对于平台的高度从小到大排序, 模拟时刻t的增长. 当 start/target 联通的时刻返回即可.
0803. 打砖块 #hard #interest #繁琐
    给定一个grid, 砖块上下左右相连, 每次打掉一个砖块, 若出现了不与顶部相连的砖块, 则会掉落/消失. 现给定一系列打掉砖块的序列, 问每次打击后会掉落多少块.
    思路1: #逆向 思考 + #并查集
        逆向考虑敲砖块的过程, 假如添加当前砖块, 会造成原本不与顶部相连的成分连接到roof, 则正向的敲击会造成砖块掉落.
        这里的一个核心点在于, 逆向考虑的过程中, 我们计算并查集连接关系的时候用到哪些节点?
1579. 保证图可完全遍历 #hard #题型
    有一个无向图有三种类型的边, 类型1仅能由A通过, 类型2仅能由B通过, 类型3均可. 已有了一组边的情况下, 问要保障A,B均能从图上某点到达任意一点的情况下, 最多可以删除多少条边
    提示: 问题等价于, 对于A和B而言, 此图都是联通的. #贪心 可知, 一定尽量保留类型3的边. 
    思路1: #贪心 保留所有的类型3; 然后AB都要使得剩余的分量之间均联通.
1998. 数组的最大公因数排序 #hard
    给定一个数组, 对于任意两个位置 i,j, 若他们存在公共因子 (`gcd(nums[i], nums[j]) > 1`) 则可进行交换. 问数组是否可以按照上述规则进行交换后, 变为递增数组.
    提示: 在一个并查集中的数字顺序可以任意调换.

0399. 除法求值 #medium #并查集 #题型 但实际上很 #hard #interest #TODO
    给定一组变量等式, 例如 `["bc","cd"]; 5.0` 对就表示等式 `bc/cd = 5.0`. 另外给定一系列的查询数组, 例如 `["a","c"]` 就是要查询表达式 `a/c` 的值. 返回所有查询的结果.


*   「力扣」第 1202 题：[交换字符串中的元素](https://leetcode-cn.com/problems/smallest-string-with-swaps)（中等）；
*   「力扣」第 947 题：[移除最多的同行或同列石头](https://leetcode-cn.com/problems/most-stones-removed-with-same-row-or-column)（中等）；
*   「力扣」第 721 题：[账户合并](https://leetcode-cn.com/problems/accounts-merge)（中等）；
"""

class UnionSet:
    """ 并查集模板 """
    def __init__(self, n) -> None:
        self.fa = list(range(n))
        self.sz = [1] * n
    def find0(self, x):
        # 这写得好烂!!!
        while x != self.fa[x]:
            self.fa[x] = self.find(self.fa[x])
            self.sz[self.fa[x]] += self.sz[x]
            x = self.fa[x]
        return x
    def find(self, x):
        if x != self.fa[x]:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]
    def merge(self, x, y):
        fx, fy = self.find(x), self.find(y)
        if fx == fy: return
        if self.sz[fx] < self.sz[fy]:
            fx, fy = fy, fx
        self.fa[fy] = fx
        self.sz[fx] += self.sz[fy]
    def get_component_count(self):
        return sum(1 for i,f in enumerate(self.fa) if i == f)
    def get_component_size(self, x):
        return self.sz[self.find(x)]
    def test_connected(self, x, y):
        return self.find(x) == self.find(y)



class Solution:
    """ 0547. 省份数量 #medium
给定一个矩阵形式的图结构, 表示节点之间的相连关系, 计算其中的联通分量的个数.
思路1: 并查集. 每次遇到一条边, 将两个集合 union.
"""
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        # 初始化所有节点的 farther 为自己
        parents = list(range(n))
        
        def find(x):
            path = []
            while parents[x] != x:
                path.append(x)
                x = parents[x]
            for i in path:
                parents[i] = x
            return x
        
        def union(x,y):
            rootx, rooty = find(x), find(y)
            parents[rootx] = rooty
            
        for i in range(n):
            for j in range(i+1, n):
                if isConnected[i][j]:
                    union(i,j)
        # 所有 root 元素的数量
        return sum(1 for i in range(n) if parents[i]==i)

    """ 0684. 冗余连接 #medium
有一个节点数为 n 的仅有一个环的联通图, 给定边序列 (长度也为n), 要求去掉「成环边」(环上的最后一条边) 使得图上没有环 (也即是树).
提示: 在顺序基于边列表连接的过程中, 将一个个不相连的分量进行了连接. 注意到, 「成环」的那条边, 其两个节点已经在一个联通分量中了! 因此, 仅需要记录每个节点所属分量即可; 可采用并查集.
思路: 利用 #并查集 记录节点连接情况
    遍历到每一条边, 检查两点是否以相连: 是则直接返回, 否则连接两个分量.
"""
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        fa = list(range(n))
        def find(x):
            """ 递归实现 """
            while fa[x] != x:
                fa[x] = find(fa[x])
                x = fa[x]
            return x
        def merge(x,y):
            fa[find(x)] = find(y)
        for u,v in edges:
            if find(u-1) == find(v-1):
                return [u,v]
            merge(u-1,v-1)
    
    """ 1319. 连通网络的操作次数 #medium
修改网络上的边, 使其成为联通图, 问最少需要求改多少条边.
思路1: 等价于求联通分量大小, 直接 #并查集 即可.
"""
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        if len(connections) < n-1: return -1
        us = UnionSet(n)
        for u,v in connections:
            us.merge(u,v)
        return us.get_component_count()-1

    """ 0959. 由斜杠划分区域 #medium #题型
有一个正方形grid, 每一个单元可能是 ` /\` 三种情况表示三种分割方式. 求这些斜杠所定义的划分方式所分割出来的区域数量.
思路1: 采用 #并查集 来记录节点之间的联通关系
    注意, 在本题中, 一个 (x,y) 应该被看成两个节点 (如果内部没有斜杠也即为 ` ` 则将两个节点连起来即可)
        例如, `/` 分割的左上/右下两个节点, 和 `\` 分割的左下/右上两个节点.
    处理起来比较麻烦的是节点之间的邻接关系, 下面的 `merge(x,y, dx,dy)` 对于 `(x,y)` 和 `(x+dx,y+dy)` 两个单元格进行连接.
        例如, 若 `(dx,dy)==(0,1)` 也即向右邻居连接, 并且两个节点分割方式为 `\`, `/` 则应该将 (x,y)中的第二个节点和 (x+dx,y+dy)中的第一个节点连接
注意: 转义字符 `\` 在字符串中的表示方式为 `\\`, 也即 `len('\\')==1`
"""
    def regionsBySlashes(self, grid: List[str]) -> int:
        n = len(grid)
        # 右、下、左、上
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        # d2idx = dict(zip(directions,range(4)))
        def merge(x,y, d):
            nx, ny = x+d[0], y+d[1]
            if not (0<=nx<n and 0<=ny<n): return
            node = 2*(x*n+y)
            if d==(0,1) and grid[x][y] in "/\\": node += 1
            if d==(1,0) and grid[x][y] in "/": node += 1
            if d==(-1,0) and grid[x][y] in "\\": node += 1
            node2 = 2*(nx*n+ny)
            if d==(0,-1) and grid[nx][ny] in "/\\": node2 += 1
            if d==(-1,0) and grid[nx][ny] in "/": node2 += 1
            if d==(1,0) and grid[nx][ny] in "\\": node2 += 1
            us.merge(node, node2)
        us = UnionSet(2*n*n)
        for i, row in enumerate(grid):
            for j, ch in enumerate(row):
                idx = 2 * (i*n+j)
                if ch == ' ':
                    us.merge(idx, idx+1)
                for d in directions:
                    merge(i,j, d)
        return us.get_component_count()

    """ 1631. 最小体力消耗路径 #medium #题型
给定一个grid每个点有一定高度, 要从grid的左上走到右下(方向可以上下左右), 路径的代价定义为, 相邻两点高度差的最小值. 要求给出最小值.
限制: m,n 100; 每个点的高度 1e6
思路1: #UCS 应该就是 #Dijkstra
    注意到, 由于这里路径代价的定义是每条边权的最大值, 因此, 回形的路径可能是最优的, 因此不能用DP等来做.
    考虑采用 #UCS, 对于frontier维护一个 #优先队列, 每次拓展代价最小的节点.
    复杂度: O(mn log(mn)) 其中对数项是优先队列的复杂度.
思路2: 比较naive的 #二分查找
    在限制路径代价的前提下尝试用BFS/DFS看能否走到终点. 二分检查答案
    复杂度: O(mn log(C))
思路3: #并查集 #star
    根据边权从小到大排序, 逐渐连边, 每次都检查是否能走到终点(联通), 显然可以用并查集来实现.
[官答](https://leetcode.cn/problems/path-with-minimum-effort/solution/zui-xiao-ti-li-xiao-hao-lu-jing-by-leetc-3q2j/)
"""
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """ 思路1: #UCS 应该就是 #Dijkstra """
        m,n = len(heights), len(heights[0])
        pq = [(0, 0,0)] # (effort, x, y)
        seen = set() #; seen.add((0,0))
        mx = 0
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        while True:
            d, x,y = heapq.heappop(pq)
            mx = max(mx, d)
            if (x,y) == (m-1, n-1): break
            seen.add((x,y))
            for dx,dy in directions:
                nx,ny = x+dx,y+dy
                if nx<0 or ny<0 or nx>=m or ny>=n or (nx,ny) in seen: continue
                d = abs(heights[nx][ny]-heights[x][y])
                heappush(pq, (d, nx,ny))
        return mx
    
    """ 0778. 水位上升的泳池中游泳 #hard
要从正方形的左上移动/游到右下, 每个位置都有一个平台的高度, 时刻t的水位为t, 只有当水位高于两个点的平台高度的时候才能通过. 假设移动速度无限, 问能到达的最小时间.
问题等价于, 在哪个时刻两个目标节点联通了.
思路1: 对于平台的高度从小到大排序, 模拟时刻t的增长. 当 start/target 联通的时刻返回即可.
"""
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if n==1: return 0
        start, target = 0, n*n-1
        xy2idx = lambda x,y: x*n+y
        us = UnionSet(n*n)
        nodes = []
        for i,j in itertools.product(range(n), range(n)):
            nodes.append((grid[i][j], i,j))
        nodes.sort()
        for t, x,y in nodes:
            # 注意需要满足 grid[x-1][y]<=t 时才可以连接
            if x>0 and grid[x-1][y]<=t: us.merge(xy2idx(x-1,y), xy2idx(x,y))
            if y>0 and grid[x][y-1]<=t: us.merge(xy2idx(x,y-1), xy2idx(x,y))
            if x<n-1 and grid[x+1][y]<=t: us.merge(xy2idx(x+1,y), xy2idx(x,y))
            if y<n-1 and grid[x][y+1]<=t: us.merge(xy2idx(x,y+1), xy2idx(x,y))
            if us.test_connected(start,target): return t
        
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """ 思路2: 比较naive的 #二分查找
        https://leetcode.cn/problems/path-with-minimum-effort/solution/zui-xiao-ti-li-xiao-hao-lu-jing-by-leetc-3q2j/ """
        m, n = len(heights), len(heights[0])
        left, right, ans = 0, 10**6 - 1, 0

        while left <= right:
            mid = (left + right) // 2
            q = collections.deque([(0, 0)])
            seen = {(0, 0)}
            
            while q:
                x, y = q.popleft()
                for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                    if 0 <= nx < m and 0 <= ny < n and (nx, ny) not in seen and abs(heights[x][y] - heights[nx][ny]) <= mid:
                        q.append((nx, ny))
                        seen.add((nx, ny))
            
            if (m - 1, n - 1) in seen:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
        
        return ans

    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """ 思路3: #并查集 #star """
        m, n = len(heights), len(heights[0])
        us = UnionSet(m*n)
        edges = []
        def xy2id(x,y): return x*n+y
        for i in range(m):
            for j in range(n):
                if i>0:
                    edges.append((xy2id(i-1,j), xy2id(i,j), abs(heights[i][j]-heights[i-1][j])))
                if j>0:
                    edges.append((xy2id(i,j-1), xy2id(i,j), abs(heights[i][j]-heights[i][j-1])))
        edges.sort(key=lambda x:x[2])   # 按照代价排序
        for u,v,w in edges:
            us.merge(u,v)
            if us.test_connected(0, m*n-1):
                return w
            
            
            
    """ 1998. 数组的最大公因数排序 #hard
给定一个数组, 对于任意两个位置 i,j, 若他们存在公共因子 (`gcd(nums[i], nums[j]) > 1`) 则可进行交换. 问数组是否可以按照上述规则进行交换后, 变为递增数组.
约束: 数组长度 3e4, 数字大小 1e5
思路1: 分解 #质因子 的 #并查集
    结论: 对于有公共因子的数字之间连边, 可知, 在一个连通分量上, 经过交换操作可以得到任意的数字顺序. 例子:  `[10,5,9,3,15]` 两个因子 3,5 通过 15 连接, 这个数组可以得到任意顺序
    因此, 就是并查集的思路. 但是元素之间两两查询的复杂度不够. 因此, 我们引入 prime 数字构成的节点.
    这样, 对于一个数字num, 我们得到所有的质因子 factors, 将 num 连到任意质因子上, 然后将 factors[1:n-1] 都连到 factors[0] 上即可.
    判断: 最后, 将 nums, sorted(nums) 的每一位比较, 两元素相同则不需要交换; 否则, 查询 x,y 是否在同一集合中, 只有在同一集合中才能交换得到.
    下面预先计算的所有可能的质因子, 但实际上可以简化, 见 [here](https://leetcode.cn/problems/gcd-sort-of-an-array/solution/bing-cha-ji-fen-jie-zhi-yin-shu-by-xin-x-ylsz/)
"""
    def gcdSort(self, nums: List[int]) -> bool:
        sortedNums = sorted(nums)
        # 预计算所有的质数因子
        primes = [2]
        for i in range(3, sortedNums[-1]+1):
            flag = True
            limit = int(math.sqrt(i))
            for j in primes:
                if j>limit: break
                if i%j==0:
                    flag = False
                    break
            if flag: primes.append(i)
        
        def getFactors(x):
            """ 得到 x 的所有因子 """
            factors = []
            for i in primes:
                if x%i==0:
                    factors.append(i)
                    x //= i
                    while x%i==0:
                        x //= i
                if x==1: break
            return factors
        
        # 并查集
        n = len(set(nums))
        num2dix = {num:i for i, num in enumerate(set(nums))}
        prime2idx = {prime:i+n for i, prime in enumerate(primes)}
        fa = list(range(n + len(primes)))
        def find(x):
            path = []
            while fa[x] != x:
                path.append(x)
                x = fa[x]
            for i in path:
                fa[i] = x
            return x
        def merge(x, y):
            """ 将 x, y 合并到一个集合中; 令 x 是 y 的父节点 """
            fa[find(y)] = find(x)
            
        for num in nums:
            if num==1: continue
            factors = getFactors(num)
            # 将 num 合并到最小的因子上去
            merge(prime2idx[factors[0]], num2dix[num])
            # 将各个因子之间进行合并
            for i in range(1, len(factors)):
                # 按照merge的规则, 尽量让小的数字作为父节点
                merge(prime2idx[factors[0]], prime2idx[factors[i]])
        
        # 检查. 判断 idx 位置的数字能否从x变为y (也即在一个并查集中)
        for x,y in zip(nums, sortedNums):
            if x==y: continue
            if find(num2dix[x]) != find(num2dix[y]): return False
        return True

    """ 0803. 打砖块 #hard #interest #繁琐
给定一个grid, 砖块上下左右相连, 每次打掉一个砖块, 若出现了不与顶部相连的砖块, 则会掉落/消失. 现给定一系列打掉砖块的序列, 问每次打击后会掉落多少块.
限制: m,n 200; 
提示:
    考虑节点之间相连情况, 可以用并查集
    但并查集无法进行删除操作, 因此考虑逆向; 另外, 本题可以添加一个虚拟的roof节点, 方便表示是否与顶部相连.
思路1: #逆向 思考 + #并查集
    逆向考虑敲砖块的过程, 假如添加当前砖块, 会造成原本不与顶部相连的成分连接到roof, 则正向的敲击会造成砖块掉落.
    这里的一个核心点在于, 逆向考虑的过程中, 我们计算并查集连接关系的时候用到哪些节点?
        注意到敲击的节点从逆向考虑是添加节点之间连接性的过程, 开始的时候都不能考虑; 逆向过程中, 逐步将还原上的节点加入到考虑范围中. (具体而言, 维护一个available节点集合)
总结: 思路比较清楚, 但代码写起来非常繁琐, 注意 #回顾.
"""
    def hitBricks(self, grid: List[List[int]], hits: List[List[int]]) -> List[int]:
        m,n = len(grid), len(grid[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # 构建所有的点
        xy2idx = {}
        for i in range(m):
            for j in range(n):
                if grid[i][j]==1:
                    xy2idx[(i,j)] = len(xy2idx) + 1 # start from 1
        # 并查集. 其中0号节点是特殊的 roof 节点
        us = UnionSet(len(xy2idx)+1)
        for j in range(n):  # 将顶部的点连到 roof 节点上
            if grid[0][j]==1:
                us.merge(xy2idx[(0,j)], 0)
        # 将敲击之外的点互相连接
        hitSet = set(tuple(h) for h in hits)
        ava = set(xy2idx.keys()).difference(hitSet) # 当前可以进行计算的点
        for x,y in ava:
            for dx,dy in directions:
                if (x+dx,y+dy) in ava:
                    us.merge(xy2idx[(x,y)], xy2idx[(x+dx,y+dy)])

        ans = []
        for x,y in hits[::-1]:
            # 边界1: 敲击错误
            if (x,y) not in xy2idx: ans.append(0); continue
            node = xy2idx[(x,y)]
            # 注意, 在计算连接的时候, 只能用到 ava 集合中的节点 (因为 hits[:i] 中的点已经被敲掉了)
            # neighbors = [xy2idx[(x+dx, y+dy)] for dx,dy in directions  if (x+dx, y+dy) in xy2idx]
            neighbors = [xy2idx[(x+dx, y+dy)] for dx,dy in directions  if (x+dx, y+dy) in ava]
            ava.add((x,y))
            # flag 标记是否与顶部相连; c统计可能掉落的砖块数
            flag = us.test_connected(0, node); c = 0
            for i,n1 in enumerate(neighbors):
                # 与之前处理过的部分在同一component中, 跳过
                if any(us.test_connected(n1, n2) for n2 in neighbors[:i]): continue
                # 
                if us.test_connected(0, n1): 
                    flag = True
                else:
                    c += us.get_component_size(n1)
                # 注意需要将当前 node 和邻居连接
                us.merge(node, n1)
            # 有相连成分连接到roof上, 则掉落
            ans.append(c if flag else 0)
        return ans[::-1]

    """ 0399. 除法求值 #medium #并查集 #题型 但实际上很 #hard #interest #TODO
给定一组变量等式, 例如 `["bc","cd"]; 5.0` 对就表示等式 `bc/cd = 5.0`. 另外给定一系列的查询数组, 例如 `["a","c"]` 就是要查询表达式 `a/c` 的值. 返回所有查询的结果.
限制: 等式数量 20, 等式中的常数大小 (0.0, 20.0]; 查询数量 20
[官答](https://leetcode.cn/problems/evaluate-division/solution/chu-fa-qiu-zhi-by-leetcode-solution-8nxb/)
思路1: 采用并查集. 注意到, 这里需要维护集合之间的相对大小关系. 那么, 的时候, 如何记录这一关系?
    注意到, 在查询的时候, 只有root相同(在同一集合内)的两个数才能比较, 因此 **只需要记录节点与根节点的大小关系**, 在查询时不需要考虑不同集合的倍率.
    因此, 问题转为, 如何在合并时记录两集合的大小关系? 只需要记录在跟节点上, 在 find 的时候更新子节点即可!
    具体而言, 对于比例关系 a = v*b, 构建的时候我们令 b为根节点, 然后 `value[b]=1, value[a]=v`. 这样, 我们在同一颗树上, 跟节点的值为1, 并且有 value[a] = a/roota (后两者为真实值)
    这样, 在union过程中, 若有 x = v * y 在两个集合中; 我们求出两者的根节点, 然后令 `father[rootx] = rooty`. (根节点rooty的值仍为1)
    如何更新 rootx 的值? (注意, 这里我们仅关心 rootx 的值, x的值会在find的时候进行更新) 此时, 我们有两个参考系, 目标是将 rootx 转到y的参考系.
    下面用 value 表示参考系y, value' 表示参考系x. 则我们需要求 value[rootx].
    在y参考系下, 有 value[x] = v * value[y]
    另有 value[x] = value'[x] * value[rootx], 这是因为在不同参考系下, x/rootx 的比例关系是固定的.
    因此有, `value[rootx] = v * value[y] / value'[x]`
"""
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        # https://leetcode.cn/problems/evaluate-division/solution/pythonbing-cha-ji-fu-mo-ban-by-milomusia-kfsu/
        class UnionFind:
            def __init__(self):
                """
                记录每个节点的父节点
                记录每个节点到根节点的权重
                """
                self.father = {}
                self.value = {}
            
            def find(self,x):
                """
                查找根节点
                路径压缩
                更新权重
                """
                root = x
                # 节点更新权重的时候要放大的倍数
                base = 1
                while self.father[root] != None:
                    root = self.father[root]
                    base *= self.value[root]
                
                while x != root:
                    original_father = self.father[x]
                    ##### 离根节点越远，放大的倍数越高
                    self.value[x] *= base
                    base /= self.value[original_father]
                    #####
                    self.father[x] = root
                    x = original_father
                
                return root
            
            def merge(self,x,y,val):
                """
                合并两个节点
                """
                root_x,root_y = self.find(x),self.find(y)
                
                if root_x != root_y:
                    self.father[root_x] = root_y
                    ##### 四边形法则更新根节点的权重
                    self.value[root_x] = val * self.value[y] / self.value[x]

            def is_connected(self,x,y):
                """
                两节点是否相连
                """
                return x in self.value and y in self.value and self.find(x) == self.find(y)
            
            def add(self,x):
                """
                添加新节点，初始化权重为1.0
                """
                if x not in self.father:
                    self.father[x] = None
                    self.value[x] = 1.0


        uf = UnionFind()
        for (a,b),val in zip(equations,values):
            uf.add(a)
            uf.add(b)
            uf.merge(a,b,val)
    
        res = [-1.0] * len(queries)

        for i,(a,b) in enumerate(queries):
            if uf.is_connected(a,b):
                res[i] = uf.value[a] / uf.value[b]
        return res
    
    """ 1579. 保证图可完全遍历 #hard #题型
有一个无向图有三种类型的边, 类型1仅能由A通过, 类型2仅能由B通过, 类型3均可. 已有了一组边的情况下, 问要保障A,B均能从图上某点到达任意一点的情况下, 最多可以删除多少条边
提示:
    问题等价于, 对于A和B而言, 此图都是联通的. 而无向图联通的条件为, 联通分量只有一个 (变成了树).
    #贪心 可知, 一定尽量保留类型3的边. 
思路1: #贪心 保留所有的类型3; 然后AB都要使得剩余的分量之间均联通.
    具体而言, 在一步判断类型3边时, 对于边 (u,v), 若节点本身就联通, 则不加入; 否则进行联通.
    在第二步中, 例如对于类型A的边, 若其在A所对应的并查集中, 两个节点本来已经联通, 则不加入.
    最后需要判断两个并查集是否只剩下了一个联通分量, 否则说明问题不可行, 返回-1.
"""
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        """ 参考了 [官答](https://leetcode.cn/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/solution/bao-zheng-tu-ke-wan-quan-bian-li-by-leet-mtrw/)
        代码很简洁"""
        usa = UnionSet(n); usb = UnionSet(n)
        ans = 0
        edges = [(t, u-1,v-1) for t,u,v in edges]
        # 1) 类型3
        for t, u,v in edges:
            if t==3:
                if usa.find(u)==usa.find(v): ans +=1
                else: usa.merge(u,v); usb.merge(u,v)
        # 2) 处理类型1和类型2
        for t, u,v in edges:
            if t==1:
                if usa.find(u)==usa.find(v): ans +=1
                else: usa.merge(u,v)
            elif t==2:
                if usb.find(u)==usb.find(v): ans +=1
                else: usb.merge(u,v)
        if usa.get_component_count()!=1 or usb.get_component_count()!=1: return -1
        return ans

sol = Solution()
result = [
    # sol.findRedundantConnection(edges = [[1,2], [1,3], [2,3]]),
    # sol.findRedundantConnection(edges = [[1,2], [2,3], [3,4], [1,4], [1,5]]),
    # sol.makeConnected(n = 4, connections = [[0,1],[0,2],[1,2]]),
    # sol.makeConnected(n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]),
    # sol.minimumEffortPath(heights = [[1,2,2],[3,8,2],[5,3,5]]),
    # sol.minimumEffortPath(heights = [[1,2,3],[3,8,4],[5,3,5]]),
    # sol.minimumEffortPath(heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]),
    # sol.hitBricks(grid = [[1,0,0,0],[1,1,1,0]], hits = [[1,0]]),
    # sol.hitBricks(grid = [[1,0,0,0],[1,1,0,0]], hits = [[1,1],[1,0]]),
    # sol.hitBricks([[1],[1],[1],[1],[1]], [[3,0],[4,0],[1,0],[2,0],[0,0]]),
    # sol.hitBricks([[1,0,1],[1,1,1]], [[0,0],[0,2],[1,1]]),
    # sol.regionsBySlashes(grid = ["/\\","\\/"]),
    # sol.regionsBySlashes([" /\\"," \\/","\\  "]),
    # sol.calcEquation([["a","b"],["e","f"],["b","e"]],[3.4,1.4,2.3],[["b","a"],["a","f"],["f","f"],["e","e"],["c","c"],["a","c"],["f","e"]]),
    # sol.calcEquation(equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]),
    # sol.calcEquation([["a","b"],["c","d"]],[1.0,1.0],[["a","c"],["b","d"],["b","a"],["d","c"]]),
    # sol.maxNumEdgesToRemove(n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]),
    # sol.maxNumEdgesToRemove(n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]),
    sol.swimInWater(grid = [[0,2],[1,3]]),
    sol.swimInWater(grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]),
    
]
for r in result:
    print(r)
