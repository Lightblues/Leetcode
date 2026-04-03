from typing import *

"""
https://leetcode.cn/contest/weekly-contest-450
Easonsi @2025 """
class Solution:
    """  """
    def smallestIndex(self, nums: List[int]) -> int:
        for i, x in enumerate(nums):
            if sum(int(d) for d in str(x)) == i:
                return i
        return -1

    """ 0-1 BFS, 传送门代价为0, 普通移动代价为1
    贪心使用传送门: 在0-1 BFS中, 第一次到达某传送门时距离最小, 此时传送一定最优
    """
    def minMoves(self, matrix: List[str]) -> int:
        from collections import deque
        m, n = len(matrix), len(matrix[0])
        if matrix[0][0] == '#' or matrix[m-1][n-1] == '#':
            return -1
        if m == 1 and n == 1:
            return 0
        # 构建传送门映射
        portals = {}
        for i in range(m):
            for j in range(n):
                c = matrix[i][j]
                if c.isupper():
                    if c not in portals:
                        portals[c] = []
                    portals[c].append((i, j))

        dist = [[float('inf')] * n for _ in range(m)]
        dist[0][0] = 0
        dq = deque([(0, 0, 0)])  # (dist, row, col)
        used_portal = set()

        while dq:
            d, r, c = dq.popleft()
            if d > dist[r][c]:
                continue
            if r == m - 1 and c == n - 1:
                return d
            # 传送门: 代价0, 加入队首
            ch = matrix[r][c]
            if ch.isupper() and ch not in used_portal:
                used_portal.add(ch)
                for pr, pc in portals[ch]:
                    if (pr, pc) != (r, c) and d < dist[pr][pc]:
                        dist[pr][pc] = d
                        dq.appendleft((d, pr, pc))
            # 四方向移动: 代价1, 加入队尾
            for dr, dc in ((0,1),(0,-1),(1,0),(-1,0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] != '#' and d + 1 < dist[nr][nc]:
                    dist[nr][nc] = d + 1
                    dq.append((d + 1, nr, nc))
        return -1


    """ 树上三点Steiner树: 最小权重 = (d(s1,s2) + d(s1,d) + d(s2,d)) / 2
    用 LCA + 倍增 求树上两点距离
    """
    def minimumWeight(self, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        n = len(edges) + 1
        LOG = n.bit_length()
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        # BFS 建树, 求 depth 和 dist (到根的距离)
        depth = [0] * n
        dist = [0] * n
        parent = [[-1] * n for _ in range(LOG)]
        visited = [False] * n
        from collections import deque
        q = deque([0])
        visited[0] = True
        while q:
            u = q.popleft()
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    depth[v] = depth[u] + 1
                    dist[v] = dist[u] + w
                    parent[0][v] = u
                    q.append(v)

        # 倍增预处理
        for k in range(1, LOG):
            for v in range(n):
                p = parent[k-1][v]
                parent[k][v] = parent[k-1][p] if p != -1 else -1

        def lca(u, v):
            if depth[u] < depth[v]:
                u, v = v, u
            diff = depth[u] - depth[v]
            for k in range(LOG):
                if (diff >> k) & 1:
                    u = parent[k][u]
            if u == v:
                return u
            for k in range(LOG - 1, -1, -1):
                if parent[k][u] != parent[k][v]:
                    u = parent[k][u]
                    v = parent[k][v]
            return parent[0][u]

        def tree_dist(u, v):
            return dist[u] + dist[v] - 2 * dist[lca(u, v)]

        ans = []
        for s1, s2, d in queries:
            # Steiner tree of 3 nodes = (d(s1,s2) + d(s1,d) + d(s2,d)) / 2
            ans.append((tree_dist(s1, s2) + tree_dist(s1, d) + tree_dist(s2, d)) // 2)
        return ans

    def minSwaps(self, nums: List[int]) -> int:
        ds = lambda x: sum(int(d) for d in str(x))
        target = sorted(nums, key=lambda x: (ds(x), x))
        # 计算将 nums 变为 target 所需的最小交换次数
        # 即计算置换的环数，答案 = n - 环数
        pos = {v: i for i, v in enumerate(nums)}
        visited = [False] * len(nums)
        cycles = 0
        for i in range(len(nums)):
            if visited[i] or nums[i] == target[i]:
                if not visited[i]:
                    visited[i] = True
                    cycles += 1
                continue
            # 遍历环
            j = i
            while not visited[j]:
                visited[j] = True
                # target[j] 应该放在位置 j，它当前在 pos[target[j]]
                j = pos[target[j]]
            cycles += 1
        return len(nums) - cycles

sol = Solution()
result = [

]
for r in result:
    print(r)
