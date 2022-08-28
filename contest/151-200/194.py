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
https://leetcode.cn/contest/weekly-contest-194
@2022 """
class Solution:
    """ 1486. 数组异或操作 """
    
    """ 1487. 保证文件名唯一 #medium #细节
顺序来一系列的文件名创建请求. 若文件已经创建过, 则修改为 `name(1)` 这种形式. 要求模拟返回的结果.
注意: 可能会有 `["gta","gta(1)","gta"]` 这样的序列. 因此, 对于新生成的文件名也需要检查是否占用.
"""
    def getFolderNames(self, names: List[str]) -> List[str]:
        cnt = Counter()
        ans = []    # 记录basename下一个括号内待添入的数字.
        for name in names:
            if name not in cnt:
                ans.append(name); cnt[name] = 1
            else: 
                # 尝试添加后缀
                target = f"{name}({cnt[name]})"
                while target in cnt:
                    cnt[name] += 1
                    target = f"{name}({cnt[name]})"
                    # cnt[target] += 1
                ans.append(target); cnt[name] += 1; cnt[target] = 1
        return ans
    
    """ 1488. 避免洪水泛滥 #medium #题型
有无限个湖泊, 给定一个数组表示晴雨, 若值=0说明那天是晴天, 否则第i个湖泊会装满水. 若雨下在装满水的湖泊, 则发生洪水. 你可以在晴天抽干一个湖泊. 目标是不发生洪水, 给出一个抽水的策略. 限制: 数组长度 n 1e5
思路1: 顺序记录晴天的每个日期, 在发生洪水的日期范围内 #二分 搜索晴天.
    注意, 例如 [0,2,2] 虽然前面有一个抽水机会, 但不在两次下雨的日期范围内.
    复杂度: 若使用数组, 可能每次都需要移除第一个元素, 则这样的复杂度为 `O(n^2)`. 若采用有序数组, 则 `O(n logn)`.
"""
    def avoidFlood(self, rains: List[int]) -> List[int]:
        full = {}   # 记录每个湖泊的满水时间
        clouds = []
        ans = [-1] * len(rains)
        for i,pool in enumerate(rains):
            if pool==0: clouds.append(i)
            else:
                if pool in full:
                    # 在上一次被填满的日期之后搜索晴天
                    idx = bisect_right(clouds, full[pool])
                    if idx >= len(clouds): return []        # 无法操作, 返回 []
                    else: ans[clouds[idx]] = pool; clouds.pop(idx)
                # 注意, 只要那天下雨了, 都要更新full
                full[pool] = i
        # 剩余的随便填
        for c in clouds:
            ans[c] = 1
        return ans
    
    
    """ 1489. 找到最小生成树里的关键边和伪关键边 """

    
sol = Solution()
result = [
    # sol.getFolderNames(["gta","gta(1)","gta","avalon"]),
    # sol.getFolderNames(["wano","wano","wano","wano"]),
    sol.avoidFlood(rains = [1,2,3,4]),
    sol.avoidFlood(rains = [1,2,0,0,2,1]),
    sol.avoidFlood(rains = [0,1,1]),
    sol.avoidFlood([1,0,2,0,3,0,2,0,0,0,1,2,3]),
]
for r in result:
    print(r)
