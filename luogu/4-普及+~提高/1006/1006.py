""" P1006 [NOIP2008 提高组] 传纸条 #提高
给一个 (M,N) 的网格, 从 (1,1) 两次走到 (M,N) 的不相交路径, 使得分数和最大.
约束: M,N <= 50
思路1: 棋盘的四维 #DP
    注意复杂度: 本题的数字较为宽松, 复杂度` O(M^2*N^2)` = 50^4 大概在 10^7 级别, 可以过
    状态: `f[a][b][c][d]` 表示某一时刻两条路径分别到达 (a,b),(c,d) 的分数和.
    递推:  `f[a][b][c][d] = max{f[a-1][b][c-1][d], f[a-1][b][c][d-1], f[a][b-1][c-1][d], f[a][b-1][c][d-1]} + score(a,b)+score(c,d)`, 这里的路径要求满足不相交.
    如何满足不相交?
        正如 P1004 中所说, 由于我们考虑的是 「同时」移动, 因此满足距离相等, `a+b==c+d`. 为了保证不相交, 事实上只需要 `a!=c` 即可 (此时两条路径相交了).
        事实上, 在本题设下, 可知两条路径一个在右上一个在左下, 不妨设第一条路径为上面的那一条, 则时刻都满足 `a<c and b>d`.
    注意: 由于上面的约束, 我们不会遍历到 (m,n,m,n) 节点, 因此答案是 (m-1,n, m,m-1) 的值!
思路2: 三维 #DP
    相较于四维的, 利用每时刻距离相同的性质, 枚举时刻/距离, 可以将DP化简到三维. 空间复杂度下降了.
    状态: `f[t][a][c]` 表示两条路径时刻 `t` 到达 (a,) 和 (c,d) 的分数和.
    递推公式: `f[t][a][c] = max{f[t-1][a][c], f[t-1][a][c-1], f[t-1][a-1][c], f[t-1][a-1][c-1]} + score(a,b)+score(c,d)`, 这里的路径要求满足不相交.
        例如, max第一项表示A从 (a,t-1-a) 到 (a,t-a), B从(c,t-1-c) 到 (c,t-c); 注意, 在四种情况下, 所加的分数都是 (a,b), (c,d)
    约束:
        为了满足坐标合法, 需要满足 `0<=a<=m-1 and 0<=t-a<=n-1` (因为要取用 `grid[a][t-a]`), 因此有 `max(t-n+1, 0) <= a,c <= min(t, m-1)`
        另外注意max中的部分可能不合法, 通过加哨兵简化判断
        同样, 为了不相交, 我们可以假设 `a<c`; 
    最后返回 `f[m+n-3][m-1][m]` 注意, 这里的路径长度为 (n-1) + (m-2) 因为不会遍历到最右下角的点.
    复杂度:` O((M+N)*M*M)`
总结: 对于这类棋盘DP问题, 需要注意DP矩阵的维度和访问范围. 相较于naive的思路1, 思路2复杂度上更胜一筹, 但是对于坐标合法的判断复杂了很多.
"""

m,n = map(int, input().split())
grid = [[0]*n for _ in range(m)]
for i in range(m):
    grid[i] = list(map(int, input().split()))
def v1():
    # 注意DP的大小为 f[m][n][m][n]
    f = [[[[0]*(n+1) for _ in range(m+1)] for _ in range(n+1)] for _ in range(m+1)]
    for a in range(m):
        for b in range(n):
            for c in range(m):
                for d in range(n):
                    if not (a<c and b>d): continue
                    if not (a+b==c+d): continue
                    f[a+1][b+1][c+1][d+1] = max(
                        f[a][b+1][c][d+1], f[a][b+1][c+1][d], f[a+1][b][c][d+1], f[a+1][b][c+1][d],
                    ) 
                    f[a+1][b+1][c+1][d+1] += grid[a][b] + grid[c][d]
    print(f[m-1][n][m][n-1])

f = [[[0]*(m+1) for _ in range(m+1)] for _ in range(m+n)]
for t in range(1, m+n):
    # 为了满足坐标合法, 需要满足 `0<=a<=m-1 and 0<=t-a<=n-1`
    for a in range(max(t-n+1, 0), min(t, m-1)+1):
        # if a>=t: break
        # 再加上假设 `a<c`
        for c in range(max(t-n+1,0, a+1), min(t, m-1)+1):
            # if c>=t: break
            f[t][a+1][c+1] = max(
                f[t-1][a][c], f[t-1][a][c+1], f[t-1][a+1][c], f[t-1][a+1][c+1],
            ) + grid[a][t-a] + grid[c][t-c]
# 注意, 这里的路径长度为 (n-1) + (m-2) 因为不会遍历到最右下角的点.
print(f[m+n-3][m-1][m])