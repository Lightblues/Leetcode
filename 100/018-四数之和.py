"""
输入：nums = [1,0,-1,0,-2,2], target = 0
输出：[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]

输入：nums = [], target = 0
输出：[]


神奇的是增加了下面注释部分的两个剪枝策略之后，运行时间从 992ms 下降到了 92ms？
"""

class Solution:
    # def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
    def fourSum(self, nums, target):
        if len(nums)<4:
            return []

        results = []
        n = len(nums)
        nums.sort()
        for first in range(n-3):
            if first>0 and nums[first]==nums[first-1]: continue
            # 改进：若选定 first 之后，剩余最小的三个数也超过 target 则 break；若剩余最大的三个数也小于 target，则 continue
            if sum(nums[first:first+4])>target: break
            if nums[first] + sum(nums[-3:])<target: continue

            for second in range(first+1, n-2):
                if second>first+1 and nums[second]==nums[second-1]: continue
                # 改进
                if nums[first]+sum(nums[second:second+3])>target: break
                if nums[first]+nums[second]+sum(nums[-2:])<target: continue

                target34 = target-nums[first]-nums[second]
                third, forth = second+1, n-1
                while third<forth:
                    s = nums[third]+nums[forth]
                    if s == target34:
                        results.append([nums[first], nums[second], nums[third], nums[forth]])
                        third += 1
                        while third<forth and nums[third]==nums[third-1]:
                            third += 1
                    elif s > target34:
                        forth -=1
                        while third<forth and nums[forth]==nums[forth+1]:
                            forth -=1
                    else:
                        third += 1
                        while third < forth and nums[third] == nums[third - 1]:
                            third += 1
        return results

nums = [1,0,-1,0,-2,2]; target = 0
print(Solution().fourSum(nums, target))