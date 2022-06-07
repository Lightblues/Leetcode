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

""" 
https://leetcode.cn/contest/weekly-contest-253
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1961. 检查字符串是否为数组前缀 """
    def isPrefixString(self, s: str, words: List[str]) -> bool:
        l = len(s)
        idx = 0
        for i, w in enumerate(words):
            if idx + len(w) > l: return False
            if s[idx: idx+len(w)] != w: return False
            idx += len(w)
            if idx == l: return True
        if idx==l: return True
        return False
    
    """ 1962. 移除石子使总数最小 """
    def minStoneSum(self, piles: List[int], k: int) -> int:
        piles = [-i for i in piles]
        heapq.heapify(piles)
        for i in range(k):
            mm = heapq.heappop(piles)
            heapq.heappush(piles, -(-mm - (-mm//2)))
        return -sum(piles)
    
    """ 1963. 使字符串平衡的最小交换次数 #medium #括号 #题型
对于一个长度为2n的左右括号序列, 左右数量相等; 问最少进行多少次i,j位置元素交换, 使左右括号序列平衡.
思路1: #贪心
    [灵神](https://leetcode.cn/problems/minimum-number-of-swaps-to-make-the-string-balanced/solution/go-tan-xin-by-endlesscheng-7h9n/) 的思路太清晰了!
    简言之, 每一次遇到左括号不够的情况, 我们都需要尽量靠右 (贪心) 拿一个左括号和当前右括号进行交换
    但实际上 **我们不需要真正进行这次交换**, 因为我们并不关心拿到的左括号的位置 —— 它不会影响我们的结果
    具体到代码上, 我们用count统计剩余未匹配的左括号数量. 当遇到右括号并且count==0时, 另count, ans均+1.
思路2: 观察 + #归纳
    比较数学/玄学, 见 [官答](https://leetcode.cn/problems/minimum-number-of-swaps-to-make-the-string-balanced/solution/shi-zi-fu-chuan-ping-heng-de-zui-xiao-ji-f7ye/)
    
"""
    def minSwaps(self, s: str) -> int:
        """ [here](https://leetcode.cn/problems/minimum-number-of-swaps-to-make-the-string-balanced/solution/go-tan-xin-by-endlesscheng-7h9n/) """
        count = 0
        ans = 0
        for ch in s:
            if ch == '[':
                count += 1
            else:
                if count==0:
                    ans += 1
                    count += 1
                else: count -= 1
        return ans
            
        
    """ 1964. 找出到每个位置为止最长的有效障碍赛跑路线 #hard #DP
问题定义: 给定一个序列, 对于其中的每一个值, 计算以其结尾的递增序列的最大长度
思路1: #线段树
    我们用一个哈希表记录num结尾的递增序列的最大长度
    这样, 对于每一个元素, 我们需要查询「小于等于当前元素的数字中, 长度最大的那一个」. 因此可以用线段树来解决
思路2: #DP
    基本和 0300 「最长递增子序列」完全一致.
    核心是: dp[i] 记录长度为 i+1 的序列中, 结尾元素的最小值
"""
    def longestObstacleCourseAtEachPosition(self, obstacles: List[int]) -> List[int]:
        # 注意不能简单用单调栈: 例如 `[5,1,5,5,1,3,4,5,1,4]` 的最后一个值应该是 5 ([1,1,3,4,4]), 而单调栈因为要保证倒数第二个1, 会得到 4
        # n = len(obstacles)
        # s = []
        # ans = [0] * n
        # for i,height in enumerate(obstacles):
        #     while s and s[-1] > height:
        #         s.pop()
        #     s.append(height)
        #     ans[i] = len(s)
        # return ans
        
        n = len(obstacles)
        # 离散化
        nums = list(set(obstacles))
        nums.sort()
        num2idx = {v:i+1 for i,v in enumerate(nums)}
        obstacles = [num2idx[v] for v in obstacles]
        
        """ 定义线段树, 注意长度为所有数字(离散化之后)的数量 *4
        这里的 seg 为统计每个数字结尾的递增序列的最大长度的哈希表
        segMax 为统计每个数字结尾的递增序列的最大长度的线段树 """
        ll = len(num2idx)
        seg = defaultdict(int)
        segMax = [0] * 4*ll
        def update(idx, val, o=1, l=1,r=ll):
            if l==r:
                seg[idx] = max(seg[idx], val)
                segMax[o] = seg[idx]
                return
            m = (l+r)//2
            if m >= idx: update(idx, val, 2*o, l, m)
            else: update(idx, val, 2*o+1, m+1, r)
            # seg[o] = seg[2*o] + seg[2*o+1]
            segMax[o] = max(segMax[2*o], segMax[2*o+1])
        def query(L, R, o=1, l=1, r=ll):
            # 查询区间 [L, R] 的最大值
            if L <= l and r <= R: return segMax[o]
            # from Coplit 居然如此简洁
            if R < l or r < L: return 0
            return max(query(L, R, 2*o, l, (l+r)//2), query(L, R, 2*o+1, (l+r)//2+1, r))
            m = (l+r)//2
            ans = 0
            if m>=L: ans = max(ans, query(L, R, 2*o, l, m))
            if m+1<=R: ans = max(ans, query(L, R, 2*o+1, m+1, r))
            return ans
        
        ans = [0] * n
        for i,height in enumerate(obstacles):
            # 注意这里的查询更新逻辑: 每次查询height一下的最长递增序列; 然后+1, 并进行更新
            hisHeight = query(1, height)
            ans[i] = hisHeight + 1
            update(height, hisHeight+1)
        return ans

    def longestObstacleCourseAtEachPosition(self, obstacles: List[int]) -> List[int]:
        # 果然被线段树祸害了……
        # 直接套「序列最长递增序列」的思路 见 0300 题
        dp = []
        ans = []
        for i,height in enumerate(obstacles):
            if (not dp) or dp[-1]<=height:
                dp.append(height)
                ans.append(len(dp))
            else:
                idx = bisect.bisect_right(dp, height)
                ans.append(idx+1)
                dp[idx] = height
        return ans

sol = Solution()
result = [
    # sol.isPrefixString(s = "iloveleetcode", words = ["i","love","leetcode","apples"]),
    # sol.minStoneSum(piles = [5,4,9], k = 2),
    
    # sol.longestObstacleCourseAtEachPosition(obstacles = [1,2,3,2]),
    # sol.longestObstacleCourseAtEachPosition([2,2,1]),
    # sol.longestObstacleCourseAtEachPosition([5,1,5,5,1,3,4,5,1,4]),
    
    sol.minSwaps(s = "][]["),
    sol.minSwaps(s = "]]][[["),
    
]
for r in result:
    print(r)
