""" 
D - Circumferences
给定坐标平面上的N个圆, 能能否仅通过在圆周上的路径, 从s到达t.
限制: 圆的数量N 3e3, 圆的位置和半径 1e9
思路1: 根据是否相交, 将圆之间建模为 #并查集 关系
    若两个圆相交/切, 则可以从一个圆到另一个圆.
    注意相交的条件: 假设两圆的半径为 r1>r2, 距离为d, 则相交要求: `r1-r2<=d<=r1+r2`
    复杂度: 两两检查是否相交 O(n^2), 按秩优化的并查集接近 O(1)?
    
https://atcoder.jp/contests/abc259/tasks/abc259_d
"""

n = int(input())
sx,sy, ts,ty = map(int, input().split())
circles = []
for i in range(n):
    x,y,r = map(int, input().split())
    circles.append((x,y,r))

# 找到 s,t 所在圆
sidx, tidx = -1, -1
for i,(x,y,r) in enumerate(circles):
    if (x-sx)**2+(y-sy)**2==r**2:
        sidx = i
    if (x-ts)**2+(y-ty)**2==r**2:
        tidx = i
# 题目保证两个点都在圆周上了, 不用判断
# if sidx==-1 or tidx==-1:
#     print("NO")
#     exit()

# class UnionSet():
#     def __init__(self, n) -> None:
#         self.fa = list(range(n))
#         self.sz = [1] * n
#     def find(self, x):
#         if self.fa[x]==x:
#             return x
#         self.fa[x] = self.find(self.fa[x])
#         return self.fa[x]
#     def union(self, x, y):
#         x,y = self.find(x), self.find(y)
#         if x==y: return
#         if self.sz[x] > self.sz[y]:
#             x,y = y,x
#         self.fa[x] = y; self.sz[y] += self.sz[x]
#     def is_same(self, x, y):
#         return self.find(x)==self.find(y)

# us = UnionSet(n)
# import math
fa = list(range(n))
sz = [1] * n
def find(x):
    if fa[x]==x:
        return x
    fa[x] = find(fa[x])
    return fa[x]
def union(x, y):
    x,y = find(x), find(y)
    if x==y: return
    if sz[x] > sz[y]:
        x,y = y,x
    fa[x] = y; sz[y] += sz[x]
def is_same(x, y):
    return find(x)==find(y)

for i in range(n):
    (x1,y1,r1) = circles[i]
    for j in range(i+1,n):
        # 剪枝
        # if us.is_same(i,j): continue
        if is_same(i,j): continue
        
        (x2,y2,r2) = circles[j]
        # 注意避免浮点数误差!!!
        # d = math.sqrt((x1-x2)**2+(y1-y2)**2)
        # if r1<r2: r1,r2 = r2,r1
        # # if d<=(r1+r2) and r2>=r1-d:
        # if r1-r2 <= d <= r1+r2:
        #     us.union(i,j)
        d2 = (x1-x2)**2 + (y1-y2)**2
        # if r1<r2: r1,r2 = r2,r1
        if (r1-r2)**2 <= d2 <= (r1+r2)**2:
            # us.union(i,j)
            union(i,j)
# print("Yes" if us.find(sidx)==us.find(tidx) else "No")
print("Yes" if find(sidx)==find(tidx) else "No")

