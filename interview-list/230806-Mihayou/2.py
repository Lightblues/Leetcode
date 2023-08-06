""" 
一个队列的不同属性的法师, 有着不同的护盾值
    操作1: 对于某一个法师 -1, 消耗 1
    操作2: 消灭相邻的不同属性的发现 (-inf), 但要求这两个都存活! 需要消耗x
问最少消耗

思路1: DP #WA
    f[i] = min(f[i-1]+arr[i], f[i-2]+x)

f[i,0] 表示不用; f[i,1] 表示使用技能2
则有 f[i,0] = min{f[i-1, 0/1]} + arr[i]
    f[i,1] = min{f[i-2,0/2]} + x if (i-1,i)不同属性 else inf
"""
n,x = map(int, input().split())
arr = list(map(int, input().split()))
attr = list(input().strip())

# 错误的做法! 因为不能连续两个都用技能2
# f = [0] * n
# f[0] = arr[0]
# for i in range(1, n):
#     f[i] = f[i-1] + arr[i]
#     if attr[i]!=attr[i-1]:
#         f[i] = min(f[i], f[i-2]+x)
import math
f = [0] * n
g = [math.inf] * n
f[0] = arr[0]
g[0] = math.inf
for i in range(1,n):
    f[i] = min(f[i-1], g[i-1]) + arr[i]
    if attr[i]!=attr[i-1]:
        g[i] = x + (min(f[i-2], g[i-2]) if i>=2 else 0) # 注意这里也要取min
print(min(f[n-1], g[n-1]))

