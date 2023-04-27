""" 
给定一棵树, 再给定一个长m的数组, 计算数组中任意 (i,j) 位置节点之间的距离和. #hard
限制: n,m 1e5

"""

n = int(input())
arr = list(map(int, input().split()))
m = int(input())
g = [[] for _ in range(m+1)]
for _ in range(m-1):
    u,v = map(int, input().split())
    g[u].append(v)
    g[v].append(v)
father = [-1] * (m+1)
def dfs(u,fa):
    for v in g[u]:
        if v==fa:
            continue
        father[v] = u
        dfs(v,u)
dfs(1,-1)
print(father)
from functools import cache
@cache
def dist(u,v):
    if u==v:
        return 0
    u,v = sorted([u,v])
    if u==1:
        return dist(u,father[v]) + 1
    return min(dist(u,father[v])+1, dist(v,father[u])+1) #, dist(father[u], father[v])+2)
print(dist(1,2))
# print(dist(1,3))
    