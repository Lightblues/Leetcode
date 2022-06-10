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
https://leetcode-cn.com/contest/biweekly-contest-55
@2022 """
class Solution:
    """ 1909. 删除一个元素使数组严格递增 #easy #题型
给定一个数组, 最多删除一个元素, 判断其是否可将其变为递增数组.
思路0: #反思
    居然被一道简单题卡住……思路比较乱.
    混乱的原因在于, 本题有两种情况: `[1,2,10,5,7]` 是需要删除一个峰值, 而 `[105,924,32,968]` 是要删除一个低谷.
    假如在位置i检测到 `nums[i] <= nums[i-1]`, 情况一需要将 `i, i-2` 比较, 而情况二则是 `i+1, i-1`. 因此判断比较复杂.
    下面答案就比较清楚: 反正最多删除一个元素, 我们可以分别尝试删除 `i, i-1`, 对于每种情况进行判断即可 (写成函数 `check(i)` 来封装逻辑).
    总结: 对于相对简单的题, 在陷入复杂判断的时候, 尝试跳出来尝试更「笨」的想法, 或许更加清晰.
"""
    def canBeIncreasing(self, nums: List[int]) -> bool:
        # https://leetcode.cn/problems/remove-one-element-to-make-the-array-strictly-increasing/solution/shan-chu-yi-ge-yuan-su-shi-shu-zu-yan-ge-tnr7/
        n = len(nums)
        # 检查数组 nums 在删去下标为 idx 的元素后是否严格递增
        def check(idx: int) -> bool:
            for i in range(1, n - 1):
                prev, curr = i - 1, i
                if prev >= idx:
                    prev += 1
                if curr >= idx:
                    curr += 1
                if nums[curr] <= nums[prev]:
                    return False
            return True
        
        for i in range(1, n):
            # 寻找非递增相邻下标对
            if nums[i] <= nums[i-1]:
                return check(i) or check(i - 1)
        return True

    """ 1910. 删除一个字符串中所有出现的给定子字符串 """
    def removeOccurrences(self, s: str, part: str) -> str:
        while True:
            idx = s.find(part)
            if idx==-1: return s
            s = s[:idx] + s[idx+len(part):]
            
    """ 1911. 最大子序列交替和 #medium #dp
定义「序列交替和」为: 序列中偶数元素之和 - 序列中奇数元素之和. 要求求出给定序列的所有子序列中, 这一差值的最大值.
思路1: #dp
    dp递归的元素为 (x,y) 分别表示所选的子序列长度为 odd,even 时的最大差值.
    这样, 有递推公式 `dp[i] = [max{dp[i-1][0], dp[i-1][1]-nums[i]}, max{dp[i-1][1], dp[i-1][0]+nums[i]}]`
 """
    def maxAlternatingSum(self, nums: List[int]) -> int:
        dp = [0, 0]
        for num in nums:
            dp = [
                max(dp[0], dp[1]-num), max(dp[1], dp[0]+num)
            ]
        return max(dp)
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res


""" 1912. 设计电影租借系统 #hard #sortedcontainer
有一组n家电影租借店, (shop, movie, price) 表示在shop中有一个movie租借价格为price (注意每家店最多只有一份电影拷贝). 顾客在某一家店租界后会在原店归还.
主要是实现两种查询: 1) 对于给定的电影m, 查找还有这份影片(未租借出去)的店中价格最低的5个; 2) 查询所有已租借的影片中价格最低的5个, 按照 (price, shop, movie) 排序.
思路1: #最小推
    要实现最小值的查询, 首先考虑到堆结构.
    如何维护信息? 对于查询1, 可以给每部影片建立一个堆(索引); 然后, 用一个结构来记录该影片是否被租借: 当出堆的时候, 发现该片已被租借则舍弃, 否则加入答案中 (最后将答案中的记录再放回堆). 对于查询2, 维护一个最小堆, 每个元素为 `(price, shop, movie)` 结构; 同样, 当出堆的时候, 若发现已归还则舍弃, 否则加入答案.
思路2: #sortedcontainer
    官答则更为简单地调用了 SortedList 来记录 尚未租借的, 以及全部已经租借的影片.
    
---
search(int movie) 返回未借出的影片i 中最便宜5家商店
report() 返回已借出的所有影片中的前5部, 按照价格、影片id、商店id排序
"""

class MovieRentingSystem:
    # https://leetcode.cn/problems/design-movie-rental-system/solution/she-ji-dian-ying-zu-jie-xi-tong-by-leetc-dv3z/
    def __init__(self, n: int, entries: List[List[int]]):
        import sortedcontainers
        self.t_price = dict()
        self.t_valid = defaultdict(sortedcontainers.SortedList)
        self.t_rent = sortedcontainers.SortedList()
        
        for shop, movie, price in entries:
            self.t_price[(shop, movie)] = price
            self.t_valid[movie].add((price, shop))

    def search(self, movie: int) -> List[int]:
        t_valid_ = self.t_valid
        
        if movie not in t_valid_:
            return []
        
        return [shop for (price, shop) in t_valid_[movie][:5]]
        
    def rent(self, shop: int, movie: int) -> None:
        price = self.t_price[(shop, movie)]
        self.t_valid[movie].discard((price, shop))
        self.t_rent.add((price, shop, movie))

    def drop(self, shop: int, movie: int) -> None:
        price = self.t_price[(shop, movie)]
        self.t_valid[movie].add((price, shop))
        self.t_rent.discard((price, shop, movie))

    def report(self) -> List[List[int]]:
        return [(shop, movie) for price, shop, movie in self.t_rent[:5]]

class MovieRentingSystem:
    """ 利用堆来返回最小值 """
    def __init__(self, n: int, entries: List[List[int]]):
        self.n = n
        
        m2shops = defaultdict(list)     # 对于每部未借出电影建立索引 (heap)
        shop2movies = [set() for _ in range(n)] # 记录每家店中现存的电影
        priceMap = {}       # 记录价格
        for shop, movie, price in entries:
            # m2shops[movie][shop] = price
            heappush(m2shops[movie], (price, shop))
            shop2movies[shop].add(movie)
            priceMap[(shop, movie)] = price
            
        self.m2shops = m2shops
        self.shop2movies = shop2movies
        self.price = priceMap
        self.cheapestRant = []  # 所有借出(过)的电影, 是否归还通过 self.shop2movies 来验证. (price, shop, movie)

    def search(self, movie: int) -> List[int]:
        h = self.m2shops[movie]
        res = []
        while h and len(res) < 5:
            p,s = heappop(h)
            if movie in self.shop2movies[s] and (p,s) not in res:
                res.append((p,s))
        for i in res:
            heappush(h, i)
        return [s for p,s in res]

    def rent(self, shop: int, movie: int) -> None:
        self.shop2movies[shop].remove(movie)
        heappush(self.cheapestRant, (self.price[(shop, movie)], shop, movie))

    def drop(self, shop: int, movie: int) -> None:
        # 归还, 注意需要将其加入到 m2shops 中 (因为在 search 时会 heappop 掉)
        self.shop2movies[shop].add(movie)
        heappush(self.m2shops[movie], (self.price[(shop, movie)], shop))

    def report(self) -> List[List[int]]:
        h = self.cheapestRant
        res = []
        while h and len(res) < 5:
            p,s,m = heappop(h)
            if m not in self.shop2movies[s] and (p,s,m) not in res:
                res.append((p,s,m))
        for i in res:
            heappush(h, i)
        return [(s,m) for p,s,m in res]

sol = Solution()
result = [
    # sol.canBeIncreasing(nums = [2,3,1,2]),
    # sol.canBeIncreasing(nums = [1,2,10,5,7]),
    # sol.canBeIncreasing([105,924,32,968]),
    
    # sol.removeOccurrences(s = "daabcbaabcbc", part = "abc"),
    # sol.removeOccurrences(s = "axxxxyyyyb", part = "xy"),
    # sol.maxAlternatingSum(nums = [4,2,5,3]),
    # sol.maxAlternatingSum(nums = [6,2,1,2,4,5]),
    
#     sol.testClass("""["MovieRentingSystem", "search", "rent", "rent", "report", "drop", "search"]
# [[3, [[0, 1, 5], [0, 2, 6], [0, 3, 7], [1, 1, 4], [1, 2, 7], [2, 1, 5]]], [1], [0, 1], [1, 2], [], [1, 2], [2]]"""),
]
for r in result:
    print(r)
