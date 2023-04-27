""" 
对于一棵树, 一部分染色 RBG, 问有多少中染色方案. 对结果取模

"""
MOD = 10**9 + 7
n,m = map(int, input().split())

# construt graph
g = [[] for _ in range(n)]
for _ in range(n-1):
    u,v = map(int, input().split())
    u,v = u-1,v-1
    g[u].append(v)
    g[v].append(u)

color = [-1] * n
colorMap = {"R":0, "B":1, "G":2}
for _ in range(m):
    u,c = input().split()
    color[int(u)-1] = colorMap[c.strip()]

tree = [[] for _ in range(n)]
def buildTree(u, fa=-1):
    """ 将图根据DFS转化为树 """
    for v in g[u]:
        if v==fa: continue
        tree[u].append(v)
        buildTree(v, u)
buildTree(0, -1)

def dfs(u,fa):
    """ fa 是父亲节点的颜色; 返回所有可能的数量 """
    # 是叶子节点
    if len(tree[u])==0: 
        if color[u]==-1: return 2 if fa!=-1 else 3
        else: return 1 if color[u]!=fa else 0
    # 是中间节点!
    ans = 0
    if color[u]==-1:
        # 尝试填上颜色
        for c in colorMap.values():
            if c==fa: continue
            tmp = 1
            for v in tree[u]:
                tmp *= dfs(v, c)
            ans += tmp
    else:
        c = color[u]
        if c==fa: return 0
        tmp = 1
        for v in tree[u]:
            tmp *= dfs(v, c)
        ans += tmp
    return ans % MOD

def dfs(u):
    """ 从下往上, 返回u节点分别填充为RGB下, 可以多少解 """
    cnt = [0,0,0]
    # leaf
    if len(tree[u])==0: 
        if color[u]==-1: return [1,1,1]
        else: 
            cnt[color[u]] = 1
            return cnt
    comb = []
    for v in tree[u]:
        comb.append(dfs(v))
    c = color[u]
    if c!=-1:
        tmp = 1
        for cc in comb:
            tmp *= sum(cc)-cc[c]
        cnt[c] = tmp
    else:
        for c in colorMap.values():
            tmp = 1
            for cc in comb:
                tmp *= sum(cc)-cc[c]
            cnt[c] = tmp
    return cnt

# print(dfs(0,-1))
print(sum(dfs(0)))
