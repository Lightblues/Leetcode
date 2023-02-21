from easonsi.util.leetcode import *
from functools import cache

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

"""  01背包
灵神: https://www.bilibili.com/video/BV16Y411v7Y6/
wiki: [Knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem)

0-1背包
0416. 分割等和子集  #medium 是否可以将数组划分成两个和相等的数组.
0474. 一和零 
0494. 目标和 #medium #题型 给定一个整数数组, 在它们之间加 +/- 组成表达式, 要求返回结果为 target 的表达式数量. 限制: n 20
0879. 盈利计划 
1049. 最后一块石头的重量 II 
1230. 抛掷硬币

完全背包
1449. 数位成本和为目标值的最大数字 
0322. 零钱兑换 #medium 给定一组coins, 在不限制硬币数量的情况下, 求凑成amount的最少硬币数量.
0518. 零钱兑换 II 
0279. 完全平方数
0377. 组合总和 Ⅳ


Easonsi @2023 """
class Solution:
    """ 0494. 目标和 #medium #背包 #题型 给定一个整数数组, 在它们之间加 +/- 组成表达式, 要求返回结果为 target 的表达式数量. 限制: n 20
思路2: 转化为 #0-1背包 问题
    假设所选数字之和为p, 所有数字之和为s, 则需要满足 s-2p=target. 也即, 我们需要在数字中选择和为 (s-target)/2 的子集, 求数量
如何求01背包问题?
    1. 可以用递归, 下面 dfs(i,c) 表示用前i个数字, 组成和为c的表达式数量
    2. 可以把递归改成数组形式, dp[i][c] 表示用前i个数字, 组成和为c的表达式数量
    3. 优化空间1: 用两个数组
    4. 优化空间2: 只用一个数组! 倒序枚举
复杂度: O(np)
[灵神](https://leetcode.cn/problems/target-sum/solution/jiao-ni-yi-bu-bu-si-kao-dong-tai-gui-hua-s1cx/)
"""
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        s = sum(nums)
        if s < target or (s-target)%2 == 1: return 0    # 题目中的数组元素都是正数
        p = (s-target)//2
        # 1. 可以用递归, 下面 dfs(i,c) 表示用前i个数字, 组成和为c的表达式数量
        @cache
        def dfs(i,c):
            if i<0:  return 1 if c==0 else 0
            if c<nums[i]:  return dfs(i-1,c)
            return dfs(i-1,c-nums[i]) + dfs(i-1,c)
        return dfs(len(nums)-1,p)
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        s = sum(nums)
        if s < target or (s-target)%2 == 1: return 0    # 题目中的数组元素都是正数
        p = (s-target)//2
        # 2. 可以把递归改成数组形式, dp[i][c] 表示用前i个数字, 组成和为c的表达式数量
        f = [[0]*(p+1) for _ in range(len(nums)+1)]
        f[0][0] = 1     # 边界条件
        for i,x in enumerate(nums):
            for j in range(p+1):
                if j<x:  f[i+1][j] = f[i][j]
                else: f[i+1][j] = f[i][j] + f[i][j-x]
        return f[-1][p]
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        s = sum(nums)
        if s < target or (s-target)%2 == 1: return 0    # 题目中的数组元素都是正数
        p = (s-target)//2
        # 4. 优化空间2: 只用一个数组! 倒序枚举
        dp = [1] + [0]*p
        for x in nums:
            for i in range(p, x-1, -1):     # 倒序枚举
                # 由于只用一个数组了, 不需要上面的if判断
                dp[i] += dp[i-x]
        return dp[p]
    
    
    """ 0416. 分割等和子集 #背包 #medium 是否可以将数组划分成两个和相等的数组. 限制: n 200, 每个元素大小 100. 
思路2: #0-1背包 问题. 求是否可以满足
"""
    def canPartition(self, nums: List[int]) -> bool:
        s = sum(nums)
        if s%2: return False
        s //= 2
        # @cache
        # def dfs(i,c):
        #     if i<0: return c==0
        #     if c<nums[i]: return dfs(i-1,c)
        #     return dfs(i-1,c-nums[i]) or dfs(i-1,c)
        # return dfs(len(nums)-1,s)
        dp = [True] + [False] * s
        for i, num in enumerate(nums):
            for j in range(s, num - 1, -1):
                dp[j] |= dp[j - num]
        return dp[s]
    
    
    
    
    """ 0322. 零钱兑换 #medium 给定一组coins, 在不限制硬币数量的情况下, 求凑成amount的最少硬币数量. 如果无法凑成, 返回-1 限制: n 12, amount 10^4
思路1: #完全背包 问题
    同 [0494. 目标和] 中所介绍的多种DP写法
复杂度: O(n*amount)
[灵神](https://leetcode.cn/problems/coin-change/solution/jiao-ni-yi-bu-bu-si-kao-dong-tai-gui-hua-21m5/)
"""
    def coinChange(self, coins: List[int], amount: int) -> int:
        @cache
        def dfs(i, c):
            if i<0: return 0 if c==0 else inf
            if c<coins[i]: return dfs(i-1,c)
            return min(dfs(i-1,c), dfs(i,c-coins[i])+1)
        ans = dfs(len(coins)-1, amount)
        return ans if ans!=inf else -1
    def coinChange(self, coins: List[int], amount: int) -> int:
        n = len(coins)
        f = [[inf]*(amount+1) for _ in range(n+1)]
        f[0][0] = 0
        for i,c in enumerate(coins):
            for j in range(amount+1):   # 注意这里0也要进行转移
                if j<c: f[i+1][j] = f[i][j]
                else: f[i+1][j] = min(f[i][j], f[i+1][j-c]+1)
        ans = f[-1][-1]
        return ans if ans!=inf else -1
    def coinChange(self, coins: List[int], amount: int) -> int:
        f = [0] + [inf]*amount
        for c in coins:
            for j in range(c, amount+1):
                f[j] = min(f[j], f[j-c]+1)
        return f[-1] if f[-1]!=inf else -1
    
    """ 0518. 零钱兑换 II #medium 相较于 [0322. 零钱兑换] 要求方案数 限制: n 300; amount 5000
"""
    def change(self, amount: int, coins: List[int]) -> int:
        f = [1] + [0]*amount
        for c in coins:
            for j in range(c, amount+1):
                f[j] += f[j-c]
        return f[amount]
    
    """ 0279. 完全平方数 #medium 对于一个正整数n, 将它分解为完全平方数之和, 求最少数量 限制: n 1e4. 
思路1: #完全背包 dfs(x) 表示x最少可以分解为多少个完全平方数之和
思路1.5: 换一个角度, 从小到大DP, 更加直观
思路2: #数学, 利用 「四平方和定理」
    [官答](https://leetcode.cn/problems/perfect-squares/solution/wan-quan-ping-fang-shu-by-leetcode-solut-t99c/)
"""
    def numSquares(self, n: int) -> int:
        @cache
        def dfs(x):
            if x==0: return 0
            mn = inf
            for i in range(1, int(x**0.5)+1):
                mn = min(mn, dfs(x-i*i)+1)
            return mn
        return dfs(n)
    def numSquares(self, n: int) -> int:
        # 思路1.5: 换一个角度, 从小到大DP, 更加直观
        f = [0] + [inf]*n
        for i in range(1, n+1):
            mn = inf
            for j in range(1, int(i**0.5)+1):
                mn = min(mn, f[i-j*j]+1)
            f[i] = mn
        return f[n]
    
sol = Solution()
result = [
    # sol.findTargetSumWays(nums = [1,1,1,1,1], target = 3),
    # sol.coinChange(coins = [1, 2, 5], amount = 11),
    # sol.change(amount = 5, coins = [1, 2, 5]),
    
    # sol.canPartition(nums = [1,5,11,5]),
    # sol.numSquares(n = 12),
]
for r in result:
    print(r)
