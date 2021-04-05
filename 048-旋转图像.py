"""
顺时针旋转二维图像 90 度
你必须在 原地 旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要 使用另一个矩阵来旋转图像。


输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]

注意变换顺序：显然是有规律的
（1）先看变换行数
【第 0 行】(0,0) - (0,n-1) - (n-1,n-1) - (n-1,0)
【第 1 行】(1,1) - (1,n-2) - (n-2,n-2) - (n-2,1)
这样的旋转需要从第 0 行做到 n//2-1 行，对于奇数行矩阵来说，中心块不需要移动

（2）再来看每一行需要变换多少
【第 0 行】从 (0,0) 到 (0,n-2) 共 n-1 组点
【第 1 行】从 (1,1) 到 (1,n-3) 共 n-2 组点
...
【第 n//2-1 行】从 (n//2-1, n//2-1) 到 (n//2-1, n-(n//2-1)-2) 组点，
例如对于 n=4，就是仅变换 (1,1) 位置的点
对于 n=5，就是变换 (1,1) to (1,2) 位置的点
基于以上分析，可知两层 for 循环的起始位置

（3）最后看变换规律
以 (0,1) -> (1,n-1) -> (n-1,n-2) -> (n-2, 0) 为例，可以看到每一个点向右旋转后，y'=x, x'=(n-1)-y
也即 (i,j) -> (j,n-1-i) -> (n-1-i,n-1-j) -> (n-1-j,i)


"""
from typing import List
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        a_ = n//2-1
        for i in range(a_+1):
            for j in range(i, n-i-1):
                temp = matrix[i][j]
                matrix[i][j] = matrix[n-1-j][i]
                matrix[n-1-j][i] = matrix[n-1-i][n-1-j]
                matrix[n - 1 - i][n - 1 - j] = matrix[j][n-1-i]
                matrix[j][n - 1 - i] = temp


# matrix = [[1,2,3],[4,5,6],[7,8,9]]
matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
Solution().rotate(matrix)
print(matrix)