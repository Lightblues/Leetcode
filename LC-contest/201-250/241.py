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
https://leetcode.cn/contest/weekly-contest-241
@2022 """

""" 1865. 找出和为指定值的下标对 #medium
要求实现一个类, 初始化 nums1, nums2. 实现: 1) 将一个正数加到 `nums2[idx]`; 2) 统计满足 `nums1[i] + nums2[j]` 等于指定值的下标对 (i, j) 数目
限制: nums1 长度 m 1e3, 数据范围 1e9; nums2 长度 n 1e5, 数据范围 1e5. 操作次数1000次.
思路0: 直接用一个 #哈希表 记录两数组 (i,j) 匹配的和的数量 #TLE
    复杂度: 初始化的时候为 O(mn), 每次增加一个值的复杂度为 O(m), 因此总体复杂度为 `O(m (n+K))`, 其中K为操作数量. 所以是初始化超时了?
思路1: 直接用两个 #哈希表 来记录量数组的取值, 然后每次查询的时候遍历 num1, 求目标值的补即可.
    复杂度: 初始化 O(m+n), 每次查询 `O(m)`
总结: 放在第三题可能导致自己想多了. 思路0没有考虑初始化两两匹配的复杂度, 思路1实际上是更容易想到的.
"""
class FindSumPairs:
    # 思路0 #TLE
    def __init__(self, nums1: List[int], nums2: List[int]):
        self.nums1 = nums1
        self.nums2 = nums2
        self.cnt = defaultdict(int)
        for a in nums2:
            for b in nums1:
                self.cnt[a+b] += 1

    def add(self, index: int, val: int) -> None:
        a = self.nums2[index]
        self.nums2[index] += val
        c = self.nums2[index]
        for b in self.nums1:
            self.cnt[a+b] -= 1
            self.cnt[b+c] += 1

    def count(self, tot: int) -> int:
        return self.cnt[tot]


class FindSumPairs:
    # 思路1
    def __init__(self, nums1: List[int], nums2: List[int]):
        self.d1 = Counter(nums1)
        self.d2 = Counter(nums2)
        self.nums2 = nums2

    def add(self, index: int, val: int) -> None:
        self.d2[self.nums2[index]] -= 1
        self.nums2[index] += val
        self.d2[self.nums2[index]] += 1

    def count(self, tot: int) -> int:
        ans = 0
        for a,v in self.d1.items():
            ans += v * self.d2[tot - a]
        return ans

class Solution:
    """ 1863. 找出所有子集的异或总和再求和 #easy
对于一个数组, 求其所有子集的异或值的和. 
限制: 长度 12以内
思路: #暴力 搜索. 对于每个数字模拟是否取
"""
    def subsetXORSum(self, nums: List[int]) -> int:
        # 想错了
        # n = len(nums)
        # mul = 2**(n-1)
        # acc = 0
        # for num in nums:
        #     acc ^= num
        # return acc if mul&1 else 0
        
        n = len(nums)
        ans = 0
        def dfs(idx=0, acc=0):
            nonlocal ans
            if idx==n:
                ans += acc; return
            dfs(idx+1, acc)
            dfs(idx+1, acc^nums[idx])
        dfs(0)
        return ans
    
    """ 1864. 构成交替字符串需要的最小交换次数 #medium
要求将01数字经过若干次操作变为「交替数组」, 操作为交换任意两个位置的数字.
限制: 1e4
思路1: #分类 讨论, 然后模拟
    根据数组长度判断: 若为偶数, 并且两个字符数量相同, 则分别尝试0/1开头; 若为奇数并且0/1的数量相差1, 则按照大的那一个开头. 否则不成立.
关联: 「1888. 使二进制字符串字符交替的最少反转次数」
"""
    def minSwaps(self, s: str) -> int:
        n = len(s)
        n0 = s.count('0')
        
        chs = '01'
        def f(s, start=0):
            acc = 0
            for i, c in enumerate(s):
                acc += chs[start]!=c
                start = 1-start
            return -1 if acc&1 else acc//2
        if n&1==0:
            if n0!=n//2: return -1
            return min(f(s), f(s, 1))
        else:
            if n0==n//2: return f(s, 1)
            elif n0==n//2+1: return f(s, 0)
            else: return -1
        
    """ 1866. 恰有 K 根木棍可以看到的排列数目 #hard
对于1...n的所有排列, 问其中能从左侧正好看到k根木棍 (能看到要求没有遮挡) 的排列数目.
限制: n 1e3
思路1: #DP
    形式: `f[i][j]` 表示用 1...i 进行排列, 能够看到 j 个的排列数量.
    递归: 若能够看到第i个位置, 则其一定高为i, 在剩余的 i-1 根中可以看到 j-1 个, 也即 `f[i-1][j-1]`; 否则, 其为 1...i-1 中的某一个数字, 剩余的 i-1 个中可以看到 j根; 注意, 假设位置i的数字为k, **由于能否看到仅依赖于相对大小关系, 我们可以直接将它们看成是 1...i-1**, 因此, 等价于 `f[i-1][j]`.
    综上, 有 `f[i][j] = f[i-1][j-1] + (i-1) * f[i-1][j]`
    约束: 0<j<=i. 因此边界情况 `f[i][0] = 0`. 但由于 `f[1][1] = f[0][0]+0` 要等于1, 我们初始化 `f[0][0]=1`
    复杂度: O(nk)
思路2: 建模为 #排列 问题.
    对于可见的k个木棍, 将其和后面不可见的看成一个整体, 则n个数字被划分成了k组, 并且 **每组中的第一个数字正是其中最大的那个数, 其他数字任意排列** (注意到, 这恰好是一个 **圆排列**, 数量等于 `(len-1)!`); 而不同组之间的顺序是固定的, 因为要求从小到大.
    综上, 问题转化为: 将n个数字分成k组, 对每个组求「循环排列数」 —— 恰好是「把n个元素排列成k个非空圆圈（循环排列）的方法数目」这一[第一类斯特灵数](https://zh.wikipedia.org/wiki/%E6%96%AF%E7%89%B9%E7%81%B5%E6%95%B0) 的直观理解.
    在具体的递推公式上, 完全和思路1一致, 只不过在理解上更深了一层.
    见 [灵神](https://leetcode.cn/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/solution/zhuan-huan-cheng-di-yi-lei-si-te-lin-shu-2y1k/).
"""
    def rearrangeSticks(self, n: int, k: int) -> int:
        # 思路 1/2
        mod = 10**9+7
        # 只需要递归到 k 即可
        f = [[0] * (k+1) for _ in range(n+1)]
        f[0][0] = 1     # 初始化
        for i in range(1, n+1):
            # 注意 >i 之后是无意义的 (虽然算下来的结果也为0)
            for j in range(1, min(i+1, k+1)):
                f[i][j] = (f[i-1][j-1] + (i-1) * f[i-1][j]) % mod
        return f[n][k]

            
    
    
    

    
sol = Solution()
result = [
    # sol.subsetXORSum(nums = [1,3]),
    # sol.subsetXORSum(nums = [5,1,6]),
    # sol.minSwaps(s = "111000"),
    # sol.minSwaps(s = "1110"),
#     testClass("""["FindSumPairs", "count", "add", "count", "count", "add", "add", "count"]
# [[[1, 1, 2, 2, 2, 3], [1, 4, 5, 2, 5, 4]], [7], [3, 2], [8], [4], [0, 1], [1, 1], [7]]"""),
    sol.rearrangeSticks(n = 3, k = 2),
    sol.rearrangeSticks(n = 5, k = 5),
    sol.rearrangeSticks(n = 20, k = 11),
]
for r in result:
    print(r)
