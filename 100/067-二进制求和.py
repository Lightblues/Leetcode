"""
给你两个二进制字符串，返回它们的和（用二进制表示）。

输入为 非空 字符串且只包含数字 1 和 0。


输入: a = "11", b = "1"
输出: "100"
"""
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        # 一行解决
        # return '{0:b}'.format(int('11', 2) + int('1', 2))

        n = max(len(a), len(b))
        a, b = list(a[::-1]), list(b[::-1])
        res = []
        flag = 0
        for i in range(n):
            a_ = 1 if len(a)>i and a[i]=='1' else 0
            b_ = 1 if len(b)>i and b[i]=='1' else 0
            tmp = a_ + b_ + flag
            flag, r_ = divmod(tmp, 2)
            res.append(r_)
        if flag:
            res.append(flag)
        return ''.join(map(str, res[::-1]))

    def addBinary2(self, a, b):
        x, y = int(a, 2), int(b, 2)
        while y:
            answer = x^y
            carry = (x & y) << 2
            x, y = answer, carry
        return bin(x)[2:]       # 注意 bin 返回的是形如 '0b100010' 的字符串


a = "110010"; b = "1010001"
print(Solution().addBinary2(a, b))

