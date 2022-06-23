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

""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-49
@2022 """
class Solution:
    """ 1812. 判断国际象棋棋盘中一个格子的颜色 """
    def squareIsWhite(self, coordinates: str) -> bool:
        return ((ord(coordinates[0])-ord('a')) + (ord(coordinates[1])-ord('1'))) % 2 != 0
    
    """ 1813. 句子相似性 III #medium
有两个单词单词序列(句子), 问能否在某一个序列中插入一个任意序列(句子), 使得原本的两个句子相等.
思路1: #两端匹配
    注意到, 由于最多只能插入一个序列, 无非就是左右两端, 或者中间.
    这样, 在上面的任意情况下, 长序列从两端出发, 都可以完全匹配短序列.
    因此, 采用 #两端匹配, 用长序列从两侧匹配短的, 完全覆盖了则说明可以.
思路0: 贪心匹配, 错了!
    原本打算用短序列顺序匹配长序列, 用一个 `flag` 记录是否用过了插入的机会.
    但这样有问题, 例如 "A" 和 "a A b A" 的例子.
"""
    def areSentencesSimilar(self, sentence1: str, sentence2: str) -> bool:
        """ 错了! 不能贪心匹配, 例如 "A" 和 "a A b A" """
        words1, words2, = sentence1.split(), sentence2.split()
        if len(words2) > len(words1):
            words1, words2 = words2, words1
        idx = 0
        flag = False
        for w in words2:
            # 此时, 用掉了一次插入机会, 但是还有剩余的单词没有匹配
            if idx >= len(words1): return False
            if words1[idx] ==  w:
                idx += 1
            else:
                if flag: return False
                while idx < len(words1) and words1[idx] != w:
                    idx += 1
                idx += 1
                flag = True
        # 没有用掉插入的机会; 或者一次插入后, 匹配到了最后
        if  flag==False or idx==len(words1): return True
        return False
    
    def areSentencesSimilar(self, sentence1: str, sentence2: str) -> bool:
        # 思路1: #两端匹配
        words1, words2, = sentence1.split(), sentence2.split()
        # 令 words1 是长度较长的
        if len(words2) > len(words1):
            words1, words2 = words2, words1
        n = len(words2)
        left = 0
        while left<n and words2[left]==words1[left]:
            left += 1
        right = -1
        while right>=-n and words2[right]==words1[right]:
            right -= 1
        return left>(n+right)
    
    """ 1814. 统计一个数组中好对子的数目 """
    def countNicePairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        c = Counter()
        for num in nums:
            # num =list(map(int, str(num)))
            # if len(set(num)) == 1: 
            #     c[0] += 1
            # else:
            #     a = 0
            #     for i in range(1, len(num)):
            #         a = a*10 + num[i]-num[i-1]
            #     c[a] += 1
            # 算了, 直接算差值更方便
            diff = num - int(str(num)[::-1])
            c[diff] += 1
        ans = 0
        for _, v in c.items():
            if v >= 2:
                ans += v*(v-1)//2
        return ans % MOD
        
    """ 1815. 得到新鲜甜甜圈的最多组数 #hard #TODO
[problem](https://leetcode.cn/problems/maximum-number-of-groups-getting-fresh-donuts/)
每次烤 batchSize 个甜甜圈, 然后有一个数组 groups, 表示每次的客人需要购买的数量. 当某次顾客购买的甜甜圈中没有上一次卖剩下的情况下, 该顾客是开心的. 问, 任意调整 groups 顺序的情况下, 最多开心的数量.
约束: 每组数量 batchSize<=9; 客人组的长度最多为 30.

感觉题解的思路都不太清楚, TODO
"""
    def maxHappyGroups(self, batchSize: int, groups: List[int]) -> int:
        """ 思路0: 尝试打表求解, 失败
按照从大到小的顺序使用数字, 是不会出现问题的. 因为大数字可以被小数字的组合代替
但是, 问题在于, 打表所要的长度必须到 batchSize 级别, 例如9 的组合可能是 (1,1,2,2,3,3), 这样打表的时间也会超时.
"""
        cnt = [0] * batchSize
        for g in groups:
            cnt[g%batchSize] += 1
        pairsMap = [[], [], [(1, 1), (1, 1, 1, 1)], [(2, 1), (2, 2, 2), (1, 1, 1), (2, 2, 1, 1)], [(3, 1), (2, 2), (3, 3, 2), (2, 1, 1), (3, 3, 3, 3), (3, 3, 1, 1), (3, 2, 2, 1), (2, 2, 2, 2), (1, 1, 1, 1)], [(4, 1), (3, 2), (4, 4, 2), (4, 3, 3), (3, 1, 1), (2, 2, 1), (4, 4, 4, 3), (4, 4, 1, 1), (4, 3, 2, 1), (4, 2, 2, 2), (3, 3, 3, 1), (3, 3, 2, 2), (2, 1, 1, 1)], [(5, 1), (4, 2), (3, 3), (5, 5, 2), (5, 4, 3), (4, 4, 4), (4, 1, 1), (3, 2, 1), (2, 2, 2), (5, 5, 5, 3), (5, 5, 4, 4), (5, 5, 1, 1), (5, 4, 2, 1), (5, 3, 3, 1), (5, 3, 2, 2), (4, 4, 3, 1), (4, 4, 2, 2), (4, 3, 3, 2), (3, 3, 3, 3), (3, 1, 1, 1), (2, 2, 1, 1)], [(6, 1), (5, 2), (4, 3), (6, 6, 2), (6, 5, 3), (6, 4, 4), (5, 5, 4), (5, 1, 1), (4, 2, 1), (3, 3, 1), (3, 2, 2), (6, 6, 6, 3), (6, 6, 5, 4), (6, 6, 1, 1), (6, 5, 5, 5), (6, 5, 2, 1), (6, 4, 3, 1), (6, 4, 2, 2), (6, 3, 3, 2), (5, 5, 3, 1), (5, 5, 2, 2), (5, 4, 4, 1), (5, 4, 3, 2), (5, 3, 3, 3), (4, 4, 4, 2), (4, 4, 3, 3), (4, 1, 1, 1), (3, 2, 1, 1), (2, 2, 2, 1)], [(7, 1), (6, 2), (5, 3), (4, 4), (7, 7, 2), (7, 6, 3), (7, 5, 4), (6, 6, 4), (6, 5, 5), (6, 1, 1), (5, 2, 1), (4, 3, 1), (4, 2, 2), (3, 3, 2), (7, 7, 7, 3), (7, 7, 6, 4), (7, 7, 5, 5), (7, 7, 1, 1), (7, 6, 6, 5), (7, 6, 2, 1), (7, 5, 3, 1), (7, 5, 2, 2), (7, 4, 4, 1), (7, 4, 3, 2), (7, 3, 3, 3), (6, 6, 6, 6), (6, 6, 3, 1), (6, 6, 2, 2), (6, 5, 4, 1), (6, 5, 3, 2), (6, 4, 4, 2), (6, 4, 3, 3), (5, 5, 5, 1), (5, 5, 4, 2), (5, 5, 3, 3), (5, 4, 4, 3), (5, 1, 1, 1), (4, 4, 4, 4), (4, 2, 1, 1), (3, 3, 1, 1), (3, 2, 2, 1), (2, 2, 2, 2)], [(8, 1), (7, 2), (6, 3), (5, 4), (8, 8, 2), (8, 7, 3), (8, 6, 4), (8, 5, 5), (7, 7, 4), (7, 6, 5), (7, 1, 1), (6, 6, 6), (6, 2, 1), (5, 3, 1), (5, 2, 2), (4, 4, 1), (4, 3, 2), (3, 3, 3), (8, 8, 8, 3), (8, 8, 7, 4), (8, 8, 6, 5), (8, 8, 1, 1), (8, 7, 7, 5), (8, 7, 6, 6), (8, 7, 2, 1), (8, 6, 3, 1), (8, 6, 2, 2), (8, 5, 4, 1), (8, 5, 3, 2), (8, 4, 4, 2), (8, 4, 3, 3), (7, 7, 7, 6), (7, 7, 3, 1), (7, 7, 2, 2), (7, 6, 4, 1), (7, 6, 3, 2), (7, 5, 5, 1), (7, 5, 4, 2), (7, 5, 3, 3), (7, 4, 4, 3), (6, 6, 5, 1), (6, 6, 4, 2), (6, 6, 3, 3), (6, 5, 5, 2), (6, 5, 4, 3), (6, 4, 4, 4), (6, 1, 1, 1), (5, 5, 5, 3), (5, 5, 4, 4), (5, 2, 1, 1), (4, 3, 1, 1), (4, 2, 2, 1), (3, 3, 2, 1), (3, 2, 2, 2)]]
        pairs = pairsMap[batchSize]
        pairs = [Counter(p) for p in pairs]
        ans = cnt[0]
        cnt[0] = 0
        for pair in pairs:
            c = min(cnt[i]//cc for i,cc in pair.items())
            if c>0:
                ans += c
                for i,cc in pair.items():
                    cnt[i] -= cc*c
        return ans + any(cnt)
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res

def test(a,b):
    return a+int(str(b)[::-1]) == int(str(a)[::-1])+b

def getPairs2(total):
    ans = []
    for i in range(total-1, 0, -1):
        k = total - i
        if k<=i:
            ans.append((i, k))
    return ans
def getPairs3(total):
    ans = []
    for i in range(total-1, 0, -1):
        for j in range(i, 0, -1):
            k = total - (i+j)%total
            if k<=j:
                ans.append((i,j,k))
    return ans
def getPairs4(total):
    ans = []
    for i in range(total-1, 0, -1):
        for j in range(i, 0, -1):
            for m in range(j, 0, -1):
                k = total - (i+j+m)%total
                if k<=m:
                    ans.append((i,j,m,k))
    return ans
# T4 尝试打表, 失败
# pairs = []
# for i in range(10):
#     pairs.append(getPairs2(i)+getPairs3(i)+getPairs4(i))

sol = Solution()
result = [
    # sol.squareIsWhite(coordinates = "h3"),
    # sol.areSentencesSimilar(sentence1 = "My name is Haley", sentence2 = "My Haley"),
    # sol.areSentencesSimilar(sentence1 = "of", sentence2 = "A lot of words"),
    sol.areSentencesSimilar("A", "a A b A")
    # sol.countNicePairs(nums = [42,11,1,97]),
    # sol.countNicePairs(nums = [13,10,35,24,76]),
    # sol.countNicePairs([352171103,442454244,42644624,152727101,413370302,293999243])
    # sol.maxHappyGroups(batchSize = 3, groups = [1,2,3,4,5,6]),
    # sol.maxHappyGroups(batchSize = 4, groups = [1,3,2,5,2,2,1,6]),
    
    
]
for r in result:
    print(r)
