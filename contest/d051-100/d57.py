import tty
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
https://leetcode-cn.com/contest/biweekly-contest-57
@2022 """
class Solution:
    """ 1941. 检查是否所有字符出现次数相同 """
    def areOccurrencesEqual(self, s: str) -> bool:
        c = Counter(s)
        cc = list(c.values())
        return all(cc[i]==cc[i-1] for i in range(1, len(cc)))
    
    """ 1942. 最小未被占据椅子的编号 #medium
有n个朋友来派对, 每个人的到达和离开时间为 (arrival, leaving); 每个人到达时, 挑选位置最小的座位坐下. 问第 target 个朋友所坐的位置.
思路0: 维护 #sortedlist 记录所有的空闲座位
    将所有人的到达和离开时间作为两类事件, 统一排序. 然后暴力模拟.
    用一个 sortedlist 维护所有空闲座位, 每到达一个人移除 available[0]; 离开一个人则将该座位号添加到 available 中.
    注意, 同一时刻到达和离开, 需要先处理离开的人.
    复杂度: O(n log(n)). 我们维护长度为n的有序列表, 每次操作复杂度为O(log(n)).
思路1: 相较于有序列表这一复杂结构, 采用最小堆更为轻量.
"""
    def smallestChair(self, times: List[List[int]], targetFriend: int) -> int:
        # 展开 arrival 和 leaving 时间
        allTimes = []
        for f, (a,l) in enumerate(times):
            # 需要先处理离开的人
            allTimes.append((a,1,f))
            allTimes.append((l,0,f))
        allTimes.sort()
        # 模拟
        available = SortedList(range(len(times)))
        f2idx = {}  # friend -> idx
        for t,ttype, f in allTimes:
            if ttype == 1:
                idx = available.pop(0)
                if f==targetFriend: return idx
                # available.remove(f)
                f2idx[f] = idx
            elif ttype == 0:
                available.add(f2idx[f])
        return -1
    
    
    """ 1943. 描述绘画结果 #medium
在数轴上有一组线段 (start, end, color) 表示该区间被涂上了 color. 当一个点被涂上多种颜色后, 颜色叠加, 简记为 sum(solors). 要求返回一个数组, 元素 (start, end, color) 表示绘画结果.
限制: 题目中每个线段的颜色均不同
思路1: #差分
    如何表示累加的颜色信息, 还要记录线段位置? 不难想到 #差分数组. 也即在线段的开始位置分别 +/- color.
    得到差分数组后, accumulate 即得到最后的每个点的颜色值.
    注意到可能出现 1+4 == 2+3 的颜色记录, 但这表达的其实是两种颜色. 由于题目说明了每种颜色都只涂了一个线段. 因此可知交接点两侧的颜色值一定不同. 因此, 基于所有线段的边界划分输出结果即可.
    细节: 一开始对于 sorted(pivots) 所定义的每一个线段都输出了, 但忽略了空白线段 (颜色为 0), 注意考虑这一情况.

"""
    def splitPainting(self, segments: List[List[int]]) -> List[List[int]]:
        maxn = max(s[1] for s in segments)
        pivots = set()
        acc = [0] * (maxn+1)
        for s,e,c in segments:
            pivots.add(s)
            pivots.add(e)
            acc[s] += c
            acc[e] -= c
        for i in range(1, maxn+1):
            acc[i] += acc[i-1]
        pivots = sorted(pivots)
        ans = []
        for s,e in zip(pivots, pivots[1:]):
            # 注意需要排除空的部分!!!
            if acc[s]==0: continue
            ans.append([s,e,acc[s]])
        return ans
    
    """ 1944. 队列中可以看到的人数 #hard #单调栈
给一个数组表示序列中每个人的身高. 一个位置为i的人只能看到其右边的满足条件的人: (i,j) 满足它们中间的人的身高要小于 `min(arr[i], arr[j])`. 要求返回每个人能看到的人数.
思路1: #逆序 #单调栈
    显然, 一个人向右能看到的人的身高呈递增, 并且看到的最远的一个人满足 `arr[i] < arr[j]`. 所以, 可以用单调栈来解决.
    为此, 我们可以从右往左遍历, 维护一个单调栈. 一个人能够看到的人数为: 加入i时候其弹出栈的数量, 加上(如果有的话)栈顶那个人.

"""
    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        ans = [0] * n
        stack = []
        # stack.append(heights[-1])
        for i in range(n-1, -1, -1):
            h = heights[i]
            c = 0
            while stack and stack[-1] < h:
                stack.pop()
                c += 1
            ans[i] = c + (len(stack)>0)
            stack.append(h)
        return ans
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [
    # sol.smallestChair(times = [[1,4],[2,3],[4,6]], targetFriend = 1),
    # sol.smallestChair(times = [[3,10],[1,5],[2,6]], targetFriend = 0),
    # sol.smallestChair([[4,5],[12,13],[5,6],[1,2],[8,9],[9,10],[6,7],[3,4],[7,8],[13,14],[15,16],[14,15],[10,11],[11,12],[2,3],[16,17]],15),
    
    # sol.splitPainting(segments = [[1,4,5],[4,7,7],[1,7,9]]),
    # sol.splitPainting(segments = [[1,4,5],[1,4,7],[4,7,1],[4,7,11]]),
    
    sol.canSeePersonsCount(heights = [10,6,8,5,11,9]),
    sol.canSeePersonsCount(heights = [5,1,2,3,10]),
]
for r in result:
    print(r)
