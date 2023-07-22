""" 
树上删掉一个点, 问得到的各联通块大小
思路1: #DFS
思路2: #BFS
"""
# # set max recursion depth
# import sys
# sys.setrecursionlimit(1000000)

# n = int(input())
# g = [[] for _ in range(n+1)]
# for _ in range(n-1):
#     u,v  = map(int, input().split())
#     g[u].append(v); g[v].append(u)
# x = int(input())
# ans = []

# def dfs(u, fa):
#     ans = 1
#     for v in g[u]:
#         if v==fa: continue
#         ans += dfs(v,u)
#     return ans
# for u in g[x]:
#     ans.append(dfs(u,x))
# ans.sort()
# print(len(ans))
# print(' '.join(map(str, ans)))






n = int(input())
g = [[] for _ in range(n+1)]
for _ in range(n-1):
    u,v  = map(int, input().split())
    g[u].append(v); g[v].append(u)
x = int(input())
vis = [False] * (n+1)
from collections import deque
def bfs(x):
    vis[x] = True
    ans = 1
    q = deque([x])
    while q:
        u = q.popleft()
        for v in g[u]:
            if vis[v]: continue
            vis[v] = True
            ans += 1
            q.append(v)
    return ans
ans = []
vis[x] = True
for u in g[x]:
    ans.append(bfs(u))
ans.sort()
print(len(ans))
print(' '.join(map(str, ans)))