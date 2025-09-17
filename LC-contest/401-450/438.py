from typing import *


""" 
https://leetcode.cn/contest/weekly-contest-438
Easonsi @2025 """
class Solution:
    """ 3461. 判断操作后字符串中的数字是否相等 I """
    def hasSameDigits(self, s: str) -> bool:
        s = list(map(int, s))
        while len(s) > 2:
            s = [(s[i]+s[i+1])%10 for i in range(len(s)-1)]
        return s[0] == s[1]
    
    """ 3462. 提取至多 K 个元素的最大总和 """
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        cand = []
        for line, l in zip(grid, limits):
            cand.extend(sorted(line, reverse=True)[:l])
        cand.sort(reverse=True)
        return sum(cand[:k])
    
    """ 3463. 判断操作后字符串中的数字是否相等 II #hard 对于一个数字字符串, 每次操作: 对于所有相邻数字相加%10, 得到长i-1的新字符串. 
问最后剩余的两个数字是否相等. 限制: n 1e5

"""

    
sol = Solution()
result = [
    # sol.hasSameDigits(s = "3902"),
    # sol.hasSameDigits(s = "34789"),
    sol.maxSum(grid = [[1,2],[3,4]], limits = [1,2], k = 2),
]
for r in result:
    print(r)
