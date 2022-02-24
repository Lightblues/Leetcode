from typing import List
"""
二维前缀和: 方便地得到一个矩形中, 任意一个子矩阵的和


 304. 二维区域和检索 - 矩阵不可变
对于一个矩阵, 要求 计算其子矩形范围内元素的总和，该子矩阵的 左上角 为 (row1, col1) ，右下角 为 (row2, col2) 。
这里要求实现一个类

模型: 二维前缀和
[sol](https://leetcode-cn.com/problems/range-sum-query-2d-immutable/solution/er-wei-qu-yu-he-jian-suo-ju-zhen-bu-ke-b-2z5n/)
 """
class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        m,n = len(matrix), len(matrix[0])
        self.m = m
        self.n = n
        self.matrix = matrix
        # 拓展一个哨兵
        self.matrixSum = [[0]*(n+1) for _ in range(m+1)]
        self.calSum()

    def calSum(self):
        # 计算二维前缀和
        for i in range(1, self.m+1):
            for j in range(1, self.n+1):
                self.matrixSum[i][j] = self.matrixSum[i-1][j] + self.matrixSum[i][j-1] - self.matrixSum[i-1][j-1] + self.matrix[i-1][j-1]

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return self.matrixSum[row2+1][col2+1] - self.matrixSum[row2+1][col1] -self.matrixSum[row1][col2+1] + self.matrixSum[row1][col1]

numMatrix = NumMatrix([
    [1,0,0],
    [0,1,1],
])
rels = [
    numMatrix.sumRegion(0,0,0,0),
    numMatrix.sumRegion(0,0,1,1),
]
print(rels)
