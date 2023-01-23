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
[灵神](https://leetcode.cn/problems/minimum-sideway-jumps/solution/cong-0-dao-1-de-0-1-bfspythonjavacgo-by-1m8z4/)

#0-1BFS. 适用只有0/1边权的图; 核心是双端队列
    一般, 图上求最短路径, 可以采用 #Dijkstra 算法求最短路径. 但复杂度超过了 O(n)
    在只有0/1边权的图上, 如何进行「图上的BFS」? 要求复杂度 O(n)
        对于树上的BFS (边权均为1), 可以采用 #队列 的方式进行BFS.
        那么在图上, 
            若边权均为1, 也可以正常利用 dis 来防止重复访问, 进行BFS. 
            若边权为0/1, 则需要利用 #双端队列 的方式进行BFS. 具体见下: 
    0-1BFS
        注意, 我们需要保证当前访问的节点的距离是最小的, 因此需要用到 #双端队列.
            维护的队列有一个性质, 队列中节点的距离是递增的, 并且同时只会出现 d,d+1 距离的节点
        从距离为d的x节点出发, 对于一条 x->y 的路径: 
            若边权为1, 并且 dis[y]>d+1, 则更新y的距离, 加入队尾.
            若边权为0, 并且 dis[y]>d, 则更新y的距离; 为了保证队列的递增, 需要加入队头!
    说明: 如果边权不止 0和1，把双端队列换成最小堆，就得到了 Dijkstra 算法。

== 
1368. 使网格图至少有一条有效路径的最小代价
2290. 到达角落需要移除障碍物的最小数目
1824. 最少侧跳次数 #medium 有三条跑道, 上面各有一些石头. 要从起点跑到终点, 仅能进行侧跳 (在相同的距离处, 从跑道i跳到跑道j). 要求最少侧跳次数.


Easonsi @2023 """
class Solution:
    """ 1368. 使网格图至少有一条有效路径的最小代价 #hard #题型 要从grid的左上走到右下. 每个格子初始化的方向是上下左右. 问最少修改多少格子, 使得路径有效. 限制: m,n 100
提示: 可以将每个网格看成图上的一个节点, 网格与四周相连, 根据方向是否一致设置权重 0/1. 则原问题等价于求 #最短路径.
思路1: 根据提示建图. 然后求最短路径, 可以用 #Dijsktra 算法等.
    复杂度: 节点数量 O(mn), 边数量 O(mn), 因此复杂度 O(mnlog(mn))
思路1.2 01BFS
    对于这里的特殊情况, 也可以用 「0-1 广度优先搜索」来搜索.
    修改之处在于: 遇到权重为 0 的邻居, 需要插入到队列的头部, 而不是尾部. 因此采用 #双端队列.
    复杂度: O(mn)
[official](https://leetcode.cn/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/solution/shi-wang-ge-tu-zhi-shao-you-yi-tiao-you-xiao-lu-2/)
"""
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        BIG = int(1e9)
        dist = [0] + [BIG] * (m * n - 1)
        seen = set()
        q = collections.deque([(0, 0)])

        while len(q) > 0:
            x, y = q.popleft()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            cur_pos = x * n + y
            for i, (nx, ny) in enumerate([(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]):
                new_pos = nx * n + ny
                new_dis = dist[cur_pos] + (1 if grid[x][y] != i + 1 else 0)
                if 0 <= nx < m and 0 <= ny < n and new_dis < dist[new_pos]:
                    dist[new_pos] = new_dis
                    if grid[x][y] == i + 1:
                        q.appendleft((nx, ny))
                    else:
                        q.append((nx, ny))
        
        return dist[m * n - 1]
    
    
    
    """ 2290. 到达角落需要移除障碍物的最小数目 #hard #题型 #BFS
从gird的左上走到右下, 要求最小代价. grid中的每个元素为0/1, 其中1表示有障碍物, 移除的代价为1.
思路: #BFS 其实是最短路径的变形问题
    实际上, 这里所有相连的空白位置都可以看作是(距离图上的)一个点, 每一个障碍物一个点; 这样, 可以构建我们常见的距离图, 并且可以用BFS来求解.
    具体实现上, 由于距离图上的一个节点对应了grid上的多个点, 因此可以用优先队列 (dist, (x, y)) 来规划BFS
"""
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        checkValid = lambda i,j: 0<=i<m and 0<=j<n
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        
        visited = set([(0,0)])
        q = [(0, (0,0))]
        while q:
            dis, (i,j) = heapq.heappop(q)
            for di,dj in directions:
                ni,nj = i+di, j+dj
                if (ni,nj)==(m-1,n-1):
                    return dis
                if checkValid(ni,nj) and (ni,nj) not in visited:
                    if grid[ni][nj] == 0:
                        heapq.heappush(q, (dis, (ni,nj)))
                    elif grid[ni][nj] == 1:
                        heapq.heappush(q, (dis+1, (ni,nj)))
                    visited.add((ni,nj))
        return -1
    
    

    """ 1824. 最少侧跳次数 #medium 有三条跑道, 上面各有一些石头. 要从起点跑到终点, 仅能进行侧跳 (在相同的距离处, 从跑道i跳到跑道j). 要求最少侧跳次数.
限制: 每个距离最多有一个石子; 距离 5e5
思路2: 转为图上求最短路径, 叫做 #0-1BFS
    将路上的位置 (dist,i) 作为节点, 根据向前走/侧跳进行连边, 代价分别为 0/1. 
        这样, 可以采用 #Dijkstra 算法求最短路径. 但复杂度超过了 O(n)
        利用 01BFS, 复杂度 O(n)
    说明: 如果边权不止 0和1，把双端队列换成最小堆，就得到了 Dijkstra 算法。
    见 [灵神](https://leetcode.cn/problems/minimum-sideway-jumps/solution/cong-0-dao-1-de-0-1-bfspythonjavacgo-by-1m8z4/)
"""
    def minSideJumps(self, obstacles: List[int]) -> int:
        n = len(obstacles)
        dis = [[n] * 3 for _ in range(n)]
        dis[0][1] = 0
        q = deque([(0, 1)])  # 起点
        while True:
            i, j = q.popleft()
            d = dis[i][j]
            if i == n - 1: return d  # 到达终点
            if obstacles[i + 1] != j + 1 and d < dis[i + 1][j]:  # 向右
                dis[i + 1][j] = d
                q.appendleft((i + 1, j))  # 加到队首
            for k in (j + 1) % 3, (j + 2) % 3:  # 枚举另外两条跑道（向上/向下）
                if obstacles[i] != k + 1 and d + 1 < dis[i][k]:
                    dis[i][k] = d + 1
                    q.append((i, k))  # 加到队尾



    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
