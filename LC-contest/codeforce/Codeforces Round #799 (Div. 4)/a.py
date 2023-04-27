""" 

https://codeforces.com/contest/1692/problem/A
"""

n = int(input())
for _ in range(n):
    a, *other = map(int, input().split())
    print(sum(i>a for i in other))

