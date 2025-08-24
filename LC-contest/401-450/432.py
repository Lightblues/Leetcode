from typing import *
import math

""" 
https://leetcode.cn/contest/weekly-contest-432

Easonsi @2025 """
class Solution:
    """ 3417. 跳过交替单元格的之字形遍历 """
    def zigzagTraversal(self, grid: List[List[int]]) -> List[int]:
        m,n = len(grid),len(grid[0])
        ans = []
        flag = 0
        for i in range(m):
            line = grid[i]
            if i%2:
                line = line[::-1]
            ans += line[flag::2]
            if n%2:
                flag = 1-flag
        return ans
    
    """ 3418. 机器人可以获得的最大金币数 从 (0,0) 到 (m,n), 只能往右往下, 计算累计分数, 但最多可以避免两次负分, 求最大收益
思路1: #DP 很标准DP思路, 设 f[i,j,k] 表示到达 (i,j) 并且至多跳过k次的最大收益
    可以实用递推
    注意哨兵和边界的使用
    """
    def maximumAmount(self, coins: List[List[int]]) -> int:
        m,n = len(coins),len(coins[0])
        f = [[[-math.inf]*3 for _ in range(n+1)] for _ in range(m+1)]
        f[1][0] = [0,0,0]  # 注意这里的边界!
        for i,line in enumerate(coins):
            for j,v in enumerate(line):
                f[i+1][j+1][0] = max(f[i][j+1][0], f[i+1][j][0]) + v
                f[i+1][j+1][1] = max(f[i][j+1][1]+v, f[i+1][j][1]+v, f[i][j+1][0], f[i+1][j][0])
                f[i+1][j+1][2] = max(f[i][j+1][2]+v, f[i+1][j][2]+v, f[i][j+1][1], f[i+1][j][1])
        return f[m][n][2]
    
    """ 3419. 图的最大边权的最小值 #medium 给定一个有向带权图, 可以删除一些边, 使得 1) 所有节点都能到0; 2) 所有节点的出度最大为th. 问最终得到的图中, 最大边权的最小值 min(max(v)) 
限制: 无法到达0的话返回-1. a->b 之间可能多有条边; n 1e5
    """
    
sol = Solution()
result = [
    # sol.zigzagTraversal(grid = [[1,2],[3,4]]),
    # sol.zigzagTraversal(grid = [[1,2,3],[4,5,6],[7,8,9]]),
    sol.maximumAmount(coins = [[0,1,-1],[1,-2,3],[2,-3,4]]),
]
for r in result:
    print(r)
