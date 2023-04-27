""" A. The Third Three Number Problem
给定一个数字n, 要求找到三个非负数a,b,c, 是的` a^b+b^c+c^a == n`
思路1: #归纳
    根据给的例子, 可以发现, 在每一bit中, 若三个数字中该比特为1的次数出现了0/3次则对结构不影响, 若出现了1/2次则在结果中计数两次.
    因此, 可知n必然为偶数, 并且是a,b,c三个数中, 所谓出现1/2次的比特位所代表数字的2倍.
    现在要求找出一种 a,b,c, 只需要将 n//2 的比特位分配到三个数字上即可, 一种简单的方法就是 `(n//2, 0, 0)`

https://codeforces.com/contest/1699/problem/A
"""
t = int(input())
for i in range(t):
    n = int(input())
    if n&1:
        print(-1); continue
    print(n//2, 0, 0)
    