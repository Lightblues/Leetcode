import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
functools.cache
from functools import lru_cache, reduce, partial # cache
cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import count, product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-50
@2022 """
class Solution:
    """ 1827. 最少操作使数组递增 """
    def minOperations(self, nums: List[int]) -> int:
        last = nums[0]
        ans = 0
        for num in nums[1:]:
            last = max(last+1, num)
            if last > num:
                ans += last-num
        return ans
    
    """ 1828. 统计一个圆中点的数目 """
    def countPoints(self, points: List[List[int]], queries: List[List[int]]) -> List[int]:
        isInCircle = lambda x,y,r: x**2+y**2 <= r**2
        return [sum(isInCircle(x1-x2, y1-y2, r) for x2,y2 in points) for x1,y1,r in queries]
    
    """ 1829. 每个查询的最大异或值 """
    def getMaximumXor(self, nums: List[int], maximumBit: int) -> List[int]:
        target = (1<<maximumBit) - 1
        ans = []
        acc = 0
        for num in nums:
            acc ^= num
            ans.append(target ^ acc)
        return ans[::-1]
    
    """ 1830. 使字符串有序的最少操作次数 #hard #math
定义了对于字符串一个复杂的操作, 问经过多少次操作后, 可以原字符串 s 变为递增的形式.
操作定义为: 从后往前找到第一个 `s[i] < s[i - 1]` 的位置, 然后在 s[i:] 中找到最后一个 `s[i-1] > s[j]` 的位置. 然后 1) 将 i-1, j 两个位置的元素调换; 2) 反转 s[i:]
限制: 字符串长度最大为 3000. 对于结果取模.
见 [官答](https://leetcode.cn/problems/minimum-number-of-operations-to-make-string-sorted/solution/shi-zi-fu-chuan-you-xu-de-zui-shao-cao-z-qgra/)
思路1: #组合数学
    注意到, 在上述操作中, 找到的坐标满足 s[i:] 是递增的; 然后在后续中找到的 j 是比 s[i-1] 次小的元素; 交换 i-1, j 后, s[i:] 仍然是递增的; 交换后, s[i:] 变为递减的.
        简言之, 对于位置 i-1, 我们从其后找到了一个比它次小的元素, 然后让 s[i:] 尽可能大 —— 也即, 找到了一个字典序次小的字符串 (排列).
        将上述过程反转过来, 其实就是得到「0031. 下一个排列」
    也即, 问题等价于: 原字符串 s 是从小到大的第几个排列?
        思路: 递归求解.
        例如, 对于 [3,2,1,4] 来说, 从左往右看: 后续中比第 i=0 个数字3小的有两个 (rank=2), 因此考虑第一个数字为1/2, 这样的排列有 `2*perm(3) = rank * perm(n-i-1)`;
            然后, 问题递归为大小 -1 的子问题, 考虑 i=1 位置...
        还需要考虑重复数字的情况. 一般而言, 假设每个数字的重复数为 dup[ch], 则所有不同的排列数为 `n! / (dup[0]! * dup[1]! * ... * dup[n-1]!)`
            具体到本题中, 我们约束第一个数字为比 s[idx] 更小的, 因此公式为 `rank * (n-1)! / prod(dup[ch]!)` 这里的n是从idx位置往后的字符串长度, 而dup[ch]记录了从idx位置往后的数字的重复数.
    进阶: #乘法逆元
        在本题中, 由于字符串长度为3000, 直接计算排列数会产生很大的数字. 而在上面的公式中出现了除法, 如果要用取模运算来防止数字溢出的话, 可以考虑「乘法逆元」. (超纲了)
        所谓「乘法逆元」就是对于一个整数a, 找到另一个整数a' 使得 `aa' = 1 (mod p)`.
            利用「费马小定理」, 当p为质数时有 `a^{p-1} = 1 (mod p)`, 因此可以找到一个逆元为 `a^{p-2}` (可以在再 MOD p).
        利用乘法逆元, 我们有 `b/a = b*a' (mod p)`, 因此可以将除法转为乘法 (从而可以对两个因子分别取模).
        幸而Python不用考虑数字溢出的问题, 直接暴力计算也可以过 (就是时间慢了点).
"""
    def makeStringSorted(self, s: str) -> int:
        # 利用 Python 整数特点, 直接暴力计算
        MOD = 10**9+7
        n = len(s)
        counter = Counter(s[-1:])
        ans = 0
        for i in range(n-2, -1, -1):
            ch = s[i]
            counter[ch] += 1
            smallerChs = sum(cnt for c,cnt in counter.items() if c < ch)
            ans += smallerChs * math.perm(n-i-1) // math.prod(math.perm(cnt) for cnt in counter.values())
            ans %= MOD
        return ans
        
    def makeStringSorted(self, s: str) -> int:
        # 计算乘法逆元. 采用cache
        MOD = 10**9+7
        
        @lru_cache(maxsize=None)
        def getProductInverse(x, MOD=MOD):
            # 计算数字 x 关于质数 MOD 的乘法逆元
            return pow(x, MOD-2, MOD)
        @lru_cache(maxsize=None)
        def getModPerm(n, MOD=MOD):
            return math.perm(n) % MOD
        
        n = len(s)
        counter = Counter(s[-1:])
        ans = 0
        for i in range(n-2, -1, -1):
            ch = s[i]
            counter[ch] += 1
            rank = sum(cnt for c,cnt in counter.items() if c < ch)
            # ans += rank * math.perm(n-i-1) // math.prod(math.perm(cnt) for cnt in counter.values())
            ans += rank * getModPerm(n-i-1) * math.prod(getProductInverse(getModPerm(cnt)) for cnt in counter.values())
            ans %= MOD
        return ans

    def makeStringSorted(self, s: str) -> int:
        """ from [here](https://leetcode.cn/problems/minimum-number-of-operations-to-make-string-sorted/solution/shi-zi-fu-chuan-you-xu-de-zui-shao-cao-z-qgra/)
        预计算所有可能用到的 排列数、乘法逆元, 比上面函数cache的速度快. """
        mod = 10**9 + 7
        
        # 快速幂，用来计算 x^y mod m
        def quickmul(x: int, y: int) -> int:
            # Python 有方便的内置函数
            return pow(x, y, mod)
    
        n = len(s)
        
        # fac[i] 表示 i! mod m
        # facinv[i] 表示 i! 在 mod m 意义下的乘法逆元
        fac, facinv = [0] * (n + 1), [0] * (n + 1)
        fac[0] = facinv[0] = 1
        for i in range(1, n):
            fac[i] = fac[i - 1] * i % mod
            # 使用费马小定理 + 快速幂计算乘法逆元
            facinv[i] = quickmul(fac[i], mod - 2)
        
        # freq 存储每个字符出现的次数
        freq = collections.Counter(s)
        
        ans = 0
        for i in range(n - 1):
            # rank 求出比 s[i] 小的字符数量
            rank = sum(occ for ch, occ in freq.items() if ch < s[i])
            # 排列个数的分子
            cur = rank * fac[n - i - 1] % mod
            # 依次乘分母每一项阶乘的乘法逆元
            for ch, occ in freq.items():
                cur = cur * facinv[occ] % mod
            
            ans += cur
            freq[s[i]] -= 1
            if freq[s[i]] == 0:
                freq.pop(s[i])
        
        return ans % mod


    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [
    # sol.minOperations(nums = [1,5,2,4,1]),
    # sol.countPoints(points = [[1,3],[3,3],[5,3],[2,2]], queries = [[2,3,1],[4,3,1],[1,1,2]]),
    
    # sol.getMaximumXor(nums = [0,1,1,3], maximumBit = 2),
    # sol.getMaximumXor([0,1,2,2,5,7], maximumBit = 3),
    
    sol.makeStringSorted(s = "cba"),
    sol.makeStringSorted(s = "cdbea"),
    sol.makeStringSorted("aabaa"),
    sol.makeStringSorted(s = "leetcodeleetcodeleetcode")
]
for r in result:
    print(r)
