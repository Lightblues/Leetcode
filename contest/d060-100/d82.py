from tracemalloc import start
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
https://leetcode-cn.com/contest/biweekly-contest-82
@2022 """

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 6116. 计算布尔二叉树的值 """
    def evaluateTree(self, root: Optional[TreeNode]) -> bool:
        def dfs(node: TreeNode):
            if node.val ==0: return False
            elif node.val==1: return True
            elif node.val==2: return dfs(node.left) or dfs(node.right)
            elif node.val==3: return dfs(node.left) and dfs(node.right)
        return dfs(root)
    
    """ 6117. 坐上公交的最晚时间 #medium #细节 #模拟
给定一组 passengers 的到达时间和 buses 的出发时间, **同组中的数字各不相同**. 每辆车有capacity限制, 若人超过了则需要等下一辆. 问你想要赶上最后一辆车, 最晚要到达车站的时间.
注意: 若 `buses = [10,20], passengers = [2,17,18,19], capacity = 2` 第二辆车上的人是 [17,18], 但你不能和他们相同时间, 因此需要16的时刻到达
思路1: #双指针 遍历到结尾, 然后注意最后的判断
    需要 #分类讨论, 一般情况下, 我们在最后一个人的后面上车即可 (掐点); 那什么情况下必须像例子一样往前遍历? 1) 人数满了, 要赶在最后一个人之前; 2) 这辆车的最后一个人的到达时间刚好为发车时间.
"""
    def latestTimeCatchTheBus(self, buses: List[int], passengers: List[int], capacity: int) -> int:
        # 双指针遍历
        buses.sort(); passengers.sort()
        iP = -1; nP = len(passengers)
        startIP = -1    # 记录上一辆车的最后一个人
        for i, time in enumerate(buses):
            cnt = 0
            startIP = iP
            while iP<nP-1 and passengers[iP+1]<=time and cnt<capacity:
                cnt += 1
                iP += 1
        lastTime = buses[-1]
        
        # 边界: iP不合法. 实际上可省略
        # if iP==-1: return lastTime
        
        if iP-startIP==capacity or passengers[iP]==lastTime:
            # 两种情况: 1. 车满了; 2. 最后一个人踩点. 需要向前插空
            t = passengers[iP]
            while iP >0 and passengers[iP-1]==t-1:
                iP -=1
                t -= 1
            return passengers[iP]-1
        else:
            return  lastTime
        
    """ 6118. 最小差值平方和 #medium
化简下来, 目标是是数组中所有元素的平方和最小化, 每次可以对任意元素+/-1, 一共k次机会. 求最小值.
提示: 显然, 要求所有元素的绝对值尽可能小, 每次都对于大数字做操作即可.
思路1: 先对于数组排序, 然后按照 #阶梯 的方式往下减.
    形象化: 每次「削去」高峰, 直到操作数不够.
    好像前面的题目中有类似「蓄水」的题目, 肯定不是按照下面来写的? 但找不到题目了, 感觉下面的写法也挺烦的.
    具体如何做? 用一个哈希表记录每个高度的数量, 然后从高到低尝试「削峰」. 若操作数够, 则将当前最大值均变为次大值; 否则, 根据 divmod 将剩余操作数平均分配到这些最大值上.
关联: 找相关题进行总结.
"""
    def minSumSquareDiff(self, nums1: List[int], nums2: List[int], k1: int, k2: int) -> int:
        d = list(abs(a-b) for a,b in zip(nums1, nums2))
        k = k1 + k2
        d.sort()
        # 下面按照阶梯做减法, 感觉写烦了?
        num2cnt = defaultdict(int)
        for v in d:
            num2cnt[v] += 1
        
        last = max(num2cnt) # 上一个较大元素
        num2cnt[0] = 0      # 哨兵
        # 从高到低「削去」高峰
        for v in sorted(num2cnt.keys(), reverse=True)[1:]:
            c = num2cnt[last]
            if k >= (last-v) * c:
                num2cnt[v] +=  c
                num2cnt.pop(last)
                k -= (last-v) * c
            else:
                a,b = divmod(k, c)
                num2cnt[last-a-1] += b
                num2cnt[last-a] += c - b
                num2cnt[last] -= c
                break
            last = v
        ans = 0
        for k,v in num2cnt.items():
            ans += k*k * v
        return ans

    """ 6119. 元素值大于变化阈值的子数组 #hard #单调栈
给定一个整数数组和一个threshold, 要求找到一个整数k, 使得数组中包括一个长度为k的所有元素都大于 threshold / k 的子数字. (找到任意一个)
思路1: 找到每一个元素作为最小值的左右边界. 这样, 我们可以得到哈希表 len2max, 记录每一个长度限制下, 子数组最小值的最大值.
    为了求左右边界, 可以利用 #单调栈 求解.
    复杂度: O(n)
    关联: 「6077. 巫师的总力量和」
思路2: #并查集
    直觉: 对于数组中的元素, 从大到小考虑他们所在的以其为最小值的连续子数组 (满足当前元素是最小值), 依次判断是否满足条件即可.
    如何记录连接关系? 采用并查集. 但题目要求是相邻的两个才能连接, 如何做? 下面的思路是: 每次将被遍历的元素连接到其右侧节点上 (在最右侧加一个哨兵). 这样, **对于第i个节点, 合并到i+1节点之后, i元素的值是 `sz[j] - 1` 个元素只最小的那个**! 这是因为, 由于从大到小访问, 第i节点的大小必然是1. 若i+1节点更小, 则其大小也为1; 若i+1节点更大, 则它是一条链并且最右侧一定连着一个更小的点, 也符合上述论述.
    复杂度: 排序 O(n logn)
    from [灵神](https://leetcode.cn/problems/subarray-with-elements-greater-than-varying-threshold/solution/by-endlesscheng-j6pp/)
总结: 思路1是更为清晰的, 关键是要想到「某一元素最为最小值的左右边界」, 之前做过巫师题的情况下, 一开始没有想到有点可惜. 思路2用到并查集, 灵神的代码很简洁, 但实际上的思维量还挺大的.
"""
    def validSubarraySize(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        # 求左右边界 (严格小)
        right  = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and stack[-1][0] >= nums[i]:
                stack.pop()
            right[i] = stack[-1][1] if stack else n
            stack.append((nums[i], i))
        left = [-1] * n
        stack = []
        for i in range(n):
            while stack and stack[-1][0] >= nums[i]:
                stack.pop()
            left[i] = stack[-1][1] if stack else -1
            stack.append((nums[i], i))

        len2max = defaultdict(int)
        for i, num in enumerate(nums):
            ll = right[i]-left[i]-1
            len2max[ll] = max(len2max[ll], num)
        for l, v in len2max.items():
            if threshold/l < v: return l
        return -1

    def validSubarraySize(self, nums: List[int], threshold: int) -> int:
        # 思路2 并查集
        n = len(nums)
        fa = list(range(n + 1))
        sz = [1] * (n + 1)  # 最后一位哨兵
        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        for num, i in sorted(zip(nums, range(n)), reverse=True):
            j = find(i + 1)
            fa[i] = j  # 将元素i(由于从大到小遍历, 此时一定是单个点) 合并到 i+1 个位置. 注意, 此时num是 sz[j] - 1 个元素只最小的那个!
            sz[j] += sz[i]
            # num是 sz[j] - 1 个元素只最小的那个!
            if num > threshold // (sz[j] - 1):
                return sz[j] - 1
        return -1



    def f(self, nums: list):
        # n = len(strength)
        # # left[i] 为左侧严格小于 strength[i] 的最近元素位置（不存在时为 -1）
        # # right[i] 为右侧小于等于 strength[i] 的最近元素位置（不存在时为 n）
        # left, right, st = [-1] * n, [n] * n, []
        # for i, v in enumerate(strength):
        #     while st and strength[st[-1]] >= v: right[st.pop()] = i
        #     if st: left[i] = st[-1]
        #     st.append(i)
        # return left, right
        
        
        n = len(nums)
        # 求左右边界, 注意这里的边界都是开区间
        right  = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and stack[-1][0] >= nums[i]:
                stack.pop()
            right[i] = stack[-1][1] if stack else n
            stack.append((nums[i], i))
        left = [-1] * n
        stack = []
        for i in range(n):
            while stack and stack[-1][0] >= nums[i]:
                stack.pop()
            left[i] = stack[-1][1] if stack else -1
            stack.append((nums[i], i))
        return left

sol = Solution()
result = [
    # sol.minSumSquareDiff(nums1 = [1,4,10,12], nums2 = [5,8,6,9], k1 = 1, k2 = 1),
    # sol.minSumSquareDiff(nums1 = [1,2,3,4], nums2 = [2,10,20,19], k1 = 0, k2 = 0),
    # sol.minSumSquareDiff([1,4,10,12],[5,8,6,9],10,5),
    # sol.minSumSquareDiff([7,11,4,19,11,5,6,1,8],[4,7,6,16,12,9,10,2,10],3,6)
    
    # sol.latestTimeCatchTheBus(buses = [10,20], passengers = [2,17,18,19], capacity = 2),
    # sol.latestTimeCatchTheBus(buses = [20,30,10], passengers = [19,13,26,4,25,11,21], capacity = 2),
    # sol.latestTimeCatchTheBus(buses = [20,30,10], passengers = [19,13,26,4,25,11,21], capacity = 4),
    # sol.latestTimeCatchTheBus([3], [4], 1), # 3
    # sol.latestTimeCatchTheBus([5], [2,3], 10000),   # 5
    # sol.latestTimeCatchTheBus([18,8,3,12,9,2,7,13,20,5],[13,10,8,4,12,14,18,19,5,2,30,34],1),
    # sol.f([1,3,4,3,1]),
    
    sol.validSubarraySize(nums = [1,3,4,3,1], threshold = 6),
    # sol.validSubarraySize(nums = [6,5,6,5,8], threshold = 7),
]
for r in result:
    print(r)
