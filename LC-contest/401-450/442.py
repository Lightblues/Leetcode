from typing import *
from math import ceil

""" 
https://leetcode.cn/contest/weekly-contest-442
T2 并查集
T3 连续处理的要求, 比较数学, ling 给了四种解法 #star
T4 观察可以找到规律; 计数部分需要一些位运算.
Easonsi @2025 """
class Solution:
    """ 3492. 船上可以装载的最大集装箱数量 """
    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
        return min(n**2, maxWeight//w)

    """ 3493. 属性图 """
    def numberOfComponents(self, properties: List[List[int]], k: int) -> int:
        n = len(properties)
        g = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i+1,n):
                if len(set(properties[i]) & set(properties[j])) >= k:
                    g[i].append(j)
                    g[j].append(i)
        # 
        vis = [False]*n
        def dfs(u):
            vis[u] = True
            for v in g[u]:
                if not vis[v]:
                    dfs(v)
        ans = 0
        for i in range(n):
            if not vis[i]:
                ans += 1
                dfs(i)
        return ans
    

    """ 3494. 酿造药水需要的最少总时间 #medium 有n个巫师能力值为skill, 给定m个药水mana, 需要依次制造, 每个药水要交给0,1,...n-1号巫师按照顺序处理, 处理时间为 skill[j]*mana[i], 并且必须连续. 
问完成所有药水的最少时间. 限制 n,m 5e3
思路1: #DP
    记第i个药水在j号巫师的完成时间为 f[i,j], 
        先忽略要连续处理的要求, 则有 f[i,j] = max{ f[i-1,j], f[i,j-1] } + skill[j] * mana[i]
        如何恢复连续性要求? 在计算到 f[i,n-1] 之后倒推所有的 f[i,...]
    复杂度: O(mn)
    official: https://leetcode.cn/problems/find-the-minimum-amount-of-time-to-brew-potions/solutions/3800529/niang-zao-yao-shui-xu-yao-de-zui-shao-zo-ojii/
思路2: 优化考虑的范围! 参见 ling
    复杂度: 在随机意义下
ling: https://leetcode.cn/problems/find-the-minimum-amount-of-time-to-brew-potions/solutions/3624232/zheng-fan-liang-ci-sao-miao-pythonjavacg-5fz9/
"""
    def minTime(self, skill: List[int], mana: List[int]) -> int:
        n, m = len(skill), len(mana)
        f = [0] * (n+1)
        for mi in mana:
            for j in range(n):
                # NOTE: 用max居然会 TLE
                # f[j+1] = max(f[j], f[j+1]) + skill[j] * mi
                start = f[j] if f[j] >= f[j+1] else f[j+1]
                f[j+1] = start + skill[j] * mi
            for j in range(n-1,-1,-1):
                f[j] = f[j+1] - skill[j] * mi
        return f[-1]

    """ 3495. 使数组元素都变为零的最少操作次数 #hard 给定一组查询 [l,r], 代表 l,l+1,...r 数组, 对于每个查询, 每次可以选择其中两个数字, 将他们分别替换为 floor(x/4)
统计将 [l,r] 经过多少次操作变为全0数组; 累计所有查询之和
限制: q 1e5; S 1e9
思路1: 
    首先, 分析需要操作的次数.
        发现 1...3 需要一次; 4...15 需要两次; 16...63 需要三次, ...
        分析对于一些区间所需的操作次数, 可知所需操作次数为 ceil(M/2) 其中M为所有数字累计的操作数
    第二个问题, 如何统计 [l,r] 区间内的数字所需操作数?
        思路1: 构建 1,4,16,... 的数组, 二分查找统计
        思路2: 参见ling, 直接定义 f(x) 计算 1...x 范围的操作次数, 则答案就是 f(r) - f(l-1)
            为此, 直接二进制累计每一个位数即可!
ling: https://leetcode.cn/problems/minimum-operations-to-make-array-elements-zero/solutions/3624312/o1-gong-shi-pythonjavacgo-by-endlesschen-2gos/
    """
    def minOperations(self, queries: List[List[int]]) -> int:
        def f(x: int) -> int:
            m = x.bit_length()
            acc = 0
            for i in range(1, m):
                acc += ceil(i/2) * 2**(i-1)  # 对于长i的二进制数字, 一共有 2^(i-1) 个
            acc += (x - 2**(m-1) + 1) * ceil(m/2)
            return acc
        acc = 0
        for l,r in queries:
            acc += ceil((f(r) - f(l-1)) / 2)
        return acc
        

sol = Solution()
result = [
    # sol.numberOfComponents(properties = [[1,2],[1,1],[3,4],[4,5],[5,6],[7,7]], k = 1),
    # sol.minTime(skill = [1,5,2,4], mana = [5,1,4,2]),
    sol.minOperations(queries = [[1,2],[2,4]]),
]
for r in result:
    print(r)
