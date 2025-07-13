from typing import *
from collections import Counter

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-143

Easonsi @2025 """
class Solution:
    """  """
    def smallestNumber(self, n: int, t: int) -> int:
        pass

    """ 对于一个数组, 需要操作 o 次, 每次选择一个不同的位置, 增加 [-k, k]. 问能得到的最大频数 
限制: n 1e5; x 1e9
思路1: #滑动窗口 + #同向三指针
    考虑最终freq最大的数字为 x, 可以分为两种情况: x 不存在 / 存在 于原本数组中的
    - x 不存在: 可以用滑动窗口
        注意到, 此时答案必然 <=o, 可以维护一个宽度为 2k 的窗口, 计算最大长度!
    - x 存在于原数组: 同向三指针
        遍历x, 然后维护 left, right 分别统计 x-k, x+k 的边界
"""
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        freq = Counter(nums)
        freq = sorted(freq.items())
        # 
        ans = 0; n = len(freq)
        l = r = 0; cnt = 0
        for m, (x, c) in enumerate(freq):
            # cnt += c  # 在 r 已经算进去了
            while freq[l][0] < x-k:
                cnt -= freq[l][1]
                l += 1
            while r < n and freq[r][0] <= x+k:
                cnt += freq[r][1]
                r += 1
            ans = max(ans, min(cnt, c + numOperations))
        # 
        if ans > numOperations: return ans
        # 
        l = cnt = 0
        for x,c in freq:
            cnt += c
            while freq[l][0] < x-2*k:
                cnt -= freq[l][1]
                l += 1
            ans = max(ans, min(cnt, numOperations))
        return ans


    """ 对于没有0的整数, 返回 >=n 的, 且各位数乘积可以被 t 整除的数字, 找不到则 -1.
限制: len(n) 1e5; t 1e14
    """
    def smallestNumber(self, n: int, t: int) -> int:
        pass


sol = Solution()
result = [
    sol.maxFrequency(nums = [1,4,5], k = 1, numOperations = 2),
    sol.maxFrequency(nums = [5,11,20,20], k = 5, numOperations = 1),
    sol.maxFrequency([9], 0,0)
]
for r in result:
    print(r)
