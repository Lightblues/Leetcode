""" 
有线性n个关卡, m种宝石. 每一关为 Boss/Merchant, Boss掉落某种宝石, Merchant 花前购买宝石. 随身只能携带一个宝石. 问最优解. 
限制: n,m 1e6

5 2
b 1
b 2
m 1 10
m 2 20
m 2 30
# 30

思路1: #记忆化 搜索
    TLE 20%??
"""
# set recursion limit
import sys
sys.setrecursionlimit(1000000)
from functools import cache
n,m = map(int, input().split())
arr  = []
for _ in range(n):
    line = input().strip()
    if line.startswith('b'):
        iid = int(line[2:])
        arr.append((0, iid))
    else:
        iid, v = map(int, line[2:].split())
        arr.append((iid, v))
ans = 0
@cache
def dfs(i=0, x=0, s=tuple()):
    global ans
    ans = max(ans, x)
    if i==n: return 
    iid,v = arr[i]
    ss = set(s)
    if iid==0:
        ss.add(v)
        dfs(i+1, x, tuple(ss))
    else:
        if iid in ss:
            dfs(i+1, x+v, tuple())
        dfs(i+1, x, tuple(ss))
dfs()
print(ans)
