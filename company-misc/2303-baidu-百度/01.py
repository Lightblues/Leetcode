
""" 删除游戏
对于一组数字, 每次选择一个x获得分数, 然后数组中的所有 x-1,x+1 都会被去除. 可以获得的最大分数. 
限制: n 1e5; 数字 1e5
思路1: #DP 
    对于arr排序计数 (x,c); 转换
    记 f[i] 表示前i个数字, 取到i能获得的最大分数. g[i] 表示前i个数字, 能获得的最大分数.
    递推 f[i] = x*c + g[i-1] or g[i-2] 其中当两个数字相邻时只能选择 g[i-2]
    g[i] = max(f[i], g[i-1])
"""
from collections import Counter
n = int(input())
arr = list(map(int, input().split()))

cnt = Counter(arr)
arr = sorted(cnt.items())
nn = len(arr)
f = [0] * (nn)
g = [0] * (nn)
f[0] = g[0] = arr[0][0] * arr[0][1]
for i in range(1, nn):
    x,c = arr[i]
    if x!=arr[i-1][0]+1:
        f[i] = x*c + g[i-1]
    else:
        f[i] = x*c + g[i-2] if i>1 else x*c
    g[i] = max(f[i], g[i-1])
print(g[-1])

