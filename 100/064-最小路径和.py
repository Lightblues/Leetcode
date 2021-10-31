"""
给定一个包含非负整数的 m x n 网格 grid ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。

说明：每次只能向下或者向右移动一步

输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
输出：7
解释：因为路径 1→3→1→1→1 的总和最小。
"""
from typing import List
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        l = [grid[0][0]] + [0]*(n-1)
        for i in range(1, n):
            l[i] = l[i-1] + grid[0][i]
        for i in range(1, m):
            l[0] += grid[i][0]
            for j in range(1, n):
                l[j] = min(l[j-1], l[j]) + grid[i][j]
        return l[-1]
grid = [[1,3,1],[1,5,1],[4,2,1]]
print(Solution().minPathSum(grid))
