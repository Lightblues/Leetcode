from cmath import pi
from typing import List
import collections
import math
import bisect
import heapq

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 2144. 打折购买糖果的最小开销 """
    def minimumCost(self, cost: List[int]) -> int:
        cost.sort()
        res = 0
        for i in range(len(cost)):
            if i%3==2:
                continue
            res += cost[len(cost)-i-1]
        return res
    """ 2145. 统计隐藏数组数目 """
    def numberOfArrays(self, differences: List[int], lower: int, upper: int) -> int:
        for i in range(1, len(differences)):
            differences[i] += differences[i-1]
        # 注意, 还应该和第一个基准的比较
        # 若是原来的 max(differences) - min(differences), 在对于 differences=[-40] 时出错
        minn = min(min(differences), 0)
        maxx = max(max(differences), 0)
        # diff = max(differences) - min(differences)
        diff = maxx - minn
        return upper-lower-diff+1 if upper-lower-diff>=0 else 0
    
    """ 2146. 价格范围内最高排名的 K 样物品
网格搜索, 0表示不能走, 不同的格子有价格, 要求找到价格在 pricing = [low, high] 区间内的位置.
要求找到优先级最高的k个, 优先级为: 1. 距离; 2. 价格; 3. 行坐标; 4. 列坐标.

思路: BFS. 广度优先, 每一轮维护 paths 记录当前可到达的坐标, potentials 为满足pricing约束的坐标集合, 然后 `select(potentials, k)` 根据优先级筛选.
 """
    def highestRankedKItems(self, grid: List[List[int]], pricing: List[int], start: List[int], k: int) -> List[List[int]]:
        res = []
        m, n = len(grid), len(grid[0])
        directions = list(zip([0, 1, 0, -1], [1, 0, -1, 0]))
        visited = [[False]*n for _ in range(m)]
        def select(potentials, k):
            if not potentials:
                return []
            items = []
            for x,y in potentials:
                items.append((grid[x][y], x,y))
            items.sort()
            return [item[1:] for item in items][:k]
        def bfs(queue, k):
            potentials = []
            paths = []
            for x,y in queue:
                for dx,dy in directions:
                    nx,ny = x+dx, y+dy
                    if 0<=nx<m and 0<=ny<n and not visited[nx][ny] and grid[nx][ny]!=0:
                        paths.append((nx,ny))
                        visited[nx][ny] = True
                        if pricing[0] <= grid[nx][ny] <= pricing[1]:
                            potentials.append((nx,ny))
            selected = select(potentials, k)
            nonlocal res
            res += selected
            # 答案不足 k 个! 提前终止
            if not paths:
                return
            # 继续搜索
            if len(selected) < k:
                bfs(paths, k-len(selected))
        
        # 注意开始状态 !!
        startVal = grid[start[0]][start[1]]
        visited[start[0]][start[1]] = True
        if pricing[0]<=startVal<=pricing[1]:
            res.append(start)
            bfs([start], k-1)
        else:
            bfs([start], k)
        return res

    """ 2147. 分隔长廊的方案数 """
    def numberOfWays(self, corridor: str) -> int:
        mod = 10**9+7
        seatIndex = []
        for i,c in enumerate(corridor):
            if c=='S':
                seatIndex.append(i)
        if not seatIndex or len(seatIndex)%2 != 0:
            return 0
        res = 1
        idx = 1
        while idx < len(seatIndex)-1:
            res = res * (seatIndex[idx+1]-seatIndex[idx]) % mod
            idx += 2
        return res


sol = Solution()
rels = [
    # sol.minimumCost(cost = [6,5,7,9,2,2]),
    # sol.numberOfArrays(differences = [1,-3,4], lower = 1, upper = 6),
    # sol.numberOfArrays([-40], -46, 53),
    # sol.highestRankedKItems(grid = [[1,2,0,1],[1,3,0,1],[0,2,5,1]], pricing = [2,5], start = [0,0], k = 3),
    # sol.highestRankedKItems([[1,1,1],[0,0,1],[2,3,4]], [2,3], [0,0], 3),
    # sol.highestRankedKItems([[0,2,0]], [2,2], [0,1], 1),
    sol.numberOfWays(corridor = "SSPPSPS"),
    sol.numberOfWays(corridor = "PPSPSP"),
]
for r in rels:
    print(r)