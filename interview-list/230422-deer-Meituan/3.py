""" 种田游戏, 要求只有一块田的限制下收益最大
n中作物, m天总时间. 每种植物有 (成熟天数 ti, 买入价 ai, 卖出价格 bi)
限制: m 2e3; n 1e5
思路1: #背包 问题
    注意, 本题对于相同成熟周期的只需要保留收益最大的一个即可
    定义 f[x] 表示限制在x天情况下的最大收益
    转移: f[x] = max{ f[x-ti] + bi-ai }, 再和 f[x-1] 的最大值

"""
n,m = map(int, input().strip().split())
tt = list(map(int, input().strip().split()))
aa = list(map(int, input().strip().split()))
bb = list(map(int, input().strip().split()))
from collections import defaultdict
t2mx = defaultdict(int)
for t,a,b in zip(tt,aa,bb):
    t2mx[t] = max(t2mx[t], b-a)
plants = list(t2mx.items())
plants.sort()
f = [0]*(m+1)
for i in range(1,m+1):
    mx = f[i-1]
    for t,mxv in plants:
        if t>i: break
        mx = max(mx, f[i-t]+mxv)
    f[i] = mx
print(f[m])