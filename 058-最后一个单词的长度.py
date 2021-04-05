"""
给你一个字符串 s，由若干单词组成，单词之间用空格隔开。返回字符串中最后一个单词的长度。如果不存在最后一个单词，请返回 0 。

单词 是指仅由字母组成、不包含任何空格字符的最大子字符串。

输入：s = "Hello World"
输出：5

输入：s = " "
输出：0

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/length-of-last-word
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        inword = False
        last = 0
        length = 0
        for char in s:
            if char == ' ':
                if length:
                    last = length
                length = 0
                inword = False
            else:
                if not inword:
                    inword = True
                    length  = 1
                else:
                    length += 1
        if length:
            last = length
        return last
s = "b   a   "
print(Solution().lengthOfLastWord(s))