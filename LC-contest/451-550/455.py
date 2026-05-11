from typing import *
import math, collections
from math import floor, inf
from heapq import heappop, heappush

"""
https://leetcode.cn/contest/weekly-contest-455
Easonsi @2026 """


class Solution:
    """ 3591. 检查元素频次是否为质数 
思路 1: 预处理质数
    用埃氏筛（或者欧拉筛）预处理一个布尔数组，表示哪些数是质数
    """
    def checkPrimeFrequency(self, nums: List[int]) -> bool:
        limit = 100
        is_prime = [False, False] + [True] * limit
        # for x in range(2, limit+1):
        for x in range(2, math.isqrt(limit+1)+1):  # NOTE: 只需要枚举到 sqrt
            if is_prime[x]:
                for y in range(2*x,limit+1,x):
                    is_prime[y] = False
        cnt = set(collections.Counter(nums).values())
        return any(is_prime[c] for c in cnt)

    """ 3592. 硬币面值还原 #medium
已有的硬币面值为止, 只知道构成 1,2,...n 的方案数量 (每个硬币可无限使用). 还原出唯一的硬币组合
限制: n 100; numWays 2e8
思路 1: #完全背包：#反向构造题
    NOTE: 本题是 0518. 零钱兑换 II 的反向构造题
    显然, 我们可以找到最小硬币为第一个 =1 的位置. e.g. 考虑 [0,1,0,2,0,3] 的情况, 找到硬币 2
    在只有 {2} 的时候, 方案为 [0,1,0,1,0,1] -> 比较可找到第二个为 4
    增加到 {2,4}, 方案为 [0,1,0,2,0,3], etc
    复杂度: O(n^2)
https://leetcode.cn/problems/inverse-coin-change/solutions/3705647/wan-quan-bei-bao-pythonjavacgo-by-endles-y6oq/
    """
    def findCoins(self, numWays: List[int]) -> List[int]:
        n = len(numWays)
        ava = [0] * (n+1)
        ava[0] = 1
        ans =[]
        for i,x in enumerate(numWays,1):  # NOTE: from 1
            if x == ava[i]: continue
            elif x == ava[i]+1:
                ans.append(i)
                for j in range(i,n+1):
                    ava[j] += ava[j-i]
            else: return []  # NOTE: invalid!
        return ans

    """ 3593. 使叶子路径成本相等的最小增量 #medium
给定一个每个节点有权重的 root=0 的树, 每个操作可以给任意节点 +任意数值. 问最少操作, 使得 root->leaf 的权重和都相同. 
限制: n 1e5
思路 1: 树上 DP
    显然, 每棵子树要求都满足条件 -- 分解子问题.
    合并操作: 对于一个节点的所有子节点, 它们都要变为最大那个节点的分数 -> 加上该节点的分数再上传到上层
优化: "统计最大路径和的出现次数"
    太久没写, 下面转成了 tree, 实际上中间的 childs 构建可以去掉!
https://leetcode.cn/problems/minimum-increments-to-equalize-leaf-paths/solutions/3705650/tong-ji-zui-da-lu-jing-he-de-chu-xian-ci-bh9f/
    """
    def minIncrease(self, n: int, edges: List[List[int]], cost: List[int]) -> int:
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # find childs
        childs = [[] for _ in range(n)]
        vis = [False] * n
        vis[0] = True
        q = [0]
        while q:
            nq = []
            for u in q:
                for v in g[u]:
                    if not vis[v]:
                        childs[u].append(v)
                        vis[u] = True
                        nq.append(v)
            q = nq
        # dfs
        ans = 0
        def dfs(x: int) -> int:
            nonlocal ans
            if len(childs[x])==0: return cost[x]
            child_vs = []
            for c in childs[x]:
                child_vs.append(dfs(c))
            mx = max(child_vs)
            ans += len(child_vs) - child_vs.count(mx)
            return mx + cost[x]
        dfs(0)
        return ans

    def minIncrease(self, n: int, edges: List[List[int]], cost: List[int]) -> int:
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        g[0].append(-1)  # NOTE: 防止root被当做leaf!
        # 
        def dfs(x: int, fa: int) -> int:
            # if len(g[u])==1: return cost[u]
            max_s = cnt = 0
            for y in g[x]:
                if y == fa: continue
                mx = dfs(y, x)
                if mx > max_s:
                    cnt = 1
                    max_s = mx
                elif mx == max_s:
                    cnt += 1
            nonlocal ans
            ans += len(g[x])-1 - cnt  # NOTE: 统计最大值出现次数
            return max_s + cost[x]
        ans = 0
        dfs (0, -1)
        return ans

    """ 3594. 所有人渡河所需的最短时间 #hard
有 n 个人要渡河, 一艘船承载 k 个人; 渡河随着 m 个阶段有一个倍率 mul[j]
- 对于阶段 j 出发的一组人 g, 所需时间为 d = max{time[i], i in g} * mul[j]; 渡河后阶段前进 floor(d) % m 步
- 还有人的情况下, 需要一个人 r 带回船, 时间为 time[r] * mul[current_stage]; 阶段同样前进 floor(d) % m 步
求所有人渡河所需时间.
限制: n 12; k,m 5; mul 范围 [0.5,2]; time 限制 100
思路 1: #子集状压 + #Dijkstra
    注意: 1. 渡河的人和回来的可以不一样! 2. 一个人可以来回渡河, 将倍率调整到较低时间!
    "由于存在来来回回过河的情况，计算过程中可能会形成环，所以 DP（记忆化搜索）不太合适" -> 改成在这个有向图上跑 Dijkstra 最短路
    因此, 记 (stage, S) 表示阶段 S 为在此岸的人的集合, 起点 (0,U); 终点是 S 为空集的那些节点!
        状态转移: 枚举所有 <=k 的非空子集 T, 尝试过河;
            S!=T 的时候, 枚举所有对岸的人的中的一个人回来
    复杂度: 对于 迪杰斯特拉算法, 采用优先队列的复杂度为 O(M logM), 其中 M 为边数量
        本问题中, 考虑剩余 j 个人在岸上的子集数量 C(n,j), 从中选择的方案数为 2^j; 根据二项式定理 sum{C(n,j) 2^j, 0<=j<=n} = 3^n
            -- 也即, 「枚举子集的子集」
        再考虑枚举回来的人, 还是阶段数量 M = mn3^n
    """
    def minTime(self, n: int, k: int, m: int, time: List[int], mul: List[float]) -> float:
        u = 1 << n
        # 预处理每个 time 子集的最大值
        max_time = [0] * u
        for i, t in enumerate(time):
            high_bit = 1 << i
            for mask in range(high_bit):
                max_time[high_bit | mask] = max(max_time[mask], t)

        # 预处理每个集合的大小 <= k 的非空子集
        sub_masks = [[] for _ in range(u)]
        for i in range(u):
            sub = i
            while sub:
                if sub.bit_count() <= k:
                    sub_masks[i].append(sub)
                sub = (sub - 1) & i

        dis = [[inf] * u for _ in range(m)]
        h = []

        def push(d: float, stage: int, mask: int) -> None:
            if d < dis[stage][mask]:
                dis[stage][mask] = d
                heappush(h, (d, stage, mask))

        push(0, 0, u - 1)  # 起点

        while h:
            d, stage, left = heappop(h)  # left 是剩余没有过河的人
            if left == 0:  # 所有人都过河了
                return d
            if d > dis[stage][left]:
                continue
            # 枚举 sub 这群人坐一艘船过河
            for sub in sub_masks[left]:
                cost = max_time[sub] * mul[stage]
                cur_stage = (stage + floor(cost)) % m  # 过河后的阶段
                if sub == left:  # 所有人都过河了
                    push(d + cost, cur_stage, 0)
                    continue
                # 枚举回来的人（可以是之前过河的人）
                s = (u - 1) ^ left ^ sub
                while s:
                    lb = s & -s
                    return_time = max_time[lb] * mul[cur_stage]
                    push(d + cost + return_time, (cur_stage + floor(return_time)) % m, left ^ sub ^ lb)
                    s ^= lb

        return -1


sol = Solution()
result = [
    # sol.checkPrimeFrequency(nums = [1,2,3,4,5,4]),
    # sol.checkPrimeFrequency(nums = [1,2,3,4,5]),
    sol.findCoins(numWays = [0,1,0,2,0,3,0,4,0,5]),
    sol.findCoins([1,2,3,4,15]),
    # sol.minIncrease(n = 3, edges = [[0,1],[0,2]], cost = [2,1,3]),
    # sol.minIncrease(n = 5, edges = [[0,4],[0,1],[1,2],[1,3]], cost = [3,4,1,1,7]),
]
for r in result:
    print(r)