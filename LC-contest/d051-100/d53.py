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
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-53
@2022 """
class Solution:
    """ 1876. 长度为三且各字符不同的子字符串 """
    def countGoodSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        for i in range(n-2):
            if len(set(s[i:i+3])) == 3: ans += 1
        return ans
    
    """ 1877. 数组中最大数对和的最小值 """
    def minPairSum(self, nums: List[int]) -> int:
        nums.sort()
        ans = 0
        n = len(nums)
        for i in range(n//2):
            ans = max(ans, nums[i] + nums[n-1-i])
        return ans
    
    """ 1878. 矩阵中最大的三个菱形和 #medium
在一个矩形中, 找出所有的「菱形」中, 边所经过的点的最大(三个)和. 这里「菱形」的定义, 就是正方形旋转45度. 见 [描述](https://leetcode.cn/problems/get-biggest-three-rhombus-sums-in-a-grid/)
思路0: 本题的复杂度长款分别为 100, 因此直接暴力枚举, 大概是 O(n^4) 级别
思路1: 斜方向 #前缀和 
    考虑菱形每一条边的计算方式: 就是四条线段, 因此容易用前缀和的方式加速计算.
    为此, 需要预先计算两个方向上的前缀和.
    复杂度: 遍历每一个可能的中心点, 需要枚举所有可能的边长, 每次计算和只需 O(1), 因此总的复杂度为 O(n^3).
    见 [官答](https://leetcode.cn/problems/get-biggest-three-rhombus-sums-in-a-grid/solution/ju-zhen-zhong-zui-da-de-san-ge-ling-xing-hpko/); 下面灵神的解答更为简洁
"""
    def getBiggestThree(self, grid: List[List[int]]) -> List[int]:
        m, n = len(grid), len(grid[0])
        def getCircle(i,j,k):
            # 计算中心在 (i,j), 每个点距离中心为k的菱形的和 (边长为 k+1 各个斜格子)
            if k==0: return grid[i][j]
            ans = 0
            for x,y in zip(range(i, i+k), range(j+k, j, -1)): ans += grid[x][y]
            for x,y in zip(range(i+k, i, -1), range(j, j-k, -1)): ans += grid[x][y]
            for x,y in zip(range(i, i-k, -1), range(j-k, j)): ans += grid[x][y]
            for x,y in zip(range(i-k, i), range(j, j+k)): ans += grid[x][y]
            return ans
        
        circles = set()
        for i in range(m):
            for j in range(n):
                for k in range(min(i, j, m-1-i, n-1-j)+1):
                    circles.add(getCircle(i,j,k))
        return sorted(circles, reverse=True)[:3]
    
    """ 1879. 两个数组最小的异或值之和 #hard 
给定两个数组, 对于nums2重排序, 然后和nums1一一匹配计算异或值, 要求返回最小的异或值之和.
限制: 数组长度n为 14; 元素大小 1e7
思路1: #状压 DP
    考虑依次用nums2中的元素元素匹配nums1中的每一个; 记nums2中所用元素的二进制表示为 mask, 则已经匹配了 `c = mask.bit_count()` 个元素 (顺序匹配nums1的前 c 个数字).
    因此有: `f[mask] = min{ f[mask\i] + nums2[i] * nums1[mask.bit_count()-1] }`. 这里枚举所有mask中为1的位 i, 将其与第 nums1[c-1] 个元素匹配.
    [here](https://leetcode.cn/problems/minimum-xor-sum-of-two-arrays/solution/liang-ge-shu-zu-zui-xiao-de-yi-huo-zhi-z-2uye/)
"""
    def minimumXORSum(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        f = [inf] * (1 << n)
        f[0] = 0    # 边界
        for mask in range(1, 1<<n):
            c = mask.bit_count()    # mask所表示的分配匹配了多少个数字
            for i in range(n):
                if mask & (1 << i):
                    f[mask] = min(f[mask], f[mask ^ (1 << i)] + (nums2[i] ^ nums1[c-1])) # 注意位运算的优先级比加减更低!!!
        return f[(1<<n)-1]

        


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
    # sol.countGoodSubstrings(s = "aababcabc"),
    
    # sol.minPairSum(nums = [3,5,4,2,4,6]),
    # sol.minPairSum([3,5,2,3]),
    
    # sol.getBiggestThree(grid = [[3,4,5,1,3],[3,3,4,2,3],[20,30,200,40,10],[1,5,5,4,1],[4,3,2,2,5]]),
    # sol.getBiggestThree([[1,2,3],[4,5,6],[7,8,9]]),
    
    sol.minimumXORSum(nums1 = [1,2], nums2 = [2,3]),
    sol.minimumXORSum(nums1 = [1,0,3], nums2 = [5,3,4]),
]
for r in result:
    print(r)
