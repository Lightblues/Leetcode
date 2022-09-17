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
[力扣杯竞赛真题集](https://leetcode.cn/study-plan/lccup)




@2022 """
class Solution:
    """ LCP 39. 无人机方阵 #easy
将一组数量为n的数字, 变换为另一组长度也为n的数字, 可以随意调换顺序, 问最小需要修改多少次数字的值?
思路1: 利用 Counter 计数. 然后计算差值
    1.1 将s和t分别统计到两个哈希表. 结果是什么? 注意不应该取 (cnt_s - cnt_t) 的 abs, 而应该取正数部分! (考虑对称)
    1.2 也可以将s和t中的数字统计在一个哈希表中, 分别取 +和-. 这样答案自然就是正数/负数 之和.
 """
    def minimumSwitchingTimes(self, source: List[List[int]], target: List[List[int]]) -> int:
        cnts = Counter(itertools.chain(*source))
        # cnts = reduce(add, [Counter(s) for s in source])
        cntt = reduce(add, [Counter(s) for s in target])
        ans = 0
        for k,v in cnts.items():
            # 注意, 这里统计的不能是 abs 和!
            # 考虑 [1,2,2] -> [1,1,2] 的情况, 取一个方向的正值即可.
            ans += max(v - cntt[k], 0)
        return ans
    
    """ LCP 40. 心算挑战 #easy
要求从一组数字中选出cnt个, 要求这些数字之和为偶数. 若取不到则返回0. 限制: cnt, n 1e5
思路1: 排序+前缀和+遍历
    对于奇偶数分组, 排序.
    因为要求和为偶数, 奇数组必须选择偶数个, 遍历所有的可能, 取最大值. 为了快速得到区间和, 使用 #前缀和.
 """
    def maxmiumScore(self, cards: List[int], cnt: int) -> int:
        odds, evens = [], []
        for c in cards:
            if c & 1: odds.append(c)
            else: evens.append(c)
        odds.sort(reverse=True); evens.sort(reverse=True)
        oddcum = list(accumulate(odds, initial=0))
        evencum = list(accumulate(evens, initial=0))
        ans = 0
        for i in range(0, cnt+1, 2):
            if i > len(odds) or cnt-i > len(evens): continue
            ans = max(ans, oddcum[i] + evencum[cnt-i])
        return ans
    
    
    """ LCP 41. 黑白翻转棋 #medium 给定一个黑白棋盘, 问在任意位置下黑棋, 最多能翻转多少个白棋? 限制: 长宽 8"""
    def flipChess(self, chessboard: List[str]) -> int:
        m,n = len(chessboard), len(chessboard[0])
sol = Solution()
result = [
    # sol.minimumSwitchingTimes(source = [[1,2,3],[3,4,5]], target = [[1,3,5],[2,3,4]]),
    sol.maxmiumScore(cards = [1,2,8,9], cnt = 3),
]
for r in result:
    print(r)
