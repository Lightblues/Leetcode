""" 雷区行走 
在 (n,m) 的grid中有k个地雷, 要从start走到end, 希望路径上尽可能远离地雷, 求最大可能距离
限制: n,m 500; k 400
思路1: 先算出所有位置到地雷的距离, 然后从start出发UCS
    如何预计算到地雷的距离? 也是对于k个开始位置进行UCS
"""
import heapq
from math import inf
n,m,k = map(int, input().split())
grid = [[inf]*m for _ in range(n)]
h = []  # (dist, x,y)
for _ in range(k):
    x,y = map(int, input().split())
    h.append((0, x-1,y-1))
    grid[x-1][y-1] = 0
sx,sy, ex,ey = map(int, input().split())
sx,sy, ex,ey = sx-1,sy-1, ex-1,ey-1

dirs = [(0,1),(0,-1),(1,0),(-1,0)]
def isValid(x,y):
    return 0<=x<n and 0<=y<m
# UCS
heapq.heapify(h)
while h:
    d,x,y = heapq.heappop(h)
    for dx,dy in dirs:
        nx,ny = x+dx, y+dy
        if not isValid(nx,ny): continue
        if d+1 < grid[nx][ny]:
            grid[nx][ny] = d+1
            heapq.heappush(h, (d+1, nx,ny))
# UCS
h = [(-grid[sx][sy], sx,sy)]
mxD = grid[sx][sy]
grid[sx][sy] = -1
while h:
    d,x,y = heapq.heappop(h)
    mxD = min(mxD, -d)
    if x==ex and y==ey: break
    if d==0: break
    for dx,dy in dirs:
        nx,ny = x+dx, y+dy
        if not isValid(nx,ny): continue
        if grid[nx][ny]==-1: continue
        heapq.heappush(h, (-grid[nx][ny], nx,ny))
        grid[nx][ny] = -1
print(mxD)



