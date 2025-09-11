from typing import *
from collections import Counter
from math import inf, abs

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
    
    """ 3443. K 次修改后的最大曼哈顿距离 #medium 对于开始咋 (0,0) 然后东西南北的前进序列, 最后可以修改k次前进的方向. 问 "过程中" 达到最大曼哈顿距离是多少?
限制: n 1e5
思路1: #数学
    先不考中间过程, 对于共包含 (a,b,c,d) 个前进方向的序列来说, 修改k次能获得的最大曼哈顿距离为:
        记 x = abs(a-c), y = abs(b-d); 最大修改次数为 z = min(k, 可修改数量)
            结果为 x+y + 2z
        还可以简化! 对于一共n步, 最大距离为n, 因此为 min(n, x+y+2z)
    考虑中间过程, 每一步增量计算即可
    """
    def maxDistance(self, s: str, k: int) -> int:
        x,y = 0,0
        ans = 0
        for i,dir in enumerate(s):
            if dir == "E": x += 1
            elif dir == "W": x -= 1
            elif dir == "N": y += 1
            else: y -= 1
            ans = max(ans, min(abs(x)+abs(y)+2*k, i+1))
        return ans
    
    

    
sol = Solution()
result = [
    # sol.maxDifference(s = "aaaaabbc"),
]
for r in result:
    print(r)
