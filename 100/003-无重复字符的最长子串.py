"""
给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。

输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。

输入: s = ""
输出: 0

输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-substring-without-repeating-characters
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        chars_with_norepeat = []
        longest_len = 0
        for char in s:
            if char not in chars_with_norepeat:
                chars_with_norepeat.append(char)
            else:
                longest_len = max(longest_len, len(chars_with_norepeat))
                repeat_index = chars_with_norepeat.index(char)
                # chars_with_norepeat = chars_with_norepeat[repeat_index+1:].append(char)
                chars_with_norepeat = chars_with_norepeat[repeat_index + 1:] + [char]
                # 注意不能用 append 因为没有返回值
        return max(longest_len, len(chars_with_norepeat))
s = "pwwkew"
sol = Solution()
print(sol.lengthOfLongestSubstring(s))