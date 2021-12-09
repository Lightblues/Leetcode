"""
给定一个整数数组 nums，其中恰好有两个元素只出现一次，其余所有元素均出现两次。 找出只出现一次的那两个元素。你可以按 任意顺序 返回答案。


输入：nums = [1,2,1,3,2,5]
输出：[3,5]
解释：[5, 3] 也是有效的答案。
"""
from typing import List
class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        from collections import Counter
        counter = Counter(nums)
        res = []
        for k, v in counter.items():
            if v == 1:
               res.append(k)
        return res

    def singleNumber2(self, nums: List[int]):
        import functools
        ret = functools.reduce(lambda x,y: x^y, nums)
        div = 1
        while div ^ ret ==0:
            div <<= 1
        a, b = 0, 0
        for n in nums:
            if n & div:
                a ^=n
            else:
                b ^= n
        return [a,b]

nums = [1,2,1,3,2,5]
print(Solution().singleNumber2(nums))
