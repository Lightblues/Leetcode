"""
输入：strs = ["flower","flow","flight"]
输出："fl"
"""


class Solution:
    # def longestCommonPrefix(self, strs: List[str]) -> str:
    def longestCommonPrefix(self, strs):
        if len(strs)==0:
            return ""

        def getCommonPrefix(s1, s2):
            for i in range(min(len(s1), len(s2))):
                if s1[i] != s2[i]:
                    return s1[:i]
            return s1[:min(len(s1), len(s2))]

        longest = strs[0]
        for s in strs[1:]:
            longest = getCommonPrefix(longest, s)
            if not longest:
                return ""
        return longest

# strs = ["flower","flow","flight"]
strs = ['', '']
print(Solution().longestCommonPrefix(strs))