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
https://oi-wiki.org/graph/shortest-path/
Dijkstra 算法
    非负权图 上单源最短路径
    复杂度: 根据使用 二叉堆/优先队列 的不同, 有不同的时间复杂度, 
        采用优先队列 PriorityQueue 的复杂度为 O(m logm)


Easonsi @2023 """
class Solution:
    """ 0743. 网络延迟时间 #medium 单源最短路 Dijkstra 模板题
"""
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        g = [[] for _ in range(n+1)]
        for u,v,w in times:
            g[u].append((v,w))
        q = [(0,k)]
        dist = [0] + [inf]*n
        dist[k] = 0
        while q:
            d,u = heapq.heappop(q)
            for v,w in g[u]:
                if dist[v]<=d+w: continue
                dist[v] = d+w
                heapq.heappush(q, (d+w, v))
        return -1 if inf in dist else max(dist)
    
    """ 1631. 最小体力消耗路径 #medium #题型
给定一个grid每个点有一定高度, 要从grid的左上走到右下(方向可以上下左右), 路径的代价定义为, 相邻两点高度差的最小值. 要求给出最小值.
限制: m,n 100; 每个点的高度 1e6
思路1: #UCS 应该就是 #Dijkstra
    注意到, 由于这里路径代价的定义是每条边权的最大值, 因此, 回形的路径可能是最优的, 因此不能用DP等来做.
    考虑采用 #UCS, 对于frontier维护一个 #优先队列, 每次拓展代价最小的节点.
    复杂度: O(mn log(mn)) 其中对数项是优先队列的复杂度.
思路2: 比较naive的 #二分查找
    在限制路径代价的前提下尝试用BFS/DFS看能否走到终点. 二分检查答案
    复杂度: O(mn log(C))
思路3: #并查集 #star
    根据边权从小到大排序, 逐渐连边, 每次都检查是否能走到终点(联通), 显然可以用并查集来实现.
[官答](https://leetcode.cn/problems/path-with-minimum-effort/solution/zui-xiao-ti-li-xiao-hao-lu-jing-by-leetc-3q2j/)
"""
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """ 思路1: #UCS 应该就是 #Dijkstra """
        m,n = len(heights), len(heights[0])
        pq = [(0, 0,0)] # (effort, x, y)
        seen = set() #; seen.add((0,0))
        mx = 0
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        while True:
            d, x,y = heapq.heappop(pq)
            mx = max(mx, d)
            if (x,y) == (m-1, n-1): break
            seen.add((x,y))
            for dx,dy in directions:
                nx,ny = x+dx,y+dy
                if nx<0 or ny<0 or nx>=m or ny>=n or (nx,ny) in seen: continue
                d = abs(heights[nx][ny]-heights[x][y])
                heappush(pq, (d, nx,ny))
        return mx
    
    """ 1514. 概率最大的路径 #medium #题型 #Dijkstra 算法
等价于, 经典的「单源最短路径路径」, 在带权图上求 (s,e) 之间的最短距离.
思路1: #Dijkstra 算法
    回顾 Dijkstra算法的核心思想: 1) 将节点分成两类: 「未确定节点」和「已确定节点」; 2) (「松弛」过程) 每次从「未确定节点」中取一个与起点距离最短的点，将它归类为「已确定节点」，并用它「更新」从起点到其他所有「未确定节点」的距离。直到所有点都被归类为「已确定节点」。
    细节: 1) 如何找到「未确定节点」中最小距离点? 例如可以用最小堆实现. 2) 如何分离两类节点? 一种方式是用 `visited` 字典标记已确定节点; 另一种方式是, 用一个 `minDist` 记录当前的距离, 更新过程中只有当v的距离比minDist小时才更新, 入栈. 实验下来两种方式没有复杂度上的区别.
    [官答](https://leetcode.cn/problems/path-with-maximum-probability/solution/gai-lu-zui-da-de-lu-jing-by-leetcode-solution/)
"""
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        # 一种方式是用 `visited` 字典标记已确定节点
        g = [[] for _ in range(n)]
        for (u,v),p in zip(edges, succProb):
            g[u].append((v,p)); g[v].append((u,p))
        h = [(-1, start)]
        visited = set()     # 已确定的点
        while h:
            prob,u = heappop(h)
            if u==end: return -prob
            if u in visited: continue
            visited.add(u)  # 注意, visited 中的点的距离已确定为最小值.
            for v,p in g[u]:
                if v not in visited:
                    heappush(h, (prob*p, v))
        return 0
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
