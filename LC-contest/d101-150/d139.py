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
    
    """ 3287. 求出数组中最大序列值 #hard 长度为2k的子序列, 得分为前一半OR和后一半OR 之后, 两个数字XOR的结果. 求最大得分
限制: n 400; x 2^7
"""
    def maxValue(self, nums: List[int], k: int) -> int:
        pass
    
    """ 3288. 最长上升路径的长度 #hard 给定一组二维坐标点, 和其中一个点, 求一个最长的序列, 包含该点, 同时每个元素 x/y 严格递增
限制: n 1e5
"""
    
sol = Solution()
result = [
    sol.findSafeWalk(grid = [[1,1,1],[1,0,1],[1,1,1]], health = 5),
    sol.findSafeWalk(grid = [[0,1,1,0,0,0],[1,0,1,0,0,0],[0,1,1,1,0,1],[0,0,1,0,1,0]], health = 3),
]
for r in result:
    print(r)
