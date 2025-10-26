from typing import *
import heapq
from collections import Counter

""" 
https://leetcode.cn/contest/weekly-contest-445

Easonsi @2025 """
class Solution:
    """ 3516. 找到最近的人 """
    def findClosest(self, x: int, y: int, z: int) -> int:
        a = abs(x-z)
        b = abs(y-z)
        if a < b: return 1
        elif a > b: return 2
        else: return 0

    """ 3517. 最小回文排列 I """
    def smallestPalindrome(self, s: str) -> str:
        cnt = Counter(s)


sol = Solution()
result = [
    
]
for r in result:
    print(r)
