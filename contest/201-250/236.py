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
https://leetcode.cn/contest/weekly-contest-236
@2022 """
class Solution:
    """ 1822. 数组元素积的符号 """
    def arraySign(self, nums: List[int]) -> int:
        sign = 1
        for num in nums:
            if num==0:
                return 0
            elif num<0:
                sign *= -1
        return sign
    
    """ 1823. 找出游戏的获胜者 #medium #题型 #约瑟夫环
n个玩家围成一圈, 从1开始编号; 在剩余人数超过一人的情况下, 顺时针数第k个人出局. 问最后剩余的人是谁.
限制: 进阶要求 O(n) 的算法
思路1: 暴力模拟, 每次找到出局的人, 环的长度-1. 因此需要pop数组的中间元素, 复杂度 O(nk)
思路2: #推导 #公式. 实际上该问题正是 #约瑟夫环 [wiki](https://zh.wikipedia.org/wiki/%E7%BA%A6%E7%91%9F%E5%A4%AB%E6%96%AF%E9%97%AE%E9%A2%98)
    方便起见, 下面编号按照从0开始.
    记 `f(n, k)` 表示「长为n的环, 从0开始顺时针, 每次第k个人出局」这样的设置下, 最后剩余的人的编号.
    分类: 1) 若n=1, 则 `f(n, k) = 0`; 2) 否则, 本轮出局的人为 `x' = (k-1)%n`, 然后, 记 `x = f(n-1, k)` 表示子问题最后剩余的人. 它们之间的关系有: 由于本轮出局 x', 则子问题中编号为0的在本轮中的编号为 `x'+1`, 因此原问题最终的胜利者编号为 `f(x,n) = (x'+1 + f(n-1, k)) %n = (f(x-1,n)+k) % n`.
    当然, 得到上述推导公式之后, #递归 形式可以展开为 #迭代.
[官答](https://leetcode.cn/problems/find-the-winner-of-the-circular-game/solution/zhao-chu-you-xi-de-huo-sheng-zhe-by-leet-w2jd/)
"""
    def findTheWinner(self, n: int, k: int) -> int:
        # 思路1
        circle = [i for i in range(1, n+1)]
        idx = 0
        while len(circle)>1:
            idx = (idx + k-1) % len(circle)
            circle.pop(idx)
        return circle[0]
    
    def findTheWinner(self, n: int, k: int) -> int:
        # 思路2
        def f(n):
            if n==1: return 0
            return (k + f(n-1)) % n
        return f(n)+1
    def findTheWinner(self, n: int, k: int) -> int:
        # 展开递归为迭代
        f = 0
        for i in range(2, n+1):    # 出局 n-1 人
            f = (f+k) % i
        return f+1
    
    
    """ 1824. 最少侧跳次数 #medium #化简
有三条跑道, 上面各有一些石头. 要从起点跑到终点, 仅能进行侧跳 (在相同的距离处, 从跑道i跳到跑道j). 要求最少侧跳次数.
限制: 每个距离最多有一个石子; 距离 5e5
思路1: #DP
    记 `f[d][i]` 表示到达距离d处的跑道i的最少侧跳次数. 
    则有递推: 若i有障碍物, 则无法到达记为inf; 否则, `f[d+1][i] = min(f[d][i], f[d][j]*{f[d+1][j]!=j} + 1}` 这里的第二项表示从j跑道跳过来, 要求j报道的d+1处没有石子.
    化简: 注意到, 对于相同距离无障碍的跑道, **f[d] 之间的差距最大为1**. 将DP数组压缩为1维的情况下, 先将有障碍的位置置为inf, 然后记数组最小值为mn, 则对于非障碍位置有 `f[d+1][i] = min(f[d][i], mx+1)`
"""
    def minSideJumps(self, obstacles: List[int]) -> int:
        f  = [1, 0, 1]
        for o in obstacles:
            # 若该位置有障碍物, 先置为 inf
            if o!=0:
                f[o-1] = inf
            # 利用上面的化简公式更新
            mn = min(f)
            for i in range(3):
                if i==o-1: continue
                else: f[i] = min(f[i], mn+1)
        return min(f)
    
""" 1825. 求出 MK 平均值 #hard #题型
给定两个参数 m,k 的情况下, 处理流数据的 MK平均值: 取最后的m个元素, 除去最大最小k个元素, 计算剩余 m-2k 个元素的平均值. 
要求实现对于流数据的处理DS. 操作包括: 添加一个元素; 计算平均值.
限制: m 1e5; 操作次数 1e5
思路1: 
    考虑实际情况, 用一个大小为m的 #环形数组 latestM 来存储最近的m个数据. 并且动态更新数组和
    1.0:[这个方案不行, 因为无法记录当前元素是否在最大最小的k个数中] 如何维护最大最小的k个元素? 用两个有序数组来存储即可: 例如对于最大的k个元素, 若新元素 num>kLargest[0], 则pop第一个元素然后将num加入.
    1.1: 那就用 #有序数组 直接记录最近的m个元素, 然后动态维护 sum(sl[:]) 和 sum(sl[k:-k])
        也即, 根据每次插入/删除的位置来 #分类 讨论. 例如, 当插入第idx个数字. 我们在有序列表中找到该数字的位置 idxNew, 则: 1) 若 `idxNew<k` 则 k-1...m-k-1 部分会发生右移, 因此 midSum += sl[k-1]-sl[m-k-1]; 2) 若 `k<=idxOld<m-k`, 则 `midSum += num-sl[m-k-1`; 3) 否则, 对于midSum不影响. (一开始还要删除第idx-m个数字, 思路一致.)
    见 [here](https://leetcode.cn/problems/finding-mk-average/solution/by-981377660lmt-5hhm/)
总结: 本题的设置符合实际应用场景需求; 在试错的过程中逐步推导出所需记录的数据结构的过程很有意思.

"""
from sortedcontainers import SortedList
class MKAverage:
    def __init__(self, m: int, k: int):
        self.m = m
        self.k = k
        self.latestM = [-1] * m # 循环数组, 记录最近的元素
        self.latestSum = 0      # 循环数组的和
        self.cnt = 0            # 当前流数据的个数
        # self.flag = False
        # self.sorted = SortedList()
        # self.kLargest = SortedList()
        # self.kSmallest = SortedList()
        # self.kLargestSum = self.kSmallestSum = 0

    def addElement(self, num: int) -> None:
        # 先处理 latestM 和 latestSum
        vOld = self.latestM[self.cnt % self.m]
        self.latestM[self.cnt % self.m] = num
        self.cnt = self.cnt+1
        self.latestSum += num - vOld if vOld!=-1 else num
        # 在长度达到 m 的时候建立 SL
        if self.cnt==self.m:
            # self.flag = True
            self.sl = SortedList(self.latestM)
            self.midSum = sum(self.sl[self.k:self.m-self.k])
        # 需要对于 SL 进行维护了
        elif self.cnt>self.m:
            # 删除序列中 idx-m 个元素
            idxOld = self.sl.index(vOld)
            if idxOld<self.k:
                self.midSum += -self.sl[self.k]+self.sl[-self.k]
            elif idxOld<self.m-self.k:
                self.midSum += -vOld+self.sl[-self.k]
            self.sl.pop(idxOld)
            # 添加新的 idx 个元素
            idxNew = self.sl.bisect_right(num)
            if idxNew<self.k:
                self.midSum += self.sl[self.k-1]-self.sl[self.m-self.k-1]
            elif idxNew<self.m-self.k:
                self.midSum += num-self.sl[self.m-self.k-1]
            self.sl.add(num)

    def calculateMKAverage(self) -> int:
        if self.cnt>=self.m: return self.midSum // (self.m-2*self.k)
        else: return -1
    
sol = Solution()
result = [
    sol.findTheWinner(n = 5, k = 2),
    sol.findTheWinner(n = 6, k = 5),
    # sol.minSideJumps(obstacles = [0,2,1,0,3,0]),
    # sol.minSideJumps(obstacles = [0,1,1,3,3,0]),
    # sol.minSideJumps([0,1,2,3,0]),
#     testClass("""["MKAverage", "addElement", "addElement", "calculateMKAverage", "addElement", "calculateMKAverage", "addElement", "addElement", "addElement", "calculateMKAverage"]
# [[3, 1], [3], [1], [], [10], [], [5], [5], [5], []]"""),
#     testClass("""["MKAverage","addElement","addElement","calculateMKAverage","addElement","addElement","calculateMKAverage","addElement","addElement","calculateMKAverage","addElement"]
# [[3,1],[58916],[61899],[],[85406],[49757],[],[27520],[12303],[],[63945]]"""),
]
for r in result:
    print(r)
