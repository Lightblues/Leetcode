""" 
给定 x,y, 从数组A中选择一定的数字, 使得乘以x得到的数字大于y
"""
x,y = map(int, input().split())
n = int(input())
arr = list(map(int, input().split()))

arr = sorted(set(arr), reverse=True)
ans = 0
for i,a in enumerate(arr):
    if x>=y: break
    x *= a
    ans += 1
if x<y: print(-1)
else: print(ans)
    