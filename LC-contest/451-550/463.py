from typing import *
from itertools import accumulate
from functools import reduce
from operator import xor
from math import inf

"""
https://leetcode.cn/contest/weekly-contest-463
1. 按策略买卖股票的最佳时机 - 滑窗 & 前缀和
2. 区间乘法查询后的异或 I
3. 删除可整除和后的最小数组和, 删除满足子区间和能被 k 整除的那些, 求剩余最小和
    需要细致梳理最优情况, 之前错误尝试了贪心! 有问题
    正确应该建模为 DP; 理清之后代码异常简单; NOTE 考虑边界情况
4. 区间乘法查询后的异或 II 每次对于 l:r:k 跳步元素 *=v; 最最终数组状态
    根据这里 k 的大小, 分别适合 商分数组 (差分) & 暴力模拟两种思路
    -- 解法就是根据 k 的大小来选择合适的算法, 结合起来 👍 少见的题目
Easonsi @2026 """


class Solution:
    """ 3652. 按策略买卖股票的最佳时机 #4 
给定 prices, strategy (-1/0/1) 数组, 再给一个偶数 k, 可以将长 k 的子数组前一半变为 0 后一半变为 1; 要求最大化点积.
限制: n 1e5
方法 1: 前缀和
    滑窗将数组划分为 3 部分, 每次求三部分的和 -- 前缀和!
方法 2: 定长滑动窗口
    维护滑窗过程中的变化量, 比较细节, 参见 ling
https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-using-strategy/solutions/3755330/liang-chong-fang-fa-qian-zhui-he-ding-ch-uq98/
"""
    def maxProfit(self, prices: List[int], strategy: List[int], k: int) -> int:
        s = list(accumulate(prices, initial=0))
        t = list(accumulate((i*j for i,j in zip(prices, strategy)), initial=0))
        k2 = k//2
        ans = t[-1]
        # for i in range(k,len(prices)+1):  # NOTE: 考虑前缀和的计算, 这里统一将 index+1
        #     ans = max(ans, t[i-k] + t[-1]-t[i] + s[i]-s[i-k2])
        for i in range(k-1,len(prices)):  # 或者之前的写法
            ans = max(ans, t[i-k+1] + t[-1]-t[i+1] + s[i+1]-s[i-k2+1])
        return ans

    """ 3653. 区间乘法查询后的异或 I #4 
对于每次查询 (l,r,k,v), 对于数组 l:r:k (k 为步长) 范围的数字都 *=k. 问最后得到的数组的异或和
限制: n 1e3; q 1e3
    """
    def xorAfterQueries(self, nums: List[int], queries: List[List[int]]) -> int:
        MOD = 10**9+7
        for l,r,k,v in queries:
            for i in range(l,r+1,k):
                nums[i] = (nums[i]*v) % MOD
        return reduce(xor, nums)

    """ 3654. 删除可整除和后的最小数组和 #5
对于一个 nums, 给定 k, 每次可选择和可被 k 整除子数组删除, 最小化剩余和
限制: n 1e5
尝试 1: 贪心的, 删除连续的能被 k 整除的区间
    问题: 假设可删除的区间相交 (但不包含), 就有问题!!
方法 1: 动态规划 + 前缀和
    首先, 注意到若 k=2, 则对于子区间 [1,2,2,3] 来说, 分两次删和整个删除是等价的! -- 因此可以不考虑顺序
        PS: 注意这是对于包含关系而言的! "尝试 1" 的错误即在于没考虑相交!
    考虑 f[i] 表示前缀剩余最小和, 考虑:
        - 不删除 i: 转为 f[i-1]
        - 删除: 考虑所有前缀和同余的位置, 取他们的 minF -- NOTE: 这是和贪心的差异!
    复杂度: O(n+k)
https://leetcode.cn/problems/minimum-sum-after-divisible-sum-deletions/solutions/3755268/dong-tai-gui-hua-qian-zhui-he-pythonjava-nia8/
    """
    def minArraySum(self, nums: List[int], k: int) -> int:
        pass
        # 错误的尝试: 贪心
        # acc = 0
        # st = []
        # reminders = set()
        # for x in nums:
        #     nr = (acc+x) % k
        #     if nr == 0:
        #         acc = 0
        #         st = []
        #         reminders = set()
        #         continue
        #     if nr in reminders:
        #         while st and st[-1][0] != nr:
        #             acc -= st[-1][1]
        #             reminders.remove(st[-1][0])
        #             st.pop()
        #         if x < st[-1][1]:
        #             acc -= st[-1][1] - x
        #             st[-1][1] = x
        #     else:
        #         acc += x
        #         reminders.add(nr)
        #         st.append([nr, x])
        # return acc
    
    def minArraySum(self, nums: List[int], k: int) -> int:
        min_f = [inf] * k
        min_f[0] = 0  # NOTE: 对应可以完整消除!
        f = 0
        r = 0
        for x in nums:
            r = (r+x) % k
            f = min(f + x, min_f[r])
            min_f[r] = f  # min(min_f[r], f)
        return f

    """ 3655. 区间乘法查询后的异或 II #8
数据范围拓展到 n,q 1e5
思路 1: 上面的暴力模拟
    复杂度: 整体 O(nq/k)
思路 2: 差分数组（商分数组）
    当 k=1 的时候, 类似差分数组, 对于 d[l] * v; d[r+1] / v (乘逆元)
    当 k>1 的时候, 可以转为维护 k 个商分数组
    复杂度: 1. 处理的时候, log(M) 计算逆元, 其中 M 为 MOD, 整体 O(q logM); 2. 得到结果, 需要处理 k 个长n 的商分数组, 因此 O(nk + q logM)
方法 1: 结合上面的两个思路!
    - 思路 1 在 k比较大的时候更快; 思路 2 适合 k 比较小的情况!
    - 比较两者复杂度, 我们可以根据 k 和 B=sqrt(q) 的关系来选择那种算法!
    整体复杂度为 O(nq/B + nB + qlogM) -- 根据我们的选择, 最小值为 O(n sqrt(q) + qlogM)
    """
    def xorAfterQueries(self, nums: List[int], queries: List[List[int]]) -> int:
        # TODO: 参考 ling
        MOD = 1_000_000_007
        n = len(nums)
        B = isqrt(len(queries))
        diff = [None] * B

        for l, r, k, v in queries:
            if k < B:
                # 懒初始化
                if not diff[k]:
                    diff[k] = [1] * (n + k)
                diff[k][l] = diff[k][l] * v % MOD
                r = r - (r - l) % k + k
                diff[k][r] = diff[k][r] * pow(v, -1, MOD) % MOD  # NOTE: 求逆元
            else:
                for i in range(l, r + 1, k):
                    nums[i] = nums[i] * v % MOD

        for k, d in enumerate(diff):
            if not d:
                continue
            for start in range(k):
                mul_d = 1
                for i in range(start, n, k):
                    mul_d = mul_d * d[i] % MOD
                    nums[i] = nums[i] * mul_d % MOD

        return reduce(xor, nums)

sol = Solution()
result = [
    # sol.maxProfit(prices = [4,2,8], strategy = [-1,0,1], k = 2),
    # sol.xorAfterQueries(nums = [2,3,1,5,4], queries = [[1,4,2,3],[0,2,1,2]]),
    # sol.xorAfterQueries([780], [[0,0,1,13],[0,0,1,17],[0,0,1,9],[0,0,1,18],[0,0,1,16],[0,0,1,6],[0,0,1,4],[0,0,1,11],[0,0,1,7],[0,0,1,18],[0,0,1,8],[0,0,1,15],[0,0,1,12]]),
    sol.minArraySum(nums = [1,1,1], k = 2),
    sol.minArraySum(nums = [3,1,4,1,5], k = 3),
    sol.minArraySum([58,68,57,71,52,6,40,22,13,29,26,17,47,31,51,73,59,69,37,14], 34),
]
for r in result:
    print(r)
