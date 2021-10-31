"""
给定一个排序数组，你需要在 原地 删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。

不要使用额外的数组空间，你必须在 原地 修改输入数组 并在使用 O(1) 额外空间的条件下完成。

给定 nums = [0,0,1,1,1,2,2,3,3,4],
函数应该返回新的长度 5, 并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4。
你不需要考虑数组中超出新长度后面的元素。


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    # def removeDuplicates(self, nums: List[int]) -> int:
    def removeDuplicates(self, nums):
        if len(nums)==0:
            return 0
        now = nums[0]
        count = 1
        for n in nums[1:]:
            if n != now:
                nums[count] = n
                count += 1
                now = n

        return count

        # i = 0
        # for j in range(len(nums)):
        #     if nums[j] != nums[i]:
        #         i += 1
        #         nums[i] = nums[j]
        # return i + 1

print(Solution().removeDuplicates([1,1,2]))