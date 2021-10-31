"""
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。

输入：s = "a"
输出："a"
"""



class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 2:
            return s

        # normal case
        totalLen = len(s)
        maxLen = 0  #maxLen, start 记录最长回文子串
        start = 0
        i = 0
        while i<totalLen:
            # 排除不必要的搜索：当检索到位置为 i 时，其可能的最大长度为 1+2*(totalLen-i)
            if 1+2*(totalLen-i) <= maxLen:
                break

            left = i
            right = i
            while right != totalLen-1 and s[left] == s[right+1]:
                right += 1
            # 注意 i 的更新：若有重复的则从下一个字符开始
            i = right+1
            while left!=0 and right!=totalLen-1 and s[left-1]==s[right+1]:
                right+=1
                left-=1
            if right-left+1 > maxLen:
                maxLen = right-left+1
                start = left


        return s[start:start+maxLen]

s = "baaabad"
sol = Solution()
print(sol.longestPalindrome(s))
