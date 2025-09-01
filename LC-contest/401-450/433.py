from itertools import accumulate
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
    
    """ 3428. 最多 K 个元素的子序列的最值之和 """
    def minMaxSums(self, nums: List[int], k: int) -> int:
        
        nums.sort()

    
    

    
sol = Solution()
result = [
    sol.subarraySum(nums = [2,3,1]),
]
for r in result:
    print(r)
