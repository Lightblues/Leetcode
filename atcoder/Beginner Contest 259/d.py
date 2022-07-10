""" 
D - Circumferences
给定坐标平面上的N个圆, 能能否仅通过在圆周上的路径, 从s到达t.
思路1: 根据是否相交, 将圆之间建模为 #并查集 关系
    若两个圆相交/切, 则可以从一个圆到另一个圆.
    注意相交的条件: 假设两圆的半径为 r1>r2, 距离为d, 则相交要求: `r1-r2<=d<=r1+r2`
"""

n = int(input())
sx,sy, ts,ty = map(int, input().split())
circles = []
for i in range(n):
    x,y,r = map(int, input().split())
    circles.append((x,y,r))

sidx, tidx = -1, -1
for i,(x,y,r) in enumerate(circles):
    if (x-sx)**2+(y-sy)**2==r**2:
        sidx = i
    if (x-ts)**2+(y-ty)**2==r**2:
        tidx = i
if sidx==-1 or tidx==-1:
    print("NO")
    exit()

class UnionSet():
    def __init__(self, n) -> None:
        self.fa = list(range(n))
    def find(self, x):
        if self.fa[x]==x:
            return x
        self.fa[x] = self.find(self.fa[x])
        return self.fa[x]
    def union(self, x, y):
        x,y = self.find(x), self.find(y)
        if x==y: return
        self.fa[x] = y

us = UnionSet(n)
import math
for i,(x1,y1,r1) in enumerate(circles):
    for j,(x2,y2,r2) in enumerate(circles):
        if i==j: continue
        d = math.sqrt((x1-x2)**2+(y1-y2)**2)
        if r1<r2: r1,r2 = r2,r1
        if d<=(r1+r2) and r2>=r1-d:
            us.union(i,j)
print("YES" if us.find(sidx)==us.find(tidx) else "NO")