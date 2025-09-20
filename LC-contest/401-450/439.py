from typing import *
from collections import *

""" 
https://leetcode.cn/contest/weekly-contest-439
Easonsi @2025 """
class Solution:
    """ 3471. 找出最大的几近缺失整数 #easy 分类讨论, 边界条件需要注意
https://leetcode.cn/problems/find-the-largest-almost-missing-integer/solutions/3591774/on-zuo-fa-nao-jin-ji-zhuan-wan-pythonjav-y0q3/
"""
    def largestInteger(self, nums: List[int], k: int) -> int:
        if k==len(nums):
            return max(nums)
        if k==1:
            cand = [v for v,c in Counter(nums).items() if c==1]
            return max(cand) if cand else -1
        ans = -1
        if nums[0] not in nums[1:]: ans = max(ans, nums[0])
        if nums[-1] not in nums[:-1]: ans = max(ans, nums[-1])
        return ans
    
    """ 3472. 至多 K 次操作后的最长回文子序列 #medium 每次操作可以把一个字符替换为相邻字符 (z可以变为a), 问k次操作后得到的最长回文子串
限制: n 200; k 200
    """
    def longestPalindromicSubsequence(self, s: str, k: int) -> int:
        s = [ord(c)-ord('a') for c in s]
        n = len(s)
        ans = 1
        def calc_d(l,r):
            return min(abs(l-r), 26-abs(l-r))
        for center in range(1,n-1):
            remain = k
            for i in range(1, min(center+1, n-center)):
                l,r = s[center-i], s[center+i]
                d = calc_d(l,r)
                if d > remain: break
                remain -= d
                ans = max(ans, 2*i+1)
            remain = k - calc_d(s[center], s[center+1])
            for i in range(1, min(center+1, n-center-1)):
                l,r = s[center-i], s[center+i+1]
                d = calc_d(l,r)
                if d > remain: break
                remain -= d
                ans = max(ans, 2*i+2)
        return ans
    
    

    
sol = Solution()
result = [
    sol.longestPalindromicSubsequence(s = "abced", k = 2),
    sol.longestPalindromicSubsequence(s = "aaazzz", k = 4),
]
for r in result:
    print(r)
