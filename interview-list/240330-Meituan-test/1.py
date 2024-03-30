""" 
24春招第一场
https://www.nowcoder.com/exam/test/79025101/detail?pid=55750543

T4 小美的朋友关系 #hard 有意思
对于一个图结构的朋友关系, 某些节点会发生遗忘, 对于某些查询, 看他们是否相连. 
限制; n 1e9; m,q 1e5
思路1: #并查集
    反向模拟构建关联的过程.
    如何处理大的数量? 对于id进行离散化
NOTE: 注意处理不存在的情况: 查询的id不在remap中, 遗忘的边原本不存在 & 剩余的边记得需要初始化
"""
n,m,q = map(int, input().split())
edges_raw = []
ids = set()
for _ in range(m):
    a,b = map(int, input().split())
    edges_raw.append((a,b))
    ids.add(a)
    ids.add(b)
remap = {id:i for i,id in enumerate(sorted(ids))}
edges = set()
for u,v in edges_raw:
    edges.add((remap[u],remap[v]))

nn = len(remap)
# 并查集
fa = [i for i in range(nn)]
def find(x):
    if fa[x] != x:
        fa[x] = find(fa[x])
    return fa[x]
def union(x,y):
    fa[find(x)] = find(y)

records = []
for _ in range(q):
    t,a,b = map(int, input().split())
    if a not in remap or b not in remap:
        if t==1: 
            continue                    # 删除了不存在的边
        else:
            records.append((3, (0,0)))  # 查询的本身就没有关联
    else:
        a,b = remap[a],remap[b]
        if t==1:                        # 遗忘
            if ((a,b) not in edges) and ((b,a) not in edges):   # 原本不存在
                continue
            else:
                records.append((1, (a,b)))
                edges.discard((a,b))
                edges.discard((b,a))
        else:
            records.append((2, (a,b)))

# 构建剩余的连接管理
for u,v in edges:
    union(u,v)
ans = []
for t,(a,b) in records[::-1]:
    if t==3: ans.append('No')
    elif t==1: union(a,b)
    elif t==2: ans.append('Yes' if find(a)==find(b) else 'No')

for a in ans[::-1]:
    print(a)