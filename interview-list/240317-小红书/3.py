""" 
#P1711. 2024.3.17-小红书-第三题-塔子哥的题解
https://codefun2000.com/p/P1711
from https://mp.weixin.qq.com/s/e8dq30_u_SogkEMgizIM3Q
"""

def ksm(a, b):
        res = 1
        while b:
                if b & 1:
                        res = res * a % mod
                a = a * a % mod
                b >>= 1
        return res
n = int(input())
a = list(map(int, input().split()))
cnt = sum([x%2 for x in a])
mod = 10**9+7
dp = [0] * (n+1)
for i in range(n):
        p = (n-i) * ksm(n, mod-2) % mod
        dp[i+1] = ( p + (1-p+mod) * dp[i] ) % mod * ksm(p, mod-2) % mod
for i in range(1, n+1):
        dp[i] += dp[i-1]
ans = (sum(a) + dp[n] - dp[cnt-1] +mod)% mod
print(ans)
