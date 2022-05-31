from curses.ascii import SO
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
from functools import lru_cache, cache, reduce, partial
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

""" [单点更新, 区间查询, 就可以考虑线段树]
https://oi-wiki.org/ds/seg/

TODO: https://leetcode.cn/problems/count-of-range-sum/solution/by-ac_oier-b36o/

0327. 区间和的个数 #hard
    给定一个数组, 要求其所有的子区间中, 区间和在 [lower, upper] 范围内的数量

0729. 我的日程安排表 I #medium
    给定一组左开右闭的区间表示课程. 对于一个课程序列, 依次判断是否会与之前的产生冲突 (不冲突的就加入课程集合).
0731. 我的日程安排表 II
    相较于 0729, 这里的限制是三个课程不能同时进行, 也即重叠时间不能超过2.



"""
class Solution:
    def testClass(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
    """ 0327. 区间和的个数 #hard #题型 #线段树
给定一个数组, 要求其所有的子区间中, 区间和在 [lower, upper] 范围内的数量
限制: 数组长度 1e5, 元素大小 32bit
see [官答](https://leetcode.cn/problems/count-of-range-sum/solution/qu-jian-he-de-ge-shu-by-leetcode-solution/)
思路0: 归并排序
思路1: #线段树
    区间和问题, 考虑采用前缀和, preSum. 一个 [i,j] 区间和为 `preSum[j+1]-preSum[i]`
    我们需要遍历所有的区间. 为此, 每次仅考虑位置为j结尾的区间可以构成多少个符合条件的?
    因为区间和需要在 `[lower, upper]`, 则该对于j位置, 假设 `preSum[j+1]=a`, 则位置i的 **前缀和 preSum[i] 需要在 [a-upper, a-lower] 范围内**.
    求在一个范围内的数字有多少, 显然可以用 #线段树 来做.
    具体而言, 对于每一个位置的元素, 先按照上式统计满足条件的以j结尾的区间数量, 然后将 preSum[j+1] 加入线段树.
    另外, 本题的数字上限很大, 需要将其转为连续整数 (#离散化), 也即, 将线段树中所有出现过的数字 (包括需要查询的 left, right) 变为 0~n-1 的连续整数.
思路2: 动态增加节点的线段树
思路3: 树状数组
思路4: 平衡二叉搜索树

输入：nums = [-2,5,-1], lower = -2, upper = 2
输出：3
解释：存在三个区间：[0,0]、[2,2] 和 [0,2] ，对应的区间和分别是：-2 、-1 、2 。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/count-of-range-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        """ [官答](https://leetcode.cn/problems/count-of-range-sum/solution/qu-jian-he-de-ge-shu-by-leetcode-solution/) 
        改成了 Python版本, 下面的 SegTree_0 居然超时了, 重新实现了 SegTree 过"""
        # 利用哈希表将所有可能出现的整数，映射到连续的整数区间内
        preSum = list(accumulate(nums, initial=0)) 
        allNums = set(preSum)
        allNums = allNums.union(set(i-lower for i in allNums)).union(set(i-upper for i in allNums))
        allNums = sorted(list(allNums))
        kth = {j:i+1 for i,j in enumerate(allNums)}
        
        # t = SegTree(len(allNums) * 4)
        # t.build(1, 1, len(kth))
        # t.inc(1, kth[0])        # 将0映射后的值加入到线段树中 (因为假如单个数字符合要求, 也OK)
        # ans = 0
        # for s in preSum[1:]:
        #     left, right = kth[s-upper], kth[s-lower]
        #     ans += t.query(1, left, right)
        #     t.inc(1, kth[s])
        # return ans
        
        n = len(allNums)
        t = SegTree(n)      # 内部生成 4*n 的数组记录
        t.inc(1, 1, n, kth[0])
        ans = 0
        for s in preSum[1:]:
            left, right = kth[s-upper], kth[s-lower]
            ans += t.query(1, 1, n, left, right)
            t.inc(1,1,n, kth[s])
        return ans

class SegTree_0():
    """ 改写自 0327 题官答.
    这里新定义了一个 struct 包括了其所管辖的 l,r 位置, 实际上可以通过参数的形式传入, 这样可以提升性能, 参见 SegTree """
    class Node():
        def __init__(self) -> None:
            """ 线段树节点, 记录了 [l,r] 区间内的数字数量为 val """
            self.val = 0
            self.l = None
            self.r = None
    
    def __init__(self, n) -> None:
        self.t = [self.Node() for _ in range(n)]
    
    def build(self, o, l,r):
        """ 递归建树 """
        self.t[o].l = l
        self.t[o].r = r
        if l==r: return
        m = (l+r)//2
        self.build(2*o, l, m)
        self.build(2*o+1, m+1, r)
    
    def inc(self, o, i):
        """ 递归对于第i个元素 +1, o为当前访问的节点 """
        if self.t[o].l==self.t[o].r:
            self.t[o].val += 1
            return
        if i <= (self.t[o].l + self.t[o].r)//2:
            self.inc(2*o, i)
        else:
            self.inc(2*o+1, i)
        self.t[o].val = self.t[2*o].val + self.t[2*o+1].val
    
    def query(self, o, l,r):
        """ 查询 [l,r] 范围内的元素个数 """
        if l<=self.t[o].l and r>=self.t[o].r: return self.t[o].val
        m = (self.t[o].l+self.t[o].r)//2
        if r <= m: return self.query(2*o, l, r)
        if l >= m+1: return self.query(2*o+1, l, r)
        return self.query(2*o, l, m) + self.query(2*o+1, m+1, r)
    
    
class SegTree:
    """ 
    更为简洁的线段树实现
    调用的时候需要输入 o,l,r, 即当前的位置 o 的节点及其所管辖的区间 [l,r]. 一般而言, 对于一个总长度为 n的线段树而言, 调用形式都是 (1,1,n), 也即从根节点出发, 其所管辖的范围为 [1,n]
    from [灵神](https://leetcode.cn/problems/booking-concert-tickets-in-groups/solution/by-endlesscheng-okcu/)
    """
    def __init__(self, n) -> None:
        self.t = [0] * 4 * n
    def inc(self, o,l,r, i, val=1):
        """ 对于i位置元素加val """
        if l==r:
            self.t[o] += val
            return
        m = (l+r)>>1
        if m>=i: self.inc(2*o, l, m, i, val)
        else: self.inc(2*o+1, m+1, r, i, val)
        self.t[o] = self.t[2*o] + self.t[2*o+1]
        
    def query(self, o,l,r, left, right):
        """ 查询 [left, right] 区间元素个数
        注意, 在递归过程中不需要考虑修改查询区间 [left, right] """
        if l>=left and r<=right: return self.t[o]
        m = (l+r)>>1
        sum = 0
        if m>=left: sum += self.query(2*o, l, m, left, right)
        if m+1<=right: sum += self.query(2*o+1, m+1, r, left, right)
        return sum
    
""" 0729. 我的日程安排表 I #medium
给定一组左开右闭的区间表示课程. 对于一个课程序列, 依次判断是否会与之前的产生冲突 (不冲突的就加入课程集合).
思路1: 维护一个有序的列表, 二分判断当前课程是否会与之前的冲突.
    时间复杂度: 由于插入操作, 复杂度为 O(n^2).
    [官答](https://leetcode.cn/problems/my-calendar-i/solution/wo-de-ri-cheng-an-pai-biao-i-by-leetcode/) 解法1就是暴力 O(n^2).
    Python 可以用 SortedList, 在对数时间实现插入 (应该是平衡树?), 见思路2.
思路2: #平衡树
    官答还用了二叉树来存储时序关系的课程, 但最坏情况还是 O(n^2). 在JAVA中直接调用 `TreeMap `, 而Python手写一个平衡树超纲了.

"""
class MyCalendar:
    # 维护有序列表, 直接调包
    def __init__(self):
        from sortedcontainers import SortedList
        self.cal = SortedList()

    def book(self, start: int, end: int) -> bool:
        idx = self.cal.bisect_right((start, end))
        if idx>0 and self.cal[idx-1][1]>start: return False
        if idx<len(self.cal) and self.cal[idx][0]<end: return False
        self.cal.add((start, end))
        return True

""" 0731. 我的日程安排表 II
相较于 0729, 这里的限制是三个课程不能同时进行, 也即重叠时间不能超过2.
注意判断两个区间是否有交集的方法: 对于 [start, end] 和 [i,j] 两个区间, 它们存在交集的条件为 `start<j and end>i`.
思路1: 暴力法
    用两个数组分别存储已有的课程和重复的时间片段. 暴力遍历
    [here](https://leetcode.cn/problems/my-calendar-ii/solution/wo-de-ri-cheng-an-pai-biao-ii-by-leetcode/)
"""

class MyCalendarTwo:
    """ 思路1: 用两个数组分别存储已有的课程和重复的时间片段. 暴力遍历
    [here](https://leetcode.cn/problems/my-calendar-ii/solution/wo-de-ri-cheng-an-pai-biao-ii-by-leetcode/) """
    def __init__(self):
        # from sortedcontainers import SortedList
        self.cal = []
        self.dupCal = []

    def book(self, start: int, end: int) -> bool:
        # 检查是否有三重重复
        for i,j in self.dupCal:
            if start<j and end>i: return False
        # 检查是否与已有课程重复.
        for i,j in self.cal:
            if start<j and end>i: self.dupCal.append((max(start,i), min(end,j)))
        self.cal.append((start, end))
        return True


sol = Solution()
result = [
#     sol.testClass("""["MyCalendar", "book", "book", "book"]
# [[], [10, 20], [15, 25], [20, 30]]"""),
#     sol.testClass("""["MyCalendar","book","book","book","book","book","book","book","book","book","book"]
# [[],[48,50],[0,6],[6,13],[8,13],[15,23],[49,50],[45,50],[29,34],[3,12],[38,44]]"""),

    sol.countRangeSum(nums = [-2,5,-1], lower = -2, upper = 2),
    sol.countRangeSum([-3,1,2,-2,2,-1],-3,-1),
]
for r in result:
    print(r)
