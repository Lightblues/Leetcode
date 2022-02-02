from operator import ne
from os import times
from turtle import st
from typing import List
import collections
import math
import bisect
import heapq

class Solution:
    def longestNiceSubstring(self, s: str) -> str:
        """ 1763. 最长的美好子字符串 easy
当一个字符串 s 包含的每一种字母的大写和小写形式 同时 出现在 s 中，就称这个字符串 s 是 美好 字符串。
给你一个字符串 s ，请你返回 s 最长的 美好子字符串 。如果有多个答案，请你返回 最早 出现的一个。如果不存在美好子字符串，请你返回一个空字符串。

输入：s = "YazaAay"
输出："aAa"
解释："aAa" 是一个美好字符串，因为这个子串中仅含一种字母，其小写形式 'a' 和大写形式 'A' 也同时出现了。
"aAa" 是最长的美好子字符串。

1 <= s.length <= 100
暴力遍历
         """
        def check(s):
            lower = [ch for ch in s if ch.islower()]
            upper = [ch.lower() for ch in s if ch.isupper()]
            return set(lower) == set(upper)
        longest = ""
        for i in range(len(s)):
            for j in range(i+1,len(s)+1): # 注意这里的范围
                if check(s[i:j]) and j-i > len(longest):
                    longest = s[i:j]
        return longest

    """ 2000. 反转单词前缀 easy
输入：word = "abcdefd", ch = "d"
输出："dcbaefd"
解释："d" 第一次出现在下标 3 。 
反转从下标 0 到下标 3（含下标 3）的这段字符，结果字符串是 "dcbaefd" 。
 """
    def reversePrefix(self, word: str, ch: str) -> str:
        index = word.find(ch)
        if index != -1:
            return word[:index+1][::-1] + word[index+1:]
        else:
            return word

sol = Solution()
rels = [
    # sol.longestNiceSubstring(s = "dDzeE"),
    sol.longestNiceSubstring("Bb"),
]
for r in rels:
    print(r)


