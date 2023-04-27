""" 
树上一组边坏掉了, 从root出发, 到达每个点都要求最短路的情况, 问最少需要派出所少人?
思路1: 树上的 #DFS #树形 #DP
    定义 dfs(u,ifBreak)
"""
n = int(input())
g = [[] for _ in range(n)]
for _ in range(n-1):
    u,v,ifBreak = map(int, input().split())
    u,v = u-1,v-1
    g[u].append((v,ifBreak))
    g[v].append((u,ifBreak))
tree = [[] for _ in range(n)]
def buildTree(u,fa):
    for v,ifBreak in g[u]:
        if v==fa: continue
        tree[u].append((v,ifBreak))
        buildTree(v,u)
buildTree(0,-1)
# 
def dfs(u,ifBreak):
    """ 返回到这个节点为止的最少人数 """
    if len(tree[u])==0: return ifBreak
    res = 0
    for v,ii in tree[u]:
        res += dfs(v,ii)
    return max(res, ifBreak)
print(dfs(0,0))