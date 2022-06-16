import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
from bisect import bisect_right, bisect_left
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, reduce, partial # cache
# cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # 注意 pow 与默认环境下的 pow(x,y, MOD) 签名冲突
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
import sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
1960. 两个回文子字符串长度的最大乘积 #hard #题型
    给定一个字符串, 要求找到两个连续的不相交子串 (0 <= i <= j < k <= l < s.length), 都是长度为奇数的回文串, 使得两者的乘积最大.
    注意子问题: 计算 nums[:i] 范围内的最长子串.


@2022 """

class Manacher:
    '''马拉车算法 O(n)
[here](https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-substrings/solution/ma-la-che-si-xing-bu-han-mo-ban-by-98137-22qf/)
    '''

    def __init__(self, s: str):
        self._s = s
        self._n = len(s)
        self._odds = self._getOddRadius()
        self._evens = self._getEvenRadius()
        self._maxOdd1: Optional[List[int]] = None
        self._maxOdd2: Optional[List[int]] = None
        self._maxEven1: Optional[List[int]] = None
        self._maxEven2: Optional[List[int]] = None

    def getLongestOddStartsAt(self, index: int) -> int:
        """以s[index]开头的最长奇回文子串的长度
        """
        if self._maxOdd1 is None:
            self._maxOdd1 = [1] * self._n
            self._maxOdd2 = [1] * self._n
            for i, radius in enumerate(self._odds):
                start, end = i - radius + 1, i + radius - 1
                length = 2 * radius - 1
                self._maxOdd1[start] = max(self._maxOdd1[start], length)
                self._maxOdd2[end] = max(self._maxOdd2[end], length)
                
            # 根据左右更新端点
            for i in range(self._n):
                if i - 1 >= 0:
                    self._maxOdd1[i] = max(self._maxOdd1[i], self._maxOdd1[i - 1] - 2)
                if i + 1 < self._n:
                    self._maxOdd2[i] = max(self._maxOdd2[i], self._maxOdd2[i + 1] - 2)
        return self._maxOdd1[index]

    def getLongestOddEndsAt(self, index: int) -> int:
        """以s[index]结尾的最长奇回文子串的长度
        """
        if self._maxOdd2 is None:
            self._maxOdd1 = [1] * self._n
            self._maxOdd2 = [1] * self._n
            for i, radius in enumerate(self._odds):
                start, end = i - radius + 1, i + radius - 1
                length = 2 * radius - 1
                self._maxOdd1[start] = max(self._maxOdd1[start], length)
                self._maxOdd2[end] = max(self._maxOdd2[end], length)

            # 根据左右更新端点
            for i in range(self._n):
                if i - 1 >= 0:
                    self._maxOdd1[i] = max(self._maxOdd1[i], self._maxOdd1[i - 1] - 2)
                if i + 1 < self._n:
                    self._maxOdd2[i] = max(self._maxOdd2[i], self._maxOdd2[i + 1] - 2)
        return self._maxOdd2[index]

    def getLongestEvenStartsAt(self, index: int) -> int:
        """以s[index]开头的最长偶回文子串的长度
        """
        if self._maxEven1 is None:
            self._maxEven1 = [0] * self._n
            self._maxEven2 = [0] * self._n
            for i, radius in enumerate(self._evens):
                if radius == 0:
                    continue
                start = i - radius
                end = start + 2 * radius - 1
                length = 2 * radius
                self._maxEven1[start] = max(self._maxEven1[start], length)
                self._maxEven2[end] = max(self._maxEven2[end], length)

            # 根据左右更新端点
            for i in range(self._n):
                if i - 1 >= 0:
                    self._maxEven1[i] = max(self._maxEven1[i], self._maxEven1[i - 1] - 2)
                if i + 1 < self._n:
                    self._maxEven2[i] = max(self._maxEven2[i], self._maxEven2[i + 1] - 2)
        return self._maxEven1[index]

    def getLongestEvenEndsAt(self, index: int) -> int:
        """以s[index]结尾的最长偶回文子串的长度
        """
        if self._maxEven2 is None:
            self._maxEven1 = [0] * self._n
            self._maxEven2 = [0] * self._n
            for i, radius in enumerate(self._evens):
                if radius == 0:
                    continue
                start = i - radius
                end = start + 2 * radius - 1
                length = 2 * radius
                self._maxEven1[start] = max(self._maxEven1[start], length)
                self._maxEven2[end] = max(self._maxEven2[end], length)

            # 根据左右更新端点
            for i in range(self._n):
                if i - 1 >= 0:
                    self._maxEven1[i] = max(self._maxEven1[i], self._maxEven1[i - 1] - 2)
                if i + 1 < self._n:
                    self._maxEven2[i] = max(self._maxEven2[i], self._maxEven2[i + 1] - 2)
        return self._maxEven2[index]

    def _getOddRadius(self) -> List[int]:
        '''获取每个中心点的奇回文半径`radius`

        回文为`[pos-radius+1:pos+radius]`
        '''
        res = [0] * self._n
        left, right = 0, -1
        for i in range(self._n):
            k = 1 if i > right else min(res[left + right - i], right - i + 1)
            while 0 <= i - k and i + k < self._n and self._s[i - k] == self._s[i + k]:
                k += 1
            res[i] = k
            k -= 1
            if i + k > right:
                left = i - k
                right = i + k
        return res

    def _getEvenRadius(self) -> List[int]:
        '''获取每个中心点的偶回文半径`radius`

        回文为`[pos-radius:pos+radius]`
        '''
        res = [0] * self._n
        left, right = 0, -1
        for i in range(self._n):
            k = 0 if i > right else min(res[left + right - i + 1], right - i + 1)
            while 0 <= i - k - 1 and i + k < self._n and self._s[i - k - 1] == self._s[i + k]:
                k += 1
            res[i] = k
            k -= 1
            if i + k > right:
                left = i - k - 1
                right = i + k
        return res

    def __len__(self) -> int:
        return self._n


class Solution:
    """  """
    """ 1960. 两个回文子字符串长度的最大乘积 #hard #题型
给定一个字符串, 要求找到两个连续的不相交子串 (0 <= i <= j < k <= l < s.length), 都是长度为奇数的回文串, 使得两者的乘积最大.
限制: 长度 1e5
思路1: #Manacher 算法计算所有回文串长度, 然后分别计算左右两侧的最大回文串长度, 遍历匹配.
    [here](https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-substrings/solution/ma-la-che-suan-fa-xiang-xi-tu-jie-by-new-m2zj/)
    首先, 利用 Manacher 马拉车算法计算所有位置为中心的回文串长度. 算法概要:
        初始化: 遍历 i=0...n-1 为当前位置; 初始化 mx=-1 表示之前的回文串拓展到达的最右边界, j=-1 表示mx所对应的中心位置.
        拓展: 当 i<=mx 时, 我们可以利用已有信息, 初始化 `plen[i] = min(plen[2*j-i], mx-i)`; 否则初始化为 1 (仅包括i位置)
            从 plen[i] 出发, 向两侧检测拓展回文串
        更新: 若本次拓展的位置超过了之前的边界 `i+plen[i]>mx` 则更新 mx, j.
        说明: plen[i] 表示一半的长度, 可以从0开始也可以从1开始, 需要注意代码.
    然后, 如何保证两个子串不相交?
        我们分别从左右两侧遍历, 例如 left[i] 表示 nums[:i+1] 中所包含的最大回文长度. 然后根据分割点, 匹配左右位置即可.
        思路: #DP 在遍历 i=0...n-1 的过程中, 维护一个此前的中心位置 l 和最大长度 mx.
            当进入下一个位置i时, 不断尝试右移l, 直到 `l + plen[l] -1 >= i`. 
            l+plen[l] 可能会超过当前位置i, 此时需要进行裁剪. 这需要和 l+=1 以及 mx 的计算相匹配.
        注意: 这里维护的指针 l 的更新公式中, 确保了 (l, i) 范围内不会出现更长的合法回文串. 其实和 Manacher 算法中的思想类似.
        这里看上去简单, 实际折腾了很久 —— 主要写之前没有考虑dp的更新公式.
"""
    def maxProduct(self, s: str) -> int:
        # 计算每个位置的回文串长度
        n = len(s)
        plen = [1] * n
        j, mx = -1, -1
        for i in range(n):
            if i<=mx:
                plen[i] = min(plen[2*j-i], mx-i)
            while 0<=i-plen[i] and i+plen[i]<n and s[i+plen[i]]==s[i-plen[i]]:
                plen[i] += 1
            if i+plen[i]>mx:
                j, mx = i, i+plen[i]
        # 计算 nums[0...i] 范围内的最长回文串长度
        leftLens = [1] * n
        l, mx = 0, 1
        for i in range(1, n):
            # while l+1<n-1 and l + plen[l+1] <= i:
            #     l += 1
            #     mx = max(mx, 2*plen[l]-1)
            while l + plen[l] -1 < i: l += 1
            mx = max(mx, 2*(i-l)+1)
            leftLens[i] = mx
        rightLens = [1] * n
        r, mx = n-1, 1
        for i in range(n-2, -1, -1):
            while r - plen[r] + 1 > i:
                r -= 1
            mx = max(mx, 2*(r-i)+1)
            rightLens[i] = mx
        # 遍历匹配两部分
        ans = 1
        for i in range(n-1):
            ans = max(ans, leftLens[i]*rightLens[i+1])
        return ans
    
    def maxProduct(self, s: str) -> int:
        # [here](https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-substrings/solution/ma-la-che-si-xing-bu-han-mo-ban-by-98137-22qf/)
        n, M = len(s), Manacher(s)
        leftMax = list(accumulate([M.getLongestOddEndsAt(i) for i in range(n)], max))
        rightMax = list(accumulate([M.getLongestOddStartsAt(i) for i in range(n - 1, -1, -1)], max))[::-1]
        return max(leftMax[i] * rightMax[i + 1] for i in range(len(s) - 1))

    

    
sol = Solution()
result = [
    sol.maxProduct(s = "ababbb"),
    sol.maxProduct(s = "zaaaxbbby"),
    sol.maxProduct("ggbswiymmlevedhkbdhntnhdbkhdevelmmyiwsbgg")
]
for r in result:
    print(r)
