"""
输入: nums = [-1,0,3,5,9,12], target = 9
输出: 4
解释: 9 出现在 nums 中并且下标为 4

输入: nums = [-1,0,3,5,9,12], target = 2
输出: -1
解释: 2 不存在 nums 中因此返回 -1
"""

from typing import List
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)-1
        while left <= right:
            pivot = (left+right)//2
            if nums[pivot]==target:
                return pivot
            elif nums[pivot]<target:
                left = pivot+1
            else:
                right = pivot-1
        return -1