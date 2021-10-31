"""

'?' 可以匹配任何单个字符。
'*' 可以匹配任意字符串（包括空字符串）。

两个字符串完全匹配才算匹配成功。


输入:
s = "aa"
p = "*"
输出: true
解释: '*' 可以匹配任意字符串。

s = "adceb"
p = "*a*b"
输出: true
解释: 第一个 '*' 可以匹配空字符串, 第二个 '*' 可以匹配字符串 "dce".
"""

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)

        dp = [[False]*(n+1) for _ in range(m+1)]
        dp[0][0] = True
        for j in range(n):
            if p[j] == '*':
                dp[0][j+1] = dp[0][j]
            else:
                break

        for i in range(m):
            for j in range(n):
                if p[j]=='?' or (p[j]==s[i]):
                    dp[i+1][j+1] = dp[i][j]
                elif p[j]=='*':
                    dp[i+1][j+1] = dp[i][j+1] or dp[i+1][j]
        return dp[m][n]

s = "adceb"
p = "*a*b"
print(Solution().isMatch(s,p))
