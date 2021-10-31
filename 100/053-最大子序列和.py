"""
给定一个整数数组 nums，找出其中具有最大和的连续自数组，返回最大和

输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
"""
from typing import List
class Solution:
    """
    dp 记录「以 i 元素结尾的最大和」，然后返回 max(dp) 即可
    更新公式：dp[i] = max(dp[i-1]+nums[i], nums[i])
    """
    def maxSubArray(self, nums: List[int]) -> int:
        dp = [0 for _ in range(len(nums))]
        dp[0] = nums[0]
        for i in range(1, len(nums)):
            dp[i] = max(dp[i-1]+nums[i], nums[i])
        return max(dp)
    
    """
    上述空间复杂度为 O(N)
    事实上由于更新 dp 过程中仅需要前一个元素即可，而 max 操作也可分步进行，因此可将其减少为 O(1)
    「滚动数组」
    """

    def maxSubArray2(self, nums: List[int]) -> int:
        pre = 0
        max_temp = nums[0]
        for num in nums:
            pre = max(pre+num, num)
            max_temp = max(max_temp, pre)
        return max_temp


nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(Solution().maxSubArray2(nums))

