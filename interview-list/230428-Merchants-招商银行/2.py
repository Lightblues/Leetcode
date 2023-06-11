""" 
对于一个数组, 我们要计算T的值为它们以权重 [1,2...n] 之和的最小值. 
对于Q次将i位置改为x的操作, 输出T值
限制: n 1e5; 数值 1e8; Q 1e5

5
1 10 3 4 6
3
2 1
2 4
4 6
# 32
# 43
# 57

思路1: 
    显然, T值是对于排序结果 [a1,...,an] 分别赋权 w[n,n-1,...1]之和. 
    现在将ai替换为x, T - ai * w[i]
    (假设x>ai) 然后将x插入数组中, 假设插入位置为j, 则 a[i+1...j] 的元素发生左移, 权重都 +1
"""
from itertools import accumulate
from bisect import bisect_right
n = int(input())
arr = list(map(int, input().split()))
tmp = [(x,i) for i,x in enumerate(arr)]
tmp.sort()
sarr = [x for x,_ in tmp]
# 旧版本中没有这个语法
# sacc = list(accumulate(sarr, initial=0))
sacc = [0] + list(accumulate(sarr))
idxMap = {raw:i for i,(_,raw) in enumerate(tmp)}
factor = list(range(n, 0, -1))
T = sum([a*f for a,f in zip(sarr,factor)])

def f(idx, x):
    i = idxMap[idx]
    ans = T
    if sarr[i]==x: return ans
    if sarr[i]<x:
        ans -= sarr[i] * factor[i]
        # [i+1...j-1]
        j = bisect_right(sarr, x)
        ans += sacc[j] - sacc[i+1]
        ans += factor[j-1] * x
    else:
        ans -= sarr[i] * factor[i]
        # [j...i-1]
        j = bisect_right(sarr, x)
        ans -= sacc[i] - sacc[j]
        ans += factor[j] * x
    return ans

Q = int(input())
for _ in range(Q):
    i,x = map(int, input().split())
    ans = f(i-1, x)
    print(ans)
