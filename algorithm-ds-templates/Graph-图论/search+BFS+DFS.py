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
[BDF vs DFS]
注意: DFS 若要不重复访问节点, 就要用visited记录访问的点; 但第一次访问不一定是最短, 因此无法得到最短路径; 若要得到最短路径, 就只能记录当前路径经过的点, 会带来重复访问的问题!
用BFS 同样可以记录路径: 只需要记录当前路径经过的点即可, 增加少量的存储开销


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

== Dijkstra
1514. 概率最大的路径 #medium #题型 #Dijkstra 算法
    等价于, 经典的「单源最短路径路径」, 在带权图上求 (s,e) 之间的最短距离.


== 最短路径数
1976. 到达目的地的方案数 #medium #题型 #最短路径
    求出从s到e的最短路径的数量.
    约束: 节点数量 n为200, 题目确保了是连通图; 需要对答案取 MOD
    思路: 1) 为了统计路径数量, 需要保证第一次访问节点(拓展节点, 累计最短路径数)的时候就是最短距离, 因此, 采用PQ结构; 2) 为了保证不重复统计边, 应该在第一次拓展节点后不进行拓展, 仅更新其最短路径数.

"""
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
    


    """ 1514. 概率最大的路径 #medium #题型 #Dijkstra 算法
等价于, 经典的「单源最短路径路径」, 在带权图上求 (s,e) 之间的最短距离.
思路1: #Dijkstra 算法
    回顾 Dijkstra算法的核心思想: 1) 将节点分成两类: 「未确定节点」和「已确定节点」; 2) (「松弛」过程) 每次从「未确定节点」中取一个与起点距离最短的点，将它归类为「已确定节点」，并用它「更新」从起点到其他所有「未确定节点」的距离。直到所有点都被归类为「已确定节点」。
    细节: 1) 如何找到「未确定节点」中最小距离点? 例如可以用最小堆实现. 2) 如何分离两类节点? 一种方式是用 `visited` 字典标记已确定节点; 另一种方式是, 用一个 `minDist` 记录当前的距离, 更新过程中只有当v的距离比minDist小时才更新, 入栈. 实验下来两种方式没有复杂度上的区别.
    [官答](https://leetcode.cn/problems/path-with-maximum-probability/solution/gai-lu-zui-da-de-lu-jing-by-leetcode-solution/)
"""
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        # 一种方式是用 `visited` 字典标记已确定节点
        g = [[] for _ in range(n)]
        for (u,v),p in zip(edges, succProb):
            g[u].append((v,p)); g[v].append((u,p))
        h = [(-1, start)]
        visited = set()     # 已确定的点
        while h:
            prob,u = heappop(h)
            if u==end: return -prob
            if u in visited: continue
            visited.add(u)  # 注意, visited 中的点的距离已确定为最小值.
            for v,p in g[u]:
                if v not in visited:
                    heappush(h, (prob*p, v))
        return 0
    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
