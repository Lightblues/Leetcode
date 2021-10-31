# coding=utf-8
"""
给定整数数组 nums 和整数目标值 target，找出和为目标值的两个整数，返回下标

输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/two-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
nums = [2,7,11,15]
target = 9

class Solution:
    # def twoSum(self, nums: List[int], target: int) -> List[int]:
    def twoSum(self, nums, target):
        partner = {}
        for index, num in enumerate(nums):
            if target-num in partner:
                return index, partner[target-num]
            partner[num] = index
s = Solution()
print(s.twoSum(nums, target))