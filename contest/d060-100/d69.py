from typing import List, Optional
import collections
import math
import bisect
import heapq

from structures import ListNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 2129. 将标题首字母大写 """
    def capitalizeTitle(self, title: str) -> str:
        words = title.split()
        for i,word in enumerate(words):
            if len(word) < 3:
                words[i] = word.lower()
            else:
                words[i] = word[0].upper() + word[1:].lower()
        return " ".join(words)

    """ 2130. 链表最大孪生和 """
    def pairSum(self, head: Optional[ListNode]) -> int:
        numbers = []
        while head:
            numbers.append(head.val)
            head = head.next
        return max([i+j for i,j in zip(numbers, reversed(numbers))])

    """ 2131. 连接两字母单词得到的最长回文串
给一组长度为2的字符串, 将他们拼接, 形成最大的回文串

考虑 1. aa 的形式, 若数量为奇数, 只能放在中间, 若为偶数, 可以两侧对应位置放置; 
2. ab + ba 的形式, 左右对称放置
 """
    def longestPalindrome(self, words: List[str]) -> int:
        diffWords = [w for w in words if w[0]!=w[1]]
        sameWords = [w for w in words if w[0]==w[1]]
        result = 0

        # aa 的形式
        sameDict = collections.Counter(sameWords)
        # result += max(list(sameDict.values()) + [0]) * 2
        flag = False
        for k,v in sameDict.items():
            if v%2!=0:
                flag = True
            result += v//2 * 2 * 2
        if flag:
            result += 2

        # ab + ba 的形式
        diffDict = collections.Counter(diffWords)
        tmp = 0
        for k,v in diffDict.items():
            if k[::-1] in diffDict:
                tmp += min(v, diffDict[k[::-1]])
        return result + tmp * 2


    """ 2132. 用邮票贴满网格图 [prefix-sum]
 """



sol = Solution()
result = [
    # sol.capitalizeTitle("capiTalIze tHe titLe"),
    # sol.longestPalindrome(words = ["ab","ty","yt","lc","cl","ab"]),
    # sol.longestPalindrome(words = ["lc","cl","gg"]),
    # sol.longestPalindrome(["dd","aa","bb","dd","aa","dd","bb","dd","aa","cc","bb","cc","dd","cc"]),
    sol.possibleToStamp(grid = [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], stampHeight = 4, stampWidth = 3),
    sol.possibleToStamp(grid = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], stampHeight = 2, stampWidth = 2),
]
for r in result:
    print(r)