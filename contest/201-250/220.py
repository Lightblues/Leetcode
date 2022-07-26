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
https://leetcode.cn/contest/weekly-contest-220
@2022 """
class Solution:
    """ 1694. 重新格式化电话号码 """
    def reformatNumber(self, number: str) -> str:
        number = number.replace(" ", "").replace("-", "")
        n = len(number)
        remains = ""
        if n%3==1:
            number, remains = number[:-4], number[-4:]
        splits = []
        for i in range(math.ceil(len(number)/3)):
            splits.append(number[3*i:3*(i+1)])
        if remains:
            splits += remains[:2], remains[2:]
        return '-'.join(splits)
    
    """ 1695. 删除子数组的最大得分 #medium #题型
给定一个数组, 求其 (连续) 子数组中, 和最大值.
思路: #双指针.
"""
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        # l 记录最后一个不在set中的元素位置
        l = -1
        s = set(); acc = 0
        mx = 0
        for i,num in enumerate(nums):
            if num not in s:
                acc += num; s.add(num)
                mx = max(mx, acc)
            else:
                while nums[l+1]!=num:
                    l += 1
                    acc -= nums[l]; s.remove(nums[l])
                l += 1
        return mx
    
    """ 1696. 跳跃游戏 VI #medium
从左到右, 每次最多跳k步, 每个位置有一定分数, 要求最大分数.
限制: 长度, k 1e5
思路1:
    注意到, 直接使用DP的复杂度不够的. 而由于可调到某一位置的必然是前面的k个位置, 每次取其中最大的即可.
    为此, 用一个 #最大堆 来维护 (score, idx) 信息, 后者用来判断是否可达
"""
    def maxResult(self, nums: List[int], k: int) -> int:
        # 边界
        if len(nums)==1: return nums[0]
        h = [(-nums[0], 0)]
        # ans = -inf
        for i in range(1, len(nums)):
            score = nums[i]
            while i - h[0][1] > k:
                heappop(h)
            # s,idx = heappop(h)
            s = h[0][0]
            if i==len(nums)-1: return -s+score
            heappush(h, (s-score, i))
    
    """ 1697. 检查边长度限制的路径是否存在 #hard
一张图, 节点之间可能有多跳权重不等的边. 给一组查询 (p,q,limit) 判断两点之间是否有一条权重都严格小于limit的路径.
限制: 节点, 边数量 1e5; 查询数量 1e5
思路: 利用 #并查集 表示连通性, 对于权重排序, 根据查询的限制逐步加边.
"""
    def distanceLimitedPathsExist(self, n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
        fa = [i for i in range(n)]
        def find(x):
            if fa[x]!=x:
                fa[x] = find(fa[x])
            return fa[x]
        def merge(x,y):
            if x>y:
                x,y = y,x
            fx,fy = find(x), find(y)
            fa[fy] = fx
        def isConnected(x,y):
            return find(x)==find(y)
        # 
        edges = sorted([(l,u,v) for u,v,l in edgeList])
        ans = [None] * len(queries)
        ne = len(edges)
        idx = 0
        for l,u,v,i in sorted([(l,u,v,i) for i,(u,v,l) in enumerate(queries)]):
            while idx<ne and edges[idx][0]<l:
                _,a,b = edges[idx]
                merge(a,b)
                idx += 1
            ans[i] = isConnected(u,v)
        return ans
    
    
sol = Solution()
result = [
    # sol.reformatNumber(number = "123 4-5678"),
    # sol.reformatNumber(number = "--17-5 229 35-39475 "),
    # sol.maximumUniqueSubarray(nums = [4,2,4,5,6]),
    # sol.maximumUniqueSubarray(nums = [5,2,1,2,5,2,1,2,5]),
    # sol.maximumUniqueSubarray([187,470,25,436,538,809,441,167,477,110,275,133,666,345,411,459,490,266,987,965,429,166,809,340,467,318,125,165,809,610,31,585,970,306,42,189,169,743,78,810,70,382,367,490,787,670,476,278,775,673,299,19,893,817,971,458,409,886,434])
    # sol.maxResult(nums = [1,-1,-2,4,-7,3], k = 2),
    # sol.maxResult(nums = [1,-5,-20,4,-1,3,-6,-3], k = 2),
    sol.distanceLimitedPathsExist(n = 5, edgeList = [[0,1,10],[1,2,5],[2,3,9],[3,4,13]], queries = [[0,4,14],[1,4,13]]),
    sol.distanceLimitedPathsExist(n = 3, edgeList = [[0,1,2],[1,2,4],[2,0,8],[1,0,16]], queries = [[0,1,2],[0,2,5]])
]
for r in result:
    print(r)
