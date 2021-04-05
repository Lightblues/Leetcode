"""
给定一个整数数组 nums，找出其中所有和为 0 的三元组，不包含重复

输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]

输入：nums = []
输出：[]
"""
class Solution:
    # def threeSum(self, nums: List[int]) -> List[List[int]]:
    def threeSum(self, nums):
        nums = sorted(nums)
        n = len(nums)
        results = []
        # 枚举 a
        for first in range(n):
            # 注意！为了避免重复，需要保证 a 不能和上一次遍历过的 a 不一致
            # 注释掉的是条件满足下继续，但写成下面哪种条件不满足时 continue 可以避免频繁 tab
            # if first==0 or nums[first]!=nums[first-1]:
            #     pass
            if first>0 and nums[first]==nums[first-1]:
                continue

            # 给定了一个 a 之后，下面需要搜索的是在一个排序数字中找到和为 -nums[first] 的两个数
            # 可以用双指针法
            third = n-1     # 将指针 c 指向最右侧
            target23 = -nums[first]
            # 枚举 b
            for second in range(first+1, n):
                # 同样要避免重复
                if second>first+1 and nums[second]==nums[second-1]:
                    continue
                # 注意 b 指向的数是不断增大的，因此 bc 指向的数之和若超过 target，则 c 需要向左移动
                while second<third and nums[second]+nums[third]>target23:
                    third -= 1
                # 退出条件：指针 b 和 c 相遇
                if second == third:
                    break
                if nums[second]+nums[third]==target23:
                    results.append([nums[first], nums[second], nums[third]])
        return results
nums = [-1,0,1,2,-1,-4]
print(Solution().threeSum(nums))