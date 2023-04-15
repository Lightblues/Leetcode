""" 
树节点值为0/1, 对于树上的所有路径, 找到范围在 [l,r] 的二进制数量. 
限制: n 1e3, l,r 1e14
思路1: #DFS 
    对于 f(u), 返回以u出发的值为x的数量; 以及从下往上以u结尾的值为x的数量 (Counter)
    在f函数内: 先得到所有孩子的返回结果
        构造返回: 综合所有孩子的结果
        路径匹配: 还要对于两个孩子 a,b 的结果进行综合
"""
import collections
n,l,r = map(int, input().split())
vals = list(map(int, input().strip()))
g = [[] for _ in range(n)]
for _ in range(n-1):
    u,v = map(int, input().split())
    u,v = u-1,v-1
    g[u].append(v); g[v].append(u)

ans = 0
def dfs(u, fa):
    global ans
    # 分别以孩子u出发/结尾的值为x的路径Counter列表
    uds, dus = [], []
    ud, du = collections.Counter(), collections.Counter()
    vv = vals[u]
    ud[(vv,1)] += 1
    du[vv] += 1
    for v in g[u]:
        if v==fa: continue
        cud, cdu = dfs(v,u)
        uds.append(cud); dus.append(cdu)
        # 
        for (val,ll),c in cud.items():
            nval = vals[u]<<ll | val
            if nval>r: continue
            if l<=nval<=r: ans += c
            ud[(nval,ll+1)] += c
        for val,c in cdu.items():
            nval = vals[u] | val<<1
            if nval>r: continue
            if l<=nval<=r: ans += c
            du[nval] += c
    # 
    # nchild = len(uds)
    for i,cdu in enumerate(dus):
        for j,cud in enumerate(uds):
            if i==j: continue
            for vdu,c1 in cdu.items():
                for (vud,ll),c2 in cud.items():
                    nval = vals[u]<<ll | vdu<<(ll+1) | vud
                    # if nval>r: continue
                    if l<=nval<=r: ans += c1*c2
    return ud, du
dfs(0,-1)
print(ans)
