""" 对一个矩形切成两块, 求两部分和之差的最小值
限制: n,m 1e3
"""
n,m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]

def f(arr):
    """ 找到一个序列的最优分割 """
    s = sum(arr)
    acc = 0
    ans = s
    for i,x in enumerate(arr):
        acc += x
        ans = min(ans, abs(s-2*acc))
    return ans

srows = [sum(r) for r in arr]
scols = [sum(c) for c in zip(*arr)]
print(min(f(srows), f(scols)))