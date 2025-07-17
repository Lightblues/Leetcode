from typing import *
from math import ceil

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-145

Easonsi @2025 """
class Solution:
    """ 3375. 使数组的值全部为 K 的最少操作次数 """
    def minOperations(self, nums: List[int], k: int) -> int:
        ans = 0
        for x in sorted(set(nums), reverse=True):
            if x < k: return -1
            elif x==k: continue
            else: ans += 1
        return ans

    """ 3376. 破解锁的最少时间 I #medium 有一组锁需要一定消耗一定分数可以打开. 
每一时刻: 分数S增加 X (初始S=0; X=1); 决定是否开锁, 若开锁, 消耗分数, 但 X+=K. 问所需最小时间
限制: n 8; val 1e6
思路1: #模拟 #贪心
    """
    def findMinimumTime(self, strength: List[int], k: int) -> int:
        x = 1; s = 0
        ans = 0
        for val in sorted(strength):
            delta = ceil(val / x)
            ans += delta
            


sol = Solution()
result = [
    sol.minOperations(nums = [9,7,5,3], k = 1),
    sol.minOperations(nums = [5,2,5,4,5], k = 2),
]
for r in result:
    print(r)
