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
https://leetcode.cn/contest/weekly-contest-239
@2022 """
class Solution:
    """ 1848. 到目标元素的最小距离 """
    def getMinDistance(self, nums: List[int], target: int, start: int) -> int:
        # ans = len(nums)
        # for i, num in enumerate(nums):
        #     if num
        return min(abs(i-start) for i, num in enumerate(nums) if num == target)
    
    """ 1849. 将字符串拆分为递减的连续值 #medium
给定一个字符串, 问能否将其拆分成递减, 并且相邻元素正好 -1 的部分. 例子: "0090089" 可以拆成 ["0090", "089"]
限制: 长度 20
思路1: 暴力 #DFS
    函数签名 `dfs(idx=0, last=None)`
思路2: 实际上仅需要枚举第一个数字, 然后遍历验证是否符合要求即可
    复杂度: O(n^2)
"""
    def splitString(self, s: str) -> bool:
        n = len(s)
        def dfs(idx=0, last=None) -> bool:
            if idx==n: return True
            if last is None:
                for end in range(idx, n-1): # 注意必须要拆分成两个及以上!
                    if dfs(end+1, int(s[idx:end+1])): return True
                return False
            for end in range(idx, n):
                if int(s[idx:end+1]) >= last: break
                elif int(s[idx:end+1]) == last-1:
                    if dfs(end+1, last-1): return True
            return False
        return dfs()
    
    
    def splitString(self, s: str) -> bool:
        # https://leetcode.cn/problems/splitting-a-string-into-descending-consecutive-values/solution/jiang-zi-fu-chuan-chai-fen-wei-di-jian-d-ggl2/
        n = len(s)
        start = 0
        # 枚举第一个子字符串对应的初始值
        # 第一个子字符串不能包含整个字符串
        for i in range(n - 1):
            start = 10 * start + int(s[i])
            # 循环验证当前的初始值是否符合要求
            pval = start
            cval = 0
            cidx = i + 1
            for j in range(i + 1, n):
                if pval == 1:
                    # 如果上一个值为 1，那么剩余字符串对应的数值只能为 0
                    if all(s[k] == '0' for k in range(cidx, n)):
                        return True
                    else:
                        break
                cval = 10 * cval + int(s[j])
                if cval > pval - 1:
                    # 不符合要求，提前结束
                    break
                elif cval == pval - 1:
                    if j + 1 == n:
                        # 已经遍历到末尾
                        return True
                    pval = cval
                    cval = 0
                    cidx = j + 1     
        return False

    """ 1850. 邻位交换的最小次数 #medium #题型 #逆序对
给定一个数字排列(数字可重复), 想要得到比它大的第k个排列, 问最少需要 **相邻交换** 多少次.
限制: 长度 1e3
思路1: 先用 nextPermutation 得到目标结果, 然后 #贪心 计算需要交换多少次.
    nextPermutation 参见「0031. 下一个排列」
    如何将 num0 通过相邻元素交换变为 numk? 下面介绍一种贪心的计算方法:
        依次遍历初始序列num0的每一个位置i, 若 `num0[i]==numk[i]`, 则不需要交换; 否则, 从左往右找到第一个 num0[j]=numk[i] 的位置, 将其移动到i (发生 j-i 次交换)
    我们通过 #逆序对 来进行考察. 将目标的结果重新标号为 `1,2,...,n` (并且可以假设所有数字不同) 这样, 目标序列的逆序数就为 0.
        考虑交换 i,i+1: 若 `nums[i]>nums[i+1]` 则逆序数 -1, 若 `nums[i]<nums[i+1]` 则逆序数 +1
        每次操作最多使得逆序数-1, 而我们上述算法的每次操作都是满足逆序数减少的.
    see [官答](https://leetcode.cn/problems/minimum-adjacent-swaps-to-reach-the-kth-smallest-number/solution/lin-wei-jiao-huan-de-zui-xiao-ci-shu-by-xerp9/)
"""
    def nextPermutation(self, nums: List[int]) -> None:
        # 0031. 下一个排列
        # 按照wiki的算法: https://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order
        n = len(nums)
        k = n-2
        # 从右往左找到第一个 nums[k]<nums[k+1] 的位置. 注意 nums[k+1...n-1] 是递减的.
        while k>=0 and nums[k]>=nums[k+1]:
            k -= 1
        if k>=0:
            # 若 k==-1, 说明已经是最大排列
            # 从k出发找到最后一个 nums[k] < nums[l] 的位置
            l = k+1
            while l<n-1 and nums[l+1]>nums[k]:
                l += 1
            # 交换. 注意, 此时 nums[k...l...n-1] 是递减的.
            nums[k], nums[l] = nums[l], nums[k]
        # 找到了一个次大的元素放到位置k, 然后 nums[k+1...n-1] 需要是最小排列: 反转即可
        l,r = k+1, n-1
        while l<r:
            nums[l], nums[r] = nums[r], nums[l]
            l,r = l+1, r-1
    def getMinSwaps(self, num: str, k: int) -> int:
        num = list(map(int, num))
        numk = num[:]
        for _ in range(k):
            self.nextPermutation(numk)
        
        # 贪心将 num 变为 numk
        n = len(num)
        ans = 0
        for i in range(n):
            # 找到 num
            j = i
            while num[j] != numk[i]:
                j += 1
            if j>i:
                ans += j-i
                num[i:j+1] = [numk[i]] + num[i:j]
        return ans
    
    
    """ 1851. 包含每个查询的最小区间 #hard
有一组区间 [left, right], 然后对于每一个查询位置idx, 要求返回包含idx的区间中的长度最小值.
限制: 区间数量n, 查询数量q 1e5; 数值 1e7.
思路1: #离线 算法. 将区间和查询点都看成一系列的 #事件, 然后排序
    对于区间左右端点和查询点, 看成是三类事件. 我们对于这些事件根据事件进行排序
    然后在遍历过程中, 我们用一个数据结构来 **动态维护当前范围内的合法区间的长度**: 1) 遇到左端点就插入该区间长度; 2) 遇到查询点, 就是该DS中返回最小值; 3) 遇到右端点就从DS中删除该区间的长度. 由此可见, 支持上述插入、删除、查询最小值的数据结构是 #有序集合, 可以调用 #SortedList.
    细节: 时间点相同时如何排序? 由于区间是必区间, 显然按照左、查询、右的顺序来处理. 
    另外, 官答中定义了一个Event类表示事件, 当然自己实现的时候没有必要.
    see [官答](https://leetcode.cn/problems/minimum-interval-to-include-each-query/solution/bao-han-mei-ge-cha-xun-de-zui-xiao-qu-ji-e21j/)
思路2: 按区间长度排序+ #离线 询问+ #并查集 #TODO
    以区间为主体，回答在该区间内的询问。
    首先, 对于区间长度和查询的时间进行排序. 然后, 一次回复每个区间内的查询. 那么, 如何避免重复呢?
    答案是 **采用并查集来维护**. 具体而言, 对于已经回答过的查询i, 我们将其指向下一个查询i+1. 这样, 当我们回复 [l,r] 这一区间内的查询的时候, 每次都更新 `i = find(i + 1)` 即可 (我们回复了位置i的查询之后, 查找下一个可能还没有回复的位置)
    复杂度: 排序 `O(n log n + q log(q))`; 在遍历区间的过程中, 每次需要找到开始位置l, 采用 #二分 查找的复杂度`O(log q)`, 这样算下来的复杂度为 `O(n*log(q))`. 注意这里没有算遍历 [l,r] 的过程中, 因为从整体来看, 每个节点被访问一次后就会往后指, 因此整体复杂度为 O(q).
    from [灵神](https://leetcode.cn/problems/minimum-interval-to-include-each-query/solution/an-qu-jian-chang-du-pai-xu-chi-xian-bing-6jzs/)
"""
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        n, m = len(intervals), len(queries)

        events = list()
        for i, query in enumerate(queries):
            # 询问事件
            events.append(Event(1, query, i))

        for i, (x, y) in enumerate(intervals):
            # 左端点事件
            events.append(Event(0, x, y))
            # 右端点事件
            events.append(Event(2, y, x))

        events.sort()

        ans = [-1] * m
        # 存储区间长度的有序集合，支持重复元素
        # 需要导入 sortedcontainers 库
        seg = sortedcontainers.SortedList()
        for event in events:
            if event.op == 0:
                # 左端点事件，将区间长度加入有序集合
                seg.add(event.para - event.pos + 1)
            elif event.op == 1:
                # 询问事件，答案为有序集合中的最小值
                if seg:
                    ans[event.para] = seg[0]
            else:
                # 右端点事件，将区间长度从有序集合中移除
                seg.remove(event.pos - event.para + 1)
            
        return ans

class Event:
    """
    op: 事件的类型，0 表示左端点，1 表示询问，2 表示右端点
    pos: 事件的位置
    para: 事件的额外参数
        如果是 0 左端点事件，那么 para 记录右端点的位置
        如果是 1 询问事件，那么 para 记录它是第几个询问，以便于返回答案数组
        如果是 2 右端点事件，那么 para 记录左端点的位置
    """
    def __init__(self, op: int, pos: int, para: int):
        self.op = op
        self.pos = pos
        self.para = para

    """
    自定义比较函数，按照事件的位置升序排序
    如果位置相同，按照左端点、询问、右端点的顺序排序
    """
    def __lt__(self, other: "Event") -> bool:
        return self.pos < other.pos or (self.pos == other.pos and self.op < other.op)


sol = Solution()
result = [
    # sol.splitString(s = "1234"),
    # sol.splitString(s = "050043"),
    
    # sol.getMinSwaps(num = "5489355142", k = 4),
    # sol.getMinSwaps(num = "11112", k = 4),
    
    sol.minInterval(intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]),
    sol.minInterval(intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]),
]
for r in result:
    print(r)
