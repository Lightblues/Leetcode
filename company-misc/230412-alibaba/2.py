""" 
对于两个字符串, 将其中的字符看成节点, 对于相同字符之间连边. 问有多少可能的二分图. 对结果取模

不知道哪里错了? 只过了5%
"""
from collections import Counter
from math import perm
mod = 10**9 + 7
n = int(input())
s1 = input().strip()
s2 = input().strip()
c1,c2 = Counter(s1), Counter(s2)
ans = 1
for v,cc1 in c1.items():
    cc2 = c2[v]
    a,b = sorted([cc1,cc2])
    # 下面人循环 % 会快一些
    ans = (ans*perm(b,a))%mod
print(ans)
