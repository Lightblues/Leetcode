""" 
对于一棵树, 相同奇偶性节点之间构成联通块.
对于每个节点计算, 计算其子树包含的不同的联通块. 求和
限制 n 1e5

f(i) -> 返回该节点结果, 有: 
    1 + sum{ f(c) - (0 if child奇偶不同 else 1) }
"""
# set max recursion depth
import sys
sys.setrecursionlimit(1000000)
n,k = map(int, input().split())
tree = [[] for _ in range(n)]
for _ in range(n-1):
    u,v = map(int, input().split())
    u -= 1
    v -= 1
    tree[u].append(v)
    tree[v].append(u)
ans = 0
def f(u, fa):
    global ans
    acc = 1
    for v in tree[u]:
        if v!=fa:
            if (u-v) % 2:
                acc += f(v,u)
            else:
                acc += f(v, u) - 1
    ans += acc
    return acc
f(k-1, -1)
print(ans)
