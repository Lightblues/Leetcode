""" 
#P1710. 2024.3.17-小红书-第二题-推荐算法
https://codefun2000.com/p/P1710
"""
from collections import defaultdict
n,q = map(int, input().split())
keywords = set(input().split())
num2list = defaultdict(list)
for _ in range(n):
    name, _ = input().split()
    keys = set(input().split())
    num_inter = len(keywords & keys)
    num2list[num_inter].append(name)
for num in sorted(num2list.keys(), reverse=True):
    for name in num2list[num]:
        print(name)

