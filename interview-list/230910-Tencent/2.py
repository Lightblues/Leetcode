""" 
对于共n个柱子, 给定 first,last 的高度, 高度差距最多为1, 问可能的最大高度. 
"""

def f():
    n, first, last = map(int, input().split())
    if first>last:
        first, last = last, first
    if last - first > n-1:
        print(-1)
        return
    x = (last-first +n-1) // 2
    print(first+x)

n = int(input())
for _ in range(n):
    f()
