"""
给你两个按 非递减顺序 排列的整数数组 nums1 和 nums2，另有两个整数 m 和 n ，分别表示 nums1 和 nums2 中的元素数目。
请你 合并 nums2 到 nums1 中，使合并后的数组同样按 非递减顺序 排列。
原地操作

输入：nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
输出：[1,2,2,3,5,6]
解释：需要合并 [1,2,3] 和 [2,5,6] 。
合并结果是 [1,2,2,3,5,6] ，其中斜体加粗标注的为 nums1 中的元素。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/merge-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        i1, i2 = m-1, n-1
        j = m+n-1
        while j >= 0:
            # 判断边界条件：注意nums2空了即可结束，num1空了则将nums2复制过去
            # if i2 < 0: break
            # if i1 < 0:
            #     pass
            if i1==j:
                return
            if i2==j:
                for i in range(j, -1, -1):
                    nums1[i] = nums2[i]
                return
            # 正常循环
            if nums1[i1] > nums2[i2]:
                nums1[j] = nums1[i1]
                i1 -= 1
            else:
                nums1[j] = nums2[i2]
                i2 -= 1
            j -= 1

# nums1 = [1,2,3,0,0,0]
# m = 3
# nums2 = [2,5,6]
# n = 3    

nums1 = [0]
m = 0
nums2 = [1]
n = 1
Solution().merge(nums1, m, nums2, n)
print(nums1)