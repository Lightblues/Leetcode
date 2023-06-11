""" 维修管道
需要修从位置1到位置N的一条水管, 从i到j的代价为 |i-j|
有N种不同的类型; 矩阵S表示兼容情况
限制: 无
思路: #Dijstra
    问题转化: 搜索从位置1到位置N的最短路径, 节点转移的代价为 |i-j|, 只有当节点类别 ti,tj 兼容的情况下才能进行转移
"""
N,K = map(int,input().split())
types = list(map(int,input().split()))
S = []
for _ in range(K):
    S.append(list(map(int,input().strip())))

import heapq
# (dist, idx)
q = [(0,0)]
visited = set([0])
while q:
    # 这里
    d, idx = heapq.heappop(q)
    if idx==N-1:
        print(d)
        exit()
    for j in range(N):
        ti,tj = types[idx]-1,types[j]-1
        if j not in visited and S[ti][tj]==1:
            # 这里
            heapq.heappush(q,(d + abs(idx-j), j))
            visited.add(j)
            # visited.add(i)
print(-1)
