from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-394
https://leetcode.cn/circle/discuss/kiOnsy/

T4 的图找最短路子图, 有点意思. 
Easonsi @2023 """
class Solution:
    """ 3120. 统计特殊字母的数量 I """
    def numberOfSpecialChars(self, word: str) -> int:
        ans = 0
        for i,j in zip(string.ascii_lowercase, string.ascii_uppercase):
            if i in word and j in word:
                ans += 1
        return ans
    
    """ 3121. 统计特殊字母的数量 II """
    def numberOfSpecialChars(self, word: str) -> int:
        ans = 0
        for i,j in zip(string.ascii_lowercase, string.ascii_uppercase):
            if i in word and j in word:
                if word.rindex(i) < word.index(j):
                    ans += 1
        return ans
    
    """ 3122. 使矩阵满足条件的最少操作次数
思路1: #DP
    f[i,t] 表示将 0...i 列满足条件, 且第 i 列的状态为 t 的最少操作次数
    返回: max{ f[n-1, ...] }
可以优化空间, 见 [ling](https://leetcode.cn/problems/minimum-number-of-operations-to-satisfy-conditions/solutions/2749283/ji-yi-hua-sou-suo-pythonjavacgo-by-endle-8i0e/)
    """
    def minimumOperations(self, grid: List[List[int]]) -> int:
        m,n = len(grid),len(grid[0])
        f = [[inf]*10 for _ in range(n)]
        cnt = Counter(grid[i][0] for i in range(m))
        for t in range(10):
            f[0][t] = m - cnt[t]
        for i in range(1,n):
            cnt = Counter(grid[j][i] for j in range(m))
            for t in range(10):
                mn = inf
                for s in range(10):
                    if s == t: continue
                    mn = min(mn, f[i-1][s] + m - cnt[t])
                f[i][t] = mn
        return min(f[-1])
    
    """ 3123. 最短路径中的边 #hard 可能有多条最短路. 求所有最短路中的边
限制: n, m 5e4
思路1 比较巧妙的 「记录父亲节点」的做法?
    如何找到最短路? 可以对于每个节点记录 fa, 然后从终点开始回溯
    如何找到所有路径? BFS之后, 根据 end节点的fa, 逆序找到所有路径! 
更常规的是 Dijkstra 最短路 + DFS/BFS 找边, 见 [ling](https://leetcode.cn/problems/find-edges-in-shortest-paths/solutions/2749274/dijkstra-zui-duan-lu-dfsbfs-zhao-bian-py-yf48/)
    """
    def findAnswer(self, n: int, edges: List[List[int]]) -> List[bool]:
        m = len(edges)
        g = [[] for _ in range(n)]
        edge2id = {}
        for i,(u,v,w) in enumerate(edges):
            g[u].append((v,w))
            g[v].append((u,w))
            edge2id[(u,v)] = i
            edge2id[(v,u)] = i
        dist = [-1] * n     # 记录从起点到每个点的距离
        # BFS
        dist[0] = 0
        q = [(0,0)]  # (dist, node) -- heapq
        vis = [False] * n
        fa = [set() for _ in range(n)]
        while q:
            d,v = heapq.heappop(q)
            if vis[v]: continue
            for u,w in g[v]:
                if dist[u] == -1 or dist[u] > d+w:
                    dist[u] = d+w
                    fa[u] = {v}
                    heapq.heappush(q, (d+w, u))
                elif dist[u] == d+w:
                    fa[u].add(v)
            vis[v] = True
        # 回溯
        ans = [False] * m
        if dist[n-1] == -1: return ans
        vis = set()
        q = [n-1]
        while q:
            v = q.pop()
            for u in fa[v]:
                if (u,v) in edge2id:
                    ans[edge2id[(u,v)]] = True
                if u not in vis:
                    vis.add(u)
                    q.append(u)
        return ans

    
sol = Solution()
result = [
    # sol.numberOfSpecialChars(word = "AbBCab"),
    # sol.minimumOperations(grid = [[1,0,2],[1,0,2]]),
    # sol.minimumOperations(grid = [[1,1,1],[0,0,0]]),
    sol.findAnswer(n = 6, edges = [[0,1,4],[0,2,1],[1,3,2],[1,4,3],[1,5,1],[2,3,1],[3,5,3],[4,5,2]]),
    sol.findAnswer(n = 4, edges = [[2,0,1],[0,1,1],[0,3,4],[3,2,2]]),
]
for r in result:
    print(r)
