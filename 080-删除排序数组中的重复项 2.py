"""
给定一个增序排列数组 nums ，你需要在 原地 删除重复出现的元素，使得每个元素最多出现两次，返回移除后数组的新长度。

不要使用额外的数组空间，你必须在 原地 修改输入数组 并在使用 O(1) 额外空间的条件下完成。


输入：nums = [1,1,1,2,2,3]
输出：5, nums = [1,1,2,2,3]
解释：函数应返回新长度 length = 5, 并且原数组的前五个元素被修改为 1, 1, 2, 2, 3 。 你不需要考虑数组中超出新长度后面的元素。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        before = None
        count = 0
        index = 0   # 下一个要插入的元素位置
        length = len(nums)
        for i, num in enumerate(nums):
            if num != before:
                before = num
                count = 1
                nums[index] = num
                index += 1
            else:
                if count == 2:
                    length -= 1
                else:
                    nums[index] = num
                    count += 1
                    index += 1
        return length

nums = [1,1,1,2,2,3]
length = Solution().removeDuplicates(nums)
print(nums[:length])