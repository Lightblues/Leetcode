from easonsi.util.leetcode import *
from itertools import pairwise

""" 
https://leetcode.cn/contest/weekly-contest-410
T4: 可以用DP来做, 但组合数学的直接求解非常精妙
Easonsi @2023 """
class Solution:
    """ 3248. 矩阵中的蛇 """
    def finalPositionOfSnake(self, n: int, commands: List[str]) -> int:
        x,y = 0,0
        for c in commands:
            if c=="RIGHT": x+=1
            elif c=="LEFT": x-=1
            elif c=="UP": y-=1
            else: y+=1
        return n*y+x
            
    """ 3249. 统计好节点的数目 """
    def countGoodNodes(self, edges: List[List[int]]) -> int:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        
        ans = 0
        def dfs(u, fa) -> int:
            nonlocal ans
            chlid_num_counts = []
            for v in g[u]:
                if v==fa: continue
                chlid_num_counts.append(dfs(v,u))
            if len(chlid_num_counts)==0 or len(set(chlid_num_counts))==1:
                ans += 1
            return sum(chlid_num_counts+[1])
        dfs(0,-1)
        return ans
    
    """ 3250. 单调数组对的数目 I 
    3251. 单调数组对的数目 II #hard 给定长n的数组, 对于每个元素分解为 nums[i] = a1[i] + a2[i], 要求分解后 a1 单调非递减, a2 单调非递减. 求数量. 
限制: n 2e3; nums[i] 1e3
思路1: 前缀和优化 DP
    考虑 f[i,j] 表示前i个元素, 且 a1[i]=j 的方案数.
    状态转移: 枚举 i-1 位置的元素范围, 若 a1[i-1] = k, 则 a1[i-1] <= a1[i], a2[i-1] >= a2[i]
        也即, k <= min{j, nums[i-1]-nums[i]+j}, 定义右边的max为 maxK, 则有
        f[i,j] = sum_{k=0}^{maxK} f[i-1,k] if maxK >=0 else 0, 其中的求和可以用 #前缀和 优化
    答案: 枚举a1[n-1]的取值, 累加得到 sum{j=0}^{nums[n-1]} f[n-1,j]
    复杂度: O(nm), 其中 m=max(nums)
思路2: #组合数学
    考虑特殊情况: nums[i] 都是相同元素 m, 则 a1 递增的时候, a2 递减是天然满足的! 
        此时, 答案为 C(n+m,n), 即在 n 个位置上插入 m 个隔板.
        图形化的理解: 从 (0,0) 走到 (n,m) 的路径数, 每次只能向右或向上走. 上面的组合数也就是在一共n+m步中, 选择哪些步向右走!
    回到原问题, 记 x=a1[i-1] <= a1[i]=y, 则 a2[i-1] >= a2[i] 等价于 nums[i-1]-x >= nums[i]-y,
        因此, y <= x + max{nums[i]-nums[i-1], 0}, 分类讨论
        nums[i]-nums[i-1] <= 0, 不影响!
        nums[i]-nums[i-1] > 0, 也就是在第i步至少要往上走 d=nums[i]-nums[i-1] 步, 可选空间减少, 因此问题变为 C(n+m-d, n)
    一般的, 记 d[i] = max{nums[i]-nums[i-1], 0}, 累计 m = nums[n-1] - d[1] -d[2] - ... - d[n-1], 
        则答案为 C(n+m, n) if m >=0 else 0
    复杂度: O(n)
ling: https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-ii/solutions/2876190/qian-zhui-he-you-hua-dppythonjavacgo-by-3biek/
"""
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        n = len(nums)
        m = max(nums)
        f = [[0] * (m + 1) for _ in range(n)]
        for j in range(nums[0] + 1):
            f[0][j] = 1
        for i in range(1, n):
            s = list(accumulate(f[i - 1]))  # f[i-1] 的前缀和
            for j in range(nums[i] + 1):
                max_k = j + min(nums[i - 1] - nums[i], 0)
                f[i][j] = s[max_k] % MOD if max_k >= 0 else 0
        return sum(f[-1][:nums[-1] + 1]) % MOD

    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        m = nums[-1]
        for x,y in pairwise(nums):
            if y > x:
                m -= (y - x)
        return math.comb(n + m, n) % MOD if m >= 0 else 0

sol = Solution()
result = [
    # sol.countGoodNodes(edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]),
    sol.countOfPairs([1,40,20]),
]
for r in result:
    print(r)
