"""
请你来实现一个  myAtoi(string s) 函数，使其能将字符串转换成一个 32 位有符号整数（类似 C/C++ 中的 atoi 函数）。

函数myAtoi(string s) 的算法如下：

读入字符串并丢弃无用的前导空格
检查下一个字符（假设还未到字符末尾）为正还是负号，读取该字符（如果有）。 确定最终结果是负数还是正数。 如果两者都不存在，则假定结果为正。
读入下一个字符，直到到达下一个非数字字符或到达输入的结尾。字符串的其余部分将被忽略。
将前面步骤读入的这些数字转换为整数（即，"123" -> 123， "0032" -> 32）。如果没有读入数字，则整数为 0 。必要时更改符号（从步骤 2 开始）。
如果整数数超过 32 位有符号整数范围 [−2^31, 2^31− 1] ，需要截断这个整数，使其保持在这个范围内。具体来说，小于 −2^31 的整数应该被固定为 −2^31 ，大于 2^31− 1 的整数应该被固定为 231− 1 。
返回整数作为最终结果。
注意：

本题中的空白字符只包括空格字符 ' ' 。
除前导空格或数字后的其余字符串外，请勿忽略 任何其他字符。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/string-to-integer-atoi
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

输入：s = "4193 with words"
输出：4193
解释：
第 1 步："4193 with words"（当前没有读入字符，因为没有前导空格）
         ^
第 2 步："4193 with words"（当前没有读入字符，因为这里不存在 '-' 或者 '+'）
         ^
第 3 步："4193 with words"（读入 "4193"；由于下一个字符不是一个数字，所以读入停止）
             ^
解析得到整数 4193 。
由于 "4193" 在范围 [-231, 231 - 1] 内，最终结果为 4193

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/string-to-integer-atoi
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    # 自己的实现
    # def myAtoi(self, s: str) -> int:
    #     INT_MAX = 2147483647
    #     INT_MIN = -2147483648
    #     max_div10 = 214748364
    #     # min_div10 = -214748364
    #
    #     signal = 1
    #     result = 0
    #
    #     s_list = list(s)
    #     while s_list:
    #         char = s_list.pop(0)
    #         # if char == " ":
    #         #     continue
    #         if char == '-':
    #             signal = -1
    #             break
    #         elif char == '+':
    #             break
    #         elif char.isdigit():
    #             result = int(char)
    #             break
    #         elif char == ' ':
    #             continue
    #         else:   # 出现其他字符，直接返回
    #             return 0
    #     while s_list:
    #         char = s_list.pop(0)
    #         # 非数字，结束
    #         if not char.isdigit():
    #             return signal*result
    #         # 需要判断是否溢出
    #         pop = int(char)
    #         if signal==1 and (result>max_div10 or result==max_div10 and pop>7):
    #             return INT_MAX
    #         if signal==-1 and (result>max_div10 or result==max_div10 and pop>8):
    #             return INT_MIN
    #         result = 10*result+pop
    #     return signal*result

    def myAtoi(self, s: str) -> int:
        INT_MAX = 2147483647
        INT_MIN = -2147483648
        class Automaton:
            def __init__(self):
                self.state = 'start'
                self.sign = 1
                self.ans = 0
                self.table = {
                    'start': ['start', 'signed', 'in_number', 'end'],
                    'signed': ['end', 'end', 'in_number', 'end'],
                    'in_number': ['end', 'end', 'in_number', 'end'],
                    'end': ['end', 'end', 'end', 'end']
                }

            def get_col(self, c):
                if c.isspace():
                    return 0
                if c=='+' or c=='-':
                    return 1
                if c.isdigit():
                    return 2
                return 3

            def get(self, c):
                self.state = self.table[self.state][self.get_col(c)]
                if self.state == 'in_number':
                    self.ans = self.ans*10 + int(c)
                    self.ans = min(self.ans, INT_MAX) if self.sign == 1 else min(self.ans, -INT_MIN)
                elif self.state == 'signed':
                    self.sign = 1 if c=='+' else -1

        automaton = Automaton()
        for c in s:
            automaton.get(c)
            if automaton.state == 'end':
                return automaton.sign * automaton.ans
        return automaton.sign * automaton.ans

# s = '4193 with words'
# s = '-91283472332'
# s = '42'
s = "num 655"
sol = Solution()
print(sol.myAtoi(s))
