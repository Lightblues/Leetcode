""" 
5
1 3 2 5 4
# 5 6 5 10 8
"""
n = int(input())
arr = list(map(int, input().split()))
mx = max(arr)
res = [mx] * n
for i,x in enumerate(arr):
    if 2*x > mx:
        res[i] = 2*x
print(" ".join(map(str, res)))