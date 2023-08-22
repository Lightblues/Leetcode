""" 给定一个环, 两点最小距离 """
n = int(input())
arr = list(map(int, input().split()))
a,b = map(int, input().split())
s = sum(arr)
a,b = sorted((a-1,b-1))
d1 = sum(arr[a:b])
ans = min(d1, s-d1)
print(ans)