"""
给你一个正整数 n ，生成一个包含 1 到 n2 所有元素，且元素按顺时针顺序螺旋排列的 n x n 正方形矩阵 matrix 。

输入：n = 3
输出：[[1,2,3],[8,9,4],[7,6,5]]
"""
from typing import List
class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        matrix = [[1]*n for _ in range(n)]
        count = 1
        left, right, top, bottom = 0, n - 1, 0, n - 1
        while left <= right and top <= bottom:
            for column in range(left, right + 1):
                matrix[top][column] = count
                count += 1
            for row in range(top + 1, bottom + 1):
                matrix[row][right] = count
                count += 1
            if left < right and top < bottom:
                for column in range(right - 1, left, -1):
                    matrix[bottom][column] = count
                    count += 1
                for row in range(bottom, top, -1):
                    matrix[row][left] = count
                    count += 1
            left, right, top, bottom = left + 1, right - 1, top + 1, bottom - 1
        return matrix

print(Solution().generateMatrix(3))


