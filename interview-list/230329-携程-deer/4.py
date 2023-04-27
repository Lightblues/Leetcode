""" 对于一棵树不相邻染色, 求最大边权和
给定一棵树, 边权, 可以对一些边染色, 要求不能同一个点的两条边都染色, 求最大染色边和

思路1; #树形 #DP
f(u,w) 返回 (a,b) 表示是否用了该节点的最大值
    u: 当前访问的节点
    w: 此前传入的边权
    边界 (孩子): (w,0)
    状态转移: 先收集孩子的结果
        对于a, 只能匹配孩子结果中的bb
        对于b, 可以从孩子中选择一个aa
"""
# 先建树; 后面的在写
n = int(input())
g = [[] for _ in range(n)]
for _ in range(n-1):
    u,v,w = map(int, input().split())
    u,v = u-1,v-1
    g[u].append((v,w))
    g[v].append((u,w))
tree = [[] for _ in range(n)]
def buildTree(u, fa=-1):
    """ 将图根据DFS转化为树 """
    for v,w in g[u]:
        if v==fa: continue
        tree[u].append((v,w))
        buildTree(v, u)
buildTree(0, -1)

def dfs(u, w):
    """ 返回 (a,b) """
    if len(tree[u])==0: return (w,0)
    aas, bbs = [], []
    for (v,ww) in tree[u]:
        aa,bb = dfs(v,ww)
        aas.append(aa); bbs.append(bb)
    a = w + sum(bbs)
    b = max(
        sum(bbs) + max(aa-bb for aa,bb in zip(aas,bbs)),
        # 注意! a 并不一定大于 b
        sum(bbs)
    )
    return (a,b)
print(max(dfs(0,0)))
