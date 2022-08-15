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


 """
class Solution:
    """ 1392. 最长快乐前缀 #hard #KMP
给定一个字符串s, 要求最长的, 既是s的前缀也是后缀的子串.
思路1: #KMP
    显然, 如果知道KMP算法, 那么答案就可由 #部分匹配表 或者 #前缀函数 直接得到, 也即长为 `fail[len-1]+1` 的前缀
    复杂度: O(n)
思路2: #Rabin-Karp 字符串编码   通过字符串编码来判断前后缀是否相同
    注意到, 既可以从左往右也可以从右往左拓展计算编码的字符串长度. 因此我们1...n枚举长度, 每次比较前后缀是否相同即可.
[官答](https://leetcode.cn/problems/longest-happy-prefix/solution/zui-chang-kuai-le-qian-zhui-by-leetcode-solution/)
"""
    
    def longestPrefix(self, s: str) -> str:
        # 思路1: #KMP
        n = len(s)
        fail = [-1] * n
        
        for i in range(1, n):
            j = fail[i - 1]
            while j != -1 and s[j + 1] != s[i]:
                j = fail[j]
            if s[j + 1] == s[i]:
                fail[i] = j + 1

        return s[:fail[-1] + 1]
    def longestPrefix(self, s: str) -> str:
        # 思路2: #Rabin-Karp 字符串编码
        n = len(s)
        prefix, suffix = 0, 0
        base, mod, mul = 31, 1000000007, 1
        happy = 0
        for i in range(1, n):
            prefix = (prefix * base + (ord(s[i - 1]) - 97)) % mod
            suffix = (suffix + (ord(s[n - i]) - 97) * mul) % mod
            if prefix == suffix:
                happy = i
            mul = mul * base % mod
        return s[:happy]

    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
