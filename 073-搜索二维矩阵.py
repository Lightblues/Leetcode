"""
编写一个高效的算法来判断m x n矩阵中，是否存在一个目标值。该矩阵具有如下特性：

每行中的整数从左到右按升序排列。
每行的第一个整数大于前一行的最后一个整数。

输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true

---
就是将升序数组排列成了二维矩阵形式
"""
from typing import List
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        def listIndex2matrixIndes(i):
            quotient, remainder = divmod(i, n)
            return quotient, remainder
        left, right = 0, m*n-1
        while left <= right:
            mid = (left+right)//2
            i,j = listIndex2matrixIndes(mid)
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] < target:
                left = mid+1
            else:
                right = mid-1
        return False
# matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]; target = 20
matrix = [[1,3]]; target = 1
print(Solution().searchMatrix(matrix, target))
