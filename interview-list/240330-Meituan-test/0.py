""" 
IO 的方法

给定 n,m 求数组 n, \sqrt{n}, \sqrt\sqrt{n}... 前m项之和
"""
from math import sqrt
import sys
sys.setrecursionlimit(100000)

def f():
    n,m = map(int, input().split())
    ans = 0
    for i in range(m):
        ans += n
        n = sqrt(n)
    print(f"{ans:.2f}")


# while True:
#     try:
#         f()
#     except:
#         break

for line in sys.stdin:
    if line == '\n':
        break
    n,m = map(int, line.strip().split())
    ans = 0
    for i in range(m):
        ans += n
        n = sqrt(n)
    print(f"{ans:.2f}")