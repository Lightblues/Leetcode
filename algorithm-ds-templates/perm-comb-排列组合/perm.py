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
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
0031. 下一个排列 #medium #题型
    给定一个数组, 要求得到它的一个重排, 是「下一个字典序比它大的」排列.
    例如, [1,3,2] 的下一个排列就是 [2,1,3].
    应用: 1947. 最大兼容性评分和 #medium

 """
class Solution:
    """ 0031. 下一个排列 #medium #题型
给定一个数组, 要求得到它的一个重排, 是「下一个字典序比它大的」排列.
    例如, [1,3,2] 的下一个排列就是 [2,1,3]. 注意最常用的就是排列的定义, 但对于任意数组都成立, 例如 [1,1,5] 的下一个排列是 [1,5,1]
    约束: 长度100; 必须原地修改数组 (也即只允许使用额外常数空间).
思路1: #两遍扫描
    例如, 对于 [4,5,2,6,3,1] 我们如何考虑下一个排列? 顺序扫描过去, 我们会把2替换成3, 然后把剩余的[6,2,1]三个元素sort.
    因此, 我们要找到一组下标 (i,j) 满足 `i<j; arr[i]<arr[j]` 并且这里的 **i尽可能右, arr[j] 尽可能小**, 这样直觉来看增长最小.
    如何寻找? 从左往右查找第一个下标 i, 满足 `i<j; arr[i]<arr[j]` 的组合.
    需要和i右边的所有元素比较吗? 实际上只需要比较 arr[i]<arr[i+1] 是否成立即可! 因为这样从右往左遍历下来, arr[i+1:] 是递减的.
    如何找到j? 再一次从左往右遍历, 找到第一个 arr[i]<arr[j] 的位置j. 然后交换 ij, 对于 arr[i+1:] 进行排序
    需要sort吗? 前面说到 arr[i+1:] 是递减的, 而交换ij之后性质不变, 因此 **只需要反转这一数组即可**.
    [官答](https://leetcode.cn/problems/next-permutation/solution/xia-yi-ge-pai-lie-by-leetcode-solution/)
"""
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        [官答](https://leetcode.cn/problems/next-permutation/solution/xia-yi-ge-pai-lie-by-leetcode-solution/)
        """
        # 第一次, 找到 i
        n = len(nums)
        for i in range(n-2, -2, -1):
            if nums[i] < nums[i+1]:
                break
        # 边界情况: 已经是最大的排列了
        if i==-1:
            nums.reverse()
            return
        # 第二次: 找到j
        for j in range(n-1, i, -1):
            if nums[i] < nums[j]: break
        # 交换
        nums[i], nums[j] = nums[j], nums[i]
        # 反转
        l,r = i+1, n-1
        while l<r:
            nums[l], nums[r] = nums[r], nums[l]
            l,r = l+1, r-1
            
    def test_nextPermutation(self, nums):
        pre = nums[:]
        self.nextPermutation(nums)
        print(f"{pre} -> {nums}")


sol = Solution()
sol.test_nextPermutation(nums = [1,2,3]),
sol.test_nextPermutation(nums = [3,2,1]),
sol.test_nextPermutation([1,1,5])
result = [
    
]
for r in result:
    print(r)
