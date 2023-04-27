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
https://leetcode.cn/contest/weekly-contest-218
@2022 """
class Solution:
    """ 1678. 设计 Goal 解析器 """
    def interpret(self, command: str) -> str: 
        idx = 0; n = len(command)
        ans = ""
        while idx<n:
            if command[idx] == 'G': ans += 'G'
            else:
                if command[idx+1] == ")": ans += 'o'; idx += 1
                else: ans += 'al'; idx += 3
            idx += 1
        return ans
    
    """ 1679. K 和数对的最大数目 """
    def maxOperations(self, nums: List[int], k: int) -> int:
        cnt = Counter(nums)
        ans = 0
        m = k//2 if k%2==0 else -1
        limit = k//2
        for i,v in cnt.items():
            if i==m: ans += v//2
            elif i<=limit: ans += min(v, cnt[k-i])
        return ans
    
    """ 1680. 连接连续二进制数字 #medium
技巧: 如何判断是2的整数次幂? 
    一种方式是计算 `i & (i-1) == 0`, 参见 [zero](https://leetcode.cn/problems/concatenation-of-consecutive-binary-numbers/solution/lian-jie-lian-xu-er-jin-zhi-shu-zi-by-ze-t40j/)
"""
    def concatenatedBinary(self, n: int) -> int:
        mod = 10**9 + 7
        ans = 0
        for i in range(1, n+1):
            ans = ((ans<<i.bit_length()) + i) % mod
        return ans
    
    """ 1681. 最小不兼容性 #hard
将数组nums分成 **大小相等的** k组, 要求每组的数字都不相同. score定义为所有组最大最小差值的和, 要求score最小.
限制: 数组长度 n 16
思路0: 没有看到分组大小相同的限制, #error 记录
    记 `f(i,mask)` 表示将mask分成前i个组, 当前score最小值. 则有递归 `f(i,mask) = min{ f(i-1,sub) + s(mask\sub) }` 其中sub为所有符合条件的子集.
    子集遍历: `sub = {mask & (sub-1)}`
    复杂度: O(k 3^n) 这样显然会超时
思路1: #状压 #子集遍历
    事实上, 于之前遍历子数组不同的是, 这里限制了分组大小相同, 因此仅需要遍历所有符合条件的分组即可.
    如何做? 每组大小为size, 则我们可以遍历所有大小为size的整数倍的组. 则递推公式 `f[mask] = min{ f[mask\sub] + s(sub) }` 其中mask的大小为size整数倍, sub为所有大小为k的mask的子集.
    see [zero](https://leetcode.cn/problems/minimum-incompatibility/solution/zui-xiao-bu-jian-rong-xing-by-zerotrac2-rwje/)
    在具体的实现上, 还可以直接通过 #DFS 来解决, see [here](https://leetcode.cn/problems/minimum-incompatibility/solution/python-zhuang-ya-dfs-by-qin-qi-shu-hua-2-lwff/)
"""
    def minimumIncompatibility(self, nums: List[int], k: int) -> int:
        # 在思路0 的基础上修改了, 超时
        if max(Counter(nums).values()) > k: return -1
        n = len(nums); mx = 1<<n
        size = n//k
        # @lru_cache(None)
        # def s(mask):
        #     idx = (i for i in range(n) if mask&(1<<i))
        #     num = [nums[i] for i in idx]
        #     if len(num) != len(set(num)): return inf
        #     return max(num) - min(num)
        @lru_cache(None)
        def s(mask):
            idxs = [i for i in range(n) if mask&(1<<i)]
            # assert len(idxs) == size
            if len(idxs) != size: return inf
            num = [nums[i] for i in idxs]
            if len(num) != len(set(num)): return inf
            return max(num) - min(num)
        f = [s(mask) for mask in range(mx)]
        for _ in range(k-1):
            for mask in range(mx-1, -1, -1):
                sub = mask & (mask-1)
                while sub:
                    f[mask] = min(f[mask], f[mask^sub] + s(sub))
                    sub = mask & (sub-1)
        return f[mx-1]
    def minimumIncompatibility(self, nums: List[int], k: int) -> int:
        if max(Counter(nums).values()) > k: return -1
        n = len(nums); mx = 1<<n; size = n//k
        # 计算所有大小为size的组的分数
        s = {}
        for mask in range(1, mx):
            if mask.bit_count() == size:
                num = [nums[i] for i in range(n) if mask & (1<<i)]
                # 组内数字都不同
                if len(num) != len(set(num)): continue
                s[mask] = max(num) - min(num)
        # 从小到大遍历所有大小为size整数倍的mask
        f = [inf]*mx
        for kk,v in s.items():
            f[kk] = v
        for mask in range(1, mx):
            if mask.bit_count() % size == 0:
                for sub in s:
                    if sub&mask != sub: continue
                    f[mask] = min(f[mask], f[mask^sub] + s[sub])
        return f[mx-1]

sol = Solution()
result = [
    # sol.interpret(command = "G()(al)"),
    # sol.maxOperations(nums = [1,2,3,4], k = 5),
    # sol.maxOperations(nums = [3,1,3,4,3], k = 6),
    # sol.concatenatedBinary(n = 3),
    # sol.concatenatedBinary(12),
    sol.minimumIncompatibility(nums = [1,2,1,4], k = 2),
    sol.minimumIncompatibility(nums = [6,3,8,1,3,1,2,2], k = 4),
    sol.minimumIncompatibility(nums = [5,3,3,6,3,3], k = 3),
    sol.minimumIncompatibility([7,3,16,15,1,13,1,2,14,5,3,10,6,2,7,15], 8),
    
]
for r in result:
    print(r)
