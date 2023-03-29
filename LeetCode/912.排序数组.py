#
# @lc app=leetcode.cn id=912 lang=python3
#
# [912] 排序数组
#

# @lc code=start
import random
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def quicksort(l,r):
            if l>=r: return
            idx = partition(l,r)
            quicksort(l,idx-1)
            quicksort(idx+1,r)
        def partition(l,r):
            idx = random.randint(l,r)
            nums[l],nums[idx] = nums[idx],nums[l]
            pivot = nums[l]
            i,j = l,r
            while i<j:
                while i<j and nums[j]>=pivot: j -= 1
                while i<j and nums[i]<=pivot: i += 1
                nums[i],nums[j] = nums[j],nums[i]
            nums[l],nums[i] = nums[i],nums[l]
# @lc code=end

