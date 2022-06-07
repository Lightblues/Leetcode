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
from functools import lru_cache, reduce, partial # cache
cache = partial(lru_cache, maxsize=None)
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
https://leetcode.cn/contest/weekly-contest-259
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 2011. 执行操作后的变量值 """
    def finalValueAfterOperations(self, operations: List[str]) -> int:
        ans = 0
        for op in operations:
            if '--' in op: ans -= 1
            else: ans += 1
        return ans
    
    """ 2012. 数组美丽值求和 """
    def sumOfBeauties(self, nums: List[int]) -> int:
        n = len(nums)
        rightMin = [0] * n
        rightMin[-1] = nums[-1]
        for i in range(n-2, -1, -1):
            rightMin[i] = min(rightMin[i+1], nums[i])
        leftMax = nums[0]
        ans = 0
        for i in range(1, n-1):
            if leftMax < nums[i] < rightMin[i+1]: ans += 2
            elif nums[i-1] < nums[i] < nums[i+1]: ans += 1
            leftMax = max(leftMax, nums[i])
        return ans
    
    """ 2014. 重复 K 次的最长子序列 #hard
给定一个长度为n的字符串, 对于一个给定的整数 k, 要求从中找到最长的字符串 sub, 使得 sub * k 是原字符串的子串.
约束: 2 <= k <= 2000, 而字符串长度 2 <= n < k * 8
思路1: #枚举排列
    注意这里的数据特性: 由于字符串长度小于 `k * 8`, 而我们要的目标串重复度为 k. **因此可能出现的字符最多只有7个**.
    因此, 可以枚举所有的目标字符 (从长到短, 根据字典序从大到小), 然后判断是否满足条件即可.
    Note: 下面第一个是我自己写的, 极为冗长; 第二个是 [here](https://leetcode.cn/problems/longest-subsequence-repeated-k-times/solution/zui-jian-ji-yi-dong-de-fang-fa-li-yong-z-hay1/) 利用了 1) combinations函数; 2) iter+in + all 判断子序列是否包含的神奇用法(替代双指针), 极为优雅.
另外, 手动 #枚举排列 参见 [灵神](https://leetcode.cn/problems/longest-subsequence-repeated-k-times/solution/mei-ju-pai-lie-zi-xu-lie-pi-pei-by-endle-oi2h/) #TODO
"""
    def longestSubsequenceRepeatedK(self, s: str, k: int) -> str:
        counter = Counter(s)
        chars = ''
        for ch, cnt in counter.items():
            chars += ch * (cnt // k)
        # 
        def test(pattern):
            # 检测s中是否包含k个pattern
            idx = 0
            cnt = 0
            for ch in s:
                if ch == pattern[idx]:
                    idx += 1
                    if idx==len(pattern):
                        if cnt==k-1: return True
                        cnt += 1
                        idx = 0
            return False
        
        def getPermutations(s: str):
            # 得到s的所有可能的排列形式
            if len(s)==1: return [s]
            ret = []
            for i,ch in enumerate(s):
                ret += [ch+p for p in getPermutations(s[:i]+s[i+1:])]
            return ret
        
        # 从所有可能使用的字符集合 (最大长度为7) 中得到所有可能的子集
        len2patterns = defaultdict(set)
        for mask in range(1, 1<<len(chars)+1):
            pattern = ''
            for i in range(len(chars)):
                if mask & (1<<i):
                    pattern += chars[i]
            len2patterns[len(pattern)].add(pattern)
        for l in range(len(chars), 0, -1):
            # 对于所选的子集, 检查所有的排列形式
            # for p in sorted(len2patterns[l], reverse=True):
            patterns = set()
            for ss in len2patterns[l]:
                patterns |= set(getPermutations(ss))
            patterns = sorted(patterns, reverse=True)
            for p in patterns:
                if test(p): return p
        return ""
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res

    def longestSubsequenceRepeatedK(self, s: str, k: int) -> str:
        """ from [here](https://leetcode.cn/problems/longest-subsequence-repeated-k-times/solution/zui-jian-ji-yi-dong-de-fang-fa-li-yong-z-hay1/)
        充分利用了 Python 的简洁特性"""
        num = Counter(s)
        hot = ''.join(ele * (num[ele] // k) for ele in sorted(num, reverse=True))
        for i in range(len(hot), 0, -1):
            # permutations 得到所有从 iterable 中得到 k 个元素的排列
            for item in permutations(hot, i):
                word = ''.join(item)
                ss = iter(s)
                # `iter` 配合 `in` 的用法! 替代了双指针判断
                # 利用到的是python迭代器只能前进的特性
                if all(c in ss for c in word * k):
                    return word
        return ''


""" 2013. 检测正方形 #medium
要求实现一个类, 可以计算在平面内的轴对齐正方形数量. 实现操作: 1) 在平面上加一个点; 2) 查询, 给定一个位置, 计算其与平面上其他三个点构成正方形的数量.
思路: #枚举 匹配边
    主要是查询: 对于给定的位置 (x1, y1), 我们可以将其与同一列中 x2 进行匹配, 这样我们确定了正方形的一条边, 可能的组合直接往左右两侧尝试, 计数即可.
    具体实现上, 可以用 `self.x2ys = defaultdict(Counter)` 统计每个单元格被加入的点数.
"""
class DetectSquares:
    def __init__(self):
        self.x2ys = defaultdict(Counter)

    def add(self, point: List[int]) -> None:
        x, y = point
        self.x2ys[x][y] += 1

    def count(self, point: List[int]) -> int:
        x1, y1 = point
        potentialPairs = self.x2ys[x1]
        ans = 0
        # (x1, y2)
        for y2, c2 in potentialPairs.items():
            if y2==y1: continue
            d = abs(y2 - y1)
            for x2 in [x1-d, x1+d]:
                counter = self.x2ys[x2]
                ans += c2 * counter[y2] * counter[y1]
        return ans

sol = Solution()
result = [
    # sol.sumOfBeauties(nums = [1,2,3]),
    # sol.sumOfBeauties(nums = [2,4,6,4]),
#     sol.testClass("""["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
# [[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]"""),

    sol.longestSubsequenceRepeatedK(s = "letsleetcode", k = 2),
    sol.longestSubsequenceRepeatedK("bb", 2),
    sol.longestSubsequenceRepeatedK("mciuctbmciuctb",2),
]
for r in result:
    print(r)
