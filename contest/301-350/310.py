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
https://leetcode.cn/contest/weekly-contest-310

T4 是带约束的「最长递增子序列」, 就无法采用 0300 题的 贪心+二分 的框架了; 需要用到线段树才实现「区间查询」.

@2022 """
class Solution:
    """ 6176. 出现最频繁的偶数元素 """
    
    """ 6177. 子字符串的最优划分 #medium #贪心 """
    
    """ 6178. 将区间分为最少组数 #medium #题型 有一组 [s,e] 区间, 要求划分成数量最少的组, 每一组区间之间不相交.
思路1: 根据开始时间排序. 记录当前所划分的组; 遍历过程中, 每次在合法的组中添加即可 #贪心 思想.
    可以用一个堆来判断是否合法.
"""
    def minGroups(self, intervals: List[List[int]]) -> int:
        intervals.sort()
        ends = []
        cnt = 0; avas = 0
        for s,e in intervals:
            while ends and ends[0] < s:
                heapq.heappop(ends)
                avas += 1
            if avas==0:
                cnt += 1
            else: avas -= 1
            heapq.heappush(ends, e)
        return cnt

    """ 6206. 最长递增子序列 II #hard #题型 对于给定的数组, 找到其中最长的严格递增子序列, 要求相邻元素差值不超过 k.
限制: n 1e5; k 1e5
思路1: 建立 {val: LIS} 的字典记录以val结尾的LIS 长度. 遍历过程中, 对于val, 在 [val-k,val] 范围内查询最大值.
    考虑到数据范围, 可以采用 #线段树.
    技巧: 由于我们线段树的定义从节点1开始, 下面注释部分要避免出现区间非法! 为此, 我们可以将数字整体shift一下.
拓展: 若本题的数据范围在 1e9, 则需要采用 #动态开点线段树. 
参见 [灵神](https://leetcode.cn/problems/longest-increasing-subsequence-ii/solution/zhi-yu-xian-duan-shu-pythonjavacgo-by-en-p1gz/)
"""
    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        # 思路1: 线段树. 注意下面因为「线段树从1开始」导致的边界情况.
        # 线段树框架
        # u = max(nums)
        u = max(nums) + 1  # 对于num进行shift, 从而避免下面注释部分的判断.
        mx = [0] * (u*4)
        def modify(o,l,r,i,val):
            # 修改 a[i] = val
            if l==r: mx[o]=val; return
            m = (l+r)//2
            if i<=m: modify(o*2,l,m,i,val)
            else: modify(o*2+1,m+1,r,i,val)
            mx[o] = max(mx[o*2], mx[o*2+1])
        def query(o,l,r,L,R):
            # 查询 max(a[L:R+1])
            if L<=l and r<=R: return mx[o]
            res = 0
            m = (l+r)//2
            if L<=m: res = query(o*2,l,m,L,R)
            if R>m: res = max(res, query(o*2+1,m+1,r,L,R))
            return res
        
        # for x in nums:
        #     # 注意, 线段树从 1 开始!!!
        #     if x==1: 
        #         modify(1,1,u,1,1)       # 都是正数, 次数长度一定为1
        #     else: 
        #         res = 1 + query(1,1,u,max(1,x-k),x-1)     # 这里的 x-1 应该 >= 1
        #         modify(1,1,u,x,res)
        for x in nums:
            x += 1
            res = 1 + query(1,1,u,max(1,x-k),x-1)
            modify(1,1,u,x,res)
        return mx[1] # 对于线段树, 最大值就是根节点.
    
sol = Solution()
result = [
    # sol.minGroups([[5,10],[6,8],[1,5],[2,3],[1,10]]),
    # sol.minGroups([[1,3],[5,6],[8,10],[11,13]]),
    sol.lengthOfLIS(nums = [4,2,1,4,3,4,5,8,15], k = 3), 
],
for r in result:
    print(r)
