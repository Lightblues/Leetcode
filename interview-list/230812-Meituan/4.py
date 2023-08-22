""" 给定一棵树, 问最多有多少组相邻节点, 他们的乘积是完全平方数, 节点不能复用
限制: n 1e5

定义 f(u,used) 表示该节点是否被father匹配情况下的答案
    若 used=True: return sum{ f(c,False) }
    若 used=False: sum{ f(c,False) }  的基础上, 若有的话选择可匹配的子节点
注意, 在树结构上, 二元组匹配 #贪心 即可
"""
import math
n = int(input())
vals = list(map(int, input().split()))
g = [[] for _ in range(n)]
for _ in range(n-1):
    u,v = map(int, input().split())
    u,v = u-1,v-1
    g[u].append(v); g[v].append(u)
# 
def f(u, fa, used):
    """ 写复杂了 """
    if fa!=-1 and len(g[u])==1:
        return 0
    if used:
        arr1 = []
        for c in g[u]:
            if c==fa: continue
            arr1.append(f(c, u, False))
        return sum(arr1)
    else:
        arr1 = []
        arr2 = []   # 看能否匹配
        for c in g[u]:
            if c==fa: continue
            arr1.append(f(c, u, False))
            x = vals[c]*vals[u]
            flag = (int(math.sqrt(x)) ** 2) == x
            arr2.append(
                0 if not flag else 2 + f(c,u,True)
            )
        s = sum(arr1)
        diff = (a-b for a,b in zip(arr2, arr1))
        s += max(max(diff), 0)
        return s
# print(max(
#     f(0,-1,True), f(0,-1,False)
# ))
def f2(u, fa, used):
    """ 上面写复杂了! 贪心匹配即可 """
    ans = 0
    for c in g[u]:
        if c==fa: continue
        if not used:
            x = vals[c]*vals[u]
            flag = (int(math.sqrt(x)) ** 2) == x
            if flag:
                ans += 2 + f2(c, u, True)
                used = True
            else:
                ans += f2(c, u, False)
        else:
            ans += f2(c, u, False)
    return ans
print(f2(0,-1,False))
