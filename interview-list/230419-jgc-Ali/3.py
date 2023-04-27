""" 姜国超 阿里 230419
统计所有长度为n的小写字符串中, 逆序对的数量. 限制: n 1e12; 对结果取模
思路1: #数学
    对于长度为n的所有字符串, 考虑b作为较大元素的数量, ...
只通过了 5%?
"""

def exgcd(a, b):
    if b == 0:
        x = 1
        y = 0
        return x, y
    x1, y1 = exgcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return x, y

mod = 10 ** 9 + 7
n = int(input())
fac = (1+25) * 25 // 2 
base = 26
# a = (1 - pow(base, n-1, mod)) // (1-base)
invBase = exgcd(1-base, mod)[0]
a = (1 - pow(base, n-1, mod)) * invBase % mod

ans = a * fac % mod
print(ans)
