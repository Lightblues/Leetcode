""" 
定义「平衡字符串」表示仅仅包括两种字符并且出现次数相同的. 对于一个数组, 统计多少子序列是平衡的. 
限制: N 1e5 对结果取模
思路1: 分解+递推
    枚举所有 c/d 两个字符的匹配, 可以看成是 01 序列
    问题化简为枚举 01序列中出现平衡字符串的个数. 统计0/1出现的次数分别为 a,b
        每个字符有1个: C(a,1) * C(b,1), 有2个: C(a,2) * C(b,2), ...

5
ababc
# 9
"""
import sys
sys.setrecursionlimit(int(1e9))
# import math

# @lru_cache(None)
# def comb(n, k):
#     # return math.factorial(n) // math.factorial(k) // math.factorial(n-k)
#     if k==0 or k==n: return 1
#     return comb(n-1, k-1) + comb(n-1, k)

# from math import comb
import math
from functools import lru_cache
from collections import Counter
MOD = 10**9+7

n = int(input())
s = input().strip()
cnt = Counter(s)
cnt_list = list(cnt.values())

@lru_cache(None)
def comb(n, k):
    # return math.comb(n, k) % MOD
    if k==0 or k==n: return 1
    return (comb(n-1, k-1) + comb(n-1, k)) % MOD

@lru_cache(None)
def f(a,b):
    """ 对于出现次数分别为 a,b 的两种字符, 计算可能的数量 
    # NOTE: TTL
    """
    a,b = sorted((a,b))
    ans = 0
    # NOTE: 这里可以优化的, 因为 i -> i+1 可以推理计算出来! 
    for x in range(1, a+1):
        ans += comb(a,x) * comb(b,x)
        ans %= MOD
    return ans

ans = 0
for i,c in enumerate(cnt_list):
    for j in range(i+1, len(cnt_list)):
        d = cnt_list[j]
        ans = (ans + f(c, d)) % MOD
print(ans)