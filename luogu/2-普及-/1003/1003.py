""" P1003 [NOIP2011 提高组] 铺地毯 #普及-
"""

n = int(input())
record = [[0]*4 for _ in range(n)]
for i in range(n):
    record[i] = list(map(int, input().split()))
x,y = list(map(int, input().split()))
ans = -1
for i,(a,b,g,k) in enumerate(record):
    if a<=x<=a+g and b<=y<=b+k:
        ans = i+1
print(ans)
