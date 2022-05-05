from typing import List, Optional
import collections
import math
import bisect
import heapq
import functools, itertools
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)

from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 2006. 差的绝对值为 K 的数对数目 """
    def countKDifference(self, nums: List[int], k: int) -> int:
        counter = collections.Counter(nums)
        res = 0
        for key, val in counter.items():
            if key-k in counter:
                res += val*counter[key-k]
        return res
    
    """ 2007. 从双倍数组中还原原数组
对于一个数组的所有数字变为双倍, 混入原数组. 现在要求还原数字.

思路: Counter 之后从大到小遍历.
"""
    def findOriginalArray(self, changed: List[int]) -> List[int]:
        if len(changed) % 2 == 1: return []
        counter = collections.Counter(changed)
        result = []
        for key in sorted(list(counter.keys()), reverse=True):
            v = counter[key]
            if v==0: continue
            if key%2==1: return []
            # 特殊: 0 的双倍还是 0
            if key==0:
                if v%2 == 1: return []
                result += [0] * (v//2)
                continue
            half = key//2
            if half not in counter or counter[half]<v: return []
            counter[half] -= v
            result += [half] * v
        return result
        
    """ 2008. 出租车的最大盈利
出租车从 1开到n, 给定一组 `rides[i] = [start_i, end_i, tip_i]` 表示可以接到的单子, 每单的价格为 `end_i - start_i + tip_i`, 要求一趟下来最多获得多少钱.
复杂度 n 为 1e5, rides 长度 3e4

思路: DP
用 dp[s] 表示从时刻 s 开始接单的最大收益.
因此, 对于 rides 基于 start 逆序排序. 对于第i个交易 `dp[start] = max(dp[start], dp[end] + fee_i)`.
存储方式1: (超时了, 按理说复杂度应该还行) 考虑到不连续性, 对于dp key 采用排序数组, 然后对于有值的那部分用字典存下来 (bisect 查找)
存储方式2: 更为经典的连续存储方案, 通过 `dp[start] = dp[start+1]` 进行初始化
"""
    def maxTaxiEarnings_0(self, n: int, rides: List[List[int]]) -> int:
        # 添加边界
        keys = [n+1]
        values = {n+1: 0}

        rides.sort(reverse=True)
        for s,e, tip in rides:
            # 注意可以在同一点结束并开始下一单, 因此不是 e+1
            idx1 = bisect.bisect_left(keys, e)
            fee1 = values[keys[idx1]] + e-s+tip
            idx2 = bisect.bisect_left(keys, s)
            fee2 = values[keys[idx2]]
            if s not in keys:
                # idx = bisect.bisect(keys, s)
                bisect.insort(keys, s)
                values[s] = max(fee1, fee2)
            else:
                values[s] = max(fee1, fee2, values[s])
        return values[keys[0]]

    
    def maxTaxiEarnings(self, n: int, rides: List[List[int]]) -> int:
        grouped = collections.defaultdict(list)
        for s,e,tip in rides:
            grouped[s].append((e, tip))
        
        dp = [0] * (n+1)
        # start 范围为 1~n-1
        for start in range(n-1, 0, -1):
            dp[start] = dp[start+1]
            for end, tip in grouped[start]:
                dp[start] = max(dp[start], dp[end] + end-start+tip)
        return dp[1]
    
    """ 2009. 使数组连续的最少操作数
给定一个长度为L的数组, 每次可以对于数组的任意一个元素替换为任意的值, 要求最少替换次数, 是的数组中的元素构成连续的L的整数. 例如 nums = [4, 2, 5, 3] 是 连续的

思路1: 排序+双指针
注意到出现多次的数字一定需要被修改, 因此取 unique 然后对于数组排序. 用 left 指针从左往右扫描, 尝试移动 right 指针, 满足 `nums[right] - nums[left] < L`. 
这样对于每一个 left 位置, 原数组中保持不变的index区间为 [left, right], 每次更新答案 `ans = min(ans, L-(right-left+1))`
see [here](https://leetcode-cn.com/problems/minimum-number-of-operations-to-make-array-continuous/solution/on-zuo-fa-by-endlesscheng-l7yi/) 对于 right 如果不用双指针还可以直接 bisect
"""
    def minOperations(self, nums: List[int]) -> int:
        nNums = len(nums)
        # 注意需要去重
        unique = sorted(set(nums))
        n = len(unique)
        r = 0
        ans = nNums
        for l in range(n):
            while r<n-1 and unique[r+1]-unique[l]<nNums:
                r += 1
            ans = min(ans, nNums-(r-l+1))
        return ans
    
sol = Solution()
result = [
    # sol.findOriginalArray(changed = [1,3,4,2,6,8]),
    # sol.findOriginalArray(changed = [6,3,0,1]),
    
    # sol.maxTaxiEarnings(n = 5, rides = [[2,5,4],[1,5,1]]),
    # sol.maxTaxiEarnings(n = 20, rides = [[1,6,1],[3,10,2],[10,12,3],[11,12,2],[12,15,2],[13,18,1]]),
    
    sol.minOperations(nums = [4,2,5,3]),
    sol.minOperations(nums = [1,2,3,5,6]),
    sol.minOperations([8,5,9,9,8,4]),
    sol.minOperations([41,33,29,33,35,26,47,24,18,28]),

]
for r in result:
    print(r)
