from typing import List, Optional
import collections
import math
import bisect
import heapq
import functools, itertools
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
from utils_leetcode import (
    testClass,
)
from structures import ListNode, TreeNode
import numpy as np

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 6051. 统计是给定字符串前缀的字符串数目 """
    def countPrefixes(self, words: List[str], s: str) -> int:
        ans = 0
        for w in words:
            if w == s[:len(w)]:
                ans += 1
        return ans
    
    """ 6052. 最小平均差 """
    def minimumAverageDifference(self, nums: List[int]) -> int:
        s = sum(nums)
        minAvgDiff, ans = s, 0
        l, r = 0, s
        for i in range(len(nums)-1):
            l += nums[i]
            r -= nums[i]
            diff = abs(
                l // (i + 1) - r // (len(nums) - i - 1)
            )
            if diff < minAvgDiff:
                minAvgDiff = diff
                ans = i
        if abs(s//len(nums)) < minAvgDiff:
            ans = len(nums) - 1
        return ans
    
    """ 6053. 统计网格图中没有被保卫的格子数 """
    def countUnguarded(self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]) -> int:
        grid = [[0] * n for _ in range(m)]
        for x,y in guards:
            grid[x][y] = 1
        for x,y in walls:
            grid[x][y] = 2
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        checkValid = lambda x, y: x >= 0 and x < m and y >= 0 and y < n
        for x,y in guards:
            for dx,dy in directions:
                nx,ny = x+dx, y+dy
                while True:
                    if not checkValid(nx,ny): break
                    # 注意 guard 的视线可以交错, 因此遇到 3 需要继续往下找
                    if grid[nx][ny] in (1,2): break
                    grid[nx][ny] = 3
                    nx,ny = nx+dx, ny+dy
        return sum([sum([i==0 for i in r]) for r in grid])
        
    """ 6054. 逃离火灾 https://leetcode-cn.com/problems/escape-the-spreading-fire
给定一个 grid, 有一组火源和一组墙, 每过一个时刻, 火网四周蔓延一圈, 但是不能穿过墙. 人要从左上角逃到右下角, 问人能够在起点等待的最长时间.

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

思路: BFS.
1) 先从所有的火点开始进行BFS, 记录所有点距离火的位置; 2) 然后从起点出发BFS, 对于路径上的每一个点, 火到达的时间为 `fireDist[(nx,ny)]`, 而距离为 `nd`, 因此:
1. 若 fireDist[(nx,ny)]<=nd 说明火先到达, 该点探索失败; 2. 否则, 所能等待的时间为 `nLimit = fireDist[(nx,ny)] - nd - 1`; 3) 这样, 进行 BFS遍历后, 若能到达终点, 该条路径的最大等待时间为 `max([nLimit])`.
繁琐的是要处理边界情况: 当人和火同时到达终点时, 算成功逃生.
"""
    def maximumMinutes0(self, grid: List[List[int]]) -> int:
        """ 用了 DFS 重复访问, 超时 """
        grid = np.array(grid)
        m, n = grid.shape
        fires = np.where(grid == 1)
        # walls = np.where(grid == 2)
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        def bfs(points, grid):
            """ 从 queue 所定义的一组点出发, 计算其他点的距离 """
            # directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
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
                    if nx < 0 or nx >= m or ny < 0 or ny >= n: continue
                    if grid[nx,ny] == 0:
                        q.append(((nx,ny), d+1))
                        dist[(nx,ny)] = d+1
            return dist
        fireDist = bfs(zip(*fires), grid)
        # destDist = bfs([(m-1, n-1)], gird)

        # 从人的起点出发 DFS
        ans = -1 # 若找不到路径就返回 -1
        def testValid(x, y):
            return x >= 0 and x < m and y >= 0 and y < n
        
        def dfs(x, y, d, pathLimit=int(1e9)):
            """ 
                d: (x, y) 从原点出发的距离
                pathLimit: 这条路径上的最大等待时间
            返回: 最大等待时间 (因此, 对于各条路径的结果取 max)
            """
            if (x,y) == (m-1, n-1):
                nonlocal ans
                ans = max(ans, pathLimit)
                # return pathLimit
            grid[x,y] = 3   # 标记已经访问过
            nd = d+1
            # ans = pathLimit
            for dx,dy in directions:
                nx,ny = x+dx, y+dy
                if not testValid(nx, ny) or grid[nx,ny] != 0: continue
                nLimit = int(1e9)
                if (nx,ny) in fireDist:
                    nLimit = fireDist[(nx,ny)] - nd - 1
                if (nx,ny) == (m-1, n-1):
                    ans = max(ans, min(pathLimit, nLimit+1))
                if nLimit < 0: continue
                dfs(nx, ny, nd, min(pathLimit, nLimit))
                # ans = max(ans, a)
            grid[x,y] = 0
            # return ans
        dfs(0, 0, 0)
        return ans

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
        

sol = Solution()
result = [
    # sol.countPrefixes(words = ["a","b","c","ab","bc","abc"], s = "abc"),
    
    # sol.minimumAverageDifference(nums = [2,5,3,9,5,3]),
    # sol.minimumAverageDifference([0]),
    
    sol.countUnguarded(m = 4, n = 6, guards = [[0,0],[1,1],[2,3]], walls = [[0,1],[2,2],[1,4]]),
    
    # sol.maximumMinutes([[0,0,0,0,0],[0,2,0,2,0],[0,2,0,2,0],[0,2,1,2,0],[0,2,2,2,0],[0,0,0,0,0]]),
    # sol.maximumMinutes([[0,2,0,0,1],[0,2,0,2,2],[0,2,0,0,0],[0,0,2,2,0],[0,0,0,0,0]]),
    # sol.maximumMinutes(grid = [[0,2,0,0,0,0,0],[0,0,0,2,2,1,0],[0,2,0,0,1,2,0],[0,0,2,2,2,0,2],[0,0,0,0,0,0,0]]),
    # sol.maximumMinutes(grid = [[0,0,0,0],[0,1,2,0],[0,2,0,0]]),
    # sol.maximumMinutes(grid = [[0,0,0],[2,2,0],[1,2,0]]),
]
for r in result:
    print(r)
