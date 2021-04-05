"""
实现 pow(x, n) ，即计算 x 的 n 次幂函数（即，xn）

输入：x = 2.00000, n = 10
输出：1024.00000

输入：x = 2.10000, n = 3
输出：9.26100

输入：x = 2.00000, n = -2
输出：0.25000
解释：2^-2 = (1/2)^2 = 1/4 = 0.25
"""
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n==0:
            return 1
        if n<0:
            x = 1/x
            n = -n
        result = 1
        # 超时了！
        # for _ in range(n):
        #     result *= x
        while n>0:
            if n%2:
                result *= x
                n -= 1
            else:
                x *= x
                n /= 2
        return result
    
# x = 2.10000; n = 3
# x = 2.00000; n = -2
x = 2.00000; n = 10
print(Solution().myPow(x,n))