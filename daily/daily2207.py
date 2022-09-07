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
@2022 """
class Solution:
    """ 0719. 找出第 K 小的数对距离 #hard #题型 #二分
给定一个数组, 每个数对构成「绝对差值」. 问第k小的差值. 限制: 长度 n 1e4. 数字大小 C 1e6.  
思路0: #二分. 一个比较蠢的实现
    考虑问题「对于给定的d问差值小于d的数对有多少」, 可以通过排序+bisct解决. 每次检查的复杂度为 `O(n log(n))`.
    搜索空间为 [0,C]. 因此可以用二分来查找, 总体复杂度 `O(log(C) * n log(n))`.
    注意: 本题二分的特殊性在于, 搜索的值可能无法取到! 可以通过检查函数返回一个flag来标记数组中是否存在该差值.
"""
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        # 思路0: #二分. 一个比较蠢的实现
        nums.sort(); n = len(nums)
        def f(d):
            # 统计nums中差值 <d 的组数
            # 返回: (cnt, flag) 后者标记是否存在该差值
            cnt = 0; flag = False
            for i,a in enumerate(nums):
                lmt = bisect_left(nums, a+d, i)
                cnt += lmt - i - 1
                if lmt<n and nums[lmt]==a+d: flag=True
            return cnt,flag
        # 二分
        l,r = 0,max(nums) - min(nums)
        ans = 0
        while l<=r:
            m = (l+r)>>1
            cnt,flag = f(m)
            if cnt<k:
                l = m+1
                # 只有存在时才更新
                if flag: ans = m
            else: r = m-1
        return ans

    """ 0407. 接雨水 II #hard #题型
相较于 「0042. 接雨水」 变成了二维形式. 限制: 矩阵 m,n 200
思路1: 向内传播「约束高度」, 采用 #最小堆.
    每个位置的水位受什么决定? 四周三个柱子的(水位)高度的最小值. 
        因此直觉是: **根据已经确定的较小值来更新周围位置**. —— 「约束传播」
    本题中, 矩形四边上肯定无法蓄水, 将约束条件向内传递即可.
        如何确定更新的顺序? 向内传播「约束高度」, 每次取约束高度最小的位置更新.
        为什么最小值? 因为最小值的蓄满水之后可能变高, 需要更新传递给周围的位置.
    具体而言, **维护一个 #最小堆 记录当前边界上的约束高度**.
    复杂度: O(mn log(m+n))
思路2: 上面的思路理解为一个一个「加水」, 另一种思路是「漏水」. 初始时假设水位是最高的柱子高度. 然后从四周开始漏水, 将新的高度约束向内传递.
    具体而言, 可以用一个 #队列 来记录更新过的水位, 然后用起来更新周围的位置.
    复杂度: 由于采用的是队列, 更新某一位置的高度, 可能需要传播到整个矩阵, 因此复杂度 `O(m^2 n^2)`.
[官答](https://leetcode.cn/problems/trapping-rain-water-ii/solution/jie-yu-shui-ii-by-leetcode-solution-vlj3/)
"""
    def trapRainWater(self, heightMap: List[List[int]]) -> int:
        m,n = len(heightMap), len(heightMap[0])
        # 边界
        if m<3 or n<3: return 0
        ans = 0
        visited = [[0] * n for _ in range(m)]
        q = []
        # (h, i,j) 蓄水高度(约束), 位置
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        def check(x,y): return 0<=x<m and 0<=y<n
        # 初始化边界
        for x in range(m):
            for y in range(n):
                if x==0 or x==m-1 or y==0 or y==n-1:
                    visited[x][y] = 1
                    for dx,dy in directions:
                        nx,ny = x+dx, y+dy
                        if not check(nx,ny) or visited[nx][ny]: continue
                        # 约束传播
                        nHeight = max(heightMap[nx][ny], heightMap[x][y])
                        heappush(q, (nHeight, nx,ny))
        # 
        while q:
            nh,x,y = heappop(q)
            # 避免重复访问!
            if visited[x][y]: continue
            visited[x][y] = 1       # 标记访问
            # 可蓄水高度 > 柱子, 更新 ans
            if nh > heightMap[x][y]: ans += nh - heightMap[x][y]
            # 直接传播的约束
            h = max(nh, heightMap[x][y])
            for dx,dy in directions:
                nx,ny = x+dx, y+dy
                if not check(nx,ny) or visited[nx][ny]: continue
                # 约束传播
                nHeight = max(heightMap[nx][ny], h)
                heappush(q, (nHeight, nx,ny))
        return ans
    
    """ 1095. 山脉数组中查找目标值 #hard 
给定一个「山脉数组」, 元素严格递增递减. 在其中查找 =target 的元素 idx. 
限制: 本题是一个 #交互题, 对于 n 1e4, 要求 100次调用内解决.
思路1: 模拟搜索的过程, #细节比较多
思路2: 官答分解成两步, 先用二分找到peak点, 然后在两个有序数组中 #二分 找目标值. 更清楚
    [official](https://leetcode.cn/problems/find-in-mountain-array/solution/shan-mai-shu-zu-zhong-cha-zhao-mu-biao-zhi-by-leet/)
"""
    def findInMountainArray(self, target: int, mountain_arr: 'MountainArray') -> int:
        def find(l,r):
            if l > r: return -1
            m = (l+r) // 2
            vm = mountain_arr.get(m)
            if vm==target:
                # 注意不能直接返回! 因为可能mid可能是等高的靠右的那个. 
                v = find(l,m-1)
                if v!=-1: return v
                return m
            if m==0: return find(l+1,r)
            vml = mountain_arr.get(m-1)
            # if vml==target: return m-1
            if vm > vml:
                if target > vm: return find(m+1,r)
                else:
                    v = find(l,m-1)
                    if v!=-1: return v
                    else: return find(m+1,r)
            else:
                if target > vm: return find(l,m-1)
                else:
                    v = find(l,m-1)
                    if v!=-1: return v
                    else: return find(m+1,r)
        return find(0, mountain_arr.length()-1)
    
    
    
sol = Solution()
result = [
    # sol.smallestDistancePair([1,3,1], 1),
    # sol.smallestDistancePair(nums = [1,1,1], k = 2),
    # sol.smallestDistancePair(nums = [1,6,1], k = 3),
    # sol.smallestDistancePair([9,10,7,10,6,1,5,4,9,8], 18),
    sol.trapRainWater(heightMap = [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]),
    sol.trapRainWater(heightMap = [[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]),
]
for r in result:
    print(r)
