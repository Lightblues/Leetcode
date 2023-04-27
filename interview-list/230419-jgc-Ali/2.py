""" 姜国超 阿里 230419
对于一棵小写字母的树上, 长度为4的回文串有多少个? 限制: n 1e5
思路1: #树形 #DP
超时了, 通过90%
"""
from collections import defaultdict
n = int(input())
colors = input().strip()
g = [[] for _ in range(n)]
for _ in range(n-1):
    u,v = map(int, input().split())
    u,v = u-1,v-1
    g[u].append(v); g[v].append(u)

ans = 0
def dfs(u, fa):
    """ 返回长为 1,2,3 的路径的数量 """
    global ans

    c = colors[u]
    childs = []
    for v in g[u]:
        if v == fa: continue
        childs.append(dfs(v, u))
    ret = [defaultdict(int) for _ in range(3)]
    ret[0][c] += 1
    for c1,c2,c3 in childs:
        for s1,v in c1.items():
            ret[1][s1+c] += v
        for s2,v in c2.items():
            if c!=s2[1]: continue
            ret[2][s2+c] += v
        for s3,v in c3.items():
            if c==s3[0]: 
                ans += v
    for i,(c1,_,_) in enumerate(childs):
        for j,(_,c2,_) in enumerate(childs):
            if i==j: continue
            for s1,v1 in c1.items():
                for s2,v2 in c2.items():
                    if s1==s2[0] and c==s2[1]: 
                        ans += v1*v2
    return ret
dfs(0, -1)
print(ans)
