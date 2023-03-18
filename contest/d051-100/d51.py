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
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # 注意 pow 与默认环境下的 pow(x,y, MOD) 签名冲突
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
https://leetcode-cn.com/contest/biweekly-contest-51
@2022 """
class Solution:
    """ 1844. 将所有数字用字符替换 """
    def replaceDigits(self, s: str) -> str:
        l = list(s)
        for i in range(len(l)//2):
            ch = chr(ord(l[2*i]) + int(l[2*i+1]))
            l[2*i+1] = ch
        return "".join(l)
    
    
    """ 1846. 减小和重新排列数组后的最大元素 """
    def maximumElementAfterDecrementingAndRearranging(self, arr: List[int]) -> int:
        arr.sort()
        arr[0] = 1
        for i in range(1, len(arr)):
            arr[i] = min(arr[i], arr[i-1]+1)
        return arr[-1]
    
    """ 1847. 最近的房间 #hard
有一组房间 [(id, size)]; 每次查询 (preferred, minSize) 要从至少为 minSize 的房间中找到与 preferredID 绝对差最小的房间号 (相同的话返回较小的).
限制: 房间数量n 1e5; 查询次数 k 1e4; 房间大小 1e7
思路1: #离线查询 #SortedList
    由于每个查询有minSize的限制, 考虑对其从大到小排序, 这样可选的房间 potential 逐渐变多.
    如何在potential中找到与preferredID绝对差最小的房间号? 维护房间id有序然后, 二分查找. 具体实现上又用了 SortedList.
[官答](https://leetcode.cn/problems/closest-room/solution/zui-jin-de-fang-jian-by-leetcode-solutio-9ylf/) 也是一样的思路, 不过做了更高级的抽象.
"""
    def closestRoom(self, rooms: List[List[int]], queries: List[List[int]]) -> List[int]:
        n = len(rooms)
        # 对于 minSize 从大到小 (分组) 排序
        minSize2querys = defaultdict(list)
        for i, (p, s) in enumerate(queries):
            minSize2querys[s].append((p, i))
        # room按照size从大到小排序; 方便依次加入到SortedList (potentials) 中
        rooms.sort(key=lambda x: x[1], reverse=True)
        potentials = SortedList([], key=lambda x: x[0])
        idx = 0
        ans = [-1] * len(queries)
        # 随着minSize从大到小, 依次将符合条件的房间加入到potentials中
        for minSize in sorted(minSize2querys.keys(), reverse=True):
            while idx < n and rooms[idx][1] >= minSize:
                potentials.add(rooms[idx])
                idx += 1
            if idx==0: continue # potential 为空
            for perferredID, i in minSize2querys[minSize]:
                # 蠢哭! 原本这里又用了idx, 居然变量冲突了
                j = bisect.bisect_right(potentials, [perferredID, -1])
                if j==0:
                    ans[i] = potentials[0][0]
                    continue
                delta, idd = abs(perferredID - potentials[j-1][0]), potentials[j-1][0]
                if j<len(potentials) and abs(perferredID - potentials[j][0]) < delta:
                    idd = potentials[j][0]
                ans[i] = idd
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

""" 1845. 座位预约管理系统 #medium
实现一个类管理n个座位, 可以 1) reserve 返回最小的空位; 2) unreserve(i) 取消座位i.
复杂度: 座位数量n为 1e5, 总的函数调用次数 1e5
思路0: 无脑用了 SortList 类
思路1: 实际上用一个最小推, 来维护还剩余的座位即可 (因为每次 reserve 只需要得到最小值)
"""
class SeatManager:
    from sortedcontainers import SortedList
    def __init__(self, n: int):
        self.n = n
        self.frontier = 1
        self.unreserved = SortedList()

    def reserve(self) -> int:
        if self.unreserved:
            return self.unreserved.pop(0)
        self.frontier += 1
        return self.frontier-1

    def unreserve(self, seatNumber: int) -> None:
        self.unreserved.add(seatNumber)

sol = Solution()
result = [
    # sol.replaceDigits(s = "a1c1e1"),
#     sol.testClass("""["SeatManager", "reserve", "reserve", "unreserve", "reserve", "reserve", "reserve", "reserve", "unreserve"]
# [[5], [], [], [2], [], [], [], [], [5]]"""),
    # sol.maximumElementAfterDecrementingAndRearranging(arr = [100,1,1000]),
    
    # sol.closestRoom(rooms = [[2,2],[1,2],[3,2]], queries = [[3,1],[3,3],[5,2]]),
    # sol.closestRoom(rooms = [[1,4],[2,3],[3,5],[4,1],[5,2]], queries = [[2,3],[2,4],[2,5]]),
    sol.closestRoom([[23,22],[6,20],[15,6],[22,19],[2,10],[21,4],[10,18],[16,1],[12,7],[5,22]], [[12,5],[15,15],[21,6],[15,1],[23,4],[15,11],[1,24],[3,19],[25,8],[18,6]]),
]
for r in result:
    print(r)
