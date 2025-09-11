from typing import *
from collections import Counter
from math import inf

""" 
https://leetcode.cn/contest/weekly-contest-435

Easonsi @2025 """
class Solution:
    """ 3442. 奇偶频次间的最大差值 I """
    def maxDifference(self, s: str) -> int:
        mx, mn = -inf, inf
        for freq in Counter(s).values():
            if freq % 2 == 1:
                mx = max(mx, freq)
            else:
                mn = min(mn, freq)
        return mx - mn
    
    """ 3443. K 次修改后的最大曼哈顿距离 """
    
    
    

    
sol = Solution()
result = [
    sol.maxDifference(s = "aaaaabbc"),
]
for r in result:
    print(r)
