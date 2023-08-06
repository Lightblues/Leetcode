""" 
对于矩阵, 对角线元素逆时针90, 其余元素顺时针90度选装
思路1: 如何实现顺时针旋转? 
    可以先水平翻折, 再副对角线翻折
    如何对于对角线元素逆时针? 可知对于顺时针旋转的结果, 再反转对角线即可!
"""
n = int(input())
mat = []
for _ in range(n):
    mat.append(list(map(int, input().split())))
    
# 先水平翻折
for i in range(n):
    for j in range(n//2):
        mat[i][j], mat[i][n-1-j] = mat[i][n-1-j], mat[i][j]
# 再副对角线翻折
# 满足 (i, j) -> (n-1-j, n-1-i)
for i in range(n):
    for j in range(n-1-i):
        i2,j2 = n-1-j, n-1-i
        mat[i][j], mat[i2][j2] = mat[i2][j2], mat[i][j]

# 对于对角线进行翻折
for i in range(n//2):
    mat[i][i], mat[n-1-i][n-1-i] = mat[n-1-i][n-1-i], mat[i][i]
for i in range(n//2):
    j = n-1-i
    i2,j2 = n-1-i, n-1-j
    mat[i][j], mat[i2][j2] = mat[i2][j2], mat[i][j]

for row in mat:
    print(" ".join(map(str, row)))
