"""
给定两个整数，被除数 dividend 和除数 divisor。将两数相除，要求不使用乘法、除法和 mod 运算符。

返回被除数 dividend 除以除数 divisor 得到的商。

整数除法的结果应当截去（truncate）其小数部分，例如：truncate(8.345) = 8 以及 truncate(-2.7335) = -2

输入: dividend = 7, divisor = -3
输出: -2
解释: 7/-3 = truncate(-2.33333..) = -2
"""


class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        # 脑回路清奇才会用加法吧……
        # if dividend<0:
        #     dividend, divisor = -dividend, -divisor
        # flag = 1
        # if divisor<0:
        #     divisor = -divisor
        #     flag = -1
        # res = 0
        # while dividend>=0:
        #     dividend -= divisor
        #     res += 1
        # return flag*(res-1)

        # 模拟 int32
        INT_MAX = 2147483647
        if dividend == -INT_MAX-1 and divisor==-1:
            return INT_MAX

        # 用 flag 表示结果正负，将两数均转化为正数
        if dividend<0:
            dividend, divisor = -dividend, -divisor
        flag = 1
        if divisor<0:
            divisor = -divisor
            flag = -1

        def div(dividend: int, divisor: int) -> int:
            if dividend < divisor:
                return 0
            count = 1
            divisor_2 = divisor # 倍增 divisor
            while dividend>divisor_2+divisor_2:
                # 从加法变为左移，运行时间从 52ms 降到 40ms
                # divisor_2 = divisor_2+divisor_2
                # count = count + count
                divisor_2 <<= 1
                count <<= 1
            return count + div(dividend-divisor_2, divisor)

        if flag>0:
            return div(dividend, divisor)
        else:
            return -div(dividend, divisor)

print(Solution().divide(7, -3))
