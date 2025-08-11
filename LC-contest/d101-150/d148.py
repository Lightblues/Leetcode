from typing import *
from math import comb

""" 
https://leetcode.cn/contest/biweekly-contest-148 质量也非常高的两题
T3 树上滑窗, 考验代码功底 #细节
T4 的数学题相当精彩! 
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
    复杂度: O(n)
    代码分析: 为什么下面是对的? -- 太多 #细节
    1. 如何设计 DFS 的 "路径记录"? 下面通过 dis 来记录从root到当前节点的累计路径长度, 而且其 len 就是当前节点深度!
    2. dfs的函数签名如何设计? 正常树搜索 (u, fa) 的基础上, 引入 "滑动窗口" 的边界 -- 也即 top_depth 表示当前路径上最上侧节点的深度
    3. 如何 更新 和 #回溯 ? 也即灵神所谓 "记录现场" 和 "恢复现场", 应该发生在for循环前后! 
[ling](https://leetcode.cn/problems/longest-special-path/solutions/3051377/shu-shang-hua-chuang-pythonjavacgo-by-en-rh5m/)
    """
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        g = [[] for _ in range(len(nums))]
        for u,v,d in edges:
            g[u].append((v,d))
            g[v].append((u,d))
        
        dis = [0]       # 从root到当前节点的累计路径长度 -- 因此 len 就是当前节点深度!
        last_depth = {} # 记录每种节点值 (label) 最后出现的深度 (dis), 从1开始 (dis[root]=1)
        ans = (0,-1)    # 最长路径, -节点数
        def dfs(u:int, fa:int, top_depth:int):
            # top_depth: 路径最上一个节点的深度
            color = nums[u]
            old_depth = last_depth.get(color, 0)  # 记录现场
            top_depth = max(top_depth, old_depth)       # 更新 top_depth (滑窗左端点)
            
            nonlocal ans
            ans = max(ans, (dis[-1]-dis[top_depth], -(len(dis)-top_depth)))

            last_depth[color] = len(dis)
            for v,d in g[u]:
                if v == fa: continue
                dis.append(d+dis[-1])  # record the acc distance
                dfs(v, u, top_depth)
                dis.pop()
            last_depth[color] = old_depth               # 恢复现场
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
            化简 = n * n(n-1)/2 - (n-1)n(2n-1)/6 = (n+1)n(n-1)/6 = C(n+1,3)
        remark: 这里用到了平方和公式 1^2 + 2^2 + ... + n^2 = n(n+1)(2n+1)/6
    - 回到二维情况, 仅考虑 x 方向的 |xi-xj| 的贡献!
        显然要求 i!=j 的时候才不为0. 对于所选的两列都能放在任意m位置. 因此有 m^2 重数
        也即, C(m*n-2,k-2) * m^2 * C(n+1,3)
        同理, y 方向上 C(m*n-2,k-2) * n^2 * C(m+1,3)
[ling](https://leetcode.cn/problems/manhattan-distances-of-all-arrangements-of-pieces/solutions/3051398/gong-xian-fa-yu-chu-li-hou-o1pythonjavac-2hgt/)
    """
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 1_000_000_007
        return comb(m*n-2,k-2) % MOD * (m**2 * comb(n+1,3) + n**2 * comb(m+1,3)) % MOD

sol = Solution()
result = [
    # sol.maxAdjacentDistance(nums = [1,2,4]),
    # sol.minCost(arr = [-7,9,5], brr = [7,-2,-5], k = 2),
    sol.longestSpecialPath(edges = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], nums = [2,1,2,1,3,1]),
    # sol.distanceSum
]
for r in result:
    print(r)