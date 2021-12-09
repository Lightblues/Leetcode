"""
给你一个字符串表达式 s ，请你实现一个基本计算器来计算并返回它的值。

整数除法仅保留整数部分。

输入：s = "3+2*2"
输出：7
"""
class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        preSign = '+'
        num = 0

        for c in s+'/':
            if c.isdigit():
                num = 10*num+int(c)
            elif c in '+-*/':
                if preSign == '+':
                    stack.append(num)
                elif preSign == '-':
                    stack.append(-num)
                elif preSign == '*':
                    stack.append(stack.pop()*num)
                else:
                    # 注意不能用 stack.pop()//num，因为在 python 中 -3//2 = -2，而按照题目要求应该是 -1
                    stack.append(int(stack.pop()/num))
                num = 0
                preSign = c

        return sum(stack)

s = "14-3/2"
print(Solution().calculate(s))