""" LeetCode Python 本地测试模板 @Lightblues 221102
本模板是什么? 用于本地测试 LeetCode 的代码, 试图还原Leetcode的测试环境
    直接复制测试用例, 可以在本地编辑器中调试.
    导入了常见的包函数, 可以直接使用 (并且可以方便查到这些函数是来自哪些包的, 熟悉库函数)
    提供了类测试函数, 直接测试需要实现类的那种题目
为什么要在本地测试? 
    代码留存, 方便日后查看
    本地调试, 相较于LC的在线编辑器这一功能稍微好一些
    代码编辑器有更好的自动补全等方便的功能
如何使用? 
    可以复制下面的模板, 修改下面注释部分的代码, 尝试在本地运行~
    对于一般的要求实现函数的题目, 在Solution类中实现, 然后复制用例到result列表中, 本地运行/调试即可.
    对于要实现类的题目, 在全局环境实现要求的类, 然后在result中调用testClass函数进行测试. 
实用: 打断点; 配合Copilot等. 

实际使用例子: https://github.com/Lightblues/Leetcode/blob/main/contest/151-200/161.py
"""

""" 下面导入的包是在leetcode中常用的, 可以直接在其编程环境下使用这些函数. 
我也写到了自己的包 easonsi 中, 等价于下面这行
from easonsi.util.leetcode import *
"""
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

class Solution:
    """ ########################## 1.1 实现函数的题目 ##########################
0001. 两数之和 #easy
https://leetcode.cn/problems/two-sum/
"""
    def twoSum(self, nums, target):
        partner = {}
        for index, num in enumerate(nums):
            if target-num in partner:
                return index, partner[target-num]
            partner[num] = index

""" ########################## 1.2 实现类的题目 ##########################
2241. 设计一个 ATM 机器 #medium
https://leetcode.cn/problems/design-an-atm-machine/
"""
class ATM:
    def __init__(self):
        self.values = [20, 50, 100, 200, 500]
        self.counts = [0] * 5

    def deposit(self, banknotesCount: List[int]) -> None:
        for i,num in enumerate(banknotesCount):
            self.counts[i] += num

    def withdraw(self, amount: int) -> List[int]:
        reversedCount = []
        for v, count in zip(reversed(self.values), reversed(self.counts)):
            a = min(count, amount // v)
            reversedCount.append(a)
            amount -= a * v
        if amount != 0:
            return [-1]
        counts = list(reversed(reversedCount))
        for i,c in enumerate(counts):
            self.counts[i] -= c
        return counts
    
sol = Solution()
""" ########################## 2. 在这里填入测试用例 ########################## """
result = [
    # sol.twoSum(nums = [2,7,11,15], target = 9),
    # sol.twoSum(nums = [3,2,4], target = 6),
    testClass("""["ATM", "deposit", "withdraw", "deposit", "withdraw", "withdraw"]
[[], [[0,0,1,2,1]], [600], [[0,1,0,1,1]], [600], [550]]"""),
]
for r in result:
    print(r)
