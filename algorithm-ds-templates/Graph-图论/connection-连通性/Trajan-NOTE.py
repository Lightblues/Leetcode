""" 
https://oi-wiki.org/graph/scc
图: https://www.cnblogs.com/yanyiming10243247/p/9294160.html
但上面的初始化错了?? 看不懂. 
"""

N = 100
class Node:
    def __init__(self, t, nex):
        self.t = t
        self.nex = nex
nnode = 6
nedge = 8
h = [None] * (nedge+1)
e = [None] * (nnode + 1)
edgeIdx = 0
def add(u, v):
    global edgeIdx
    e[edgeIdx] = Node(v, h[u])
    edgeIdx = edgeIdx + 1
    h[u] = edgeIdx
for u,v in [[1,2], [1,3], [2,4], [3,4], [4,1], [3,5], [4,6], [5,6]]:
    add(u, v)

# Python Version
dfn = [] * N; low = [] * N; dfncnt = 0; s = [] * N; in_stack  = [] * N; tp = 0
scc = [] * N; sc = 0 # 结点 i 所在 SCC 的编号
sz = [] * N # 强连通 i 的大小
def tarjan(u):
    low[u] = dfn[u] = dfncnt; s[tp] = u; in_stack[u] = 1
    dfncnt = dfncnt + 1; tp = tp + 1
    i = h[u]
    while i:
        v = e[i].t
        if dfn[v] == False:
            tarjan(v)
            low[u] = min(low[u], low[v])
        elif in_stack[v]:
            low[u] = min(low[u], dfn[v])
        i = e[i].nex
    if dfn[u] == low[u]:
        sc = sc + 1
        while s[tp] != u:
            scc[s[tp]] = sc
            sz[sc] = sz[sc] + 1
            in_stack[s[tp]] = 0
            tp = tp - 1
        scc[s[tp]] = sc
        sz[sc] = sz[sc] + 1
        in_stack[s[tp]] = 0
        tp = tp - 1
tarjan(1)
print(scc)