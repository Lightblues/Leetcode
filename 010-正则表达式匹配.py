"""
给定字符串 s 和规律 p，实现一个支持 . 和 * 格式的正则匹配，完全匹配
其中 . 匹配任意单个字符，* 匹配 0 或多个前一个元素（可能是字符也可能是 .）

输入：s = "ab" p = ".*"
输出：true
解释：".*" 表示可匹配零个或多个（'*'）任意字符（'.'）。

输入：s = "aab" p = "c*a*b"
输出：true
解释：因为 '*' 表示零个或多个，这里 'c' 为 0 个, 'a' 被重复一次。因此可以匹配字符串 "aab"。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/regular-expression-matching
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)

        def match(i, j):
            # 辅助函数，判断 s[i-1] 是否等于 p[j-1]。成立条件：1. p[j-1] == '.'则可匹配任意非空字符；2. 或者 s[i-1]=p[j-1]
            # 考虑边界条件：i>=0, j>=1
            if i == 0:
                # 加上这一行的目的在于：例如 "" 无法被 "." 匹配，但不加的话因为 p[j-1] == '.' 而返回 True
                return False
            if p[j-1] == '.':
                return True
            return s[i-1] == p[j-1]

        f = [[False] * (n+1) for _ in range(m+1)]
        f[0][0] = True
        for i in range(m+1):
            # 注意 0 长度的 s 是可能和如 'a*' 的 p 匹配的，因此要从开始循环
            for j in range(1, n+1):
                # 而 0 长度 p 只能和 0 长 s 匹配
                if p[j-1] != '*':
                    if match(i, j):
                        f[i][j] |= f[i-1][j-1]
                    # else:
                    #     f[i][j] = False
                else:
                    # if match(i, j-1):
                    #     f[i][j] |= f[i][j-2] | f[i-1][j]
                    # else:
                    #     f[i][j] |= f[i][j-2]
                    f[i][j] |= f[i][j - 2]
                    if match(i, j - 1):
                        f[i][j] |= f[i-1][j]
        return f[m][n]

sol = Solution()
# s = ''; p = '.'     #边界
s = "aaaab"; p = "a*ab"   #懒惰匹配
# s = "ab"; p = ".*"
# s = "aab"; p = "c*a*b"
print(sol.isMatch(s,p))
