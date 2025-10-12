""" 
有k个骰子, 每轮投掷全部, 计算和, 问总点数为p的概率. 
将结果对 1e9+7 取模
限制: k,p 1e3

思路1: #DP
    首先, 计算一次投出某一数值的概率, 记 f[i,j] 表示i个骰子投出j的概率, 则有
        f[i,j] = 1/6 * f[i-1,j-1] + 1/6 * f[i-1,j-2] + ... + 1/6 * f[i-1,j-6]
        边界: f[i,i] = 1/6**i
    然后只需要上一轮得到的最后一行, 也即 f[j] 表示投掷k个得到j的概率;
    再考虑多次累计得到x的概率, 有递推
        g[x] = sum{ f[j] * g[x-j], 其中 j = k...x-1 } + f[x]

5 5
> 答案是 1 / 6^5
490869345

1 3
> 分别可能投掷 1/2/3 次, 总概率为 1/6 + 2/6**2 + 1/6**3
893518525

8 927
> 
179918124
"""
import sys

MOD = 10**9 + 7

def inv(x):
    return pow(x, MOD-2, MOD)

INV_6 = inv(6)

k,p = map(int, sys.stdin.readline().split())

f = [0] + [INV_6] * 6 + [0] * (p-6)
for i in range(2,k+1):
    f_new = [0] * (p+1)
    for j in range(i, min(6*i,p)+1):
        for jj in range(j-1, j-7, -1):
            if jj <= 0: break
            f_new[j] += f[jj] * INV_6
            f_new[j] %= MOD
    f = f_new
# for x in f: # 检查
#     print(x * 6**k % MOD, end=" ")

g = [0] * (p+1)
for i in range(k, p+1):
    g[i] = f[i]
    for j in range(k, i):
        g[i] += g[i-j] * f[j]
        g[i] %= MOD
print(g[p])

""" 另一种写法: 第一个DP不计算分母
M = 10 ** 9 + 7
k, p = list(map(int, input().strip().split()))
dp = [[0] * (1 + k) for _ in range(1 + p)]
dp[0][0] = 1


for i in range(1, p + 1):
    for t in range(1, min(k + 1, i + 1)):
        for j in range(1,7):
            if i>=j:
                dp[i][t] = (dp[i][t]%M+dp[i - j][t - 1]%M)%M
            
MOD = 10**9+7
denom = pow(6, k, MOD)
inv_denom = pow(denom, MOD - 2, MOD)

dp2=[0]*(p+1)
dp2[0]=1
f=[0]*(p+1)
for s in range(k,p+1):
    f[s]=dp[s][k]*inv_denom%MOD
for i in range(1,p+1):
    val=0  
    for t in range(k,i+1):
        if f[t]==0:
            continue
        
        val=(val+f[t]*dp2[i-t])%MOD
    dp2[i]=val
print(dp2[p]) 
"""
