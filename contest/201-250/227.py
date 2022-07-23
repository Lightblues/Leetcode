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
https://leetcode.cn/contest/weekly-contest-227
@2022 """
class Solution:
    """ 1752. 检查数组是否经排序和轮转得到 """
    def check(self, nums: List[int]) -> bool:
        n = len(nums)
        for i in range(1, n):
            if nums[i-1]>nums[i]:
                if nums[-1]>nums[0]: return False
                for j in range(i+1,n):
                    if nums[j]<nums[j-1]: return False
                return True
        return True
    
    """ 1753. 移除石子的最大得分 """
    def maximumScore(self, a: int, b: int, c: int) -> int:
        a,b,c = sorted([a,b,c])
        if a+b<=c: return a+b
        return (a+b+c)//2

    """ 1754. 构造字典序最大的合并字符串 #medium #题型
给定两个字符串. 每次选择其中一个取最左边的字符. 要求得到的合并字符串字典序最大.
限制: 长度  3e3
思路1: #贪心 #双指针
    用两个指针记录在两字符串上遍历的位置, 若不同时显然贪心选择较大的那一个.
    难点是相同的时候? 例如: "aa", "ab" 显然应该选择后者. 因此, 直观的想法从i,j顺序向后, 直到直线不同的.
        一开始走到死胡同: 想要直接用 i:ii 这一段遍历的部分. 但这样有问题: 例如 "babb", "baa", 最大merge应该是 `bbabbaa`, 若直接用的话会变成 `bab...`
        转换思路: 比较结束之后, 只使用当前的开始char即可. 然后从新开始比较即可.
        事实上, 这样的话, 可以直接用内置的字符串比较函数 `word1[i:]>word2[j:]` 即可
    see [here](https://leetcode.cn/problems/largest-merge-of-two-strings/solution/27zhou-sai-gou-zao-zi-dian-xu-zui-da-de-u0fhx/)
"""
    def largestMerge(self, word1: str, word2: str) -> str:
        n1, n2 = len(word1), len(word2)
        i,j = 0,0
        ans = ""
        while i<n1 or j<n2:
            # 一个用完了
            if i>=n1: ans += word2[j:]; break
            if j>=n2: ans += word1[i:]; break
            # 选择较大的
            if word1[i]>word2[j]:
                ans += word1[i]
                i+=1
            elif word1[i]<word2[j]:
                ans += word2[j]
                j += 1
            else:
                # 1.0 从 i,j 出发向后遍历. 事实上就是比较 word1[i:]>word2[j:]
                # ii,jj = i+1,j+1
                # target = 1
                # while ii<n1 or jj<n2:
                #     if jj==n2: break
                #     if ii==n1: target = 2; break
                #     if word1[ii]<word2[jj]: target = 2; break
                #     elif word1[ii]>word2[jj]: break
                #     else: 
                #         # if word1[ii]>word1[i]:
                #         #     break
                #         ii,jj = ii+1, jj+1
                # # if target == 1:
                # #     ans += word1[i:ii+1]
                # #     i = ii+1
                # # else:
                # #     ans += word2[j:jj+1]
                # #     j = jj+1
                # if target==1:
                #     ans += word1[i]; i+= 1
                # else:
                #     ans += word2[j]; j+= 1
                
                # 1.1 直接比较后续字符串的字典序
                if word1[i:]>word2[j:]:
                    ans += word1[i]; i+= 1
                else: ans += word2[j]; j+= 1
        return ans


    """ 1755. 最接近目标值的子序列和 see subset_half """

sol = Solution()
result = [
    sol.largestMerge(word1 = "cabaa", word2 = "bcaaa"),
    sol.largestMerge("jxddxdxddddxddddjdxdddddd", "ddddxddxdjdddxddjjddjdjdxdddj"),
]
for r in result:
    print(r)
