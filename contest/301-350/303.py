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
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 6124. 第一个出现两次的字母 """
    def repeatedCharacter(self, s: str) -> str:
        ss = set()
        for ch in s:
            if ch in ss: return ch
            ss.add(ch)
    
    """ 6125. 相等行列对 """
    def equalPairs(self, grid: List[List[int]]) -> int:
        n = len(grid)
        row2cnt = Counter()
        for i in grid:
            row2cnt[tuple(i)] += 1
        ans = 0
        for j in range(n):
            col = tuple(grid[i][j] for i in range(n))
            ans += row2cnt[col]
        return ans
    
    """ 6127. 优质数对的数目 #hard
给定一个正整数数组, 要求统计「优质数对」的数目. (num1, num2) 优质要求满足, 两者都在数组中出现过, 并且 `num1 OR num2` 和 `num1 AND num2` 两个数字的 `bit_count` 之和 >=k.
限制: 数组长度 1e5. 元素大小 1e9, k<=6
提示: `(a | b).bc() = a.bc() + b.bc() - (a & b).bc()`
思路1: 根据提示, 可知, 两个数字只需要满足 `a.bc() + b.bc() >= k` 即可.
    细节: 这里要求统计的不同的数对 `(num1, num2)`, 即使num1仅在数组中出现一次, 也可以有 (num1, num1). 如何区别相同数字和不同数字的情况?
        简单思路是直接对于bc进行排序, 每次暴力二分查找可匹配的部分. 复杂度 O(n logn)
        另一种思路是对于bc进行Counter (实际上是分组排序). 注意到, 数字的bc最多为 30. 因此, 假设bc从0...30的数量向量为arr, 对于a, `arr[a] * sum{ arr[k-a...30] }` 对于后者可以用前缀和计算 `acc[-1] - acc[max(k-a, 0)]`. 复杂度 `O(n + 30)`
"""
    def countExcellentPairs(self, nums: List[int], k: int) -> int:
        nums = set(nums)
        bc = sorted(i.bit_count() for i in nums)
        ans = 0; n = len(bc)
        for a in bc:
            idx = bisect_left(bc, k-a)
            ans += n-idx
        return ans
    def countExcellentPairs(self, nums: List[int], k: int) -> int:
        nums = set(nums)
        # 下面两种方式来统计不同bc的数量多少
        # 因为 (10**9).bit_length() == 30
        # bc = Counter(i.bit_count() for i in nums)
        # arr = [0]*31
        # for a,b in bc.items(): arr[a] = b
        arr = [0]*31
        for i in nums:
            arr[i.bit_count()] += 1
        # 计算acc加速
        acc = list(accumulate(arr, initial=0))
        # 按照 num1, num2 的方式枚举两个数! 注意, 正因如此, 这里不需要减去 num1==num2 可能重复计数的问题!
        ans = 0
        for a,count in enumerate(arr):
            ans += count * (acc[-1] - acc[max(0,k-a)])
        # for a,count in bc.items():
        #     if 2*a >= k: ans -= count
        return ans
    
""" 6126. 设计食物评分系统 这里无脑用了 SortedList, 实际上可以用最大堆, 然后用当前的食物评分来丢弃已被更新过的分数 """
from sortedcontainers import SortedList
class FoodRatings:
    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.cu2food = defaultdict(SortedList)
        self.food2cu = {}
        for f,c,r in zip(foods, cuisines, ratings):
            # rating 降序, food 升序
            self.cu2food[c].add((-r, f))
            self.food2cu[f] = (c, r)

    def changeRating(self, food: str, newRating: int) -> None:
        c, r = self.food2cu[food]
        self.cu2food[c].remove((-r, food))
        self.cu2food[c].add((-newRating, food))
        self.food2cu[food] = (c, newRating)

    def highestRated(self, cuisine: str) -> str:
        return self.cu2food[cuisine][0][1]
    
sol = Solution()
result = [
    # sol.equalPairs(grid = [[3,1,2,2],[1,4,4,5],[2,4,2,2],[2,4,2,2]]),
#     testClass("""["FoodRatings", "highestRated", "highestRated", "changeRating", "highestRated", "changeRating", "highestRated"]
# [[["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"], ["korean", "japanese", "japanese", "greek", "japanese", "korean"], [9, 12, 8, 15, 14, 7]], ["korean"], ["japanese"], ["sushi", 16], ["japanese"], ["ramen", 16], ["japanese"]]"""),
    sol.countExcellentPairs(nums = [1,2,3,1], k = 3),
    sol.countExcellentPairs(nums = [5,1,1], k = 10),
    sol.countExcellentPairs([1,2,4,8,16,32,64,128,256], 2),
]
for r in result:
    print(r)
