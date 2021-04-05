"""
联系 415 题字符串相加

给定两个以字符串形式表示的非负整数 num1 和 num2，返回 num1 和 num2 的乘积，它们的乘积也表示为字符串形式。

输入: num1 = "123", num2 = "456"
输出: "56088"

---

感觉有点奇怪就直接搬了源码过来。
【思路一】就是算式运算，根据数位，将每一轮乘法的结果调用字符串实现的加法。
【思路二】所谓的提升就是用了数组形式，我们知道 m, n 位的两数相乘，结果为 m+n-1 或 m+n 位，因此事先生成长度为 m+n 的数组。
然后对于两个乘数的每一位，将其结果加到这个数组的对应位上，例如两个数中的百位数相乘，将乘积放在数组的万位上。最后，将这个数组按从第到高位转化成合理的数字形式。
在思路一中我们维护为了中间结果是有效的十进制数，从而带了一定的时间损耗。但我觉得这个影响有限。
而且这里的实现本身感觉没什么意义？
"""
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        ans = "0"
        m, n = len(num1), len(num2)
        for i in range(n - 1, -1, -1):
            add = 0
            y = int(num2[i])
            curr = ["0"] * (n - i - 1)
            for j in range(m - 1, -1, -1):
                product = int(num1[j]) * y + add
                curr.append(str(product % 10))
                add = product // 10
            if add > 0:
                curr.append(str(add))
            curr = "".join(curr[::-1])
            ans = self.addStrings(ans, curr)

        return ans

    def addStrings(self, num1: str, num2: str) -> str:
        i, j = len(num1) - 1, len(num2) - 1
        add = 0
        ans = list()
        while i >= 0 or j >= 0 or add != 0:
            x = int(num1[i]) if i >= 0 else 0
            y = int(num2[j]) if j >= 0 else 0
            result = x + y + add
            ans.append(str(result % 10))
            add = result // 10
            i -= 1
            j -= 1
        return "".join(ans[::-1])

