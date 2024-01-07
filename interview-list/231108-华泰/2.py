""" 
大小为k的滑窗, 依次计算最大值. 
思路1: 利用堆, 记录时间戳
"""
import heapq

arr = list(map(int, input().split()))
k = int(input())
arr = [-i for i in arr]
h = []
ans = []
for i in range(k-1):
    heapq.heappush(h, (arr[i], i))
for i in range(k-1,len(arr)):
    heapq.heappush(h, (arr[i], i))
    while h[0][1] <= i-k:
        heapq.heappop(h)
    ans.append(-h[0][0])
print(ans)
