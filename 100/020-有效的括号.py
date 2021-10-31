"""
判断仅包含括号的字符串是否有效

输入：s = "()[]{}"
输出：true
输入：s = "([)]"
输出：false
"""

class Solution:
    def isValid(self, s: str) -> bool:
        partner = {
            '(': ')',
            '[': ']',
            '{': '}'
        }
        parentheses_stack = []
        for char in s:
            # if not parentheses_stack or partner[parentheses_stack[-1]]!=char:
            if char in partner.keys():
                parentheses_stack.append(char)
            elif parentheses_stack and char==partner[parentheses_stack[-1]]:
                parentheses_stack.pop(-1)
            else:
                return False
        if not parentheses_stack:
            return True
        return False
s = "([)]"
# s = "()[]{}"
print(Solution().isValid(s))