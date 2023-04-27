""" 最优规划
从 (0,0) 位置探索一个 (n,m) 的矩阵, 矩阵格子由 B/R 两种颜色组成, 每个格子有一个分数
可以 向下、向右 移动; 若相邻格子颜色不同色需要支付 k的代价; 获得格子分数.
问在金币数量不得<0 的限制下, 移动到任意位置停止得到的最大分数.
限制: m,n 200; k [1,5]; score [0,10]

思路1: 基本 #DP 
    f[i,j] = max{ f[i,j-1] - cost, f[i-1,j] - cost } + score[i,j]
    其中cost是移动的代价, 可能为 0/k.
    注意限制条件
 """

from functools import cache

n,m,k = list(map(int, input().split()))
color = [['B']*m for _ in range(n)]
score = [[0]*m for _ in range(n)]

for i in range(n):
    co = input().strip()
    for j,c in enumerate(co):
        if c=='R': color[i][j] = 'R'
for i in range(n):
    sc = list(map(int, input().split()))
    for j,s in enumerate(sc):
        score[i][j] = s
@cache
def f(i,j):
    if i==j==0: return 0
    res = -1
    if i>0:
        s = f(i-1,j)
        if color[i][j]!=color[i-1][j]: s-=k
        # 注意限制条件
        if s>=0:
            res = max(res, s+score[i][j])
    if j>0:
        s = f(i,j-1)
        if color[i][j]!=color[i][j-1]: s-=k
        if s>=0:
            res = max(res, s+score[i][j])
    return res

res =  max(max(f(i,j) for j in range(m)) for i in range(n))
print(res)


