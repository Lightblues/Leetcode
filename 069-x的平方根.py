"""
实现 int sqrt(int x) 函数

输入: 8
输出: 2
说明: 8 的平方根是 2.82842...,
     由于返回类型是整数，小数部分将被舍去。
"""
class Solution:
    def mySqrt(self, x: int) -> int:
        # def bisect(left, right):
        #     mid =
        if x == 0:
            return 0
        left, right = 1, x
        while left <= right:
            mid = (left+right) // 2
            if mid*mid <= x < (mid + 1)*(mid + 1):
                return mid
            elif mid*mid < x:
                left = mid +1
            else:
                right = mid -1

print(Solution().mySqrt(1))