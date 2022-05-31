"""
实现获取 下一个排列 的函数，算法需要将给定数字序列重新排列成字典序中下一个更大的排列。
如果不存在下一个更大的排列，则将数字重新排列成最小的排列（即升序排列）。
必须 原地 修改，只允许使用额外常数空间。

输入：nums = [1,2,3]
输出：[1,3,2]

输入：nums = [3,2,1]
输出：[1,2,3]

输入：nums = [1,1,5]
输出：[1,5,1]

输入：nums = [1]
输出：[1]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/next-permutation
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

---
[1 2 3]
[1 3 2]
[2 1 3]
[2 3 1]
[3 1 2]
[3 2 1]

"""

from typing import List
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """ 和下面的是一样的思路, 这里写得太烦了
        Do not return anything, modify nums in-place instead.
        https://leetcode.cn/problems/next-permutation/solution/xia-yi-ge-pai-lie-by-leetcode-solution/
        """
        l = len(nums)
        def sort(start,end):
            # 对 nums[start:end] 实现原地排序
            for i in range(start, end):
                idx_min = i
                for j in range(i+1, end):
                    if nums[j]<nums[idx_min]:
                        idx_min = j
                if idx_min != i:
                    nums[i], nums[idx_min] = nums[idx_min], nums[i]
        # sort(0, len(nums))
        # print(nums)
        def is_reverse(start, end):
            # 判断 nums[start:end] 是否逆序
            for i in range(start, end-1):
                if nums[i]<nums[i+1]:
                    return False
            return True
        # print(is_reverse(1,3))

        # flag = False
        for i in range(l-2, -1, -1):
            if is_reverse(i, l):
                continue
            # 若不为逆序，找到 [i+1:] 最比 nums[i] 大的元素中最小的那一个，然后对 [i+1:] 排序
            idx = i+1
            for j in range(i+2, l):
                if nums[idx] > nums[j] > nums[i]:
                    idx = j

            nums[idx], nums[i] = nums[i], nums[idx]
            sort(i+1, l)
            return
        # 若未发生上述操作，说明已是最大的排列
        # if not flag:
        #     nums.sort()
        nums.sort()

    def nextPermutation2(self, nums: List[int]) -> None:
        """ Do not return anything, modify nums in-place instead. """
        # https://leetcode.cn/problems/next-permutation/solution/xia-yi-ge-pai-lie-by-leetcode-solution/
        l = len(nums)

        # 从后向前，找出第一个非逆序的元素
        i = l-2
        while i>=0 and nums[i]>=nums[i+1]:
            i -= 1
        """
        两种情况
        1. i>=0，此时需要在 [i+1:] 中找到大于 nums[i] 的元素中最小的那一个，设指标为 j；然后需要（1）交换 ij；（2）将 [i+1:] 逆序，此时设置 left=i+1
        2. i=-1，说明完全逆序（最大），下面的 left, right 指针为数组头尾，注意此时 left=i+1 仍满足
        """
        if i>=0: # 注意 [i+1:] 是逆序的
            j = i+1
            while j<l-1 and nums[i]<nums[j+1]:
                j += 1
            nums[j], nums[i] = nums[i], nums[j]

        # 然后需要对 [i+1:n] 部分进行所谓排序，但实际上这部分是降序的，所以进行一次反转即可
        left, right = i+1, l-1
        while left<right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
        return



        # 若未发生上述操作，说明已是最大的排列
        # if not flag:
        #     nums.sort()



# nums = [1,2,3]
# nums = [3,2,1]
# nums = [1,3,2]
# nums = [4,2,0,2,3,2,0]
# [4,2,0,3,0,2,2]
nums = [5,1,1]
Solution().nextPermutation2(nums)
print(nums)