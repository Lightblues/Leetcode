from easonsi.util.leetcode import *
from functools import cache

""" 
【买卖股票系列问题】与【状态机 DP】，包括【至多/恰好/至少】的讲解
https://www.bilibili.com/video/BV1ho4y1W7QK/

0122. 买卖股票的最佳时机 II #medium base 场景: 每次最多持有一个, 不限制交易次数
0309. 最佳买卖股票时机含冷冻期 #medium 增加了在i-1天卖出则不能在i天买入的限制
0188. 买卖股票的最佳时机 IV #hard 增加了最多交易k次的限制 限制: n,k 1e3
    需要另加k这个维度的DP

0121. 买卖股票的最佳时机 #easy 只能进行一次交易 https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/
0123. 买卖股票的最佳时机 III #hard 最多完成两笔交易 限制: n 1e5 https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/
    思路0: 前缀/后缀
0714. 买卖股票的最佳时机含手续费 #medium 每笔交易有手续费 https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/
1911. 最大子序列交替和  #medium #题型 定义子序列的交替和为, 偶数下标的元素和减去奇数下标的元素和 限制: n 1e5 https://leetcode.cn/problems/maximum-alternating-subsequence-sum/
    巧妙的角度转换! 

Easonsi @2023 """
class Solution:
    """ 0122. 买卖股票的最佳时机 II #medium base 场景: 每次最多持有一个, 不限制交易次数
思路1: #贪心 记录前一天价格
    是否在i天卖出, 只需要看前一天的价格pre即可! 
思路2: 形式化 #DP 
    f(i, hold) 表示第i天持有/不持有股票的最大收益 (注意hold=1时不一定是当天买入的)
    转移: f(i,0) = max(f(i-1,0), f(i-1,1)+prices[i])
        f(i,1) = max(f(i-1,1), f(i-1,0)-prices[i])
    返回: f(n-1,0)
    边界: 当i<0时, hold=0直接返回0即可, hold=1返回-inf (表示不合法!)
复杂度: O(n)
[灵神](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/solution/shi-pin-jiao-ni-yi-bu-bu-si-kao-dong-tai-o3y4/)
     """
    def maxProfit(self, prices: List[int]) -> int:
        # 思路1
        pre = inf
        ans = 0
        for x in prices:
            if x>pre:
                ans += x-pre
            pre = x
        return ans
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        @cache
        def f(i, hold):
            if i<0: return 0 if hold==0 else -inf
            if hold==0: return max(f(i-1,0), f(i-1,1)+prices[i])
            else: return max(f(i-1,1), f(i-1,0)-prices[i])
        return f(n-1,0)
    
    """ 0309. 最佳买卖股票时机含冷冻期 #medium 增加了在i-1天卖出则不能在i天买入的限制
思路1: #DP 修改转移方程
    转移: f(i,0) = max(f(i-1,0), f(i-1,1)+prices[i])
        f(i,1) = max(f(i-1,1), f(i-2,0)-prices[i])
    """
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        @cache
        def f(i, hold):
            if i<0: return 0 if hold==0 else -inf
            if hold==0: return max(f(i-1,0), f(i-1,1)+prices[i])
            else: return max(f(i-1,1), f(i-2,0)-prices[i])
        return f(n-1,0)
    
    """ 0188. 买卖股票的最佳时机 IV #hard 增加了最多交易k次的限制 限制: n,k 1e3
思路1: #DP 在转移方程中增加 k的限制 这一维度
    f(i,k,hold) 记录在在i时刻剩余k次交易机会, 是否持有股票的最大收益
    转移: f(i,k,0) = max(f(i-1,k,0), f(i-1,k,1)+prices[i])
        f(i,k,1) = max(f(i-1,k,1), f(i-1,k-1,0)-prices[i])
    边界: 注意除了 i<0 的边界, 还要考虑 k<0 的边界 (返回-inf标记不合法)
    复杂度: O(nk)
笔记: 注意下面的代码是正确的! 只需要访问 f(n-1,k,0)
空间优化等技巧见 [灵神](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/solution/shi-pin-jiao-ni-yi-bu-bu-si-kao-dong-tai-kksg/)
见 [0123]
    """
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)
        @cache
        def f(i,k,hold):
            if k<0: return -inf
            if i<0: return 0 if hold==0 else -inf
            if hold==0: return max(f(i-1,k,0), f(i-1,k,1)+prices[i])
            else: return max(f(i-1,k,1), f(i-1,k-1,0)-prices[i])
        # 注意, 只需要访问 f(n-1,k,0) 就可以了!
        return f(n-1,k,0)


    """ 0121. 买卖股票的最佳时机 #easy 只能进行一次交易
思路0: 记录前缀min
思路1: 当然, 也可以写成 恰好/至少 一次的DP形式
    """
    def maxProfit(self, prices: List[int]) -> int:
        mn = inf
        ans = 0
        for x in prices:
            ans = max(ans, x-mn)
            mn = min(mn, x)
        return ans

    """ 0123. 买卖股票的最佳时机 III #hard 最多完成两笔交易 限制: n 1e5
思路0: 枚举所有分割点, 在两部分分别求一次交易最大
    为此, 联系「0121」, 建立前缀/后缀一次最大
思路1: #DP 就是「0188 至多k笔交易」取 k=2
    不过由于题目n比较大, 用cache会 #TLE
    所以下面展开成了数组 DP
    """
    def maxProfit(self, prices: List[int]) -> int:
        # 思路0: 枚举所有分割点, 在两部分分别求一次交易最大
        n = len(prices)
        left = [0] * n
        right = [0] * n
        # 
        mn = inf; ans = 0
        for i in range(n):
            ans = max(ans, prices[i]-mn)
            left[i] = ans
            mn = min(mn, prices[i])
        mx = -inf; ans = 0
        for i in range(n-1,-1,-1):
            ans = max(ans, mx-prices[i])
            right[i] = ans
            mx = max(mx, prices[i])
        # 
        return max(a+b for a,b in zip(left,right))
    def maxProfit(self, prices: List[int]) -> int:
        # 思路1: #DP 就是「0188 至多k笔交易」取 k=2
        # 注意, 直接用 0188 的代码 cache些会超时! 
        n = len(prices)
        k = 2
        # def f(i,k,hold):
        # 注意, k的维度 +2, 首位标记-1 不合法!
        f = [[[-inf]*2 for _ in range(k+2)] for _ in range(n+1)]
        for kk in range(k+1):
            f[0][kk+1][0] = 0
        # if k<0: return -inf
        # if i<0: return 0 if hold==0 else -inf
        for i in range(n):
            for kk in range(k+1):
                f[i+1][kk+1][0] = max(f[i][kk+1][0], f[i][kk+1][1]+prices[i])
                f[i+1][kk+1][1] = max(f[i][kk+1][1], f[i][kk][0]-prices[i])
            # if hold==0: return max(f(i-1,k,0), f(i-1,k,1)+prices[i])
            # else: return max(f(i-1,k,1), f(i-1,k-1,0)-prices[i])
        # 注意, 只需要访问 f(n-1,k,0) 就可以了!
        return f[n][k+1][0]

    """ 0714. 买卖股票的最佳时机含手续费 #medium 每笔交易有手续费 限制: n 5e4
思路1: DP 转移的时候减去fee
    f(i,1) = max(f(i-1,1), f(i-1,0)-prices[i]-fee)
    f(i,0) = max(f(i-1,0), f(i-1,1)+prices[i])
    """
    def maxProfit(self, prices: List[int], fee: int) -> int:
        n = len(prices)
        @cache
        def f(i,hold):
            if i<0: return 0 if hold==0 else -inf
            if hold==0: return max(f(i-1,0), f(i-1,1)+prices[i])
            else: return max(f(i-1,1), f(i-1,0)-prices[i]-fee)
        return f(n-1,0)


    """ 1911. 最大子序列交替和 #medium #题型 定义子序列的交替和为, 偶数下标的元素和减去奇数下标的元素和 限制: n 1e5
思路1: #转换 倒过来看, 股票是先-后+, 这里是先+后-
    然而, 相较于「0122. 买卖股票的最佳时机 II」有思路1, 简单写法比较困难
思路2: #DP 更简单些
    f(i,isEven) 表示到位置i, 是否偶数(选取) 的最优解
    转移: f(i,True) = max(f(i-1,True), f(i-1,False)+nums[i])
        f(i,False) = max(f(i-1,False), f(i-1,True)-nums[i])
    """
    def maxAlternatingSum(self, nums: List[int]) -> int:
        @cache
        def f(i,isEven):
            if i<0: return -inf if isEven else 0
            if isEven: return max(f(i-1,True), f(i-1,False)+nums[i])
            else: return max(f(i-1,False), f(i-1,True)-nums[i])
        return f(len(nums)-1,True)
    def maxAlternatingSum(self, nums: List[int]) -> int:
        # 展开成数组 DP
        dp = [0, 0]
        for num in nums:
            dp = [ max(dp[0], dp[1]-num), max(dp[1], dp[0]+num) ]
        return max(dp)  # dp[0]

sol = Solution()
result = [
    # sol.maxProfit(prices = [7,1,5,3,6,4]),

    # sol.maxProfit(prices = [1,2,3,0,2]),

    # sol.maxProfit(k = 2, prices = [2,4,1]),
    # sol.maxProfit(k = 2, prices = [3,2,6,5,0,3]),

    # 0121
    # sol.maxProfit([7,1,5,3,6,4]),

    # 0123
    # sol.maxProfit(prices = [3,3,5,0,0,3,1,4]),

    # 0714
    # sol.maxProfit(prices = [1, 3, 2, 8, 4, 9], fee = 2),

    sol.maxAlternatingSum(nums = [4,2,5,3]),
    sol.maxAlternatingSum(nums = [5,6,7,8]),
]
for r in result:
    print(r)
