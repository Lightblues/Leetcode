"""
给定两个字符串形式的非负整数 num1 和num2 ，计算它们的和。


"""
class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        result = []
        n1_chars = list(num1)
        n2_chars = list(num2)
        base = ord('0')
        flag = 0
        while True:
            c1 = n1_chars.pop() if n1_chars else ''
            c2 = n2_chars.pop() if n2_chars else ''
            if not c1 and not c2:
                if flag:
                    result.append('1')
                break
            c1 = ord(c1) - base if c1 else 0
            c2 = ord(c2) - base if c2 else 0
            added = c1+c2+flag
            added, flag = added%10, added//10
            result.append(chr(added+base))
        return "".join(result[::-1])


num1 = '123'
num2 = '111'
print(Solution().addStrings('0', '0'))
