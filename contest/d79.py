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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 6083. 判断一个数的数字计数是否等于数位的值 """
    def digitCount(self, num: str) -> bool:
        for i,c in enumerate(num):
            if int(c) != num.count(str(i)): return False
        return True
    
    """ 6084. 最多单词数的发件人 """
    def largestWordCount(self, messages: List[str], senders: List[str]) -> str:
        counter = defaultdict(int)
        for s,m in zip(senders, messages):
            counter[s] += len(m.split())
        maxC = max(counter.values())
        persons = [k for k,v in counter.items() if v==maxC]
        return sorted(persons, reverse=True)[0]
    
    """ 6085. 道路的最大总重要性 """
    def maximumImportance(self, n: int, roads: List[List[int]]) -> int:
        degress = [0]*n
        for u,v in roads:
            degress[u] += 1
            degress[v] += 1
        degress.sort()
        ans = 0
        for i,d in zip(range(1,n+1), degress):
            ans += i*d
        return ans
    
    def testClass(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
""" 10011. 以组为单位订音乐会的门票 #hard #线段树 #题型
场景是一个订票系统, 有n排座位每排m座. 要求实现两种需求: 1) gather(int k, int maxRow) 要求在 maxRow 以下的行中(同一行中)有连续k个座位; 2) scatter(int k, int maxRow) 要求在 maxRow 以下的行中有k个空座位 (不要求连续).
思路1: #线段树
    灵神 [here](https://leetcode.cn/problems/booking-concert-tickets-in-groups/solution/by-endlesscheng-okcu/)
    先看基本的gather操作: 要求在maxRow范围内找到最小的位置进行插入, 也即求最小值, 可以用 #线段树. (注意看这里的index函数)
    对于 scatter操作而言, 维护一个sum线段树, 然后依次从前往后安排座位即可

"""
class BookMyShow:
    """ [here](https://leetcode.cn/problems/booking-concert-tickets-in-groups/solution/by-endlesscheng-okcu/) """
    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.min = [0] * (n * 4)
        self.sum = [0] * (n * 4)

    # 将 idx 上的元素值增加 val
    def add(self, o: int, l: int, r: int, idx: int, val: int):
        if l == r:
            self.min[o] += val
            self.sum[o] += val
            return
        m = (l + r) // 2
        if idx <= m: self.add(o * 2, l, m, idx, val)
        else: self.add(o * 2 + 1, m + 1, r, idx, val)
        self.min[o] = min(self.min[o * 2], self.min[o * 2 + 1])
        self.sum[o] = self.sum[o * 2] + self.sum[o * 2 + 1]

    # 返回区间 [L,R] 内的元素和
    def query_sum(self, o: int, l: int, r: int, L: int, R: int):
        if L <= l and r <= R: return self.sum[o]
        sum = 0
        m = (l + r) // 2
        if L <= m: sum += self.query_sum(o * 2, l, m, L, R)
        if R > m: sum += self.query_sum(o * 2 + 1, m + 1, r, L, R)
        return sum

    # 返回区间 [1,R] 中 <= val 的最靠左的位置，不存在时返回 0
    def index(self, o: int, l: int, r: int, R: int, val: int):
        if self.min[o] > val: return 0  # 说明整个区间的元素值都大于 val
        if l == r: return l
        m = (l + r) // 2
        if self.min[o * 2] <= val: return self.index(o * 2, l, m, R, val)  # 看看左半部分
        if m < R: return self.index(o * 2 + 1, m + 1, r, R, val)  # 看看右半部分
        return 0

    def gather(self, k: int, maxRow: int) -> List[int]:
        i = self.index(1, 1, self.n, maxRow + 1, self.m - k)
        if i == 0: return []
        seats = self.query_sum(1, 1, self.n, i, i)
        self.add(1, 1, self.n, i, k)  # 占据 k 个座位
        return [i - 1, seats]

    def scatter(self, k: int, maxRow: int) -> bool:
        if (maxRow + 1) * self.m - self.query_sum(1, 1, self.n, 1, maxRow + 1) < k:
            return False  # 剩余座位不足 k 个
        i = self.index(1, 1, self.n, maxRow + 1, self.m - 1)  # 从第一个没有坐满的排开始占座
        while True:
            left_seats = self.m - self.query_sum(1, 1, self.n, i, i)
            if k <= left_seats:  # 剩余人数不够坐后面的排
                self.add(1, 1, self.n, i, k)
                return True
            k -= left_seats
            self.add(1, 1, self.n, i, left_seats)
            i += 1

class BookMyShow:
    # 代码练习, 重新写了一遍. 注释还是看上面的更清楚!!!
    def __init__(self, n: int, m: int):
        self.m = m
        self.n = n
        self.min = [0] * (n * 4)
        self.sum = [0] * (n * 4)
    
    def add(self, o,l,r, idx, val):
        if l==r:
            self.min[o] += val
            self.sum[o] += val
            return
        m = (l+r)//2
        if m>=idx: self.add(2*o,l,m, idx, val)
        else: self.add(2*o+1,m+1,r, idx, val)
        self.min[o] = min(self.min[o*2], self.min[o*2+1])
        self.sum[o] = self.sum[o*2] + self.sum[o*2+1]
    def query(self, o,l,r, left, right):
        if l>=left and r<=right: return self.sum[o]
        m = (l+r)>>1
        s = 0
        if m>=left: s += self.query(o*2, l, m, left, right)
        if m+1<=right: s+= self.query(o*2+1, m+1, r, left, right)
        return s

    def index(self, o: int, l: int, r: int, R: int, val: int):
        """ 在小于等于R的范围内找到第一个小于等于val的位置 """
        if self.min[o] > val: return 0
        if l==r: return l
        m = (l+r)>>1
        if self.min[2*o]<=val: return self.index(2*o,l,m,R,val)
        if m+1>R: return 0
        return self.index(2*o+1,m+1,r,R,val)

    def gather(self, k: int, maxRow: int) -> List[int]:
        """ 在 maxRow 之下找剩余大雨k的 """
        idx = self.index(1,1,self.n,maxRow+1,self.m-k)
        if idx==0: return []
        r = [idx-1,self.query(1,1,self.n, idx,idx)]
        self.add(1,1,self.n,idx,k)
        return r

    def scatter(self, k: int, maxRow: int) -> bool:
        if (1+maxRow) * self.m - self.query(1,1,self.n,1,maxRow+1) < k: return False
        i = self.index(1,1,self.n, maxRow+1,self.m-1)
        while k>0:
            remain = self.m - self.query(1,1,self.n, i,i)
            a = min(remain, k)
            k -= a
            self.add(1,1,self.n, i,a)
            i += 1
        return True

sol = Solution()
result = [
    # sol.digitCount(num = "1210"),
    # sol.largestWordCount(messages = ["How is leetcode for everyone","Leetcode is useful for practice"], senders = ["Bob","Charlie"]),
    # sol.maximumImportance(n = 5, roads = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]),
    # sol.maximumImportance(n = 5, roads = [[0,3],[2,4],[1,3]]),
    
#     sol.testClass("""["BookMyShow", "gather", "gather", "scatter", "scatter"]
# [[2, 5], [4, 0], [2, 0], [5, 1], [5, 1]]"""),
    sol.testClass("""["BookMyShow","gather","scatter","gather","gather","gather"]
[[5,9],[10,1],[3,3],[9,1],[10,2],[2,0]]"""),
    
]
for r in result:
    print(r)
