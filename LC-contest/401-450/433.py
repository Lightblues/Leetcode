from itertools import accumulate
from math import comb, inf
from functools import cache
from typing import *


""" 
https://leetcode.cn/contest/weekly-contest-433

Easonsi @2025 """
class Solution:
    """ 3427. 变长子数组求和 """
    def subarraySum(self, nums: List[int]) -> int:
        acc = list(accumulate(nums, initial=0))
        ans = 0
        for i,x in enumerate(nums):
            start = max(0, i-x)
            ans += acc[i+1] - acc[start]
        return ans
    
    """ 3428. 最多 K 个元素的子序列的最值之和 #medium 对于一个数字, 求所有长度不大于k的子数组的最大+最小值之和的和
限制: n 1e5; n 100
思路1: 排序
    """
    def minMaxSums(self, nums: List[int], k: int) -> int:
        # TLE
        MOD = 10**9 + 7
        nums.sort()
        n = len(nums)
        ans = 0
        @cache
        def f(l: int) -> int:
            # #method to get 0,1,...l from l items
            acc = 0
            mx = min(l, k-1)
            for i in range(mx+1):
                acc += comb(l,i)
            return acc % MOD
        for i,x in enumerate(nums):
            ans += ( f(i) + f(n-i-1) ) * x
            ans %= MOD
        return ans
    
    """ 3429. 粉刷房子 IV #medium 用三种颜色刷偶数的房子, 要求: 1) 相邻颜色不同; 2) 距离两端相等距离的颜色不同. cost[i][j] 表示将第i个房子刷成颜色j的代价, 求最小代价
限制: n 1e5
思路1: #DP
    记 f[i,j,k] 表示将位置i刷成j, 对偶位置刷为k的最小代价
    转移: f[i+1,j,k] = mn(i, j',k') + cost[i+1,j] + cost[n-i-2,k]
        其中 mn(i, j',k') 满足 j' != j, k' != k, 且 j' != k'
    """
    def minCost(self, n: int, cost: List[List[int]]) -> int:
        f = [[0]*3 for _ in range(3)]
        def mn(j,k):
            m = inf
            for jj in range(3):
                if jj==j: continue
                for kk in range(3):
                    if kk==k or kk==jj: continue
                    m = min(m, f[jj][kk])
            return m
        for i in range(n//2):
            nf = [[inf]*3 for _ in range(3)]
            for j in range(3):
                for k in range(3):
                    if j==k: continue
                    nf[j][k] = min(nf[j][k], mn(j,k) + cost[i][j] + cost[n-i-1][k])
            f = nf
        return min(f[i][j] for i in range(3) for j in range(3))

    """ 3430. 最多 K 个元素的子数组的最值之和 #hard 相较于 3428, 限制是子数组 -- 也即对于数组的所有长度不大于k的子数组, 计算最大/最小值之和的和
限制: n, k 8e4
思路1: #贡献法
    对于数组中的每个元素, 计算其贡献最大/最小的次数. 
        例如, 对于 [1,2,3], 计算每个元素作为最大值的贡献, 分别是 [1], [1,2], [2,3] 因此贡献次数为 1/2/2
    先不考虑限制 k, 则贡献的次数取决于元素 x 作为max的左右边界!
 """
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:


    
sol = Solution()
result = [
    # sol.subarraySum(nums = [2,3,1]),
    # sol.minMaxSums(nums = [1,2,3], k = 2),
    # sol.minMaxSums(nums = [5,0,6], k = 1),
    sol.minCost(n = 4, cost = [[3,5,7],[6,2,9],[4,8,1],[7,3,5]]),
    sol.minCost(n = 6, cost = [[2,4,6],[5,3,8],[7,1,9],[4,6,2],[3,5,7],[8,2,4]]),
]
for r in result:
    print(r)
