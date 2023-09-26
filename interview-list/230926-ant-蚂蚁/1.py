""" 对于一个长为n的序列, 从中挑选两次长度为m的子序列, 要求最大和! 
思路1: 左右前缀最大! 
    但这里的 left/right 注意计算时候的边界问题!
"""
from itertools import accumulate
n,m = map(int, input().split())
arr = list(map(int, input().split()))
acc = list(accumulate(arr, initial=0))
left = [0] * (n+1)
right = [0] * (n+1)
tmp = 0
for i in range(m,n+1):
    t = acc[i] - acc[i-m]
    tmp = max(tmp, t)
    # left[i-1] = tmp
    left[i] = tmp
tmp = 0
for j in range(n-m,-1,-1):
    t = acc[j+m] - acc[j]
    tmp = max(tmp, t)
    right[j] = tmp
ans = max(i+j for i,j in zip(left,right))
print(ans)















