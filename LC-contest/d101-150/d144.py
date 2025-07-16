from typing import *

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-144

Easonsi @2025 """
class Solution:
    """ 3360. 移除石头游戏 """
    def canAliceWin(self, n: int) -> bool:
        t = 10
        for i in range(10):
            if n >= t:
                n -= t
                t -= 1
            else:
                return i % 2 == 1

sol = Solution()
result = [
    sol.canAliceWin(n = 12),
    sol.canAliceWin(2),
]
for r in result:
    print(r)
