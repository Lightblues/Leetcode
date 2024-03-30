""" 
对于n个人需要请客. 有一组暗恋关系, u->v, 若邀请了v则必须要求u (但反过来可以), 问有多少种可能的方案. 
限制: n,m 1e5 对结果取模. 每个人最多暗恋一个人
思路1:
    由于一个节点最多一个出边 (out_degree <= 1), 只可能出现简单的「环」, 带有一些链
    核心在于识别图中的环! —— 可以对于图中 in_degree==0 的节点开始进行删减. 最终剩下的就是环上的节点!
    然后, 对于每个环, 环上的人只能一次全请
        (不请环上的人) 对于每个链结构, 是 * 关系
    对于不同的环结构, 是 * 关系
        注意, 除了环之外, 剩下的是单个节点或者链结构

2 1
1 2
# 2     单个链

3 2
1 2
2 3
# 33 2
1 2
2 3
# 3

3 3
1 2
2 3
3 1
# 1     单个环

4 4
1 2
2 3
3 1
4 1
# 2     带了1个分支

5 5
1 2
2 3
3 1
4 1
5 1
# 4     带了2个分支

5 5
1 2
2 3
3 1
4 1
5 2
# 4     带了2个分支

6 6
1 2
2 3
3 1
4 1
5 2
6 3
# 8     带了3个分支

6 6
1 2
2 3
3 1
4 1
5 1
6 3
# 8

4 3
2 1
3 1
4 2
# 6     单个树结构

5 4
2 1
3 1
4 2
5 2
# 10    单个树结构

3 0
# 7     多节点的情况
"""
from collections import deque
import sys
sys.setrecursionlimit(int(1e9))
MOD = 10**9+7
# num_split = 0

n,m = map(int, input().split())
in_degree = [0] * n
in_G = [[] for _ in range(n)]
out_edge = [-1] * n
for _ in range(m):
    u,v = map(int, input().split())
    u,v = u-1,v-1
    in_degree[v] += 1
    in_G[v].append(u)
    out_edge[u] = v

def find_circle_nodes(in_degree):
    """ 识别图中的环 """
    in_degree = in_degree[:]        # copy
    nodes = set(); tmp = deque([])
    for i,x in enumerate(in_degree):
        if x==0: tmp.append(i)
        else: nodes.add(i)
    while tmp:
        u = tmp.popleft()
        if out_edge[u] in nodes:
            in_degree[out_edge[u]] -= 1
            if in_degree[out_edge[u]] == 0:
                tmp.append(out_edge[u])
                nodes.remove(out_edge[u])
    return nodes
circle_nodes_set = find_circle_nodes(in_degree)

def find_circle(x):
    """ 找到这个环 """
    s = set([])
    fa = {}
    while x not in s:
        s.add(x)
        fa[out_edge[x]] = x
        x = out_edge[x]
    return s, fa
# def dfs(x:int, fa:int=None) -> int:
#     """ 计算该支链(树结构)的长度 
#     返回: 该分支的方案数 (包括了空)
#     """
#     ans = 1
#     for y in in_G[x]:
#         if y == fa: continue
#         ans = (ans * dfs(y, x)) % MOD
#     ans += 1    # 选择当前节点
#     return ans
# def process_circle(x):
#     """ 处理单个环
#     返回: 该环的方案数 (包括了空), 该环的节点set 
#     FIXME: 这里其实可以看成是一个大的root! 然后逻辑跟下面的 dfs_tree 是一样的
#     """
#     s, fa = find_circle(x)
#     # 遍历每个节点, 计算支链长度
#     ans = 1
#     num_link_nodes = 0
#     for x,f in fa.items():
#         if len(in_G[x])==1: continue
#         num_link_nodes += 1
#         ans = (ans * dfs(x, f)) % MOD
#     if num_link_nodes == 0:
#         ans = 2
#     return ans, s

def dfs_tree(x:int) -> int:
    """ 计算该树结构上的方案数
    返回: 该树结构的方案数 (包括了空)
    """
    ans = 1
    for y in in_G[x]:
        # 遍历子树之间的组合, 包括了空!
        ans = (ans * dfs_tree(y)) % MOD
    ans += 1    # 选择当前节点, 即整个子树
    return ans

# 主循环. 先处理环结构, 再处理树结构
ans = 1
while circle_nodes_set:
    # num_split += 1
    x = circle_nodes_set.pop()
    a_, s_ = process_circle(x)
    ans = (ans * a_) % MOD
    circle_nodes_set -= s_
# 其他节点的出度为0
other_roots = [i for i,x in enumerate(out_edge) if x==-1]
# num_split += len(other_roots)
for x in other_roots:
    ans = (ans * dfs_tree(x)) % MOD

ans = (ans-1) % MOD
print(ans)
