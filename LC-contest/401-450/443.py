from typing import *
from math import inf
from functools import cache

""" 
https://leetcode.cn/contest/weekly-contest-443

Easonsi @2025 """
class Solution:
    """ 3502. 到达每个位置的最小费用 """
    def minCosts(self, cost: List[int]) -> List[int]:
        pre = inf
        for i,x in enumerate(cost):
            pre = min(pre, x)
            cost[i] = pre
        return cost
    
    """ 3503. 子字符串连接后的最长回文串 I """

    """ 3504. 子字符串连接后的最长回文串 II #hard 给定两个字符串 s,t 从中选两个 (连续) 子串连接, 求得到的最长回文子串的长度
限制: n 2e3
--- 理解错题目了: 等价于给定一个字符串, 找到最大回文子串的长度
思路1: #DP 
    记 f[i,j] 为 s[i:j] 范围内的最长回文子串的长度, 则有
        f[i,j] = f[i+1,j-1]+2 if s[i]==s[j-1] else max(f[i+1,j], f[i,j-1])
        边界: j=i+1 / i

--- from ling
思路1:
    假设两字符串中取的分别为 x,y, 考虑长度
        |x| == |y|, 则 y = rev(x)
        |x| > |y|, 则x有一个长 |x|-|y| 的后缀回文串, 其前缀串满足 y = rev(x_prefix)
        |x| < |y|, 同理
    考虑 |x| == |y| 的情况, 使用 DP:
        记 f[i,j] 表示以 s[i] 结尾, t[j] 开头的两子串的最长匹配长度, 则有
            s[i] != t[j] 时, =0
            否则, f[i,j] = f[i-1,j+1] + 1
        最后答案为 max(2*f[i,j])
    """
    def longestPalindrome_error(self, s: str, t: str) -> int:
        # 理解错题目了, 以为是子序列
        s = s + t
        n = len(s)
        @cache
        def f(i:int, j:int) -> int:
            if j <= i:
                return 0
            if j == i+1:
                return 1 if s[i] != s[j] else 2
            if s[i] == s[j]:
                return f(i+1, j-1) + 2
            else:
                return max(f(i+1, j), f(i, j-1))
        return f(0, n-1)

    def longestPalindrome(self, s: str, t: str) -> int:


    """ 3505. 使 K 个子数组内元素相等的最少操作数 """
    
sol = Solution()
result = [
    # sol.minCosts(cost = [5,3,4,1,3,2]),
    # sol.longestPalindrome(s = "abc", t = "cba"),
    sol.longestPalindrome(s = "abcde", t = "ecdba"),
]
for r in result:
    print(r)
