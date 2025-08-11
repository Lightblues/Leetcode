from typing import *

""" 
https://leetcode.cn/contest/biweekly-contest-148
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
    """
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:

sol = Solution()
result = [
    # sol.maxAdjacentDistance(nums = [1,2,4]),
    sol.minCost(arr = [-7,9,5], brr = [7,-2,-5], k = 2),
]
for r in result:
    print(r)