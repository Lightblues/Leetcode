"""
给定一个矩阵，按照顺时针方式返回每一个元素

输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]
"""
from typing import List
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        if n == 1:
            return [matrix[r][0] for r in range(m)]

        limits = [n, m, -1, 0]
        direction = 0
        result = []
        r, c = 0, 0
        result.append(matrix[0][0])
        while True:
            if direction==0:
                if c==limits[0]-1:
                    break
                for col in range(c+1, limits[0]):
                    result.append(matrix[r][col])
                c = limits[0]-1
                limits[0] -= 1
            elif direction==1:
                if r==limits[1]-1:
                    break
                for row in range(r+1, limits[1]):
                    result.append(matrix[row][c])
                r = limits[1]-1
                limits[1] -= 1
            elif direction==2:
                if c==limits[2]+1:
                    break
                for col in range(c-1, limits[2], -1):
                    result.append(matrix[r][col])
                c = limits[2]+1
                limits[2] += 1
            elif direction==3:
                if r==limits[3]+1:
                    break
                for row in range(r-1, limits[3], -1):
                    result.append(matrix[row][c])
                r = limits[3]+1
                limits[3] += 1
            direction = (direction+1)%4
        return result

    def spiralOrder2(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return list()

        rows, columns = len(matrix), len(matrix[0])
        order = list()
        left, right, top, bottom = 0, columns - 1, 0, rows - 1
        while left <= right and top <= bottom:
            for column in range(left, right + 1):
                order.append(matrix[top][column])
            for row in range(top + 1, bottom + 1):
                order.append(matrix[row][right])
            if left < right and top < bottom:
                for column in range(right - 1, left, -1):
                    order.append(matrix[bottom][column])
                for row in range(bottom, top, -1):
                    order.append(matrix[row][left])
            left, right, top, bottom = left + 1, right - 1, top + 1, bottom - 1
        return order

# matrix = [[1,2,3],[4,5,6],[7,8,9]]
matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
# matrix = [[1],[2]]
print(Solution().spiralOrder2(matrix))


