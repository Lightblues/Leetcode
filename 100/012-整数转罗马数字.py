"""
字符          数值
I             1
V             5
X             10
L             50
C             100
D             500
M             1000

一些特例
4   IV
9   IX
40  XL
90  XC
400 CD
900 CM

【输入不大于 3999】

输入: 58
输出: "LVIII"
解释: L = 50, V = 5, III = 3.

输入: 1994
输出: "MCMXCIV"
解释: M = 1000, CM = 900, XC = 90, IV = 4.


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/integer-to-roman
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    def intToRoman(self, num: int) -> str:
        roman_digits = []
        digits = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I")
        ]
        for value, symbol in digits:
            count, num = divmod(num, value)
            roman_digits.append(symbol*count)
            if not num:
                break
        return "".join(roman_digits)

num = 1994
sol = Solution()
print(sol.intToRoman(num))