""" 
https://codeforces.com/contest/1701
"""
t = int(input())
for i in range(t):
    s = 0
    s += sum(map(int, input().split()))
    s += sum(map(int, input().split()))
    if s==0: print(0)
    elif s==4: print(2)
    else: print(1)