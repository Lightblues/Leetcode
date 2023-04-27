""" 必经之路
对于一棵树, 指定一条边, 求经过该边路径的最大值
限制: n 2e5
思路1: 带限制的 DFS
    对于一条边所划分的两个子树, 分别计算其作为root的最大路径
    #WA 90%? 原来是爆递归栈了!
"""
# set recursion limit
import sys
# 原来是爆递归栈了!
sys.setrecursionlimit(1000000)

from collections import defaultdict
n = int(input())
g = defaultdict(list)
edges = list(map(int, input().split()))

for i,v in enumerate(edges):
    g[v].append(i+2)
    g[i+2].append(v)
a,b = map(int, input().split())

def dfs(x,fa, d=0):
    mx = d
    for v in g[x]:
        if v==fa: continue
        r = dfs(v,x,d+1)
        mx = max(mx, r)
    return mx
print(dfs(a,b)+dfs(b,a)+1)

