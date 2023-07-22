""" 
树上删掉一个点, 问得到的各联通块大小
"""
# set max recursion depth
import sys
sys.setrecursionlimit(1000000)
n = int(input())
g = [[] for _ in range(n+1)]
# vis = [False] * (n+1)
for _ in range(n-1):
    u,v  = map(int, input().split())
    g[u].append(v); g[v].append(u)
x = int(input())
ans = []
def dfs(u, fa):
    # if vis[u]: return 0
    # vis[u] = True
    ans = 1
    for v in g[u]:
        # if vis[v]: continue
        if v==fa: continue
        ans += dfs(v,u)
    return ans
for u in g[x]:
    ans.append(dfs(u,x))
ans.sort()

print(len(ans))
print(' '.join(map(str, ans)))


