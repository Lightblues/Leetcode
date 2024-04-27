""" 
有n天, 每天有若干选项, 问连续的两天选项不同的可能方案数. 
限制: n 1e5; len(arr[i]) <=20; 取模
思路1: #DP
    f[i][c] 表示第i天选择c的方案数量
    转移: 若第i天选项c存在, 则 sum{f[i-1][x] | x!=c}
2
ab
bcd
# 5
"""
MOD = 10**9+7
from string import ascii_lowercase
m = {c:i for i,c in enumerate(ascii_lowercase)}

n = int(input())
f = [0] * 26
options = input().strip()
options = set(m[i] for i in options)
for o in options:
    f[o] = 1
for _ in range(n-1):
    options = input().strip()
    options = set(m[i] for i in options)
    s = sum(f) % MOD
    nf = [0] * 26
    for o in options:
        nf[o] = s - f[o]
    f = nf
ans = sum(f) % MOD
print(ans)
