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
https://leetcode.cn/contest/weekly-contest-232
@2022 """
class Solution:
    """ 1790. 仅执行一次字符串交换能否使两个字符串相等 """
    def areAlmostEqual(self, s1: str, s2: str) -> bool:
        cnt = sum(a!=b for a,b in zip(s1, s2))
        return cnt in [0,2] and Counter(s1)==Counter(s2)
        
    """ 1791. 找出星型图的中心节点 """
    def findCenter(self, edges: List[List[int]]) -> int:
        s = set(edges[0]).intersection(set(edges[1]))
        return list(s)[0]

    
    """ 1792. 最大平均通过率 #medium #数学
有一组班级, 每个班的通过率为考试通过人数/总人数. 然后额外有 extraStudents个学生可以保证通过, 将他们分配到各个班级中, 使得整体的平均通过率最大.
思路1: 计算加入一个可通过学生的「收益」, 利用最大堆维护, 每次加入收益最大的班级即可.
    假设通过/全部人数为 `a/b`, 则新加一人后变为 `(a+1)/(b+1)`, 通过率差值 `(a-b)/a(a+1) = d/a(a+1)` 其中d表示这个班的未通过人数, 固定; a是班级总人数, 浮动. 
    因此, 每次选取这一差值最大的班级即可; 可采用 #最大堆 实现. 
"""
    def maxAverageRatio(self, classes: List[List[int]], extraStudents: int) -> float:
        classes = [[a-b, a] for b,a in classes]
        h = []
        for i,(d,a) in enumerate(classes):
            if d==0: continue
            heappush(h, (a*(a+1)/d, i))
        # 边界: 空
        if len(h)==0: return 1.0
        for _ in range(extraStudents):
            _, i = heappop(h)
            classes[i][1] += 1
            d,a = classes[i]
            heappush(h, (a*(a+1)/d, i))
        ans = 0
        for d,a in classes:
            ans += (a-d)/a
        return ans / len(classes)
    
    """ 1793. 好子数组的最大分数 #hard
定义子数组的score为, 数组中的最小值*数组长度. 现给定一个数组和一个下标k, 要求找到包含下标k的子数组的最大score.
思路1: 找到idx作为最小值的左右边界. 然后依次遍历区间范围包括所给k的那些区间即可. 参见 [zerotrac](https://leetcode.cn/problems/maximum-score-of-a-good-subarray/solution/hao-zi-shu-zu-de-zui-da-fen-shu-by-zerot-537w/)
    另外 [here](https://leetcode.cn/problems/maximum-score-of-a-good-subarray/solution/python-dan-diao-zhan-by-qin-qi-shu-hua-2-69cs/) 指出使用单调递增栈, 不需要记录左右边界: 因为, 1) 「当前索引为i且栈中值被弹出时，当前值作为最小值的区间就是 `[栈中上一个下标 + 1，i - 1]`」; 2) 此外, 对于遍历结束栈内剩余元素, 其区间就是 `[栈中上一个下标 + 1，n-1]`.
思路2: #双指针 因为坐标k必须出现在结果区间中, 可以从k开始 (将其作为最小值mn) 向两边搜索. 然后依次将最小值mn减小以拓展边界, 在此过程中计算score即可. 这一方案适用性相对窄一些.
    见 [here](https://leetcode.cn/problems/maximum-score-of-a-good-subarray/solution/c-shuang-zhi-zhen-tan-xin-zui-jian-ji-zu-b3vf/)
"""
    def maximumScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        left = [0]*n; right = [n-1]*n
        s = []
        for i,num in enumerate(nums):
            while s and s[-1][0]>=num:      
                right[s[-1][1]] = i-1       # s[-1][0] >= num
                s.pop()
            if s: left[i] = s[-1][1]+1      # s[-1][0] < num
            s.append((num, i))
        ans = 0
        for num,l,r in zip(nums, left, right):
            if l<=k<=r:
                ans = max(ans, num*(r-l+1))
        return ans
    def maximumScore(self, nums: List[int], k: int) -> int:
        # 思路 1.1 from https://leetcode.cn/problems/maximum-score-of-a-good-subarray/solution/python-dan-diao-zhan-by-qin-qi-shu-hua-2-69cs/
        stack = [-1]
        l = len(nums)
        res = 0
        for i, n in enumerate(nums):
            while len(stack) > 1 and nums[stack[-1]] >= n:#当出栈时
                if stack[-2] < k and i > k:#区间条件判断
                    res = max(res, nums[stack[-1]] * (i - stack[-2] - 1)) #区间左侧为 stack[-2] + 1， 区间右侧为i - 1
                stack.pop()
            stack.append(i)
        for i in range(1, len(stack)):#未弹出的栈中元素再次遍历
            if stack[i - 1] < k:
                res = max(res, nums[stack[i]] * (l - stack[i - 1] - 1))#区间左侧为 stack[i - 1]， 区间右侧为 l - 1
        return res

sol = Solution()
result = [
    # sol.findCenter(edges = [[1,2],[2,3],[4,2]]),
    # sol.maxAverageRatio(classes = [[1,2],[3,5],[2,2]], extraStudents = 2),
    # sol.maxAverageRatio(classes = [[2,4],[3,9],[4,5],[2,10]], extraStudents = 4),
    sol.maximumScore(nums = [1,4,3,7,4,5], k = 3),
    sol.maximumScore(nums = [5,5,4,5,4,1,1,1], k = 0),
]
for r in result:
    print(r)
