""" 对于红/白球, 要求排列长度为n, 并且不能有连续的红球, 问排列数量, 取模
思路1: DP
    记 f[i,0/1] 分别表示以白/红球结尾的长度为i的排列数量
    f[i,0] = f[i-1,0] + f[i-1,1]
    f[i,1] = f[i-1,0]
对于时间的要求好高!
"""
MOD = 10**9+7
# set max recursion depth
# import sys
# sys.setrecursionlimit(1000000)
# from functools import lru_cache
# @lru_cache(None)
# def f(i:int, x:int):
#     if i==1: return 1
#     if x==0: return (f(i-1,0) + f(i-1,1)) % MOD
#     else: return f(i-1,0)
    
n = int(input())
# f = [[0,0] for _ in range(n+1)]
f = [1,1]
for i in range(2,n+1):
    # f[i][0] = (f[i-1][0] + f[i-1][1]) % MOD
    # f[i][1] = f[i-1][0]
    f = [(f[0]+f[1])%MOD, f[0]]
ans = sum(f) % MOD
print(ans)
