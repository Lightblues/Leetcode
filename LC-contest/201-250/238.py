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
https://leetcode.cn/contest/weekly-contest-238
@2022 """
class Solution:
    """ 1837. K 进制表示下的各位数字总和 """
    def sumBase(self, n: int, k: int) -> int:
        ans = 0
        while n:
            n, a = divmod(n,k)
            ans += a
        return ans
    
    """ 1838. 最高频元素的频数 #medium #题型
给定一个数组, 每次操作可以给其中一个数字+1, 在操作数k的限制下, 要求最后的数组中, 相同大小的数量最大.
限制: 数组长度 1e5, 数字大小 1e5
思路1: 先对于数组排序, 计算 #前缀和 之后 #二分
    先对于数组排序, 这样, 我们需要填充更低的「阶梯」来得到更高的位置. 考虑对于每个位置可以往前前中多少个阶梯.
    对于每一个idx, 我们检查在操作次数k的限制下, 最多可以向前填充多少个数字 (排序之后的数组). 为了快速计算是否可行, 通过前缀和来加速. 利用二分搜索来在 O(log n) 时间内得到结果.
    复杂度: O(n logn)
    图示见 [here](https://leetcode.cn/problems/frequency-of-the-most-frequent-element/solution/1838-zui-gao-pin-yuan-su-de-pin-shu-shua-ub57/)
思路2: 其实差不错, 只不过上面的二分可以替换为 #双指针
    see [官答](https://leetcode.cn/problems/frequency-of-the-most-frequent-element/solution/zui-gao-pin-yuan-su-de-pin-shu-by-leetco-q5g9/)
"""
    def maxFrequency(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # sort
        nums.sort()
        
        acc = list(accumulate(nums, initial=0))
        def bisect(idx) -> int:
            ans = 0
            l,r = 0,idx
            while l<=r:
                # test
                mid = (l+r)//2
                if nums[idx]*(idx-mid+1) - (acc[idx+1]-acc[mid]) <= k:
                    ans = mid
                    r = mid-1
                else:
                    l = mid+1
            return idx-ans+1
        
        ans = 0
        for idx in range(n):
            ans = max(ans, bisect(idx))
        return ans
    def maxFrequency(self, nums: List[int], k: int) -> int:
        # 思路2
        nums.sort()
        n = len(nums)
        l = 0
        total = 0
        res = 1
        for r in range(1, n):
            total += (nums[r] - nums[r - 1]) * (r - l)
            while total > k:
                total -= nums[r] - nums[l]
                l += 1
            res = max(res, r - l + 1)
        return res

    """ 1839. 所有元音按顺序排布的最长子字符串 #medium
给定一个仅包含元音字母的字符串, 在所有的子字符串 (连续) 中, 找到符合要求的的最长长度. 要求: 1) 按照顺序排列 (aeiou); 2) 五个元音都包含.
思路1: #双指针 模拟
    在遍历l边界的过程中, 判断是否符合条件, 用一个r指针来记录满足条件的最左边 (必然指向第一个元音a).
思路2: #状态机
    将五个元音看成是一些状态, 其中a是起始状态u是目标状态, 再用x表示非法状态. 定义出合法的转移; 并在该过程中维护当前长度.
    见 [官答](https://leetcode.cn/problems/longest-substring-of-all-vowels-in-order/solution/suo-you-yuan-yin-an-shun-xu-pai-bu-de-zu-9wqg/)
"""
    def longestBeautifulSubstring(self, word: str) -> int:
        m = dict(zip('aeiou', range(5)))
        word = [m[ch] for ch in word]

        ans = 0
        l = -1; isIn = False
        for i,ch in enumerate(word):
            if not isIn:
                if ch == 0:
                    l = i
                    isIn = True
            else:
                if ch==word[i-1] or ch==word[i-1]+1:    # 此时必然 i>0
                    if ch==4: ans = max(ans, i-l+1)
                else:
                    # 注意, 若该字符为 a, 可以从头开始计算
                    if ch==0:
                        l = i
                    else: isIn = False
        return ans

    TRANSIT = {
        ("a", "e"), ("e", "i"), ("i", "o"), ("o", "u"),
        ("a", "a"), ("e", "e"), ("i", "i"), ("o", "o"), ("u", "u"),
        ("x", "a"), ("e", "a"), ("i", "a"), ("o", "a"), ("u", "a"),
    }
    def longestBeautifulSubstring(self, word: str) -> int:
        # 思路2: 状态机
        cur, ans = 0, 0
        status = "x"    # x 表示非法状态
        
        for ch in word:
            if (status, ch) in Solution.TRANSIT:
                # 从其他状态转移到 a, 需要重新计数
                if status != "a" and ch == "a":
                    cur = 1
                # 否则, 长度 +1
                else:
                    cur = cur + 1
                status = ch
            else:
                # 非法转移, 重置
                cur = 0
                status = "x"
            if status == "u":
                # u 是目标状态, 记录最长长度
                ans = max(ans, cur)

        return ans

    """ 1840. 最高建筑高度 #hard
给定一个街道, 建筑高度有限制: 相邻建筑之间的高度差最多为1. 现在给定一组限制的情况下, 问最高可以有多少.
限制: 街道长度 1e9; 限制数量 1e5
思路1: 对于限制排序之后, 两两处理可能达到的最大高度.
    若相邻两个限制的高度分别为 a,b (并假设 a<b), 1) 若距离d足够的情况下, 先上升在下降, 则最大高度h需要满足 `d >= 2(h-b)+(b-a)`, 也即 `h <= 1/2 * (h+b+a)`; 2) 若d仅支持上升 (也即 d=b-a), 则最大高度为 b.
    补丁: 
        上述的问题在于, 有些限制是无法达到的; **因为若前面升的太高, 后面无法下降到限制高度**. 考虑在遍历过程中需要更新上一个位置可以达到的最大高度, 但还是不对.
        参考官答, 在遍历之前, 先 **从左往右从右往左** 对于高度限制进行递推更新: 通过预先的计算, 使得所有的高度限制都是可达的.
    总结: 关键在于通过两个方向的遍历, 来计算每个限制点的最大高度.
    见 [官答](https://leetcode.cn/problems/maximum-building-height/solution/zui-gao-jian-zhu-gao-du-by-leetcode-solu-axbb/)
"""
    def maxBuilding(self, n: int, restrictions: List[List[int]]) -> int:
        # 思路0 , 错的
        restrictions.append([1, 0])
        restrictions.sort()
        ans = 0
        for i in range(len(restrictions)-1):
            a, b = sorted((restrictions[i][1], restrictions[i+1][1]))
            ans = max(ans, (a+b+restrictions[i][0])//2, b)
        ans = max(ans, restrictions[-1][1] + n-restrictions[-1][0])
        return ans
    def maxBuilding(self, n: int, restrictions: List[List[int]]) -> int:
        restrictions.append([1,0])
        restrictions.sort()
        l = len(restrictions)
        for i in range(1, l):
            restrictions[i][1] = min(restrictions[i][1], restrictions[i-1][1] + restrictions[i][0]-restrictions[i-1][0])
        for i in range(l-2, -1, -1):
            restrictions[i][1] = min(restrictions[i][1], restrictions[i+1][1] + restrictions[i+1][0]-restrictions[i][0])
        # lastIdx = 1; lastH = 0
        ans = 0
        for i in range(1, l):
            a,b = sorted((restrictions[i-1][1], restrictions[i][1]))
            ans = max(ans, (a+b+restrictions[i][0]-restrictions[i-1][0])//2, b)
            # lastIdx = idx; lastH = maxH
        # return max(ans, lastH + n-lastIdx)
        return max(ans, restrictions[-1][1] + n-restrictions[-1][0])

sol = Solution()
result = [
    # sol.sumBase(n = 34, k = 6),
    # sol.maxFrequency(nums = [1,2,4], k = 5),
    # sol.maxFrequency(nums = [1,4,8,13], k = 5),
    # sol.maxFrequency(nums = [3,9,6], k = 2),
    # sol.longestBeautifulSubstring("aeiaaioaaaaeiiiiouuuooaauuaeiu"),
    # sol.longestBeautifulSubstring("aeeeiiiioooauuuaeiou"),
    # sol.longestBeautifulSubstring("a"),
    
    sol.maxBuilding(n = 10, restrictions = [[5,3],[2,5],[7,4],[10,3]]),
    sol.maxBuilding(n = 6, restrictions = []),
]
for r in result:
    print(r)
