""" P1004 [NOIP2000 提高组] 方格取数 #提高
有一个 (N,N) 的grid, 包含一些分数, 可以两次从 (1,1) 走到 (N,N), 方向只能向下向右, 问两条路径最多能够得到分数和为多少.
限制: N<=9
思路1: 四维 #DP
    注意: 从左上到右下的路径长度是固定的 2N-2; 考虑两个人「同时从起点出发走向终点」, 某一时刻两人距离起点的曼哈顿距离是固定的, 
        因此, 不会出现B在时刻t2到达A在时刻t1!=t2的所在点的情况. 根据这一性质, 可以避免重复记分的问题.
    因此, 用 f[a][b][c][d] 表示A,B分别在 (a,b) 和 (c,d) 的最大分数和.
    递推公式: f[a][b][c][d] = max{f[a-1][b][c-1][d], f[a-1][b][c][d-1], f[a][b-1][c-1][d], f[a][b-1][c][d-1]} + score{(a,b), (c,d)},
        其中前一项是上一状态的最大分数(两两组合), 第二项是当前时刻的得到分数, 注意避免 (a,b)==(c,d) 重复记分.
思路2: 实际上利用上述性质, 可以优化到三维 #DP, 参见 P1006
"""

n = int(input())
grid = [[0] * n for _ in range(n)]
while True:
    x,y,v = map(int, input().split())
    if x==y==v==0: break
    grid[x-1][y-1] = v
f = [[[[0] * (n+1) for _ in range(n+1)] for _ in range(n+1)] for _ in range(n+1)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                f[a+1][b+1][c+1][d+1] = max(
                    f[a][b+1][c][d+1], f[a][b+1][c+1][d], f[a+1][b][c][d+1], f[a+1][b][c+1][d],
                )
                f[a+1][b+1][c+1][d+1] += grid[a][b]
                if not (a==c and b==d):
                    f[a+1][b+1][c+1][d+1] += grid[c][d]
print(f[n][n][n][n])