"""
假设按照升序排序的数组在预先未知的某个点上进行了旋转。
( 例如，数组[0,0,1,2,2,5,6]可能变为[2,5,6,0,0,1,2])。
编写一个函数来判断给定的目标值是否存在于数组中。若存在返回true，否则返回false。


这是 搜索旋转排序数组 的延伸题目，本题中的 nums  可能包含重复元素。【之前的 033 中元素的互不相同的】
这会影响到程序的时间复杂度吗？会有怎样的影响，为什么？


输入: nums = [2,5,6,0,0,1,2], target = 0
输出: true

输入: nums = [2,5,6,0,0,1,2], target = 3
输出: false
"""
from typing import List
class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        if not nums:
            return False
        while len(nums)>1 and nums[0] == nums[-1]:
            nums.pop()

        base = nums[0]

        left, right = 0, len(nums)-1
        while left <= right:
            mid = (left + right)//2
            if nums[mid] == target:
                return True
            if nums[mid] >= base:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return False

# nums = [2,5,6,0,0,1,2]; target = 3
nums = [1,3,5]; target = 1
print(Solution().search(nums, target))