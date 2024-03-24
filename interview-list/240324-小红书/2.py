""" 
5 8
1 2 3 4 10
# 2

从arr中选择最少的若干数字, 使得 sum(ai//2) == x, 其中最多可以选择一个为 ai 而非 ai//2
限制: n 1e2
思路1: DP
    记 f[i,s,flag] 表示是否用了特殊操作 (flag=0/1), 前i个数字得到和s的最小数量, 则有
    若 flag==0, 
        f[i,s,0] = min{ f[i-1,s,0], f[i-1,s-ai//2,0] }
    若 flag==1
        f[i,s,1] = min{ f[i-1,s,1], f[i-1,s-ai,0], f[i-1,s-ai//2,1] }
    若非法, 计作 inf
"""
from math import inf
from functools import lru_cache
n,x = map(int, input().split())
arr = list(map(int, input().split()))
# arr.sort()
@lru_cache(None)
def f(i:int, s:int, flag:int):
    if i<0: return inf
    if s<0: return inf
    if s==0: 
        return 0
    if flag==0:
        return min(f(i-1,s,0), f(i-1,s-arr[i]//2,0)+1)
    else:
        return min(f(i-1,s,1), f(i-1,s-arr[i],0)+1, f(i-1,s-arr[i]//2,1)+1)
ans = min(f(n-1,x,1), f(n-1,x,0))
if ans==inf:
    print(-1)
else:
    print(ans)
