""" 
小红在整理自己小红书上发布的笔记时，会发现，每过一段时间，都会随机有一个笔记点赞数量加 1（每个笔记被点赞的概率是相同的）。
现在小红想知道，当第一次出现所有笔记点赞数量均为偶数时，所有笔记的总赞数之和的期望是多少？

Output:
一个整数，代表最终总赞数的期望对10^9+7取模的值。可以证明，最终的答案一定是个有理数，你只需要输出其对10^9+7取模的结果。
分数取模的定义：假设答案是x/y，那么其对p取模的答案是找到一个整数a满足a∈[0,p-1]且a*y对p取模等于x。

2
1 2
> output
6

思路1: #数学 #DP 
    显然, 有影响的只有数组中奇数数量, 不妨记作k
    记E[k]表示状态为k第一次到达状态0 (全为偶数) 的期望步骤数, 则有转移
        E[0] = 0
        E[k] = 1 + k/n * E[k] + (n-k)/n * E[k+1]
        E[n] = 1 + E[n-1]
        注意这里的边界条件! 其中的1是当前步骤
    未知数和方程数量相同, 理论上可解. 如何化简呢? 
    神来之笔是定义 d[k] = E[k] - E[k-1], 也即下一个状态的增量. 代入转移方程, 有
        d[k] = 1/k * [n + (n-k)d[k+1]]
        又因为 d[n] = 1, 可以反向递推得到所有, 直到 d[1].
    转换答案, 是 s + E[t], 其中s为初始数量, t为初始奇数数量
"""
import sys
MOD = 10**9 + 7

def pow(x, y, mod):
    # 快速幂, 直接用内置的也OK
    if y == 0: return 1
    while y > 0:
        if y % 2 == 1: return pow(x, y-1, mod) * x % mod
        x = x * x % mod
        y = y // 2
    return x

def inv(x):
    return pow(x, MOD-2, MOD)

n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))

s = sum(a)
t = sum(1 for num in a if num % 2 != 0)

# --- 下面的居然会 OOM???
# d = [0] * (n+1)
# d[n] = 1
# for k in range(n-1, 0, -1):
#     d[k] = inv(k) * (n + (n-k)*d[k+1])
# ans = s + sum(d[:t+1])
# print(ans % MOD)

# --- 改为从后向前计算，只保留当前值
current_d = 1
sum_d = 0
# 从n-1向下计算到1
for k in range(n-1, 0, -1):
    current_d = inv(k) * (n + (n-k)*current_d) % MOD
    if k <= t:
        sum_d = (sum_d + current_d) % MOD
ans = (s + sum_d) % MOD
print(ans)
