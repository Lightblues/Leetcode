"""
判断一个整数 x 是否为回文数

输入：x = -121
输出：false
解释：从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。
"""

class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x<0:
            return False
        rev = 0
        record = x
        while x:
            rev = 10*rev + x%10
            x //= 10
        if rev == record:
            return True
        return False

x = 12321
sol = Solution()
print(sol.isPalindrome(x))