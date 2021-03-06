"""
格雷编码是一个二进制数字系统，在该系统中，两个连续的数值仅有一个位数的差异。
给定一个代表编码总位数的非负整数 n，打印其格雷编码序列。即使有多个不同答案，你也只需要返回其中一种。
格雷编码序列必须以 0 开头。

输入: 2
输出: [0,1,3,2]
解释:
00 - 0
01 - 1
11 - 3
10 - 2

对于给定的 n，其格雷编码序列并不唯一。
例如，[0,2,3,1] 也是一个有效的格雷编码序列。

00 - 0
10 - 2
11 - 3
01 - 1

输入: 0
输出: [0]
解释: 我们定义格雷编码序列必须以 0 开头。
     给定编码总位数为 n 的格雷编码序列，其长度为 2^n。当 n = 0 时，长度为 2^0 = 1。
     因此，当 n = 0 时，其格雷编码序列为 [0]。
"""
from typing import List

"""思路是递归。可以，一个位数n的序列长度为2^n，即位数 n-1 的两倍。
因此，假设有 n=i 时的解（并且规定了初始为0），我们可以镜像 正+反 ，则最中间的两个一定的相同的编码；
正向序列最高位0，反向最高位1即可"""
class Solution:
    def grayCode(self, n: int) -> List[int]:
        if n == 0:
            return [0]
        gray_pre = self.grayCode(n-1)
        return gray_pre + [i+2**(n-1) for i in gray_pre[::-1]]


print(Solution().grayCode(2))