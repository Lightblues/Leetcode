"""
给定一个 m x n 的矩阵，如果一个元素为 0，则将其所在行和列的所有元素都设为 0。请使用原地算法。

输入: 
[
 [0,1,2,0],
 [3,4,5,2],
 [1,3,1,5]
]
输出: 
[
 [0,0,0,0],
 [0,4,5,0],
 [0,3,1,0]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/set-matrix-zeroes
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m, n = len(matrix), len(matrix[0])
        zero_rows = [any([n==0 for n in row]) for row in matrix]
        zero_cols = []
        for j in range(n):
            col = [matrix[i][j] for i in range(m)]
            zero_cols.append(any([n==0 for n in col]))
        for i in range(m):
            if zero_rows[i]:
                matrix[i] = [0]*n
        for j in range(n):
            if zero_cols[j]:
                for i in range(m):
                    matrix[i][j] = 0

matrix = [
 [0,1,2,0],
 [3,4,5,2],
 [1,3,1,5]
]
Solution().setZeroes(matrix)
print(matrix)