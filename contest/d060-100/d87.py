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
https://leetcode-cn.com/contest/biweekly-contest-87



@2022 """
class Solution:
    """ 6184. 统计共同度过的日子数 #easy 需要计算 "08-15" 这种形式是一年的第几天 """
    def countDaysTogether(self, arriveAlice: str, leaveAlice: str, arriveBob: str, leaveBob: str) -> int:
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        def getdays(date: str):
            m,d = map(int, date.split('-'))
            return sum(days[:m-1]) + d
        aa, al = getdays(arriveAlice), getdays(leaveAlice)
        ba, bl = getdays(arriveBob), getdays(leaveBob)
        return max(
            min(al,bl) - max(aa,ba) + 1
            , 0
        )
    
    """ 6185. 运动员和训练师的最大匹配数 指针滑动即可 """
    def matchPlayersAndTrainers(self, players: List[int], trainers: List[int]) -> int:
        players.sort(); trainers.sort()
        cnt = 0
        idx = 0; n = len(trainers)
        for p in players:
            while idx < n and trainers[idx] < p: 
                idx += 1
            if idx==n: return cnt
            idx += 1; cnt += 1
        return cnt
    
    """ 6186. 按位或最大的最小子数组长度 #medium #题型
对于一个数组下标i, 我们从i开始往右累积或操作可以得到一个最大值 mx, 定义其「按位或最大的最小子数组长度」为从i开始的累积或变为mx的最小子数组长度.
现给定一个数组, 对每个下标球这个值. 限制: n 1e5
思路1: 先 #逆向 算出mx, 在正向 #滑动窗口
    我们可以逆向累积或, 得到每一位的目标mx值.
    提示: 
        随着i的增大, 注意到 mx 是递减的! (当然这点在本题没用)
        然后再正向考虑, 每个位置达到对应mx的右边界是递增的! 这是因为, 从 i 到 i+1, nums[i] 没有参加或运算, 所需求的最大或的目标变高了. 因此, 可以用 #滑动窗口 求解.
    还有个难点, 对于或运算, 怎样「除去」一个元素? 下面的实现cnt记录每一位上出现的次数, 从而实现 `add, remove, check` 操作, 其中 check(x) 判断cnt中的数字经过或运算是否可以得到x值.
"""
    def smallestSubarrays(self, nums: List[int]) -> List[int]:
        n = len(nums)
        mx = nums[:]
        for i in range(n-2, -1, -1):
            mx[i] = mx[i] | mx[i+1]
        class Cnt():
            def __init__(self) -> None:
                self.cnt = [0] * 32
            def add(self, x):
                xx = bin(x)[2:][::-1]
                for i,b in enumerate(xx):
                    self.cnt[i] += int(b)
            def remove(self, x):
                xx = bin(x)[2:][::-1]
                for i,b in enumerate(xx):
                    self.cnt[i] -= int(b)
            def check(self, x):
                xx = bin(x)[2:][::-1]
                for i,b in enumerate(xx):
                    if self.cnt[i] < int(b): return False
                return True
        cnt = Cnt()
        p = -1
        ans = [1] * n
        for i,num in enumerate(nums):
            if i>0: cnt.remove(nums[i-1])
            if mx[i]==0: continue
            while not cnt.check(mx[i]):
                p += 1
                cnt.add(nums[p])
            ans[i] = (p-i+1)
        return ans
    
    """ 6187. 完成所有交易的初始最少钱数 #hard 
给定一组交易, 每个交易包括 (cost, cashback), 先付出之后得到cashbacki反馈. 问初始资金至少为多少, 则无论交易的顺序如何, 都可以完成全部交易.
限制: 过程中资金量必须非负; n 1e5
例子: 交易有 [[2,1],[5,0],[4,2]], 则至少需要 10.
思路1: 
    先不考虑 cost<cashback 的赚钱情况, 对于上例如何处理? 
    结论: 对于每笔交易定义 loss = cost-cashback. 则答案是 `sum(loss) + max(cashback)`
        这是因为, 若允许负数, 则一开始需要 sum(loss) 即可; 而 max(cashback) 代表了「最大可能亏钱数」, 当先完成其他交易最后进行这个交易的时候发生.
    再考虑「盈利」交易的情况. 若不考cost则资金量会上升. 所以和上一种情况类似也要看「最大可能亏钱数」, 这个发生在 max(cost) 这笔交易上.
        因此, 答案是 `sum(loss) + max(cashback, cost)`
"""
    def minimumMoney(self, transactions: List[List[int]]) -> int:
        diffs = []
        backs = []
        mx = 0
        for c,b in transactions:
            if c<=b: 
                mx = max(mx, c)
                continue
            diffs.append(c-b)
            backs.append(b)
        return sum(diffs) + max(backs + [mx])
    
sol = Solution()
result = [
    # sol.countDaysTogether(arriveAlice = "08-15", leaveAlice = "08-18", arriveBob = "08-16", leaveBob = "08-19"),
    # sol.countDaysTogether(arriveAlice = "10-01", leaveAlice = "10-31", arriveBob = "11-01", leaveBob = "12-31"),
    # sol.countDaysTogether("10-20", "12-22", "06-21", "07-05"),
    # sol.matchPlayersAndTrainers(players = [4,7,9], trainers = [8,2,5,8]),
    # sol.matchPlayersAndTrainers(players = [1,1,1], trainers = [10]),
    # sol.smallestSubarrays(nums = [1,0,2,1,3]),
    # sol.smallestSubarrays(nums = [1,2]),
    # sol.smallestSubarrays([2,1,0,0]),
    sol.minimumMoney(transactions = [[2,1],[5,0],[4,2]]),
    sol.minimumMoney(transactions = [[3,0],[0,3]]),
    sol.minimumMoney([[7,2],[0,10],[5,0],[4,1],[5,8],[5,9]]),
]
for r in result:
    print(r)
