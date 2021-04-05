"""
将一个给定字符串 s 根据给定的行数 numRows 进行排列，然后输出
例如对于 PAYPALISHIRING 若指定行数为 3 则排列为
P   A   H   N
A P L S I I G
Y   I   R
在逐行输出为 PAHNAPLSIIGYIR


输入：s = "PAYPALISHIRING", numRows = 4
输出："PINALSIGYAHRPI"
解释：
P     I    N
A   L S  I G
Y A   H R
P     I

输入：s = "A", numRows = 1
输出："A"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zigzag-conversion
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。



---

"""


class Solution:
    """
    原本试图找出每一行的规律，非常傻
    下面的实现基于官方：利用一个二维数组记录每一行的内容，用一个 flag 记录前进的方向，以更新下一个字符应该放在第几行，一次遍历即可
    """
    # def convert(self, s: str, numRows: int) -> str:
    #     totalLen = len(s)
    #     result = []
    #     # start = 0
    #     loopLen = 2*(numRows-1)
    #
    #     i = 0
    #     while i < totalLen:
    #         result.append(s[i])
    #         i += loopLen
    #     for i in range(1, numRows-1):
    #         if i < totalLen:
    #             result.append(s[i])
    #         else:
    #             break
    #         interval1 = 2*(numRows-i-1)
    #         # interval2 = loopLen - interval1
    #         while i<totalLen:
    #             if i+interval1 < totalLen:
    #                 result.append(s[i+interval1])
    #             if i+loopLen < totalLen:
    #                 result.append(s[i+loopLen])
    #             i += loopLen
    #     i = numRows-1
    #     while i < totalLen:
    #         result.append(s[i])
    #         i += loopLen
    #     return "".join(result)

    def convert(self, s: str, numRows: int) -> str:
        # special
        if numRows==1:
            return s

        # 考虑边界 numRows=2，i % (numRows-1) == 0 始终成立，则每次迭代 direction 都取反
        results = [[] for i in range(numRows)]
        direction = 1
        results[0].append(s[0])
        toList = 1
        for i in range(1, len(s)):
            if i % (numRows-1) == 0:
                direction *= -1
            results[toList].append(s[i])
            toList += direction
        return "".join(["".join(line) for line in results])

s = "PAYPALISHIRING"
# s = 'AB'
numRows = 3
sol = Solution()
print(sol.convert(s, numRows))