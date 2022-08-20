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
https://oi-wiki.org/string/z-func/


== 题目列表
2223. 构造字符串的总得分和
    对于一个字符串, 从右往左得到长度为 1,2,... 的连续子串, 分别计算该子串与原字符串的最大前缀长.
@2022 """
class Solution:
    """ 2223. 构造字符串的总得分和
对于一个字符串, 从右往左得到长度为 1,2,... 的连续子串, 分别计算该子串与原字符串的最大前缀长.

输入：s = "babab"
输出：9
解释：
s1 == "b" ，最长公共前缀是 "b" ，得分为 1 。
s2 == "ab" ，没有公共前缀，得分为 0 。
s3 == "bab" ，最长公共前缀为 "bab" ，得分为 3 。
s4 == "abab" ，没有公共前缀，得分为 0 。
s5 == "babab" ，最长公共前缀为 "babab" ，得分为 5 。
得分和为 1 + 0 + 3 + 0 + 5 = 9 ，所以我们返回 9 。

Z 函数（扩展 KMP） 参见 https://oi-wiki.org/string/z-func/
我们定义 Z 函数为: z[i] 为 s[i:n-1] 与原字符串 s 的最长前缀匹配长度.
核心是要维护一个匹配区间 [l,r] (闭区间) 满足该区间为前缀; 在遍历过程中, 维护 `l<=i`.
    对于遍历到的 i, 若 `i<=r`, 此时有 `s[i:r] = s[i-l:r-l]` (闭区间),
        若还满足 z[i-l]<r-i+1 (区间 [i,r] 的长度为 r-i+1, 我们已经在遍历 i-l 时发现了前缀匹配长度比它小), 则有 z[i] = z[i-l]
        否则, 说明 [i,r] 区间是前缀, 从 r+1 开始继续匹配
    若不满足 `i<=r`, 则从 i+1 开始继续匹配 (和上面的情况2一样)
    注意当我们遍历超过 r 时需要更新 `l, r = i, i+z[i]-1` (显然维护的条件 `i<=l` 仍满足)
复杂度分析 (看下面的代码): 外层 i 循环一遍, 内部的 while 训练每执行一次都会使得 r 向后移动, 因此最多执行 O(n) 次; 所以总的复杂度为 O(n).
    """
    def sumScores_v0(self, s: str) -> int:
        """ 暴力方法, 时间复杂度 O(n^2) 会超时 """
        n = len(s)
        z = [0] * n
        for i in range(1, n):
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                z[i] += 1
        return sum(z) + n

    def sumScores(self, s: str) -> int:
        n = len(s)
        z = [0] * n
        l,r = 0,0
        for i in range(1,n):
            if i<=r and z[i-l]<r-i+1:
                z[i] = z[i-l]
            else:
                z[i] = max(0, r-i+1)
                while i+z[i]<n and s[z[i]]==s[i+z[i]]:
                    z[i] += 1
            if i+z[i]-1 > r:
                r = i+z[i]-1
                l = i
        return sum(z) + n
        
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
