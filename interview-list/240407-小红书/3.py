""" 
有n个数字, 都是 [1...m] 的数字, 并且知道相邻两个的大小关系, 问有多少种可能性. 
限制: n,m 2e3; 对结果取模
思路1: #DP
    记 f[i,x] 表示第i个数字为x的方案数量, 则有转移: 
        若 > 关系, 则 f[i,x] = sum{ f[i-1, 1...x-1] }, 反过来也是一样的 —— 前缀和来计算
        若 = 关系, 则 f[i,x] = f[i-1, x]
    边界: f[0, 1...m] = 1


4 3
<=>
# 5
"""
from itertools import accumulate
MOD = 10**9 + 7
n,m = map(int, input().split())
ops = input().strip()
f = [0] + [1] * (m)
acc = list(accumulate(f, initial=0))
acc = [i % MOD for i in acc]
acc.append(acc[-1])
for op in ops:
    nf = [0] * (m+1)
    if op == "<":
        for i in range(1,m+1):
            nf[i] = acc[i]
    elif op == ">":
        for i in range(1,m+1):
            nf[i] = (acc[-1] - acc[i+1]) % MOD
    else:
        nf = f
    acc = list(accumulate(nf, initial=0))
    acc = [i % MOD for i in acc]
    acc.append(acc[-1])
    f = nf
print(sum(f[1:m+1]) % MOD)
