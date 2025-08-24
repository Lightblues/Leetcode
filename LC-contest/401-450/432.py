from typing import *
import math
import bisect

""" 
https://leetcode.cn/contest/weekly-contest-432

Easonsi @2025 """
class Solution:
    """ 3417. 跳过交替单元格的之字形遍历 """
    def zigzagTraversal(self, grid: List[List[int]]) -> List[int]:
        m,n = len(grid),len(grid[0])
        ans = []
        flag = 0
        for i in range(m):
            line = grid[i]
            if i%2:
                line = line[::-1]
            ans += line[flag::2]
            if n%2:
                flag = 1-flag
        return ans
    
    """ 3418. 机器人可以获得的最大金币数 从 (0,0) 到 (m,n), 只能往右往下, 计算累计分数, 但最多可以避免两次负分, 求最大收益
思路1: #DP 很标准DP思路, 设 f[i,j,k] 表示到达 (i,j) 并且至多跳过k次的最大收益
    可以实用递推
    注意哨兵和边界的使用
    """
    def maximumAmount(self, coins: List[List[int]]) -> int:
        m,n = len(coins),len(coins[0])
        f = [[[-math.inf]*3 for _ in range(n+1)] for _ in range(m+1)]
        f[1][0] = [0,0,0]  # 注意这里的边界!
        for i,line in enumerate(coins):
            for j,v in enumerate(line):
                f[i+1][j+1][0] = max(f[i][j+1][0], f[i+1][j][0]) + v
                f[i+1][j+1][1] = max(f[i][j+1][1]+v, f[i+1][j][1]+v, f[i][j+1][0], f[i+1][j][0])
                f[i+1][j+1][2] = max(f[i][j+1][2]+v, f[i+1][j][2]+v, f[i][j+1][1], f[i+1][j][1])
        return f[m][n][2]
    
    """ 3419. 图的最大边权的最小值 #medium 给定一个有向带权图, 可以删除一些边, 使得 1) 所有节点都能到0; 2) 所有节点的出度最大为th. 问最终得到的图中, 最大边权的最小值 min(max(v)) 
限制: 无法到达0的话返回-1. a->b 之间可能多有条边; n 1e5
#反向 转化问题: 我们将边翻转, 则 "连通性" 要求等价于从0出发 #DFS 一棵树到达所有点
    注意, 条件2 在这里是冗余的! 因为DFS中每个节点只有一个入度!
思路1: #二分图 + 反向 DFS
    复杂度: O(n log(X)) 其中X为边权范围
思路2: #Dijkstra 
    想一下, Dijkstra算法解决什么问题? 从一点出发到其他所有点的最短距离
    如何应用到本题? 1) 每个点的 "距离" 定义为 max(边权); 2) 每次选择 "距离" 最小的点进行扩展
    复杂度: O(n logn)
https://leetcode.cn/problems/minimize-the-maximum-edge-weight-of-graph/solutions/3045060/liang-chong-fang-fa-er-fen-da-an-dijkstr-eb7d/
    """
    def minMaxWeight(self, n: int, edges: List[List[int]], threshold: int) -> int:
        mx = 0; g = [[] for _ in range(n)]
        for u,v,w in edges:
            g[v].append((u,w))
            mx = max(mx, w)

        def check(limit:int):
            vis = [False]*n
            def dfs(u:int):
                vis[u] = True
                for v,w in g[u]:
                    if not vis[v] and w <= limit:
                        dfs(v)
            dfs(0)
            return all(vis)
        
        ans = bisect.bisect_left(range(mx+1), True, 1, key=check)
        return ans if ans <= mx else -1
    
    """ 3420. 统计 K 次操作以内得到非递减子数组的数目 #hard 给定一个长n的数组和限制操作数k. 问所有的子数组中, 在k次+1操作内能变为 "非递减" 的子数组的数目
限制: n 1e5; k 1e9
思路1: 
https://leetcode.cn/problems/count-non-decreasing-subarrays-after-k-operations/solutions/3045053/on-xian-xing-zuo-fa-dan-diao-zhan-di-qia-ay5b/
    """

sol = Solution()
result = [
    # sol.zigzagTraversal(grid = [[1,2],[3,4]]),
    # sol.zigzagTraversal(grid = [[1,2,3],[4,5,6],[7,8,9]]),
    # sol.maximumAmount(coins = [[0,1,-1],[1,-2,3],[2,-3,4]]),
    sol.minMaxWeight(n = 5, edges = [[1,0,1],[2,0,2],[3,0,1],[4,3,1],[2,1,1]], threshold = 2),
    sol.minMaxWeight(n = 5, edges = [[0,1,1],[0,2,2],[0,3,1],[0,4,1],[1,2,1],[1,4,1]], threshold = 1),
]
for r in result:
    print(r)
