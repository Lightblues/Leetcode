import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, reduce, partial # cache
cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
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
1998. 数组的最大公因数排序 #hard
    给定一个数组, 对于任意两个位置 i,j, 若他们存在公共因子 (`gcd(nums[i], nums[j]) > 1`) 则可进行交换. 问数组是否可以按照上述规则进行交换后, 变为递增数组.
    在一个并查集中的数字顺序可以任意调换.




题目: 0547, 0399
*   「力扣」第 547 题：[省份数量](https://leetcode-cn.com/problems/number-of-provinces)（中等）；
*   「力扣」第 684 题：[冗余连接](https://leetcode-cn.com/problems/redundant-connection)（中等）；
*   「力扣」第 1319 题：[连通网络的操作次数](https://leetcode-cn.com/problems/number-of-operations-to-make-network-connected)（中等）；
*   「力扣」第 1631 题：[最小体力消耗路径](https://leetcode-cn.com/problems/path-with-minimum-effort)（中等）；
*   「力扣」第 959 题：[由斜杠划分区域](https://leetcode-cn.com/problems/regions-cut-by-slashes)（中等）；
*   「力扣」第 1202 题：[交换字符串中的元素](https://leetcode-cn.com/problems/smallest-string-with-swaps)（中等）；
*   「力扣」第 947 题：[移除最多的同行或同列石头](https://leetcode-cn.com/problems/most-stones-removed-with-same-row-or-column)（中等）；
*   「力扣」第 721 题：[账户合并](https://leetcode-cn.com/problems/accounts-merge)（中等）；
*   「力扣」第 803 题：[打砖块](https://leetcode-cn.com/problems/bricks-falling-when-hit)（困难）；
*   「力扣」第 1579 题：[保证图可完全遍历](https://leetcode-cn.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable)（困难）;
*   「力扣」第 778 题：[水位上升的泳池中游泳](https://leetcode-cn.com/problems/swim-in-rising-water)（困难）
"""
class Solution:
    """ 1998. 数组的最大公因数排序 #hard
给定一个数组, 对于任意两个位置 i,j, 若他们存在公共因子 (`gcd(nums[i], nums[j]) > 1`) 则可进行交换. 问数组是否可以按照上述规则进行交换后, 变为递增数组.
约束: 数组长度 3e4, 数字大小 1e5
思路1: 分解 #质因子 的 #并查集
    结论: 对于有公共因子的数字之间连边, 可知, 在一个连通分量上, 经过交换操作可以得到任意的数字顺序. 例子:  `[10,5,9,3,15]` 两个因子 3,5 通过 15 连接, 这个数组可以得到任意顺序
    因此, 就是并查集的思路. 但是元素之间两两查询的复杂度不够. 因此, 我们引入 prime 数字构成的节点.
    这样, 对于一个数字num, 我们得到所有的质因子 factors, 将 num 连到任意质因子上, 然后将 factors[1:n-1] 都连到 factors[0] 上即可.
    判断: 最后, 将 nums, sorted(nums) 的每一位比较, 两元素相同则不需要交换; 否则, 查询 x,y 是否在同一集合中, 只有在同一集合中才能交换得到.
    下面预先计算的所有可能的质因子, 但实际上可以简化, 见 [here](https://leetcode.cn/problems/gcd-sort-of-an-array/solution/bing-cha-ji-fen-jie-zhi-yin-shu-by-xin-x-ylsz/)
"""
    def gcdSort(self, nums: List[int]) -> bool:
        sortedNums = sorted(nums)
        # 预计算所有的质数因子
        primes = [2]
        for i in range(3, sortedNums[-1]+1):
            flag = True
            limit = int(math.sqrt(i))
            for j in primes:
                if j>limit: break
                if i%j==0:
                    flag = False
                    break
            if flag: primes.append(i)
        
        def getFactors(x):
            """ 得到 x 的所有因子 """
            factors = []
            for i in primes:
                if x%i==0:
                    factors.append(i)
                    x //= i
                    while x%i==0:
                        x //= i
                if x==1: break
            return factors
        
        # 并查集
        n = len(set(nums))
        num2dix = {num:i for i, num in enumerate(set(nums))}
        prime2idx = {prime:i+n for i, prime in enumerate(primes)}
        fa = list(range(n + len(primes)))
        def find(x):
            path = []
            while fa[x] != x:
                path.append(x)
                x = fa[x]
            for i in path:
                fa[i] = x
            return x
        def merge(x, y):
            """ 将 x, y 合并到一个集合中; 令 x 是 y 的父节点 """
            fa[find(y)] = find(x)
            
        for num in nums:
            if num==1: continue
            factors = getFactors(num)
            # 将 num 合并到最小的因子上去
            merge(prime2idx[factors[0]], num2dix[num])
            # 将各个因子之间进行合并
            for i in range(1, len(factors)):
                # 按照merge的规则, 尽量让小的数字作为父节点
                merge(prime2idx[factors[0]], prime2idx[factors[i]])
        
        # 检查. 判断 idx 位置的数字能否从x变为y (也即在一个并查集中)
        for x,y in zip(nums, sortedNums):
            if x==y: continue
            if find(num2dix[x]) != find(num2dix[y]): return False
        return True

sol = Solution()
result = [
    
]
for r in result:
    print(r)
