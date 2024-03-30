""" 
对于两个长度相等的字符串, 可以进行操作: 选择一个字符串, 将其前缀x个字符变为c. 问最少操作的次数 (和操作方式)
思路1: #贪心
    分别判断需要操作 0/1/2 的情况

aabc
abcc
# 2
# 2 3 b
# 2 2 a

"""
s = input().strip()
t = input().strip()
n = len(s)
while n>0 and s[n-1]==t[n-1]:
    n -= 1
if n==0:
    print(0)
    exit()
s,t = s[:n],t[:n]
if len(set(s)) == 1:
    print(1)
    print(f"2 {n} {s[0]}")
elif len(set(t)) == 1:
    print(1)
    print(f"1 {n} {t[0]}")
else:
    print(2)
    print(f"2 {n} a")
    print(f"1 {n} a")
