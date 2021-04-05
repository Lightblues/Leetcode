
"""
在升序数组中查找 target 复杂度为 O(log(n))
现在给的是发生了一次「旋转」的（原本升序）数组 nums，例如 [0,1,2,4,5,6,7] 在下标 3 处旋转 [4,5,6,7,0,1,2]
目标是在 nums 中进行检索
nums 中的每个值都 独一无二

输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4

输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
"""

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        base = nums[0]  # 由于旋转，假设在 k 处旋转，则 k 左侧均 >=base，右侧均 <=base
        greater_or_smaller = target>base
        left, right = 0, n-1
        for i in [left, right]:
            if nums[i] == target:
                return i
        while left<right:
            mid = (left+right)//2
            # mid = max(mid, left+1)
            if mid == left:
                break
            mid_num = nums[mid]
            if mid_num==target:
                return mid
            if mid_num>base:    # k>mid
                if greater_or_smaller:
                    if mid_num<target:
                        left = mid
                    else:
                        right = mid
                else:
                    left = mid
            else:
                if greater_or_smaller:
                    right = mid
                else:
                    if mid_num<target:
                        left = mid
                    else:
                        right = mid
        return -1

        # 标答，更清晰些
        # if not nums:
        #     return -1
        # l, r = 0, len(nums) - 1
        # while l <= r:
        #     mid = (l + r) // 2
        #     if nums[mid] == target:
        #         return mid
        #     if nums[0] <= nums[mid]:
        #         if nums[0] <= target < nums[mid]:
        #             r = mid - 1
        #         else:
        #             l = mid + 1
        #     else:
        #         if nums[mid] < target <= nums[len(nums) - 1]:
        #             l = mid + 1
        #         else:
        #             r = mid - 1
        # return -1



# nums = [4,5,6,7,0,1,2]
# target = 3
# nums = [1]; target = 0
nums = [5,1,2,3,4]; target=1
print(Solution().search(nums, target))