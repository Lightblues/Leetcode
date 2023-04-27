
""" 

思路1: #DP 记 f[i,j] 表示是否为回文串, 累计所有的 f[i,j] 即为答案
    递推公式: f[i,j] = f[i+1,j-1] and s[i] == s[j]
 """

from functools import cache
def count(s: str)->int:
    n = len(s)
    @cache
    def f(i,j):
        if i >= j: return True
        return f(i+1,j-1) and s[i] == s[j]
    return sum(f(i,j) for i in range(n) for j in range(i,n))

print(count('abbc')) # 3





