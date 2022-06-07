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
# from structures import ListNode, TreeNode

""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 2089. 找出数组排序后的目标下标
 """
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        nums.sort()
        result =[]
        for i, n in enumerate(nums):
            if n == target:
                result.append(i)
            elif n > target:
                break
        return result

    """ 2090. 半径为 k 的子数组平均值 """
    def getAverages(self, nums: List[int], k: int) -> List[int]:
        result = [-1 for _ in range(len(nums))]
        if len(nums) < 2*k+1:
            return result
        cumsum = sum(nums[:2*k+1])
        result[k] = cumsum // (2*k+1)
        # out of time
        # for i in range(k, len(nums)-k):
        #     result[i] = sum(nums[i-k: i+k+1]) // (2*k+1)
        for i in range(k+1, len(nums)-k):
            cumsum = cumsum + nums[i+k] - nums[i-k-1]
            result[i] = cumsum // (2*k+1)
        return result

    """ 2091. 从数组中移除最大值和最小值 """
    def minimumDeletions(self, nums: List[int]) -> int:
        minIndex, maxIndex = 0,0
        for i in range(len(nums)):
            if nums[i] > nums[maxIndex]:
                maxIndex = i
            elif nums[i] < nums[minIndex]:
                minIndex = i
        index1, index2 = min(minIndex, maxIndex), max(minIndex, maxIndex)
        return min(max(index1, index2)+1, len(nums)-min(index1, index2), index1+1+len(nums)-index2)

    """ 2092. 找出知晓秘密的所有专家
    给你一个整数 n ，表示有 n 个专家从 0 到 n - 1 编号。另外给你一个下标从 0 开始的二维整数数组 meetings ，其中 meetings[i] = [xi, yi, timei] 表示专家 xi 和专家 yi 在时间 timei 要开一场会。一个专家可以同时参加 多场会议 。最后，给你一个整数 firstPerson 。
    专家 0 有一个 秘密 ，最初，他在时间 0 将这个秘密分享给了专家 firstPerson 。接着，这个秘密会在每次有知晓这个秘密的专家参加会议时进行传播。更正式的表达是，每次会议，如果专家 xi 在时间 timei 时知晓这个秘密，那么他将会与专家 yi 分享这个秘密，反之亦然。
    秘密共享是 瞬时发生 的。也就是说，在同一时间，一个专家不光可以接收到秘密，还能在其他会议上与其他专家分享。
    在所有会议都结束之后，返回所有知晓这个秘密的专家列表。你可以按 任何顺序 返回答案。

    输入：n = 6, meetings = [[0,2,1],[1,3,1],[4,5,1]], firstPerson = 1
    输出：[0,1,2,3]
    解释：
    时间 0 ，专家 0 将秘密与专家 1 共享。
    时间 1 ，专家 0 将秘密与专家 2 共享，专家 1 将秘密与专家 3 共享。
    因此，在所有会议结束后，专家 0、1、2 和 3 都将知晓这个秘密。
    """
    # 不知道为啥有bug, 放弃 —— 在特殊情况下复杂度较高
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        import random
        # meetings = sorted(meetings, key=lambda x: x[2])
        time2meeting = defaultdict(list)
        for x,y,t in meetings:
            time2meeting[t].append((x,y))
        secretSet = set([0, firstPerson])
        def recc(meets):
            added = False
            random.shuffle(meets)
            for i, (x,y) in enumerate(meets):
                if x in secretSet or y in secretSet:
                    del meets[i]
                if x in secretSet and y not in secretSet:
                    secretSet.add(y)
                    added = True
                if y in secretSet and x not in secretSet:
                    secretSet.add(x)
                    added = True
            if added:
                recc(meets)
        for t, meets in sorted(time2meeting.items()):
            recc(meets)
        return list(secretSet)


    def findAllPeople2(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        meetings.sort(key=lambda x: x[2])
        secret = [False]*n
        secret[0] = secret[firstPerson] = True

        i = 0
        while i<len(meetings):
            # find meetings at same time
            j = i
            while j+1<len(meetings) and meetings[j+1][2]==meetings[j][2]:
                j+= 1
            # construct graph
            edges = defaultdict(list)
            for s,e,_ in meetings[i:j+1]:
                edges[s].append(e)
                edges[e].append(s)
            # propagate
            q = deque([e for e in edges.keys() if secret[e]])
            while q:
                u = q.popleft()
                for v in edges[u]:
                    if not secret[v]:
                        secret[v] = True
                        q.append(v)
            # update next i
            i = j+1
        return [i for i in range(len(secret)) if secret[i]]

sol = Solution()
result = [
    
]
for r in result:
    print(r)
