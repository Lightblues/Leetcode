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
from functools import lru_cache, reduce, partial, cache # cache
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

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-229
@2022 """
class Solution:
    """ 1768. 交替合并字符串 """
    def mergeAlternately(self, word1: str, word2: str) -> str:
        n = min(len(word1), len(word2))
        s = ""
        for i in range(n): s+= word1[i] + word2[i]
        s += word1[n:] + word2[n:]
        return s
        
    """ 1769. 移动所有球到每个盒子所需的最小操作数 """
    def minOperations(self, boxes: str) -> List[int]:
        n = len(boxes)
        idxs = [i for i in range(n) if boxes[i] == "1"]
        return [sum(abs(i-j) for j in idxs) for i in range(n)]
    
    """ 1770. 执行乘法运算的最大分数 #medium
给定一个长m的分数数组multipliers, 每次从长 n>m 的数组nums头/尾选择一个, 要求每次选择的加权和分数最大.
限制: m 1e3, n 1e5. 元素大小 [-1e3, 1e3]
思路: #DP
    记 `f[i][j]` 表示选择前i个后j时的最大分数 (范围 i,j 都是 `0...m`)
    递推: `f[i][j] = max{ m[i+j-1]*nums[i-1] + f[i-1][j], m[i+j-1]*nums[-j] + f[i][j-1] }`
    边界: i,j 其中一个为0的时候, 计算是固定的.
    答案: `max{ f[i][m-i] }`
    复杂度: O(m^2)
讨论: 关于 **cache的使用以及maxsize的设置**
    问题的起因是下面采用记忆化搜索, 直接用 `@lru_cache(None)` 在LC平台会爆TLE (但实际上应该是MLE). 尝试了下面的三个可以解决: 1) 修改成table dp, 不用多说; 2) 在函数执行的结尾加上 `gc.collect()` 手动清理内存; 3) 设置 `maxsize` 为合适的值.
    见提交记录 [submission](https://leetcode.cn/problems/maximum-score-from-performing-multiplication-operations/submissions/) 可以发现maxsize的设置起了一些影响 (居然在2000左右效果最好), 而开太大或者None会导致MLE.
    然后在 0516 上进一步测试了不同maxsize的影响, 见 [here](https://leetcode.cn/problems/longest-palindromic-subsequence/submissions/). 结论: 1) maxsize较小时很容易TLE; 2) 存在一个较好的区间, 使得在memory开销有限的情况下用时最短; 3) 设置成None或者很大时, 不会增加太多的用时, 但memory开销显著增加, 就有可能导致本题中出现MLE.
    参见 [here](https://leetcode.com/problems/stone-game-vii/discuss/1264544/Python-O(n*n)-dp-solution-how-to-avoid-TLE-explained/970807/) 的讨论.
"""
    def maximumScore(self, nums: List[int], multipliers: List[int]) -> int:
        """ 采用记忆化搜索.  """
        n,m = len(nums), len(multipliers)
        # @lru_cache(None)
        # @lru_cache(2000)
        def f(i: int ,j: int):
            # if i==0: return sum(x*y for x,y in zip(nums[-j:][::-1], multipliers))
            # if j==0: return sum(x*y for x,y in zip(nums[:i], multipliers))
            if i==0==j: return 0
            if i==0: return multipliers[j-1]*nums[-j] + f(i,j-1)
            if j==0: return multipliers[i-1]*nums[i-1] + f(i-1,j)
            return max(
                multipliers[i+j-1]*nums[i-1] + f(i-1,j), 
                multipliers[i+j-1]*nums[-j] + f(i,j-1)
            )
        
        # memory = {}
        # memory[(0,0)] = 0
        # for i in range(1, m+1):
        #     memory[(0,i)] = multipliers[i-1]*nums[-i] + memory[(0,i-1)]
        #     memory[(i,0)] = multipliers[i-1]*nums[i-1] + memory[(i-1,0)]
        # def f(i: int ,j: int):
        #     if (i,j) in memory: return memory[(i,j)]
        #     ans = max(
        #         multipliers[i+j-1]*nums[i-1] + f(i-1,j), 
        #         multipliers[i+j-1]*nums[-j] + f(i,j-1)
        #     )
        #     memory[(i,j)] = ans
        #     return ans
        
        return max(f(i,m-i) for i in range(m+1))
    def maximumScore0(self, nums: List[int], multipliers: List[int]) -> int:
        n,m = len(nums), len(multipliers)
        f = [[0]*(m+1) for _ in range(m+1)]
        for i in range(1,m+1):
            f[i][0] = multipliers[i-1]*nums[i-1] + f[i-1][0]
            f[0][i] = multipliers[i-1]*nums[-i] + f[0][i-1]
        for i in range(1,m+1):
            for j in range(1,m-i+1):
                f[i][j] = max(
                    multipliers[i+j-1]*nums[i-1] + f[i-1][j], 
                    multipliers[i+j-1]*nums[-j] + f[i][j-1]
                )
        return max(f[i][m-i] for i in range(m+1))
    
    
    """ 1771. 由子序列构造的最长回文串的长度 #hard #题型 #回文
给定两个字符串 word1, word2, 选择两个非空子序列拼起来, 要求构成最长的回文串.
限制: n 1e3
思路: 完全参考「0516. 最长回文子序列」, 将两个字符串拼起来找最长回文子序列. 只需要在更新过程中判断是否两个字符串都取到了即可.
"""
    def longestPalindrome(self, word1: str, word2: str) -> int:
        n1, n2 = len(word1), len(word2)
        n = n1+n2
        s = word1+word2
        f = [[0]*(n) for _ in range(n)]
        ans = 0
        for i in range(n-1, -1, -1):
            f[i][i] = 1
            for j in range(i+1, n):
                if s[i] == s[j]:
                    f[i][j] = f[i+1][j-1] + 2
                    # 只需要在这里检查即可: 这里才会增加最大长度, 并且两端都取到
                    if i<n1<=j: ans = max(ans, f[i][j])
                else:
                    f[i][j] = max(f[i+1][j], f[i][j-1])
            # 注意不能放在这里更新, 因为这里计算的值是范围内的最大.
            # if i<n1<=j:
            #     ans = max(ans, f[i][j])
        return ans
    
    """ 0516. 最长回文子序列 #medium #回文 #题型
给定一个长n的字符串, 找到最长回文子序列的长度.
思路: #DP
    `f[i][j]` 表示 s[i...j] 内的最长长度
    递推: 1) 若 s[i]==s[j], 则 `f[i][j] = f[i+1][j-1] + 2`; 2) 否则, `f[i][j] = max(f[i+1][j], f[i][j-1])`
    边界: `f[i][i] = 1`. 
    根据递推公式, 可以「斜」着进行遍历. 根据 d=j-i 从小到大遍历. i,j 需要在合适的范围内.
    [官答](https://leetcode.cn/problems/longest-palindromic-subsequence/solution/zui-chang-hui-wen-zi-xu-lie-by-leetcode-hcjqp/)
"""
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        f = [[0]*n for _ in range(n)]
        for i in range(n): f[i][i] = 1
        for d in range(1, n):
            for i in range(n-d):
                j = i+d
                if s[i]==s[j]: f[i][j] = f[i+1][j-1] + 2
                else: f[i][j] = max(f[i+1][j], f[i][j-1])
        # return max(max(f[i]) for i in range(n))
        return f[0][n-1]
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        @lru_cache(None)
        def f(i:int, j:int):
            if i>j: return 0
            if i==j: return 1
            if s[i]==s[j]: return f(i+1, j-1) + 2
            else: return max(f(i+1, j), f(i, j-1))
        return f(0, n-1)


sol = Solution()
result = [
    # sol.mergeAlternately(word1 = "abc", word2 = "pqr"),
    # sol.mergeAlternately(word1 = "abcd", word2 = "pq"),
    # sol.minOperations(boxes = "001011"),
    # sol.maximumScore(nums = [1,2,3], multipliers = [3,2,1]),
    # sol.maximumScore(nums = [-5,-3,-3,-2,7,1], multipliers = [-10,-5,3,4,6]),
    # sol.longestPalindromeSubseq(s = "bbbab"),
    
    sol.longestPalindrome(word1 = "cacb", word2 = "cbba"),
    sol.longestPalindrome(word1 = "aa", word2 = "bb"),
    
    
    
]
for r in result:
    print(r)
