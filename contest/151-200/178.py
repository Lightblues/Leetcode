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
https://leetcode.cn/contest/weekly-contest-178

这一期的质量好高! T2的排序问题很有意义; T3在二叉树上搜索链表也很有意思, 注意看复杂度分析. T4的问题建模为图论问题, 想法很妙.

@2022 """
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 1365. 有多少小于当前数字的数字 """
    
    """ 1366. 通过投票对团队排名 #medium #题型 每个队伍用一个字母表示. 现在有一组投票记录, 表示每个人的排名.
要得到每个队伍的排序. 规则: 根据每个队伍 (rank1个数, rank2个数, ...) 排序. 若全部相同, 根据队伍字母排序. 限制: 队伍数量 26; 排名数量 1000
思路1: 统计每个队伍获得的排名数量, 再加上队伍字母, 整体排序. 时间复杂度 O(nlogn)
    细节: 为了方便排序, 可以用负数表示排名数量, 从而直接用负数排序.
"""
    def rankTeams(self, votes: List[str]) -> str:
        teams = votes[0]
        team_rank = {team: [0] * len(teams) for team in teams}
        for vote in votes:
            for i, team in enumerate(vote):
                # 根据名次排序, 直接用负数更方便
                team_rank[team][i] -= 1
        teams = [(rank + [team]) for team, rank in team_rank.items()]
        teams.sort()
        return ''.join([team[-1] for team in teams])
        
    """ 1367. 二叉树中的列表 #medium #题型 给定一个二叉树的根节点 root 和一个 head 为第一个节点的链表, 问在树上是否存在从上往下的一条路径对应着链表
限制: 链表长度 100; 二叉树节点 2500
注意, 对于每个节点, 都要尝试从链表的头上开始匹配.
思路1: 对于树上的每一个节点, 若和链表头相同, 尝试dfs. 是 #暴力 #枚举
    写一个 dfs(tnode, lnode) 函数, 表示从 tnode 开始, 是否能匹配 lnode 开始的链表.
    细节: 如何从树上每一个节点尝试从头开始匹配? 递归调用 isSubPath(head, root.left) 和 isSubPath(head, root.right) 即可
复杂度: 一开始感觉复杂度爆炸. 但看解答之后清楚了很多.
    考虑从一个tnode开始匹配链表头, 最多会尝试多少次? `min{ 2^{len+1}-1, n }` 前者是满二叉树的节点数, 后者是树的节点数约束.
    因此, 实际复杂度是 O(n * min{ 2^{len+1}-1, n }). 考虑平凡情况, n^2 不会超.
[官答](https://leetcode.cn/problems/linked-list-in-binary-tree/solution/er-cha-shu-zhong-de-lie-biao-by-leetcode-solution/)
"""
    def isSubPath(self, head: ListNode, root: TreeNode) -> bool:
        def dfs(tnode: TreeNode, lnode: ListNode) -> bool:
            # 1) 匹配完成
            if not lnode:
                return True
            # 2) 匹配失败的情况
            if not tnode:
                return False
            if tnode.val != lnode.val:
                return False
            # 3) 继续匹配
            return dfs(tnode.left, lnode.next) or dfs(tnode.right, lnode.next)
        
        if not root:
            return False
        # 如何从树上每一个节点尝试从头开始匹配? 递归调用 isSubPath(head, root.left) 和 isSubPath(head, root.right) 即可
        return dfs(root, head) or self.isSubPath(head, root.left) or self.isSubPath(head, root.right)
    
    """ 1368. 使网格图至少有一条有效路径的最小代价 #hard #题型 要从grid的左上走到右下. 每个格子初始化的方向是上下左右. 问最少修改多少格子, 使得路径有效. 限制: m,n 100
提示: 可以将每个网格堪称图上的一个节点, 网格与四周相连, 根据方向是否一致设置权重 0/1. 则原问题等价于求 #最短路径.
思路1: 根据提示建图. 然后求最短路径, 可以用 #Dijsktra 算法等.
    复杂度: 节点数量 O(mn), 边数量 O(mn), 因此复杂度 O(mnlog(mn))
思路1.2 除了基本的最短路径算法, 对于这里的特殊情况, 也可以用 「0-1 广度优先搜索」来搜索.
    修改之处在于: 遇到权重为 0 的邻居, 需要插入到队列的头部, 而不是尾部. 因此采用 #双端队列.
    复杂度: O(mn)
[official](https://leetcode.cn/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/solution/shi-wang-ge-tu-zhi-shao-you-yi-tiao-you-xiao-lu-2/)
"""
    def minCost(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        # grid 中的 1,2,3,4 分别对应的方向
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        def xy2idx(x, y):
            return x * n + y
        # 构建图
        g = [[] for _ in range(m * n)]
        for x in range(m):
            for y in range(n):
                for i, (dx, dy) in enumerate(directions):
                    nx, ny = x + dx, y + dy
                    # 考虑边界
                    if 0 <= nx < m and 0 <= ny < n:
                        g[xy2idx(x, y)].append((xy2idx(nx, ny), 0 if grid[x][y] == i+1 else 1))
        # 最短路径
        def f(start, end):
            # dijkstra. Copilet 补全的.
            dist = [float('inf')] * (m * n)
            dist[start] = 0
            q = [(0, start)]
            while q:
                d, u = heapq.heappop(q)
                # 提前结束
                if u==end: return d
                if d > dist[u]:
                    continue
                for v, w in g[u]:
                    if dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w
                        heapq.heappush(q, (dist[v], v))
            return dist[end]
        return f(0, m*n-1)
    
    def minCost(self, grid: List[List[int]]) -> int:
        # 官答的简洁写法
        m, n = len(grid), len(grid[0])
        BIG = int(1e9)
        dist = [0] + [BIG] * (m * n - 1)
        seen = set()
        q = [(0, 0, 0)]

        while len(q) > 0:
            cur_dis, x, y = heapq.heappop(q)
            if (x, y) in seen:
                continue
            seen.add((x, y))
            cur_pos = x * n + y
            for i, (nx, ny) in enumerate([(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]):
                new_pos = nx * n + ny
                new_dis = dist[cur_pos] + (1 if grid[x][y] != i + 1 else 0)
                if 0 <= nx < m and 0 <= ny < n and new_dis < dist[new_pos]:
                    dist[new_pos] = new_dis
                    heapq.heappush(q, (new_dis, nx, ny))
        return dist[m * n - 1]

    
sol = Solution()
result = [
    # sol.rankTeams(votes = ["ABC","ACB","ABC","ACB","ACB"]),
    # sol.rankTeams(votes = ["WXYZ","XYZW"]),
    sol.minCost(grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]),
    sol.minCost(grid = [[1,1,3],[3,2,2],[1,1,4]]),
]
for r in result:
    print(r)
