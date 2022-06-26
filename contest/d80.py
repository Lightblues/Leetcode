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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-80
@2022 """
class Solution:
    """ 2299. 强密码检验器 II #easy #题型
要求: 至少8位; 相邻位不同字符; 至少包含一个数字; 至少包含一个小写字母; 至少包含一个大写字母; 至少包含一个特殊字符"!@#$%^&*()-+";
思路1: 用集合 intersection 判断是否包含某一类字符
思路2: 用位运算来记录是否包含某一类字符
    例如: 大/小写/数字/特殊字符分别表示1-4位, 对于所有的字符求或, 则包括所有的类型等价于, 最后的运算结果为 15.
    see [灵神](https://leetcode.cn/problems/strong-password-checker-ii/solution/go-jian-ji-xie-fa-by-endlesscheng-w3lu/)

"""
    def strongPasswordCheckerII(self, password: str) -> bool:
        if len(password) < 8: return False
        s = set(password)
        if not s.intersection(set(string.ascii_lowercase)): return False
        if not s.intersection(set(string.ascii_uppercase)): return False
        if not s.intersection(set(string.digits)): return False
        if not s.intersection(set("!@#$%^&*()-+")): return False
        for i in range(len(password)-1):
            if password[i] == password[i+1]:
                return False
        return True
    
    """ 2300. 咒语和药水的成功对数 """
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort()
        n = len(potions)
        ans = []
        for s in spells:
            ans.append(n-bisect.bisect_left(potions, success/s))
        return ans
    
    """ 2301. 替换字符后匹配 """
    def matchReplacement(self, s: str, sub: str, mappings: List[List[str]]) -> bool:
        pass
    
    """ 2302. 统计得分小于 K 的子数组数目 #hard 
see [灵神](https://leetcode.cn/problems/count-subarrays-with-score-less-than-k/solution/by-endlesscheng-b120/)
"""
    def countSubarrays(self, nums: List[int], k: int) -> int:
        """ 不知道为啥, bisect 老是越界 """
        n = len(nums)
        acc = list(accumulate(nums, initial=0))
        left = 0
        ans = 0
        for i in range(n):
            idx = bisect_left(acc, i+1, lo=left, hi=i+1, 
                              key=lambda x: 1 - ((acc[i+1] - acc[x]) * (i+1-x) >= k))
            ans += i-idx+1
            left = idx
        return ans

    
sol = Solution()
result = [
    # sol.strongPasswordCheckerII(password = "IloveLe3tcode!"),
    # sol.strongPasswordCheckerII(password = "Me+You--IsMyDream"),
    # sol.strongPasswordCheckerII(password = "1aB!"),
    # sol.successfulPairs(spells = [5,1,3], potions = [1,2,3,4,5], success = 7),
    sol.countSubarrays(nums = [2,1,4,3,5], k = 10),
]
for r in result:
    print(r)
