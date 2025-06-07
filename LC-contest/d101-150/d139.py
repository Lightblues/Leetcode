from typing import *
from heapq import heappop, heappush
# from easonsi.util.leetcode import *

# def testClass(inputs):
#     # 用于测试 LeetCode 的类输入
#     s_res = [None] # 第一个初始化类, 一般没有返回
#     methods, args = [eval(l) for l in inputs.split('\n')]
#     class_name = eval(methods[0])(*args[0])
#     for method_name, arg in list(zip(methods, args))[1:]:
#         r = (getattr(class_name, method_name)(*arg))
#         s_res.append(r)
#     return s_res

""" 
https://leetcode.cn/contest/biweekly-contest-139
TODO: T3/4
Easonsi @2025 """
class Solution:
    """ 3285. 找到稳定山的下标 """
    def stableMountains(self, height: List[int], threshold: int) -> List[int]:
        ans = []
        for i in range(1, len(height)):
            if height[i-1] > threshold:
                ans.append(i)
        return ans
    
    """ 3286. 穿越网格图的安全路径 #medium 
经典 #Dijkstra 的题目, 
但这里边权是 0/1, 因此可以用  0-1 BFS!
    """
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        m,n = len(grid), len(grid[0])
        vis = [(0,0)]
        frontier = [(grid[0][0], 0,0)]
        while frontier:
            d,i,j = heappop(frontier)
            for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                if i==m-1 and j==n-1:  # reach the target!
                    return True
                x,y = i+di, j+dj
                if x<0 or x>=m or y<0 or y>=n: continue
                if (x,y) in vis: continue
                v = d + grid[x][y]
                if v >= health: continue
                vis.append((x,y))
                heappush(frontier, (v, x, y))
        return False
    
    """ 3287. 求出数组中最大序列值 #hard """

    
sol = Solution()
result = [
    sol.findSafeWalk(grid = [[1,1,1],[1,0,1],[1,1,1]], health = 5),
    sol.findSafeWalk(grid = [[0,1,1,0,0,0],[1,0,1,0,0,0],[0,1,1,1,0,1],[0,0,1,0,1,0]], health = 3),
]
for r in result:
    print(r)
