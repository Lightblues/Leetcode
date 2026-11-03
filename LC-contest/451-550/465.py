from typing import *

"""
https://leetcode.cn/contest/weekly-contest-465
Easonsi @2026 """


class Solution:
    """ 3668. 重排完成顺序 """
    def recoverOrder(self, order: List[int], friends: List[int]) -> List[int]:
        fs = set(friends)
        return [i for i in order if i in fs]

    """ 3669. K 因数分解 #4 
将一个整数分解成 k 个整数乘积, 要求这些数字极差最小.
限制: n 1e5; k 5
    """
    def minDifference(self, n: int, k: int) -> List[int]:
        pass

    """ 3670. 没有公共位的整数最大乘积 """

sol = Solution()
result = [

]
for r in result:
    print(r)
