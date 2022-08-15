from typing import List
from collections import defaultdict

class Solution:
    """ 1192. 查找集群内的「关键连接」 `hard`

输入：n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
输出：[[1,3]]
解释：[[3,1]] 也是正确的。

from [here](https://leetcode-cn.com/problems/critical-connections-in-a-network/solution/cpython3-tarjansuan-fa-zhao-qiao-by-qrhq-vp6i/)
tarjan算法找桥 (连通分量之间的连接边 / 桥)
 """
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        # 无向图
        adjvex = defaultdict(set)
        for x, y in connections:
            adjvex[x].add(y)
            adjvex[y].add(x)
        

        dfn = [0 for _ in range(n)]    #dfs访问中的实际时间
        low = [0 for _ in range(n)]    #dfs中通过无向边可以向前回溯到的最早的时间点
        self.T = 1

        def tarjan(x: int, parent: int) -> None:
            dfn[x] = self.T
            low[x] = self.T
            self.T += 1

            for y in adjvex[x]:
                if y == parent:                 #可能是父节点
                    continue

                if dfn[y] == 0:                #还没访问过
                    tarjan(y, x)                #先访问y，访问了才能计算
                    low[x] = min(low[x], low[y])

                    # 在本题中, 「关键连接」记为所有的 联通分量 之间的边
                    if low[y] > dfn[x]:         #x 和 y不在一个强连通分量
                        res.append([x, y])
                
                elif dfn[y] != 0:              #访问过了
                    low[x] = min(low[x], dfn[y])
        
        res = []
        tarjan(0, -1)
        return res

    """ 1568. 使陆地分离的最少天数 #hard #题型
给定一个 grid, 1表示陆地, 0表示水域, 只有一个岛屿则认为是连在一起的陆地, 否则就是分离的多个岛屿. 现在要求你将陆地分离, 将陆地分离成至少两个不相交的区域, 返回最少操作数.
限制: grid 长宽 30
提示: 观察可知, 结果只能是 0,1,2.  因为对于一块陆地, 必然可以通过分割其角落的两个点分离角落的陆地.
思路1: #分类 讨论. 用DFS来计算 #连通分量
    根据提示, 只需要判断 0/1 的情况即可, 否则为2.
    为此, 实现一个 `count` 函数记录当前状态下的联通分量数量. 一开始就超过一个分量则返回0; 否则尝试将每一块陆地变为海洋, 重新count, 若某一块可以将陆地分割, 则返回1; 否则返回2.
    复杂度: O(m^2 n^2) 每次计算联通分量 mn; 陆地数量 mn.
    from [official](https://leetcode-cn.com/problems/minimum-number-of-days-to-disconnect-island/solution/shi-lu-di-fen-chi-de-zui-shao-tian-shu-by-leetcode/)
思路2: #Tarjan 算法找割点
    如果我们将每一块陆地看成无向图中的一个节点，每一组相邻的陆地之间连接一条无向边，那么得到的图 G：
    - 如果图 G 中没有节点，那么答案为 0；
    - 如果连通分量个数大于 1，那么说明陆地已经分离，答案为 0；
    - 如果连通分量个数为 1：
        - 如果图 G 中仅有一个节点，那么答案为 1；
        - 如果图 G 中存在割点，那么将割点对应的陆地变成水，就可以使得陆地分离，答案为 1；
        - 如果图 G 中不存在割点，那么答案为 2。
 """
    def minDays(self, grid: List[List[int]]) -> int:
        # 思路1: #分类 讨论. 用DFS来计算 #连通分量
        def dfs(x: int, y: int):
            grid[x][y] = 2
            for tx, ty in [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]:
                if 0 <= tx < n and 0 <= ty < m and grid[tx][ty] == 1:
                    dfs(tx, ty)
        def count():
            # 计算当前状态下的联通分量数量. 利用 DFS 实现, 方便起见对于搜索过的路径原地修改数值为2.
            cnt = 0
            for i in range(n):
                for j in range(m):
                    if grid[i][j] == 1:
                        cnt += 1
                        dfs(i, j)
            # 还原
            for i in range(n):
                for j in range(m):
                    if grid[i][j] == 2:
                        grid[i][j] = 1
            return cnt
        
        n, m = len(grid), len(grid[0])
        
        # 岛屿数量不为 1，陆地已经分离
        if count() != 1:
            return 0
        
        for i in range(n):
            for j in range(m):
                if grid[i][j]:
                    grid[i][j] = 0
                    if count() != 1:
                        # 更改一个陆地单元为水单元后陆地分离
                        return 1
                    grid[i][j] = 1
        
        return 2

    def minDays2(self, grid: List[List[int]]) -> int:
        # 思路2: Tarjan 算法找割点
        def getCuttingVertex(u: int, parent: int, ans: List[int]) -> None:
            nonlocal timestamp
            low[u] = dfn[u] = timestamp
            timestamp += 1
            fa[u] = parent
            child = 0
            iscv = False
            for v in edges[u]:
                # if v == parent:
                #     continue
                if dfn[v] == -1:
                    child += 1
                    getCuttingVertex(v, u, ans)
                    low[u] = min(low[u], low[v])
                    # 判断割点! 如果回溯到根顶点后，还有未访问过的顶点，需要在邻接顶点上再次进行DFS，根顶点就是割点
                    if not iscv and parent!=-1 and low[v] >= dfn[u]:
                        iscv = True
                        ans.append([u, v])
                elif v != parent:
                    low[u] = min(low[u], dfn[v])
            # 根节点为割点
            if not iscv and parent==-1 and child>=2:
                ans.append(u)

        def check():
            cvs = [] # cutting vertex 存储割点
            cccnt = 0 # connected components count 存储连通分量个数
            for i in range(nnodes):
                if dfn[i] == -1:
                    getCuttingVertex(i, -1, cvs)
                    cccnt += 1
            if cccnt > 1:
                return 0
            if cvs:
                return 1
            return 2

        # 构图
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        m,n = len(grid), len(grid[0])
        landCount = 0 # 陆地点数量
        # 节点重标号 (仅编号陆地单元)
        relabel = {}
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    relabel[i*n+j] = landCount
                    landCount += 1
        if not landCount:
            return 0
        if landCount==1:
            return 1
        
        # 添加图中的边
        edges = [[] for _ in range(landCount)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    for dx,dy in directions:
                        x,y = i+dx, j+dy
                        if 0<=x<m and 0<=y<n and grid[x][y] == 1:
                            edges[relabel[i*n+j]].append(relabel[x*n+y])
        nnodes = landCount
        low = [-1] * nnodes
        dfn = [-1] * nnodes
        fa = [-1] * nnodes
        timestamp = 0
        return check()

sol = Solution()
res = [
    sol.minDays2(grid =[[1,1,0,1,1],
                        [1,1,1,1,1],
                        [1,1,0,1,1],
                        [1,1,1,1,1]])
]
for r in res:
    print(r)