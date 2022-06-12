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
1928. 规定时间内到达终点的最小花费 #hard
    给定一张地图, 要从0走到 n-1 号节点. 经过每一个节点需要交fee[i] 的费用. 每条边有距离. 需要在所有长度不超过 maxTime 的路径中, 计算最小的fee.
    思路: 根据题意, 建立针对fee的最小堆.
        注意, 此时不能基于路径超出限制就break循环. 因为一条较长路径的fee可能更小.
    那么, 如何避免重复访问? 注意到, 我们第一次到达节点i的时候, fee是最小的. 但是这条路径的距离可能很长无法到达终点. 
        我们用一个哈希表minDist 来维护遍历过程中每个点的最短路径. 当下一次遍历到时比记录的 minDist[i] 小, 说明这条路径更短, 仍要入队列. 否则, 我们知道新的这条路径比已记录的某条路径fee更高, 距离也更大, 直接舍弃.
    终止条件: 注意我们第一次到达终点即可退出循环, 因为第一次到达的fee最小. 若遍历到队列为空时仍为到达终点, 说明没有在距离限制内的路径可以到达终点.
6054. 逃离火灾 #hard
    给定一个 grid, 有一组火源和一组墙, 每过一个时刻, 火往四周蔓延一圈, 但是不能穿过墙. 人要从左上角逃到右下角, 问人能够在起点等待的最长时间.
    思路1: 可以从火源出发, 预计算每个点着火的时间. 然后 **遍历从起点BFS到终点的每一条路径**, 计算这条路径上的最大等待时间.
    思路2: 相较于「遍历每条路径」, 可以利用二分查找简化逻辑.

@2022 """
class Solution:
    """ 1928. 规定时间内到达终点的最小花费 #hard
给定一张地图, 要从0走到 n-1 号节点. 经过每一个节点需要交fee[i] 的费用. 每条边有距离. 需要在所有长度不超过 maxTime 的路径中, 计算最小的fee.
思路0: 尝试通过UCS来搜索. 但问题是, 需要维护一个visited记录确定的最短路径; 但实际的最小花费路径的长度可能是更大的.
    根本原因在于, 我们 **维护的避免重复访问的值不符合题意**.
思路1: 根据fee大小建立 #最小堆.
    反思了上面的问题, 这里考虑按照fee来构建最小堆.
    关键在于如何避免重复访问? 建立 minDist 哈希表记录访问过的点的最小距离, 若新的访问比原来的访问更近, 则更新.
思路2: #dp
    更为暴力的解法: 用 f[t][i] 表示恰好在时刻t到达地点i, 所需要的最小fee.
    则有转移方程 `f[t][i] = min_j{ f[t-weight[j,i]] + fee[i] }` 这里j是所有与i相连的节点 (j,i).
    具体来说, 可以采用两层遍历: 外层循环t 从1到maxWeight, 内层遍历所有的边.
    复杂度: O((n+m) * maxWeight). 其中第一项是初始化dp矩阵的代价, 第二项是遍历过程. 显然要比思路1慢.
    [官答](https://leetcode.cn/problems/minimum-cost-to-reach-destination-in-time/solution/gui-ding-shi-jian-nei-dao-da-zhong-dian-n3ews/)

"""
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
    
    

    """ 6054. 逃离火灾 https://leetcode-cn.com/problems/escape-the-spreading-fire
给定一个 grid, 有一组火源和一组墙, 每过一个时刻, 火往四周蔓延一圈, 但是不能穿过墙. 人要从左上角逃到右下角, 问人能够在起点等待的最长时间.

输入：grid = [[0,2,0,0,0,0,0],[0,0,0,2,2,1,0],[0,2,0,0,1,2,0],[0,0,2,2,2,0,2],[0,0,0,0,0,0,0]]
输出：3
解释：上图展示了你在初始位置停留 3 分钟后的情形。
你仍然可以安全到达安全屋。
停留超过 3 分钟会让你无法安全到达安全屋。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/escape-the-spreading-fire
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

注意: DFS 若要不重复访问节点, 就要用visited记录访问的点; 但第一次访问不一定是最短, 因此无法得到最短路径; 若要得到最短路径, 就只能记录当前路径经过的点, 会带来重复访问的问题!
用BFS 同样可以记录路径: 只需要记录当前路径经过的点即可, 增加少量的存储开销

思路1: #BFS.
    先从所有的火点开始进行BFS, 记录所有点距离火的位置;
    然后从起点出发BFS, 对于路径上的每一个点, 火到达的时间为 `fireDist[(nx,ny)]`, 而距离为 `nd`, 因此:
        若 fireDist[(nx,ny)]<=nd 说明火先到达, 该点探索失败; 
        否则, 所能等待的时间为 `nLimit = fireDist[(nx,ny)] - nd - 1`; 
    这样, 进行 BFS遍历后, 若能到达终点, 该条路径的最大等待时间为 `max([nLimit])`.
    繁琐的是要处理边界情况: 当人和火同时到达终点时, 算成功逃生.
    另外, 在本题中, 可能出现多条路径都能到达终点的情况, 因此遍历到终点后, 不能直接返回!
思路2: #二分
    [灵神](https://leetcode.cn/problems/escape-the-spreading-fire/solution/er-fen-bfspythonjavacgo-by-endlesscheng-ypp1/)
    我们可以快速检查等待时长t是否可行. 
    因此, 相较于上面的分析, 直接二分更为方便.
"""
    def maximumMinutes(self, grid: List[List[int]]) -> int:
        """  """
        import numpy as np
        grid = np.array(grid)
        m, n = grid.shape
        fires = np.where(grid == 1)
        
        def testValid(x, y): return x >= 0 and x < m and y >= 0 and y < n
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        def bfs(points, grid):
            """ 从 queue 所定义的一组点出发, 计算其他点的距离 """
            dist = {}
            q = collections.deque()
            for x,y in points:
                dist[(x,y)] = 0
                q.append(((x,y), 0))
            while q:
                (x,y), d = q.popleft()
                for dx, dy in directions:
                    nx,ny = x+dx, y+dy
                    if (nx,ny) in dist: continue
                    if not testValid(nx,ny): continue
                    if grid[nx,ny] == 0:
                        q.append(((nx,ny), d+1))
                        dist[(nx,ny)] = d+1
            return dist
        fireDist = bfs(zip(*fires), grid)

        LIMIT = int(1e9)    # 若始终能到达, 则返回 LIMIT
        # 从人的起点出发 BFS
        ans = -1            # 若找不到路径就返回 -1
        queue = collections.deque()
        src, dst = (0, 0), (m-1, n-1)
        queue.append((src, 0, LIMIT))
        visited = set([src])
        while queue:
            (x,y), d, limit = queue.popleft()
            if (x,y) == dst:
                # 可能出现多条路径都能到达终点的情况, 因此遍历到终点后, 不能直接返回!
                ans = max(ans, limit)
                continue
            for dx, dy in directions:
                nx,ny = x+dx, y+dy
                nd = d+1
                # 检测边界情况
                if not testValid(nx,ny) or grid[nx,ny]!=0: continue
                # visited 禁止重复访问
                if (nx,ny) in visited: continue
                # 特殊情况: 当人和火同时到达终点时, 算成功
                # if (nx,ny) == dst:
                #     ans = max(limit, ans)
                    # nLimit = limit
                    # if (nx,ny) in fireDist:
                    #     nLimit = fireDist[(nx,ny)] - nd
                    # return min(limit, nLimit)
                nLimit = limit
                if (nx,ny) in fireDist:
                    nLimit = fireDist[(nx,ny)] - nd - 1
                    if (nx,ny) == dst:
                        # 特殊情况: 当人和火同时到达终点时, 算成功
                        # 这里重新加到了 queue中, 也可以直接判断返回
                        nLimit += 1
                    if nLimit < 0: continue
                queue.append(((nx,ny), nd, min(limit, nLimit)))
                if (nx,ny) == dst: continue
                visited.add((nx,ny))
        return ans
        

    def maximumMinutes(self, grid: List[List[int]]) -> int:
        """ 思路2: #二分
        [灵神](https://leetcode.cn/problems/escape-the-spreading-fire/solution/er-fen-bfspythonjavacgo-by-endlesscheng-ypp1/)"""
        m, n = len(grid), len(grid[0])

        def check(t: int) -> bool:
            f = [(i, j) for i, row in enumerate(grid) for j, v in enumerate(row) if v == 1]
            fire = set(f)
            def spread_fire():
                nonlocal f
                tmp = f
                f = []
                for i, j in tmp:
                    for x, y in ((i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)):
                        if 0 <= x < m and 0 <= y < n and grid[x][y] != 2 and (x, y) not in fire:
                            fire.add((x, y))
                            f.append((x, y))
            while t and f:
                spread_fire()  # 蔓延至多 t 分钟的火势
                t -= 1
            if (0, 0) in fire:  # 起点着火，寄
                return True

            q = [(0, 0)]
            vis = set(q)
            while q:
                tmp = q
                q = []
                for i, j in tmp:
                    if (i, j) not in fire:
                        for x, y in ((i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)):
                            if 0 <= x < m and 0 <= y < n and grid[x][y] != 2 and (x, y) not in fire and (x, y) not in vis:
                                if x == m - 1 and y == n - 1:  # 我们安全了…暂时。
                                    return False
                                vis.add((x, y))
                                q.append((x, y))
                spread_fire()  # 蔓延 1 分钟的火势
            return True  # 寄

        ans = bisect.bisect_left(range(m * n + 1), True, key=check) - 1
        return ans if ans < m * n else 10 ** 9

    
    
    
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
    
]
for r in result:
    print(r)
