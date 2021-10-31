"""
1.     1
2.     11
3.     21
4.     1211
5.     111221
第一项是数字 1
描述前一项，这个数是 1 即 “ 一 个 1 ”，记作 "11"
描述前一项，这个数是 11 即 “ 二 个 1 ” ，记作 "21"
描述前一项，这个数是 21 即 “ 一 个 2 + 一 个 1 ” ，记作 "1211"
描述前一项，这个数是 1211 即 “ 一 个 1 + 一 个 2 + 二 个 1 ” ，记作 "111221"

输入：n = 1
输出："1"
解释：这是一个基本样例。

输入：n = 4
输出："1211"
解释：
countAndSay(1) = "1"
countAndSay(2) = 读 "1" = 一 个 1 = "11"
countAndSay(3) = 读 "11" = 二 个 1 = "21"
countAndSay(4) = 读 "21" = 一 个 2 + 一 个 1 = "12" + "11" = "1211"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/count-and-say
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/count-and-say
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    def countAndSay(self, n: int) -> str:
        if n==1:
            return "1"

        namedstr = "1"

        def convert():
            nonlocal namedstr
            says = []
            pre = ''
            count = 1
            """
            一个有意思的小技巧：由于最后一个字符无法计数，加一个「哨兵」在最后
            """
            for c in namedstr + ' ':
                if c==pre:
                    count += 1
                else:
                    if pre:
                        # 去除第一个空的 pre 字符
                        says.append(str(count) + str(pre))
                    pre = c
                    count = 1
            namedstr = "".join(says)

        for _ in range(n-1):
            convert()

        return namedstr

print(Solution().countAndSay(4))