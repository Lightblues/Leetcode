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
这里总结如何从问题出发, 来去思考应该用什么DS.

@2022 """
class Solution:
    """ 0327. 区间和的个数 #hard #题型 #线段树
给定一个数组, 要求其所有的子区间中, 区间和在 [lower, upper] 范围内的数量
限制: 数组长度 1e5, 元素大小 32bit
see [官答](https://leetcode.cn/problems/count-of-range-sum/solution/qu-jian-he-de-ge-shu-by-leetcode-solution/)
提示: 我们从小到大遍历j, 要使得 `sum[i...j] = acc[j]-acc[i-1]` 在 [lower, upper] 范围内, 需要 acc[i-1] 在 `[acc[j]-upper, acc[j]-lower]` 范围内. 
    因此需要一个DS能够插入数据, 并查询在某一范围内的元素数量.
思路0: 归并排序
思路1: #线段树
    求在一个范围内的数字有多少, 显然可以用 #线段树 来做.
    具体而言, 对于每一个位置的元素, 先按照上式统计满足条件的以j结尾的区间数量, 然后将 preSum[j+1] 加入线段树.
    另外, 本题的数字上限很大, 需要将其转为连续整数 (#离散化), 也即, 将线段树中所有出现过的数字 (包括需要查询的 left, right) 变为 0~n-1 的连续整数.
思路2: 动态增加节点的线段树
思路3: 树状数组
思路4: 平衡二叉搜索树

"""
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        # 思路1, 作弊调用 sortedcontainers
        from sortedcontainers import SortedList
        acc = 0
        sl = SortedList([0])
        ans = 0
        for a in nums:
            acc += a
            l,r = acc-upper, acc-lower
            idxL, idxR = sl.bisect_left(l), sl.bisect_right(r)
            ans += idxR-idxL
            sl.add(acc)
        return ans
    
    
    
    
    

    
sol = Solution()
result = [
    sol.countRangeSum(nums = [-2,5,-1], lower = -2, upper = 2),
]
for r in result:
    print(r)
