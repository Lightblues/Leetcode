""" 
对于一堆N个金币轮流拿, 遇到偶数可选择 取一半/1枚; 遇到奇数只能取 1枚. 问两个人最优结果.
限制: 对于 T 1e3 个查询; n 1e9
思路1: #数学 分类
    记 f(x) 表示A可以获得的数量
    显然, 对于奇数, 有 f(x) = 1 + (x-1) - f(x-1)
    对于偶数: 猜测的一个贪心策略是, 若 //2 是一个奇数, 则转移, 否则进行-2 (分配 1,1) 操作
"""
# set max iter
import sys
sys.setrecursionlimit(100000000)
from functools import cache
@cache
def f(x):
    if x<=0: return 0
    if x<=2: return 1
    # if x==4: return 3
    if x%2: return x-f(x-1)
    else:
        # if (x//2)%2: return x//2 + f(x//2-1)
        # else: return 1 + f(x-2)
        return max(
            x - f(x//2), 1 + f(x-2)
        )

t = int(input())
for _ in range(t):
    n = int(input())
    a = f(n)
    print(a, n-a)
