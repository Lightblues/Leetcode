from typing import *

""" 
https://leetcode.cn/contest/biweekly-contest-148
Easonsi @2025 """
class Solution:
    """ 3423. 循环数组中相邻元素的最大差值 """
    def maxAdjacentDistance(self, nums: List[int]) -> int:
        return max(abs(nums[i]-nums[(i+1)%len(nums)]) for i in range(len(nums)))
    
    """ 3424. 将数组变相同的最小代价 """
    def minCost(self, arr: List[int], brr: List[int], k: int) -> int:
        return min(
            sum(abs(a-b) for a,b in zip(arr,brr)),
            sum(abs(a-b) for a,b in zip(sorted(arr),sorted(brr))) + k
        )

    """ 3425. 最长特殊路径 #hard 给定一个带边权(长度)的树, 且每个节点有一个值(标签), 定义 "特殊路径" 为从上往下走的, 并且经过节点互不相通 (长度可以为0, 也即只包含一个点)
问最长特殊路径的长度 (边权之和), 以及其中最少的节点数
限制: n 5e4
思路1: #树上滑窗
    简化成链 (数组) 结构, 则 "最长特殊路径" 问题可用 滑窗 求解!
    如何泛化到树结构? 用 #DFS 来遍历树, "滑窗" 如何维护呢? 
        - 可以用一个 dis 栈结构来记录从root到当前节点的路径长度!
        - 用一个 last_depth 字典来记录每种节点值 (label) 最后出现的深度 (dis)
    """
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        g = [[] for _ in range(len(nums))]
        for u,v,d in edges:
            g[u].append((v,d))
            g[v].append((u,d))
        
        dis = [0]
        last_depth = {}
        ans = (0,0)  # 最长路径, -节点数
        def dfs(u:int, fa:int, d:int):
            # d: 从root到节点u的深度 (root深度为0)
            nonlocal ans
            old_d = last_depth.get(nums[u], 0)  # 该节点值 (label) 最后出现的深度; 若未出现则为0 (完整路径)
            ans = max(ans, (dis[-1]-dis[old_d], -(d-old_d+1)))
            last_depth[nums[u]] = d
            for v,d in g[u]:
                if v == fa: continue
                dis.append(d+dis[-1])  # record the acc distance
                dfs(v, u, d+1)
                dis.pop()
            last_depth[nums[u]] = old_d
        dfs(0, -1, 0)
        return [ans[0], -ans[1]]

    """ 3426. 所有安放棋子方案的曼哈顿距离 #hard 在 m*n 网格中放k个棋子, 要求每个格子最多一个, 对每个方案计算任意两棋子之间的曼哈顿距离之和, 求所有方案的曼哈顿距离之和
限制: 结果取模. m,n 1e5
思路1: #数学
    - 考虑简化情况: m=1, 也即一维情况. 不放排列 n=4, k=3 的所有情况!
        发现两个位置分别在 0,1 的情况数为 C(2,1); 贡献 |0-1|
        发现两个位置分别在 0,2 的情况数为 C(2,1); 贡献 |0-2|
        ...
        推广到一般情况, 每两点摆放的方案数为 C(n-2,k-2); 贡献 |i-j|
        所有两点之间距离为 1,2,...的情况分别有 n-1,n-2,...,1 种, 共计 sum{ (n-k)*k, k=1...n-1 }
            化简 = n * n(n-1)/2 - (n+1)n(n-1)/2
    - 回到二维情况, 仅考虑 x 方向的 |xi-xj| 的贡献!
        显然要求 i!=j 的时候才不为0. 对于所选的两列都能放在任意m位置. 因此有 m^2 重数
        也即, C(m*n-2,k-2) * m^2 * sum{ (n-k)*k, k=1...n-1 }
    """
    def distanceSum(self, m: int, n: int, k: int) -> int:


sol = Solution()
result = [
    # sol.maxAdjacentDistance(nums = [1,2,4]),
    # sol.minCost(arr = [-7,9,5], brr = [7,-2,-5], k = 2),
    sol.longestSpecialPath(edges = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], nums = [2,1,2,1,3,1]),
]
for r in result:
    print(r)