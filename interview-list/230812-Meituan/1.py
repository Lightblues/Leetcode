""" 检查是否相邻
"""

n = int(input())
arr = list(map(int, input().split()))
a,b = map(int, input().split())
if abs(arr.index(a)-arr.index(b)) == 1:
    print('Yes')
else:
    print('No')