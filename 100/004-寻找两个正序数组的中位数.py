"""
给定两个从小到大（正序）数组，返回中位数

输入：nums1 = [1,2], nums2 = [3,4]
输出：2.50000
解释：合并数组 = [1,2,3,4] ，中位数 (2 + 3) / 2 = 2.5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/median-of-two-sorted-arrays
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

进阶：你能设计一个时间复杂度为 O(log (m+n)) 的算法解决此问题吗？
"""

class Solution:
    # def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
    def findMedianSortedArrays(self, nums1, nums2):
        def getKthNum(k):
            # 返回两个序列中第 k 大的数（从 1 开始）
            index1, index2 = 0, 0   # 在两个数组上向右移动的指针
            while True:
                if index1 == m:
                    return nums2[index2+k-1]
                if index2 == n:
                    return nums1[index1+k-1]
                if k == 1:      #条件 3
                    return min(nums1[index1], nums2[index2])
                # if k == 1:
                #     pass
                # normal case
                step = k//2 - 1
                # 例如 k=10 （第 10 个数），则两个待比较的树相等时，最多可能去除 5 个数（index+4+1）
                # 注意两个比较的数相等时，为了简便起见归于第一类中
                # 若 k=11，则同样最多去除 6 个数
                # 边界条件：k=2 时 newIndex=index 此时某一个 index（1或2）会+1，化归到条件 3
                # k=3 时，一轮迭代后同样可以达到 k-1 的效果，不会死循环
                newIndex1 = min(index1+step, m-1)
                newIndex2 = min(index2+step, n-1)
                if nums1[newIndex1] <= nums2[newIndex2]:
                    k -= newIndex1 - index1 + 1
                    index1 = newIndex1 + 1
                elif nums1[newIndex1] > nums2[newIndex2]:
                    k -= newIndex2 - index2 + 1
                    index2 = newIndex2 + 1

        m, n = len(nums1), len(nums2)
        total = m+n
        if total % 2 == 1:      # odd
            return getKthNum(total//2+1)  # 当 total=3 时返回第 2 大的数
        else:
            return (getKthNum(total//2) + getKthNum(total//2+1)) / 2

nums1 = [1,3]; nums2 = [2]
# nums1 = [2]; nums2 = []
# nums1 = [1,2]; nums2 = [3,4]
sol = Solution()
print(sol.findMedianSortedArrays(nums1, nums2))
