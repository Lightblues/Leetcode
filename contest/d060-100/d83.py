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
https://leetcode-cn.com/contest/biweekly-contest-83
@2022 """
class Solution:
    """ 6128. 最好的扑克手牌 """
    def bestHand(self, ranks: List[int], suits: List[str]) -> str:
        if len(Counter(suits))==1:
            return "Flush"
        cnt = Counter(ranks)
        if max(cnt.values())>=3: return "Three of a Kind"
        elif max(cnt.values())==2: return "Pair"
        else: return "High Card"
    
    
    """ 6129. 全 0 子数组的数目 """
    def zeroFilledSubarray(self, nums: List[int]) -> int:
        pre = -1; cnt = 0
        lens = []
        for num in nums + [-1]:
            if num!=0:
                if pre==0:
                    lens.append(cnt)
            else:
                if pre==0: cnt += 1
                else: cnt = 1
            pre = num
        ans = 0
        for l in lens:
            ans += l*(l+1)//2
        return ans
    
    """ 6131. 不可能得到的最短骰子序列 #hard
给定一个面为 1...k 的骰子, 然后长度为n的rolls结果. 要求得到一个最短的数组, 其在rolls的所有子序列中不存在.
问题等价于, 求长度l, 满足 k^l 种长为l的不同序列在rolls中都存在.
提示: 什么情况下, 最后一个元素为x 并且长为l的排列都存在? 假设所有长为l-1的序列中, 最靠前的末尾位置是tails. 那么要求都存在, 则要求在 max(tails)+1: 的范围内存在数字x.
思路1: #转换 #模拟
    根据提示, 对于任意的数字, **若要求能够以其结尾的所有的长l的序列都存在, 则需要在 `rolls[max(tails)+1:]` 范围内存在该数字**.
    具体, 在遍历rolls过程中, 可以用一个set记录未出现的数字, 当set为空时, 说明该长度的所有序列都存在. 重制.
思路0: 一开始错理解为k的所有permutation... #error 下面简单记录思路
    用一个 num2idxs 数组记录所有的数字出现的位置.
    然后, 对于非重复序列的长度进行遍历. 
        用 `perm2idx` 记录 perm 的首次出现的末尾位置, 例如 perm2idx[(3,1)] 记录最靠左的 (3,1) 序列中1的位置.
        在每次遍历过程中, 每次在后面可以填充的数字是 `x in set(range(k)) \ set(perm)`, 我们在 `num2idxs[x]` 中二分查找 `perm2idx[perm]`. 若找不到则失败
    复杂度: 似乎挺高? 但可能的结果应该不是很大? 没分析过, 但 `math.perm(10, 10)` 的数量级就很大了...
总结: 要看清题意啊!!!
"""
    def shortestSequence(self, rolls: List[int], k: int) -> int:
        # 思路0: 错理解成 k 的所有 permutation... #error
        # math.perm(10, 10)
        num2idxs = [[] for _ in range(k)]
        for idx,r in enumerate(rolls):
            num2idxs[r-1].append(idx)
        for i in range(k):
            if len(num2idxs[i])==0: return 1
            num2idxs[i].sort()
        # 
        s = set(range(k))
        perm2idx = {(i,):v[-1] for i,v in enumerate(num2idxs)}
        for ll in range(2, len(rolls)+1):
            newperm = {}
            for perm,idx in perm2idx.items():
                for a in s.difference(set(perm)):
                    i = bisect.bisect_right(num2idxs[a], idx-1)
                    if i==0:
                        return ll
                    newperm[(a,)+perm] = num2idxs[a][i-1]
            perm2idx = newperm

    def shortestSequence(self, rolls: List[int], k: int) -> int:
        # 修改自思路0
        # math.perm(10, 10)
        num2idxs = [[] for _ in range(k)]
        for idx,r in enumerate(rolls):
            num2idxs[r-1].append(idx)
        for i in range(k):
            if len(num2idxs[i])==0: return 1
            num2idxs[i].sort()
        # 
        # p2idx = [v[0] for v in num2idxs]
        imax = max(v[0] for v in num2idxs)
        for ll in range(2, len(rolls)+2):
            imaxNew = imax
            for v in range(k):
                idx = bisect_left(num2idxs[v], imax+1)
                if idx >= len(num2idxs[v]): return ll
                imaxNew = max(imaxNew, num2idxs[v][idx])
            imax = imaxNew

    def shortestSequence(self, rolls: List[int], k: int) -> int:
        # 思路1
        # 注意, set 是浅拷贝
        ss = set(range(1,k+1))
        s = ss.copy()
        ans = 1
        for r in rolls:
            if r in s:
                s.remove(r)
                if len(s)==0:
                    ans += 1
                    s = ss.copy()
        return ans

""" 6130. 设计数字容器系统 """
from sortedcontainers import SortedList
class NumberContainers:
    def __init__(self):
        self.num2idxs = defaultdict(SortedList)
        self.idx2num = {}

    def change(self, index: int, number: int) -> None:
        if index in self.idx2num:
            old = self.idx2num[index]
            self.num2idxs[old].remove(index)
        self.num2idxs[number].add(index)
        self.idx2num[index] = number

    def find(self, number: int) -> int:
        if number not in self.num2idxs or len(self.num2idxs[number])==0: return -1
        return self.num2idxs[number][0]
    
sol = Solution()
result = [
    # sol.bestHand(ranks = [13,2,3,1,9], suits = ["a","a","a","a","a"]),
    # sol.bestHand(ranks = [4,4,2,4,4], suits = ["d","a","a","b","c"]),
    # sol.zeroFilledSubarray(nums = [0,0,0,2,0,0]),
    # sol.zeroFilledSubarray(nums = [1,3,0,0,2,0,0,4]),
#     testClass("""["NumberContainers", "find", "change", "change", "change", "change", "find", "change", "find"]
# [[], [10], [2, 10], [1, 10], [3, 10], [5, 10], [10], [1, 20], [10]]"""),
    sol.shortestSequence(rolls = [4,2,1,2,3,3,2,4,1], k = 4),
    sol.shortestSequence(rolls = [1,1,2,2], k = 2),
    sol.shortestSequence(rolls = [1,1,3,2,2,2,3,3], k = 4),
    sol.shortestSequence([1,3,3,2,1,4,1,1,2,4,1,2,2,1,1,1,1,2,2,3,4,3,3,2,1,4,4], 4),
    sol.shortestSequence([3,2,1,3,3,3,3,3,1,2,2,3,1,3,3,1,1,3,1,1,1,3,1,3,3,1,2,3,2,1,1,2],3),
    sol.shortestSequence([2,2,2,2,2,2,1,2,2,2,1,1,1,2,2,2,2,1,2,1,1,2,2,2,2,1,1,1,1,2,1,1,2,1,1,2,2,1,1,1,2,1,1,1,2,2,1,2,1,2,1,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,2,2,1,2,1,2,1,2,2,1,1,2,1,1,1,1,2,2,2,2,1,2,1,1,2,1,2,1,1,2,2,1,2,1,1,2,2,2,1,2,2,1,1,2,2,1,2,1,1,2,1,1,1,1,2,2,1,2,2,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,1,1,2,1,1,1,1,2,1,1,2,2,2,2,2,2,2,1,2,2,2,2,2,2,1,2,1,1,2,1,2,1,2,2,2,2,2,2,1,1,2,1,2,2,2,2,1,2,1,2,1,2,1,1,1,2,1,1,1,2,1,1,2,2,1,1,1,1,2,2,2,2,1,2,1,1,1,1,1,2,1,1,1,1,2,2,1,1,1,2,2,1,2,1,2,1,1,2,2,2,1,1,2,1,2,1,2,2,1,1,1,1,2,2,2,1,1,2,2,1,1,1,1,1,1,2,1,1,2,2,2,1,1,2,1,2,2,2,2,2], 2),
    sol.shortestSequence([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 1)
    
    
    
]
for r in result:
    print(r)
