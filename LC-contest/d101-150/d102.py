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
https://leetcode-cn.com/contest/biweekly-contest-102
Easonsi @2023 """


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 6333. 查询网格图中每一列的宽度 """
    def findColumnWidth(self, grid: List[List[int]]) -> List[int]:
        n,m = len(grid),len(grid[0])
        ans = [0] * m
        for row in grid:
            for i,x in enumerate(row):
                ans[i] = max(ans[i], len(str(x)))
        return ans
    
    """ 6334. 一个数组所有前缀的分数 """
    def findPrefixScore(self, nums: List[int]) -> List[int]:
        n = len(nums)
        mx = -inf
        for i,x in enumerate(nums):
            mx = max(mx, x)
            nums[i] += mx
        return list(accumulate(nums))
    
    """ 6335. 二叉树的堂兄弟节点 II #medium 对于二叉树的每个一个节点, 将其值替换为其所有「堂兄弟节点」值的和. 所谓堂兄弟, 就是「在树中有相同的深度且它们的父节点不同」
限制: n 1e5
思路1: 先计算出层和, 然后 #DFS 过程中, 更新孩子的值!
思路1.1: 灵神 两次 #BFS
[灵神](https://leetcode.cn/problems/cousins-in-binary-tree-ii/solution/bfssuan-liang-ci-pythonjavacgo-by-endles-b72a/)
"""
    def replaceValueInTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        layer2sum = defaultdict(int)
        def dfs(u:TreeNode, l):
            if not u: return
            layer2sum[l] += u.val
            dfs(u.left, l+1)
            dfs(u.right, l+1)
        dfs(root, 0)
        # 
        def dfs(u:TreeNode, l):
            if not u: return 0
            cc = dfs(u.left, l+1) + dfs(u.right, l+1)
            if u.left: u.left.val = layer2sum[l+1] - cc
            if u.right: u.right.val = layer2sum[l+1] - cc
            return u.val
        dfs(root, 0)
        root.val = 0    # 注意以上更新无法完成root!
        return root

    
""" 6336. 设计可以求最短路径的图类 #hard #距离 实现一个数据结构, 要求在有向图上动态增加边, 查询最小距离 
限制: n 100; 增加/查询 操作 100
思路1: #最短路 的模板题
    1.1 采用 #堆 实现的 #Dijkstra 算法. 复杂度 O(m logm). 这里的图可能是稠密的, 下面可能更好
    1.2 Dijkstra 算法的邻接矩阵版本. 复杂度 O(n^2)
    这样, 加边的整体复杂度为 O(q); 查询的整体复杂度为 O(qn^2)
思路2: 采用 #Floyd 方法计算最短路
    如何更新? 注意到 (x,y) 边的加入, 只可能影响 (s,x)-(x,y)-(y,e) 的路径, 枚举所有 (s,e) 即可. 
    复杂度: 初始化的复杂度为 O(n^3); 加边的复杂度为 O(qn^2); 查询的复杂度为 O(q)
[灵神](https://leetcode.cn/problems/design-graph-with-shortest-path-calculator/solution/dijkstra-suan-fa-mo-ban-pythonjavacgo-by-unmv/) 介绍了邻接矩阵版本的代码
"""
class Graph:
    def __init__(self, n: int, edges: List[List[int]]):
        self.n = n
        g = [[] for _ in range(n)]
        for u,v,w in edges:
            g[u].append((v,w))
        self.g = g

    def addEdge(self, edge: List[int]) -> None:
        u,v,w = edge
        self.g[u].append((v,w))

    def shortestPath(self, node1: int, node2: int) -> int:
        # 自己写的 1.1 采用 #堆 实现的 #Dijkstra 算法
        q = [(0,node1)]
        seen = set((node1,))
        while q:
            d,u = heappop(q)
            if u==node2: return d
            seen.add(u)
            for v,w in self.g[u]:
                if v in seen: continue
                heappush(q, (d+w,v))
        return -1
    def shortestPath(self, start: int, end: int) -> int:
        # 1.2 Dijkstra 算法的邻接矩阵版本
        n = len(self.g)
        dis = [inf] * n  # 从 start 出发，到各个点的最短路，如果不存在则为无穷大
        dis[start] = 0
        vis = [False] * n
        while True:  # 至多循环 n 次
            # 找到当前最短路，去更新它的邻居的最短路
            # 根据数学归纳法，dis[x] 一定是最短路长度
            x = -1
            for i, (b, d) in enumerate(zip(vis, dis)):
                if not b and (x < 0 or d < dis[x]):
                    x = i
            if x < 0 or dis[x] == inf:  # 所有从 start 能到达的点都被更新了
                return -1
            if x == end:  # 找到终点，提前退出
                return dis[x]
            vis[x] = True  # 标记，在后续的循环中无需反复更新 x 到其余点的最短路长度
            for y, w in enumerate(self.g[x]):
                if dis[x] + w < dis[y]:
                    dis[y] = dis[x] + w  # 更新最短路长度

sol = Solution()
result = [
    testClass("""["Graph", "shortestPath", "shortestPath", "addEdge", "shortestPath"]
[[4, [[0, 2, 5], [0, 1, 2], [1, 2, 1], [3, 0, 3]]], [3, 2], [0, 3], [[1, 3, 4]], [0, 3]]""")
]
for r in result:
    print(r)
