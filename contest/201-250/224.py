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
https://leetcode.cn/contest/weekly-contest-224
@2022 """
class Solution:
    """ 1725. 可以形成最大正方形的矩形数目 """
    def countGoodRectangles(self, rectangles: List[List[int]]) -> int:
        rs = [min(a) for a in rectangles]
        return Counter(rs)[max(rs)]
    
    """ 1726. 同积元组 """
    def tupleSameProduct(self, nums: List[int]) -> int:
        n = len(nums)
        cnt = Counter()
        for i in range(n):
            for j in range(i+1,n):
                cnt[nums[i]*nums[j]] += 1
        ans = 0
        for _,v in cnt.items():
            ans += v*(v-1)//2
        return ans * 8
    
    """ 1727. 重新排列后的最大子矩阵 #medium #题型
有一个0/1矩阵, 可以对于列进行重排列. 问可能得到的全为1的最大矩阵的大小. 见[图](https://leetcode.cn/problems/largest-submatrix-with-rearrangements/)
限制: 矩阵面积 1e5
关联: 0085. 最大矩形
提示: 这里每一列不变, 可以参考0085进行预处理: 对于某列的i位置, 计算「以其结尾的连续1的长度」.
思路1: #预处理 之后, 排序统计
    相较于0085, 这里可以对列进行重排列. 因此, 对于每一个行指标i, 我们可以对预处理的结果进行排序. 自然得到最大的合法矩阵.
"""
    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        m,n = len(matrix), len(matrix[0])
        for i in range(1, m):
            for j in range(n):
                if matrix[i][j] == 1:
                    matrix[i][j] = matrix[i-1][j] + 1
        ans = 0
        for i in range(m):
            heights = sorted(matrix[i], reverse=True)
            for i,h in enumerate(heights):
                ans = max(ans, h*(i+1))
        return ans
    
    """ 1728. 猫和老鼠 II 见博弈论 """

    """ 0084. 柱状图中最大的矩形 #hard #题型
给定一组数表示一系列柱子的高度, 求其中包含的最大矩形的面积.
限制: 数组长度 1e5
思路1: 采用 #单调栈 来保留每一个柱子作为最大高度可以构成的矩形的底边长度.
    具体而言, 维护一个单调栈, 当栈顶元素被pop出来时, 说明 (stack[-2], i) 范围内的柱子都大于栈顶元素的高度, 可以构成面积 `stack[-1] * (i - stack[-2] - 1)` 的矩形.
"""
    def largestRectangleArea(self, heights: List[int]) -> int:
        # 思路1, from  Copilet.
        n = len(heights)
        stack = []
        ans = 0
        for i in range(n):
            while stack and heights[i] < heights[stack[-1]]:
                # stack[-1] 可以在 (stack[-2], i) 范围内作为矩形高度
                h = heights[stack.pop()]
                w = i if not stack else i - stack[-1] - 1
                ans = max(ans, h*w)
            stack.append(i)
        while stack:
            h = heights[stack.pop()]
            w = n if not stack else n - stack[-1] - 1
            ans = max(ans, h*w)
        return ans


    """ 0085. 最大矩形 #hard #题型 #interest
给定一个0/1矩阵, 问其中全1构成的最大矩形的面积. 限制: 长宽 200 [图](https://leetcode.cn/problems/maximal-rectangle/)
提示: 先进行预处理, 对于每一个位置, 记录 **该行中以它结尾的连续1的长度** (0位置对应的数量就是0). 这样, 对于每一列, 就转换成 0084 题.
思路1: 按照上述思路将其转为 0084
    说明: 如何想到等价转换? 按照官答的思路, 我们枚举以 (i,j) 点作为右下角的所有矩阵, 这样判断的方式就可以通过上述预处理机制来实现. 从而得到等价转换.
    见 [官答](https://leetcode.cn/problems/maximal-rectangle/solution/zui-da-ju-xing-by-leetcode-solution-bjlu/)
"""
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        m,n = len(matrix), len(matrix[0])
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    matrix[i][j] = 1 if j==0 else matrix[i][j-1] + 1
                else:
                    matrix[i][j] = 0
        ans = 0
        for j in range(n):
            ans = max(self.largestRectangleArea([matrix[i][j] for i in range(m)]), ans)
        return ans
    
    
sol = Solution()
result = [
    # sol.largestRectangleArea([2,1,5,6,2,3]),
    # sol.largestRectangleArea([2,4]),
    # sol.maximalRectangle(matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]),
    sol.largestSubmatrix(matrix = [[0,0,1],[1,1,1],[1,0,1]]),
]
for r in result:
    print(r)
