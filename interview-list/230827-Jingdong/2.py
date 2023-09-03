""" 左上角走到矩阵右下角. 有些房间有分数 1/-1, 魔法房间可以修改符号, 最后只有一个魔法房间. 问最大分数. 
* +1
# -1
M 改变符号

限制: m,n 1e3

思路: #DP
    记 f[i,j] -> 返回可以得到的最大/最小分数
"""
# from functools import lru_cache
# 加一个import
from math import inf
# set max recursion depth
# import sys
# sys.setrecursionlimit(1000000)

n,m = map(int, input().split())
mat = []
for _ in range(n):
    mat.append(list(input()))
# @lru_cache(None)
# def f(i,j):
#     # 修改这些行
#     mn,mx = inf,-inf
#     if i==0 and j==0:
#         mn,mx = 0,0
#     if i>0:
#         _mn,_mx = f(i-1,j)
#         mn = min(mn, _mn); mx = max(mx, _mx)
#     if j>0:
#         _mn,_mx = f(i,j-1)
#         mn = min(mn, _mn); mx = max(mx, _mx)
#     if mat[i][j] == "*":
#         return mn+1, mx+1
#     elif mat[i][j] == "#":
#         return mn-1, mx-1
#     elif mat[i][j] == ".":
#         return mn, mx
#     elif mat[i][j] == "M":
#         return -mx, -mn
# mn,mx = f(n-1,m-1)
# print(mx)

f = [(inf, -inf) for _ in range(m)] # 换成m
for i in range(n):
    nf = [(inf, -inf) for _ in range(m)]    # 换成m
    for j in range(m):
        mn,mx = inf,-inf
        if i==0 and j==0:
            mn,mx = 0,0
        if i>0:
            _mn,_mx = f[j]
            mn = min(mn, _mn); mx = max(mx, _mx)
        if j>0:
            _mn,_mx = nf[j-1]
            mn = min(mn, _mn); mx = max(mx, _mx)
        if mat[i][j] == "*":
            mn += 1; mx += 1
        elif mat[i][j] == "#":
            mn -= 1; mx -= 1
        elif mat[i][j] == ".":
            pass
        elif mat[i][j] == "M":
            mn, mx = -mx, -mn
        nf[j] = (mn, mx)
    f = nf

# 只用一个数组 f
f = [(inf, -inf) for _ in range(m)]
for i in range(n):
    for j in range(m):
        if i==j==0: 
            f[j] = (0,0)
            continue
        mn,mx = f[j]
        if j>0:
            _mn,_mx = f[j-1]
            mn = min(mn, _mn); mx = max(mx, _mx)
        if mat[i][j] == "*":
            mn += 1; mx += 1
        elif mat[i][j] == "#":
            mn -= 1; mx -= 1
        elif mat[i][j] == "M":
            mn, mx = -mx, -mn
        f[j] = (mn, mx)

result = f[m - 1]
print(result[1])

    
