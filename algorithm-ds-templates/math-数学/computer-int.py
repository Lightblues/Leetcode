from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
0007. 整数反转 #medium #题型 将一个32位有符号整数反转, 假设不能用64位数字
0029. 两数相除 #medium 但实际 #hard 不使用乘除和 mod 运算, 实现两任意整数的整除 (注意负数的情况) 

Easonsi @2023 """
class Solution:
    """ 0007. 整数反转 #medium #题型 将一个32位有符号整数反转, 假设不能用64位数字
限制: 输入为32位有符号整数, 翻转后可能发生越界, 则返回0
思路1: #数学 
    要求反转数字, 可以按照下面的规则进行 (注意对于正负都成立!)
        digit, x = x % 10, x // 10
        rev = rev * 10 + digit
    但是可能发生越界! 因为在对rev进行操作的之前要进行检查! 具体见官答
        判断条件为 INT_MIN <= rev * 10 + digit <= INT_MAX=2147483647. 如何判断中间表达式不会越界? 
        讨论 INT_MAX 的不等式, 将其替换为 INT_MAX//10 + 7, 然后在对 rev,digit 分类讨论
            最后可以得到条件为 rev <= INT_MAX // 10
        对应的, INT_MIN 部分可以化简为 rev >= INT_MIN // 10 + 1
Python特性: 上面的 digit, x = x % 10, x // 10 操作需要对负数特殊处理!!
[官答](https://leetcode.cn/problems/reverse-integer/solution/zheng-shu-fan-zhuan-by-leetcode-solution-bccn/)
"""
    def reverse(self, x: int) -> int:
        INT_MIN, INT_MAX = -2**31, 2**31 - 1

        rev = 0
        while x != 0:
            # INT_MIN 也是一个负数，不能写成 rev < INT_MIN // 10
            if rev < INT_MIN // 10 + 1 or rev > INT_MAX // 10:
                return 0
            
            digit = x % 10
            # Python3 的取模运算在 x 为负数时也会返回 [0, 9) 以内的结果，因此这里需要进行特殊判断
            if x < 0 and digit > 0: digit -= 10
            # 同理，Python3 的整数除法在 x 为负数时会向下（更小的负数）取整，因此不能写成 x //= 10
            x = (x - digit) // 10

            rev = rev * 10 + digit
        return rev

    """ 0029. 两数相除 #medium 不使用乘除和 mod 运算, 实现两任意整数的整除 (注意负数的情况) 
限制: 1] 对于结果去掉小数, 例如 8.345 将被截断为 8, -2.7335 将被截断至 -2; 2] 要求结果在32位整数范围内 (不在的话截断)
思路1: 都转化为正数情况, 然后 #倍增 divisor
"""
    def divide(self, dividend: int, divisor: int) -> int:
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

        # 下面可以优化的!
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

        return div(dividend, divisor) if flag==1 else -div(dividend, divisor)
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
