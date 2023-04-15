""" 
在 (n,m) 的grid中, 统计 (2,2) 的包含了you三个字母的矩形的个数.
"""
n,m = map(int, input().split())
grid = []
for _ in range(n):
    grid.append(list(input().strip()))
ans = 0
for i in range(n-1):
    for j in range(m-1):
        chs = [grid[i][j], grid[i+1][j], grid[i][j+1], grid[i+1][j+1]]
        if all(ch in chs for ch in "you"):
            ans += 1
print(ans)

