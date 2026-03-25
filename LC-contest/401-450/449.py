from typing import *

""" 
https://leetcode.cn/contest/weekly-contest-449
Easonsi @2025 """
class Solution:
    """  """
    def minDeletion(self, s: str, k: int) -> int:
        from collections import Counter
        freq = sorted(Counter(s).values())  # 按频次升序排列
        res = 0
        # 需要删掉 len(freq) - k 个不同字符，贪心删频次最小的
        while len(freq) > k:
            res += freq.pop(0)
        return res

    def canPartitionGrid(self, grid: List[List[int]]) -> bool:
        total = sum(sum(row) for row in grid)
        if total % 2 != 0:
            return False
        half = total // 2
        m, n = len(grid), len(grid[0])
        # 水平切割：在第 i 行和第 i+1 行之间切
        prefix = 0
        for i in range(m - 1):
            prefix += sum(grid[i])
            if prefix == half:
                return True
        # 垂直切割：在第 j 列和第 j+1 列之间切
        prefix = 0
        for j in range(n - 1):
            prefix += sum(grid[i][j] for i in range(m))
            if prefix == half:
                return True
        return False

sol = Solution()
result = [
    
]
for r in result:
    print(r)
