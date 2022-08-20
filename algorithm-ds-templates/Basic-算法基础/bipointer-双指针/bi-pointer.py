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
from functools import lru_cache, cache, reduce, partial
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
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
# from structures import ListNode, TreeNode

""" 双指针总结


"""
class Solution:
    """ 2062. 统计字符串中的元音子字符串 #easy #题型
要求统计连续子序列的数量. 条件为: 1) 所有元素为元音字符 2) 包含所有aeiou五个元素.
思路1: 暴力检索. 时间复杂度 O(n^2)
    技巧: 这里要检查数组包括的所有元素, 天然就是 set 问题.
思路2: #双指针.
    先用re抽取所有仅由元音组成的子串, 对于每一个符合要求的子串, 双指针遍历.
    具体而言, 存储左右指针内包含的元音数量. 遍历有指针的过程中, 维护左指针使得「左右指针包含的包含所有元音的最短序列」, 这样, 以右指针结尾的包含左右元音的子串数量为 left+1.
"""
    def countVowelSubstrings(self, word: str) -> int:
        """ 双指针 O(n)
[here](https://leetcode.cn/problems/count-vowel-substrings-of-a-string/solution/on-shuang-zhi-zhen-xie-fa-by-endlesschen-6dkt/)
"""
        vowelSubs = re.findall(r'[aeiou]+', word)
        ans = 0
        ch2idx = {ch:i for i,ch in enumerate("aeiou")}
        for sub in vowelSubs:
            left = 0
            count = [0] * 5
            for ch in sub:
                count[ch2idx[ch]] += 1
                while count[ch2idx[sub[left]]]>1:
                    count[ch2idx[sub[left]]] -= 1
                    left += 1
                if all(c>0 for c in count):
                    ans += left+1
        return ans


sol = Solution()
result = [
    
]
for r in result:
    print(r)
