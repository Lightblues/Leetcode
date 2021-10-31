
"""
给定一个数组 nums 和一个 target，找出其中的一个三元组，要求之和与 target 距离最小，返回这个和

输入：nums = [-1,2,1,-4], target = 1
输出：2
解释：与 target 最接近的和是 2 (-1 + 2 + 1 = 2) 。
"""



class Solution:
    # def threeSumClosest(self, nums: List[int], target: int) -> int:
    def threeSumClosest(self, nums, target):
        result = int(9999)
        diff = 9999

        n = len(nums)
        nums.sort()

        def update(threeSum):
            nonlocal diff, result
            if abs(threeSum - target) < diff:
                diff = abs(threeSum - target)
                result = threeSum
        # 枚举 a
        for first in range(n):
            if first>0 and nums[first]== nums[first-1]:
                continue
            # third = n-1
            # # 使用双指针枚举 b 和 c
            # for second in range(first+1, n):
            #     if second>first+1 and nums[second]==nums[second-1]:
            #         continue
            #     while third>second and nums[first]+nums[second]+nums[third] > target:
            #         third -= 1
            #     if second == third:
            #         update(nums[first]+nums[second]+nums[second+1])
            #         break
            #     update(nums[first]+nums[second]+nums[third])
            #     if third == second+1:
            #         break
            #     # third -= 1
            #     update(nums[first]+nums[second]+nums[third-1])

            second, third = first+1, n-1
            while second < third:
                s = nums[first]+nums[second]+nums[third]
                if s == target:
                    return s
                update(s)
                if s > target:
                    third -= 1
                    while third>second and nums[third]==nums[third+1]:
                        third -= 1
                else:
                    second += 1
                    while second<third and nums[second]==nums[second-1]:
                        second += 1
        return result






nums = [0,1,2]; target = 0
# nums = [-1,2,1,-4]; target = 1
print(Solution().threeSumClosest(nums, target))