from typing import *
import string
import collections
import math
import itertools

"""
https://leetcode.cn/contest/weekly-contest-454
Easonsi @2026 """


class Solution:
    """ 3582. 为视频标题生成标签 """
    def generateTag(self, caption: str) -> str:
        ans = ""
        for i, word in enumerate(caption.split()):
            if i == 0:
                ans += word.lower()
            else: ans += word.capitalize()
        ans = "".join(ch for ch in ans if ch in string.ascii_letters)
        return ("#"+ans)[:100]

    """ 3583. 统计特殊三元组 
统计 (i,j,k) 坐标数量, 满足 nums[i] = nums[k] = 2 * nums[j]
限制: n 1e5; 对结果取模
思路 1: 枚举中间
    复杂度: O(n)
    """
    def specialTriplets(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        cnt = collections.Counter(nums)
        pre_cnt = collections.defaultdict(int)
        ans = 0
        for i,x in enumerate(nums):
            if x != 0:
                ans = (ans + pre_cnt[2*x]*(cnt[2*x]-pre_cnt[2*x])) % MOD
            pre_cnt[x] += 1
        return (math.comb(cnt[0],3) + ans) % MOD

    """ 3584. 子序列首尾元素的最大乘积 
对于一个数组, 找所有长度为 m 的子序列中, 首尾元素乘积最大值
限制: n 1e5
思路 1: 
    对于 l 开头的子序列, 其匹配的最右位置为 l+m-1, ...
    因此, 可以枚举 l, 维护后缀的 min/max -- 因为乘积最大一定是在min/max 取到
思路 1: 脑筋急转弯 + #枚举右维护左 -- 代码可以更简洁!
    注意无需特判 m=1 的情况，此时答案来自 nums 的最大值与自己相乘 -- 可以枚举到!
https://leetcode.cn/problems/maximum-product-of-first-and-last-elements-of-a-subsequence/solutions/3700555/nao-jin-ji-zhuan-wan-mei-ju-you-wei-hu-z-93zo/
    """
    def maximumProduct(self, nums: List[int], m: int) -> int:
        # if m == 1:  # 不需要特判!
        #     return max(map(abs, nums))**2
        n = len(nums)
        suf_min, suf_max = nums[-1], nums[-1]
        ans = nums[n-m] * nums[-1]
        for l in range(n-m-1,-1,-1):
            x = nums[l]
            nr = nums[l+m-1]
            suf_min = min(suf_min, nr)
            suf_max = max(suf_max, nr)
            ans = max(ans, x*suf_min, x*suf_max)
        return ans

    """ 3585. 树中找到带权中位节点 #hard
给定一棵带权树, 对于每次查询 (u,v), 计算 "带权中位节点", 也即从 u 到 v 的路径上, 累计边权和 >= u到v总边权和的节点.
限制: n, q 1e5
思路 1: #最近公共祖先 LCA
    对于一个 root, 我们可以计算所有节点的深度. 对于原问题:
    - u->v 的距离, 就是 dis_xy = dist(x, lca) + dist(lca, y)
    - 题目要求的, 就是在该路径上距离至少为 half = cell(dis_xy / 2) 的节点! 分类讨论:
        - 若 dist(x, lca) >= half, 直接在 x 的祖先寻找
            根据下面情况 2 的思路, 可转为 "往上跳至多 half-1" 的节点, 其父节点即为答案!
        - 否则, 在 y 的祖先寻找 "往上跳至多 dis_xy-half 距离的节点" --> 可以用模板中的 `upto_dis` 来求!
    边界: u=v 的时候, 直接返回
    复杂度: O((n+q)logn)
其中, #树上倍增算法（以及最近公共祖先） TODO
    https://leetcode.cn/problems/kth-ancestor-of-a-tree-node/solutions/2305895/mo-ban-jiang-jie-shu-shang-bei-zeng-suan-v3rw/
https://leetcode.cn/problems/find-weighted-median-node-in-tree/solutions/3700556/mo-ban-zui-jin-gong-gong-zu-xian-lcapyth-6ekj/
    """
    def findMedian(self, n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        g = LcaBinaryLifting(edges)
        ans = []
        for x, y in queries:
            if x == y:
                ans.append(x)
                continue
            lca = g.get_lca(x, y)
            dis_xy = g.dis[x] + g.dis[y] - g.dis[lca] * 2
            half = (dis_xy + 1) // 2
            if g.dis[x] - g.dis[lca] >= half:  # 答案在 x-lca 路径中
                # 先往上跳至多 half-1，然后再跳一步，就是至少 half
                to = g.upto_dis(x, half - 1)
                res = g.pa[to][0]  # 再跳一步
            else:  # 答案在 y-lca 路径中
                # 从 y 出发至多 dis_xy-half，就是从 x 出发至少 half
                res = g.upto_dis(y, dis_xy - half)
            ans.append(res)
        return ans


class LcaBinaryLifting:
    def __init__(self, edges: List[List[int]]):
        n = len(edges) + 1
        self.m = m = n.bit_length()
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append((y, w))
            g[y].append((x, w))

        depth = [0] * n
        dis = [0] * n
        pa = [[-1] * m for _ in range(n)]

        def dfs(x: int, fa: int) -> None:
            pa[x][0] = fa
            for y, w in g[x]:
                if y != fa:
                    depth[y] = depth[x] + 1
                    dis[y] = dis[x] + w
                    dfs(y, x)

        dfs(0, -1)

        for i in range(m - 1):
            for x in range(n):
                if (p := pa[x][i]) != -1:
                    pa[x][i + 1] = pa[p][i]

        self.depth = depth
        self.dis = dis
        self.pa = pa

    def get_kth_ancestor(self, node: int, k: int) -> int:
        for i in range(k.bit_length()):
            if k >> i & 1:
                node = self.pa[node][i]
        return node

    # 返回 x 和 y 的最近公共祖先
    def get_lca(self, x: int, y: int) -> int:
        if self.depth[x] > self.depth[y]:
            x, y = y, x
        # 使 y 和 x 在同一深度
        y = self.get_kth_ancestor(y, self.depth[y] - self.depth[x])
        if y == x:
            return x
        for i in range(self.m - 1, -1, -1):
            px, py = self.pa[x][i], self.pa[y][i]
            if px != py:
                x, y = px, py  # 同时往上跳 2**i 步
        return self.pa[x][0]

    # 返回 x 到 y 的距离（最短路长度）
    def get_dis(self, x: int, y: int) -> int:
        return self.dis[x] + self.dis[y] - self.dis[self.get_lca(x, y)] * 2

    # 从 x 往上跳【至多】d 距离，返回最远能到达的节点
    def upto_dis(self, x: int, d: int) -> int:
        dx = self.dis[x]
        for i in range(self.m - 1, -1, -1):
            p = self.pa[x][i]
            if p != -1 and dx - self.dis[p] <= d:  # 可以跳至多 d
                x = p
        return x


sol = Solution()
result = [
    # sol.generateTag(caption = "Leetcode daily streak achieved"),
    # sol.specialTriplets(nums = [6,3,6]),
    # sol.specialTriplets(nums = [0,1,0,0]),
    sol.maximumProduct(nums = [-1,-9,2,3,-2,-3,1], m = 1),
    sol.maximumProduct(nums = [1,3,-5,5,6,-4], m = 3),
]
for r in result:
    print(r)