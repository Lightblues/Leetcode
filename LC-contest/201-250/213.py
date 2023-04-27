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
from itertools import chain, product, permutations, combinations, combinations_with_replacement, accumulate
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
https://leetcode.cn/contest/weekly-contest-213
@2022 """
class Solution:
    """ 1640. 能否连接形成数组 #easy 
能否将一个数组列表通过一定的顺序拼接为另一个数组. 已知数组中元素各不相同 """
    def canFormArray(self, arr: List[int], pieces: List[List[int]]) -> bool:
        if len(arr) != sum(map(len, pieces)): return False      # 长度相同
        # if len(set(chain(*pieces))) != len(arr): return False # 输入已经保障了
        if set(chain(*pieces)) != set(arr): return False        # 元素相同
        idx = 0; 
        i2piece = {p[0]:p for p in pieces}
        while idx<len(arr):
            if arr[idx] not in i2piece: return False
            for i,a in enumerate(i2piece[arr[idx]]):
                if arr[idx] != a: return False
                idx += 1
        return True
    
    """ 1641. 统计字典序元音字符串的数目 #medium
计算长度为n并且仅由aeiou组成并且其中字符出现顺序按照字典序排列的字符串的数目.
提示: 从5个元音字母只选择k个字母, 按照特定顺序排列的方式有 `comb(5, k)` 种. 这k个字符组成长度为n的字符串, 显然, 第一个字母是固定的, 其他的k-1的字符第一次出现的位置可以在剩余slot上选择, 方式有 `comb(n-1, k-1)` 种.
"""
    def countVowelStrings(self, n: int) -> int:
        ans = 0
        for i in range(1, min(5, n)+1):
            ans += math.comb(5, i) * math.comb(n-1, i-1)
        return ans
    
    """ 1642. 可以到达的最远建筑 #medium
有一排房子, 你要利用一定数量的「砖块」和「梯子」到达尽可能最远. 若 `h[i+1]<=h[i]` 可以直接过. 否则, 可以选择使用一架梯子或者 `h[i+1]-h[i]` 块砖块.
思路: #贪心 将l个梯子用在高度差最大的位置上. 为此, 遍历过程中, 优先用梯子, 用最小堆保存. 然后遇到更大的高度差时, 将堆中最小的换成砖块.
"""
    def furthestBuilding(self, heights: List[int], bricks: int, ladders: int) -> int:
        n = len(heights)
        heap = []
        for i in range(1, n):
            if heights[i]<=heights[i-1]: continue
            d = heights[i]-heights[i-1]
            # 还有梯子, 优先用
            if ladders > len(heap):
                heapq.heappush(heap, d)
                continue
            # 将之前最小的梯子换成砖块
            if ladders and heap and heap[0]<d:
                d = heapq.heappushpop(heap, d)
            # 不行的话, 无法到达i
            if d>bricks: return i-1
            bricks -= d
        return n-1

    """ 1643. 第 K 条最小指令 #hard
需要从(0,0)到达(row, column), 最短路径可以由长度为 row+column 的 `HV` 指令构成 (向右/向下). 问所有指令中字典序第k小的指令.
问题等价于, 给定一定数量的0/1, 问他们构成的长为n的序列中第k小的.
限制: n<=15
思路0: #组合 计数.
    考虑最高位在某一位置时, 可以有多少种序列. 例如, 有2个1的情况下, 从小到大依次为 11; 101,110; 1001,1010,1100;... 可见, 对于长度为l的包含x个1的序列, 一共有 `comb(l-1, x-1)` 种.
    因此, 递归求解 `f(x, k)` 来求 **包括x个1的第k小元素中, 序列的最高位**. 为此, 用一个acc记录用长为 l=1,2,3... 的序列可构成的包含x个1的序列的个数, 当首次出现 `acc >= k` 时, 说明第k大的元素长度为l, 然后递归 `f(x-1, k-acc)`. 边界: x=0.
思路1: 优先确定高位 + 组合计数
    上面的解法比较直观, 但不太「优雅」. 实际上, 我们可以直接从最高位往下填: 对于idx位, 我们要求包含x个1的第k小的元素, 假设填0则剩余元素最多有 `o = comb(x-1,k-1)` 种可能. 因此我们每次比较 o,k 的大小关系即可: 若 `o>=k` 则在idx位填0否则填1.
    from [zero](https://leetcode.cn/problems/kth-smallest-instructions/solution/di-k-tiao-zui-xiao-zhi-ling-by-zerotrac2/)
    复杂度: `O((h+v) * h)` 因为序列长度为 `h+v`, 而计算 `comb(x,h)` 的复杂度 h. 我们可以通过递推式 `c[n][k]=c[n-1][k-1]+c[n-1][k]` 求解组合数.
关联: 0060. 第k个排列
"""
    def kthSmallestPath(self, destination: List[int], k: int) -> str:
        # 思路0
        row, col = destination
        n = row+col
        ans = [0] * n
        def f(x, k):
            # 包括x个1的第k小元素
            if x==0: return 0
            acc = 0
            for l in range(1, n+1):
                acc += math.comb(l-1, x-1)
                if acc >= k: break
            ans[-l] = 1
            f(x-1, k-(acc-math.comb(l-1, x-1)))
            return l
        f(row, k)
        ans = ['H' if i==0 else 'V' for i in ans]
        return "".join(ans)
    
sol = Solution()
result = [
    # sol.canFormArray(arr = [91,4,64,78], pieces = [[78],[4,64],[91]]),
    # sol.canFormArray(arr = [49,18,16], pieces = [[16,18,49]]),
    # sol.countVowelStrings(2),
    # sol.countVowelStrings(33),
    # sol.furthestBuilding(heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1),
    # sol.furthestBuilding(heights = [14,3,19,3], bricks = 17, ladders = 0),
    sol.kthSmallestPath(destination = [2,3], k = 1),
    sol.kthSmallestPath(destination = [2,3], k = 2),
    sol.kthSmallestPath(destination = [2,3], k = 3),
    sol.kthSmallestPath([15,15], 155117520),
]
for r in result:
    print(r)
