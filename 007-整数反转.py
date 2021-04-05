"""
给一个 32 位有符号整数，输出数字反转后的结果
若整数超过范围 [-2^31, 2^31-1] 则返回 0
输入：x = -123
输出：-321

输入：x = 120
输出：21

正数
最大值为 2**31-1 == 2147483647
假设更新公式为 rev*10+pop，则可能溢出的情况：1. rev>INT_MAX//10; 2. rev=INT_MAX//10, pop>7
负数
1. rev<INT_MAX//10; 2. rev=INT_MAX//10, pop<-8
【注意这里用的 C 的整除，也就是 -21/10=-2, -11%10=-1；为了在 Python 中模拟用了下面的代码
tmp = int(x/10)
pop = x-10*tmp
x = tmp】
"""

class Solution:
    def reverse(self, x: int) -> int:
        # INT_MAX = 2147483647
        # INT_MIN = -2147483648
        max_div10 = 214748364
        min_div10 = -214748364
        rev = 0
        while x:
            tmp = int(x/10)
            pop = x-10*tmp
            x = tmp

            # if rev>INT_MAX//10 or (rev==INT_MAX//10 and pop >7):
            if rev>max_div10 or rev==max_div10 and pop>7:
                return 0
            if rev<min_div10 or rev==min_div10 and pop <-8:
                return 0
            rev = rev*10+pop
        return rev

# x = -123
x = 2147483647
sol = Solution()
print(sol.reverse(x))