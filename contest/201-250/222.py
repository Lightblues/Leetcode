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
https://leetcode.cn/contest/weekly-contest-222
@2022 """
class Solution:
    """ 1710. 卡车上的最大单元数 """
    def maximumUnits(self, boxTypes: List[List[int]], truckSize: int) -> int:
        boxTypes.sort(key=lambda x: -x[1])
        ans = 0; 
        idx = 0; n = len(boxTypes)
        while truckSize>0 and idx<n:
            if boxTypes[idx][0] >= truckSize:
                ans += truckSize * boxTypes[idx][1]
                break
            else:
                ans += boxTypes[idx][0] * boxTypes[idx][1]
                truckSize -= boxTypes[idx][0]
                idx += 1
        return ans

    """ 1711. 大餐计数 """
    def countPairs(self, deliciousness: List[int]) -> int:
        mod = 10**9+7
        targets = [2**i for i in range(22)]
        cnt = Counter()
        ans = 0
        for d in deliciousness:
            for t in targets:
                ans = (ans+cnt[t-d]) % mod
            cnt[d] += 1
        return ans
    
    
    """ 1712. 将数组分成三个子数组的方案数 #medium #题型 #反思
要将一个数组分成三部分, 使得三部分的和依次满足 a<=b<=c, 求分割数.
思路: 利用 #前缀和 加速, 用 #二分 搜索.
    假设数组和为 s, 给定a, 则a+b需要满足 2*a<=a+b<=(s+a)/2
    注意: #debug 这里需要明确左右边界. 假设数组分成 [0...l], [l+1...m], [m...n-1] 三部分, 都要求非空.
        则在遍历数组的过程中 (左部分 l), 我们查询的 **中间部分的 m指针的搜索范围为 `[l+1...n-2]`**
参见 [灵神](https://leetcode.cn/problems/ways-to-split-array-into-three-subarrays/solution/golang-jian-ji-xie-fa-by-endlesscheng-xaad/)
总结: 推导很简单, 但实际上 #边界 分析搞了半天. 值得 #反思
"""
    def waysToSplit(self, nums: List[int]) -> int:
        mod = 10**9+7
        s = sum(nums)
        acc = list(accumulate(nums, initial=0))
        ans = 0
        for l in range(len(nums)):
            a = acc[l+1]
            # if a>s/3: break
            limitL, limitR = 2*a, (s+a)//2
            if limitL>limitR: break
            # 注意, m 的搜索范围
            mL = bisect_left(acc, limitL, lo=l+2, hi=len(nums)-1)
            # `mR` 是下一个不能取的位置, lo 可以去mL, 也可以是 l+2 (此时一定要上面的剪枝 `if limitL>limitR: break`).
            # 注意 l==r 时实际上没法取
            mR = bisect_right(acc, limitR, lo=mL, hi=len(nums)) 
            ans = (ans + mR-mL) % mod
        return ans
    

    """ 1713. 得到子序列的最少操作次数 #hard #转化 #题型
问题等价于, 找到 s,t 两数组之间的最长公共子序列. 注意原本s中的所有整数互不相同.
限制: 两者长度 1e5
思路0: 计算 #最长公共子序列 的基本方案是 DP, 但这里的复杂度不够.
思路1: 利用这里某一「序列s中的元素互不相同」的性质, 可以将s中的元素值重新赋值为 0,1,2..., 然后t序列替换为这些重标的值. 则, 问题等价于在t中找到最长递增子序列.
    解法: 用一个数组 dp[i] 记录长度为i的子序列的结尾最小数字. 在遍历t的过程中, 若元素大于 dp[-1] 则拓展, 否则二分查找, 更新最小数字. 复杂度: `O(n logn)`
    参见 「0300. 最长递增子序列」, 见 [官答](https://leetcode.cn/problems/longest-increasing-subsequence/solution/zui-chang-shang-sheng-zi-xu-lie-by-leetcode-soluti/)
    [本题官答](https://leetcode.cn/problems/minimum-operations-to-make-a-subsequence/solution/de-dao-zi-xu-lie-de-zui-shao-cao-zuo-ci-hefgl/)
    see DP
"""

    
sol = Solution()
result = [
    sol.waysToSplit(nums = [1,1,1]),
    sol.waysToSplit(nums = [1,2,2,2,5,0]),
    sol.waysToSplit(nums = [3,2,1]),
    sol.waysToSplit([0,3,3]),
    sol.waysToSplit([0,0,0]),
    # sol.maximumUnits(boxTypes = [[5,10],[2,5],[4,7],[3,9]], truckSize = 10),
    # sol.maximumUnits(boxTypes = [[1,3],[2,2],[3,1]], truckSize = 4),
    
    # sol.countPairs(deliciousness = [1,1,1,3,3,3,7]),
    
    # sol.minOperations(target = [5,1,3], arr = [9,4,2,3,4]),
    # sol.minOperations(target = [6,4,8,1,3,2], arr = [4,7,6,2,3,8,6,1]),
    
]
for r in result:
    print(r)
