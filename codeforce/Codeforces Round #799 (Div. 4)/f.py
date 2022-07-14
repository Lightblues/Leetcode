#!/usr/bin/Python3
# 发放  coding=utf-8

""" 
F. 3SUM
给定一个数组, 若存在三个下标 i,j,k 使得三个数之和的个位数为 3, 则返回Yes.
约束: 线性复杂度
思路: 先枚举所有可以得到3的组合, 判断是否在其中即可.
"""
from collections import Counter
patterns = []
for i in range(10):
    for j in range(i, 10):
        for k in range(j, 10):
            if (i+j+k) % 10 == 3:
                patterns.append(Counter([i, j, k]))
def check(d: dict):
    for p in patterns:
        if all(d[k] >= p[k] for k in p):
            return True
    return False
def f():
    n = int(input())
    nums = map(int, input().split())
    d = Counter(a%10  for a in nums)
    print("YES" if check(d) else "NO")
    
for _ in range(int(input())):
    f()
