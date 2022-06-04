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
https://leetcode.cn/contest/weekly-contest-252
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1952. 三除数 """
    def isThree(self, n: int) -> bool:
        cnt = 0
        i = 1
        while i<=n:
            if n%i==0:
                cnt += 1
                if cnt>3: return False
            i += 1
        return cnt==3
    
    """ 1953. 你可以工作的最大周数 """
    def numberOfWeeks(self, milestones: List[int]) -> int:
        milestones.sort()
        s = sum(milestones)
        if milestones[-1] <= s-milestones[-1]+1: return s
        return 2*(s-milestones[-1])+1
        
    """ 1954. 收集足够苹果的最小花园周长
找规律题
[灵神](https://leetcode.cn/problems/minimum-garden-perimeter-to-collect-enough-apples/solution/er-fen-by-endlesscheng-xn9k/) 的思路总让人赞叹
"""
    def minimumPerimeter(self, neededApples: int) -> int:
        i = 1
        quarter = 3
        while quarter * 4 < neededApples:
            i += 1
            quarter += 3*i**2
        return 2*i * 4
        
    """ 1955. 统计特殊子序列的数目 #hard #题型
满足条件的子序列为 [0,...,0,1,...1,2,..,2] 形式的, 也即由若干个0,1,2 组成的递增序列. 现给定一个序列, 要求返回其中满足条件的子序列的数目.
约束: 数组长度 1e5, 对于结果取MOD.
除了DP思路之外, 一开始试图利用前缀和计算前后的0/2的组合数量, 然后枚举中间的1, 但是需要考虑首尾分别用的是哪个位置的1, 两两匹配似乎复杂度过高.
思路1: #DP
    考虑转移过程: 当遇到一个2时增加多少计数? 两种情况: [0,1,2]序列后添加一个2, 或者 [0,1]序列后添加2. 也即 `count012 = 2*count012 + count01`
    进一步, 如何统计在该位置之前有多少01序列? 当遇到一个1时, 递推公式 `count01 = 2*count01 + count0`
    最后, 到某一位置的0序列数量有多少? 递推 `count0 = 2*count0 + 1`
    总结: 在遍历序列过程中, 维护三个变量 (三元素DP), 当遇到 0/1/2 时分别对对应元素进行更新.
    [here](https://leetcode.cn/problems/count-number-of-special-subsequences/solution/dong-tai-gui-hua-by-endlesscheng-4onu/)
"""
    def countSpecialSubsequences(self, nums: List[int]) -> int:
        MOD = 10**9+7
        count0 = 0
        count01 = 0
        count012 = 0
        for num in nums:
            if num==0: count0 = (2*count0 + 1) % MOD
            elif num==1: count01 = (2*count01 + count0) % MOD
            elif num==2: count012 = (2*count012 + count01) % MOD
        return count012
    
sol = Solution()
result = [
    # sol.isThree(9),
    # sol.numberOfWeeks(milestones = [5,2,1]),
    # sol.numberOfWeeks([1,2,3]),
    
    # sol.minimumPerimeter(1),
    # sol.minimumPerimeter(13),
    
    sol.countSpecialSubsequences(nums = [0,1,2,2]),
    sol.countSpecialSubsequences(nums = [0,1,2,0,1,2]),
    sol.countSpecialSubsequences([2,2,0,0])
]
for r in result:
    print(r)
