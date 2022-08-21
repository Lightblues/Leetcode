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
二叉搜索树 https://leetcode.cn/leetbook/detail/introduction-to-data-structure-binary-search-tree/
@2022 """

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 验证二叉搜索树 判断给定的二叉搜索树是否合法
思路1: 递归函数 `valid(root: TreeNode, l:int, r:int)` 传入合法的区间 [l, r]
"""
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def valid(root: TreeNode, l:int, r:int) -> bool:
            if root is None: return True
            if not l<=root.val<=r: return False
            if not valid(root.left, l, root.val-1): return False
            if not valid(root.right, root.val+1, r): return False
            return True
        return valid(root, -inf, inf)
    
    
    
""" 二叉搜索树迭代器
给定一棵二叉树, 要求返回一个迭代器, 要求实现接口 `next()` 和 `hasNext()`. 限制: 节点数 O(n)
进阶要求: 限制两个操作的均摊代价为 O(1), 
"""
class BSTIterator:

    def __init__(self, root: Optional[TreeNode]):


    def next(self) -> int:


    def hasNext(self) -> bool:
    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
