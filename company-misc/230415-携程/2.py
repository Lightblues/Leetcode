""" 
对于t次查询, 将n分解成两个数字a,b之和, 使得 lcm(a,b) 最大, 最小公倍数
限制: t 1e5; n 1e13
思路1: #贪心 
    显然a,b尽可能接近的时候, 并且gcd(a,b)=1时, lcm(a,b)最大
    暴力检查
"""
import math
t = int(input())
def f(n):
    # tt = int(math.sqrt(n))
    tt = n//2
    mx = 1; ans = (1,n-1)
    for a in range(tt, 0,-1):
        b = n-a
        g = math.gcd(a,b)
        tmp = a*b//g
        if tmp>mx:
            mx = tmp
            ans = (a,b)
        if g==1: break
    return ans
for _ in range(t):
    n = int(input())
    a,b = f(n)
    print(" ".join(map(str, [a,b])))
