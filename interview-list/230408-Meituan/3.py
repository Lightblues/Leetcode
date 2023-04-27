""" 水果打包
需要对n个水果打包成若干. 每个包最多m个连续的水果; 打包一个果篮的成本是 k*floor(u+v/2)+s, k是水果数量, u,v 分别是篮子里的最大最小体积, s是参数
限制: n 1e4; m 1e3; s 1e4
思路1: DP
    记 f[i] 表示前i个水果打包的最小成本, 则 f[i] = min{ f[j] + cost(j+1, i)} 其中 j [i-m+1, i]
    #TLE 72% -> 81% (优化 max, min)
    复杂度: O(nm)
"""
n,m,s = map(int, input().split())
fruits = list(map(int, input().split()))

from math import inf
f = [0] + [inf] * n
for i in range(n):
    mn,mx = fruits[i],fruits[i]
    for j in range(i, max(-1, i-m), -1):
        if fruits[j]<mn: mn = fruits[j]
        if fruits[j]>mx: mx = fruits[j]
        new = f[j] + s + (i-j+1)*((mn+mx)//2)
        if new<f[i+1]: f[i+1] = new
print(f[-1])
