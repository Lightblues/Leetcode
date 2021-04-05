
"""
给你一个未排序的整数数组 nums ，请你找出其中没有出现的最小的正整数。

输入：nums = [3,4,-1,1]
输出：2

输入：nums = [7,8,9,11,12]
输出：1
"""
from typing import List

class Solution:
    # 想法是将所有出现在 [1,n] 范围内的数字「归位」，即 nums[i-1]=i；这样第二次遍历仅需顺序找到不满足此公式的数即可。
    # 需要注意的是所更换的数字需要二次交换，即对于第 i 位的 nums[i]=num，其指向的元素 nums[num-1] 仍是在 [1,n]，则需继续交换。注意避免死循环，即若 nums[num-1]=num，则不需要进行交换
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)

        for i in range(n):
            # num = nums[i]
            # # 若是 i 位置的元素 num<=n，则要将其放到 num 位置上，也即交换；
            # # 若交换的数字 nums[num] 仍然 <= 且在另外一个位置上，需要继续交换
            # while 0<num<=n and num!=i+1:
            #     num_to_swep = nums[num-1]
            #     if num_to_swep != num-1:    # 避免循环
            #         nums[num-1], nums[i] = num, num_to_swep
            #         num = num_to_swep
            #     else:
            #         break

            # 简化成一行
            # 需要在（1）nums[i] 属于 [1,n] 范围内；（2）nums[i]与其指向位置的值不相等时进行交换。其中第二点是为了避免死循环。
            while 0<nums[i]<=n and nums[nums[i]-1] != nums[i]:
                nums[nums[i] - 1], nums[i] = nums[i], nums[nums[i]-1]
        i = 0
        while i<n:
            if nums[i] != i+1:
                break
            i += 1
        return i+1

    # 用负数表示元素存在；为此，先将所有不在 [1,n] 范围内的数变为 n+1（或其他正数）；
    # 第二次遍历，将在 [1,n] 范围内的数字所对应的列表元素变为负数；
    # 第三次，找到第一个非负的就是所求
    def firstMissingPositive2(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            if nums[i] <= 0:
                nums[i] = n+1
        for i in range(n):
            if abs(nums[i]) <= n and nums[abs(nums[i])-1] > 0:
                nums[abs(nums[i]) - 1] *= -1
        for i in range(n):
            if nums[i] > 0:
                return i+1
        return n+1

# nums = [3,-1,2,1]
nums = [3,4,-1,1]
print(Solution().firstMissingPositive2(nums))


