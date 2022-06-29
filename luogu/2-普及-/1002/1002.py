""" [NOIP2002 普及组] 过河卒 #普及-
过河卒要从 (0,0), 走到 (m,n), 只能向右向下. 有一个马在位置 (x,y), 注意走的时候不能经过马以及马一个可跳到的位置. 问有多少条路径
思路1: #DP
    递推公式: 当 (i,j) 可以走时, 有 dp[i][j] = dp[i-1][j] + dp[i][j-1], 否则为 0.
"""
s = input().split()
m,n, x,y = list(map(int, s))
m,n = m+1, n+1
f = [[0] * n for _ in range(m)]
f[0][0] = 1
def test(a,b):
    xx, yy = abs(a-x), abs(b-y)
    if xx==yy==0: return False
    return xx**2 + yy**2 != 5
for j in range(1, n):
    if test(0, j):
        f[0][j] = 1
    else:
        break
for i in range(1, m):
    if test(i, 0):
        f[i][0] = f[i-1][0]
    for j in range(1, n):
        if test(i, j):
            f[i][j] = f[i-1][j] + f[i][j-1]
print(f[-1][-1])
