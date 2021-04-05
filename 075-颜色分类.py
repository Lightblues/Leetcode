"""
给定一个包含红色、白色和蓝色，一共 n 个元素的数组，原地对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。
此题中，我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。


输入：nums = [2,0,2,1,1,0]
输出：[0,0,1,1,2,2]


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sort-colors
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        from collections import defaultdict
        d = defaultdict(int)
        for n in nums:
            d[n] += 1
        count = 0
        for n in [0, 1, 2]:
            for i in range(d[n]):
                nums[count] = n
                count += 1
    """
    利用两个指针，分别指向下一个 0 或者 2 要存放的位置
    再用一个循环指针
    终止条件是循环指针 i 与 p2 相遇
    """
    def sortColors_2pointer(self, nums: List[int]) -> None:
        n = len(nums)
        p0 = 0  # 下一个要放 0 的位置
        p2 = n-1    # 下一个放 2 的位置
        # 循环指针
        i = 0
        while i <= p2:
            num = nums[i]
            if num == 0:
                nums[p0], nums[i] = nums[i], nums[p0]
                p0 += 1
            if num == 2:
                nums[p2], nums[i] = nums[i], nums[p2]
                p2 -= 1
            i += 1


nums = [2,0,2,1,1,0]
Solution().sortColors_2pointer(nums)
print(nums)