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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1610. 可见点的最大数目 #hard #极角
你在location有一个角度为angle的视角, 现在给定一组points, 问通过该视角最多可以看到多少点?
限制: 不考虑重叠, 边界上的点可见 (若点在location则永远可见)
思路1: #双指针 先计算所有点的角度, 排序, 然后用双指针来遍历.
    要注意: 这里的遍历过程是一个「环」而非数组, 要注意边界情况! 下面用了 `j<=n-1 and angles[j]-angles[i]<=angle` 和 `j>n-1 and 360-angles[i]+angles[j%n]<=angle` 两个条件来判断从角度i出发, j是否在其逆时针angle范围内.
    复杂度: 排序 O(n log(n))
思路2: #二分 查找边界
    也是先对于角度排序, 然后对a[i] 而非查找 a[i]+angle 的边界在哪里.
    技巧: 对于「环」的问题, 官答中给出的技巧是将angles数组每个加360之后拼接到原数组后面, 构成一个长2n的递增数组.
    复杂度: 相较于双指针遍历复杂度 O(n), 对于每个位置进行二分复杂度 O(n log(n))
另外, 需要注意 #极角 的计算. 利用atan计算, 注意y=0时是没有定义的; 另外atan的取值范围为180度, 需要根据x,y的正负来另外判断.
"""
    def visiblePoints(self, points: List[List[int]], angle: int, location: List[int]) -> int:
        a,b = location
        angles = []
        bias = 0
        for x,y in points:
            x,y = x-a, y-b
            if x==0:
                if y>0: angles.append(90)
                elif y<0: angles.append(270)
                else: bias += 1
            elif x>0:
                if y>=0: angles.append(math.atan(y/x)*180/math.pi)
                else: angles.append(360+math.atan(y/x)*180/math.pi)
            else:
                if y>=0: angles.append(180+math.atan(y/x)*180/math.pi)
                else: angles.append(180+math.atan(y/x)*180/math.pi)
        n = len(angles)
        angles.sort()
        ans = 0
        j = 0
        for i in range(0, n):
            while j<=n-1 and angles[j]-angles[i]<=angle: j += 1
            while j>n-1 and 360-angles[i]+angles[j%n]<=angle: j+= 1
            if j>=i: ans = max(ans, j-i)
            else: ans = max(ans, n-i+j)
        return ans + bias
    
    
    
    
    

    
sol = Solution()
result = [
    sol.visiblePoints(points = [[2,1],[2,2],[3,3]], angle = 90, location = [1,1]),
    sol.visiblePoints(points = [[2,1],[2,2],[3,4],[1,1]], angle = 90, location = [1,1]),
    sol.visiblePoints(points = [[1,0],[2,1]], angle = 13, location = [1,1]),
]
for r in result:
    print(r)
