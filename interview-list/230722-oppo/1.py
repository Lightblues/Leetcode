""" 
给定 x,y, 从数组A中选择一定的数字, 使得乘以x得到的数字大于y
"""
x,y = map(int, input().split())
n = int(input())
a = list(map(int, input().split()))
a = sorted(set(a), reverse=True)
ans = 0
idx = 0
while idx<(len(a)) and x<y:
    x *= a[idx]
    idx += 1
    ans += 1
if x<y: print(-1)
else: print(ans)
    