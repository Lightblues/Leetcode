"""
给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现了三次。找出那个只出现了一次的元素。
说明：
你的算法应该具有线性时间复杂度。 你可以不使用额外空间来实现吗？

输入: [0,1,0,1,0,1,99]
输出: 99
"""

class Solution:
    # 方法一：HashSet
    def singleNumber(self, nums):
        return (3 * sum(set(nums)) - sum(nums)) // 2

    # 方法二：HashMap
    def singleNumber2(self, nums):
        from collections import Counter
        counter = Counter(nums)
        for k, v in counter.items():
            if v==1:
                return k

    # 方法三：位运算符：NOT，AND 和 XOR
    def singleNumber3(self, nums):
        seen_once, seen_twice = 0, 0
        for num in nums:
            seen_once = ~seen_twice & (seen_once ^ num)
            seen_twice = ~seen_once & (seen_twice ^ num)
        return seen_once


nums = [0,1,0,1,0,1,99]
print(Solution().singleNumber3(nums))