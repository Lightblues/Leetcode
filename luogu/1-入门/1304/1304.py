""" P1304 哥德巴赫猜想 
哥德巴赫猜想：任一大于 2 的偶数都可写成两个质数之和. 现在给定一个整数n, 写出 4,6,...n 的第一个因子最小的分解式 (例如10=3+7 而非 5+5).
"""
n = int(input())
primes = set([2])
for i in range(3, n):
    flag = True
    for p in primes:
        if i%p == 0:
            flag = False
            break
    if flag:
        primes.add(i)
ps = sorted(primes)
for i in range(4, n+1, 2):
    for p in ps:
        if i-p in primes:
            print(f"{i}={p}+{i-p}")
            break
