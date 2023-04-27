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
https://leetcode.cn/contest/weekly-contest-223
@2022 """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    """ 1720. 解码异或后的数组 """
    def decode(self, encoded: List[int], first: int) -> List[int]:
        ans = [first]
        for e in encoded:
            ans.append(ans[-1]^e)
        return ans
    
    """ 1721. 交换链表中的节点 #链表 要求交换第k个倒数第k个元素 """
    def swapNodes(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        len = 0; h = head
        while h:
            h = h.next; len += 1
        h = head; idx = 1
        l,r = None,None
        while h:
            if idx==k:
                l = h
            if idx==len-k+1:
                r = h
            h = h.next; idx += 1
        l.val, r.val = r.val, l.val
        return head
    
    """ 1722. 执行交换操作后的最小汉明距离 #medium 数组的idx之间构成一组和可交换关系, 问原数组经过交换后与目标数组的最小汉明距离. 直接用 #并查集 即可 """
    def minimumHammingDistance(self, source: List[int], target: List[int], allowedSwaps: List[List[int]]) -> int:
        n = len(source)
        fa = list(range(n))
        def find(x):
            if fa[x]!=x:
                fa[x] = find(fa[x])
            return fa[x]
        def union(x,y):
            fx,fy = find(x),find(y)
            if fx!=fy:
                if x>y: fx,fy = fy,fx
                fa[fx] = fy
        for a,b in allowedSwaps:
            union(a,b)
        u2idx = defaultdict(list)
        for i in range(n):
            u2idx[find(i)].append(i)
        acc = 0
        for idxs in u2idx.values():
            ls = Counter(source[i] for i in idxs)
            lt = Counter(target[i] for i in idxs)
            acc += sum(min(ls[k], lt[k]) for k in ls.keys())
        return n - acc
    
    """ 1723. 完成所有工作的最短时间 #hard #题型 #Python #优化
给定一组数组, 要求分成k组, 使得组内的数字之和的最大值最小化
限制: k, 数组长度 <=12
思路1: 同「5289. 公平分发饼干」, 但时间要求更为苛刻. 采用 #子集遍历 #状态压缩 #DP
    `f[i][mask]` 表示给前i个工人分配, 并且已分配的工作是mask情况下的最优值.
    递推: `f[i+1][mask] = min{ max{sum(sub), f[i][mask\sub]} }` 也即经典的子集遍历问题 (可以通过 `sub = (sub-1)&mask` 来实现).
    复杂度: 子集遍历的复杂度为 O(3^n), 因此总复杂度为 O(n 3^n)
    思路是这样的, 但此题卡时间非常紧, 下面来说 [灵神](https://leetcode.cn/problems/find-minimum-time-to-finish-all-jobs/solution/by-endlesscheng-d2oa/) 的优化
优化: 1) 首先, 相较于 `sub = (sub-1)&mask` 的子集遍历方式, 在全局预计算好每一个mask的所有子集形式; 2) 把 `min` 和 `max` 拆开，改为手写，避免额外的函数调用开销
思路2: #二分 查找 + #回溯 + #剪枝
    对于一个数字, 通过DFS来判定是否可行. 但暴力回溯的复杂度高达 O(k^n), 因此采取了一系列的剪枝策略.
        优先分配工作量大的工作. 因为「更容易」找到解.
        顺序给工人分配. 因为工人之间没有差异.
        在遍历过程中, 假如任务i分配给j恰好使得j的工作量达到limit (没有浪费), 若递归函数还返回了false, 则可以直接返回false不必继续遍历.
    参见 [官答](https://leetcode.cn/problems/find-minimum-time-to-finish-all-jobs/solution/wan-cheng-suo-you-gong-zuo-de-zui-duan-s-hrhu/)
"""

    def minimumTimeRequired(self, jobs: List[int], k: int) -> int:
        # 1) 计算初始的所有 mask 的值
        # 思路1: 遍历 1...m, 每个数字减去最末尾的1来进行递归
        m = 1 << len(jobs)
        f0 = [0] * (m)
        for mask in range(1, m):
            lastBit = mask&-mask
            f0[mask] = f0[mask-lastBit] + jobs[lastBit.bit_length()-1]
        # 思路2: 遍历bit位, 根据前面计算过的位数更低的进行递归
        # f0 = [0] * m
        # for i, v in enumerate(jobs):
        #     bit = 1 << i
        #     for j in range(bit):
        #         f0[bit | j] = f0[j] + v

        # f = f0.copy()
        f = f0[:]       # 切片语法好像要比copy()快一点
        # 2) 迭代 k-1 次
        for _ in range(k-1):
            for mask in range(m-1, -1, -1):
                # 思路1: 利用经典的 `sub = (sub-1)&mask` 方式遍历子集
                # sub = mask
                # while sub:
                #     # 把 `min` 和 `max` 拆开也不够.
                #     # f[mask] = min(f[mask], max(f0[sub], f[mask^sub]))
                #     v = f[mask^sub]
                #     if f0[sub] > v: v = f0[sub]
                #     if f[mask] > v: f[mask] = v
                #     sub = (sub-1)&mask
                
                # 思路2: 利于 全局 预计算好的所有子集
                for sub in subsets[mask]:
                    # 把 `min` 和 `max` 拆开，改为手写，避免额外的函数调用开销
                    # f[mask] = min(f[mask], max(f0[sub], f[mask^sub]))
                    v = f[mask^sub]
                    if f0[sub] > v: v = f0[sub]
                    if v<f[mask]: f[mask] = v
        return f[-1]

subsets = [[] for _ in range(1 << 12)]
for i in range(1 << 12):
    s = i
    while s:
        subsets[i].append(s)
        s = (s - 1) & i


sol = Solution()
result = [
    sol.minimumTimeRequired(jobs = [3,2,3], k = 3),
    sol.minimumTimeRequired(jobs = [1,2,4,7,8], k = 2),
    sol.minimumTimeRequired([20010,20006,20014,20004,20008,20006,20005,20012,19999,20014,20003,20012],8)
]
for r in result:
    print(r)
