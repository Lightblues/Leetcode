""" 给定两个递增序列, 从两个数组中分别取一个数字相加, 问得到最大的k个数字
限制: k <= 2n. 要求复杂度 O(klogk)
"""
n,k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

import heapq
ans = []
h = []
for aa in a:
    h.append((-aa-b[-1], aa, n-1))
heapq.heapify(h)
for _ in range(k):
    mx, aa, i = heapq.heappop(h)
    ans.append(-mx)
    if i > 0:
        heapq.heappush(h, (-aa-b[i-1], aa, i-1))
print(" ".join(map(str, ans)))