"""
在排序数组中查找元素的第一个和最后一个位置

给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置和结束位置。
如果数组中不存在目标值 target，返回[-1, -1]。

输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]

输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-first-and-last-position-of-element-in-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

from typing import List
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def find_most_left(left, right):
            most_left = right
            while left<=right:
                mid = (left+right)//2
                if nums[mid]==target:
                    most_left = mid
                    right = mid - 1
                else:
                    left = mid + 1
            return most_left
        def find_most_right(left, right):
            most_right = left
            while left<=right:
                mid = (left+right)//2
                if nums[mid]==target:
                    most_right = mid
                    left = mid + 1
                else:
                    right = mid-1
            return most_right

        left, right = 0, len(nums)-1
        while left <= right:
            mid = (right+left)//2
            if nums[mid]==target:
                left_ = find_most_left(left, mid)
                right_ = find_most_right(mid, right)
                return [left_, right_]
            elif nums[mid]<target:
                left = mid+1
            else:
                right = mid-1
        return [-1, -1]



nums = [5,7,7,8,8,10]; target = 8
print(Solution().searchRange(nums, target))




