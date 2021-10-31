"""
输入: "IV"
输出: 4

输入: "LVIII"
输出: 58
解释: L = 50, V= 5, III = 3.
"""
class Solution:
    def romanToInt(self, s: str) -> int:
        result = 0
        digits = {
            "M": 1000,
            "CM": 900,
            "D": 500,
            "CD": 400,
            "C": 100,
            "XC": 90,
            "L": 50,
            "XL": 40,
            "X": 10,
            "IX": 9,
            "V": 5,
            "IV": 4,
            "I": 1
        }
        for symbol, value in digits.items():
            while s.startswith(symbol):
                result += value
                s = s[len(symbol):]
        return result

s = "LVIII"
print(Solution().romanToInt(s))