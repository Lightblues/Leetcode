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
https://leetcode.cn/contest/weekly-contest-256
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1984. 学生分数的最小差值 """
    def minimumDifference(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = inf
        for i in range(k-1, len(nums)):
            ans = min(ans, nums[i] - nums[i-k+1])
        return ans
    
    """ 1985. 找出数组中的第 K 大整数 """
    def kthLargestNumber(self, nums: List[str], k: int) -> str:
        nums = [int(i) for i in nums]
        nums.sort()
        return str(nums[-k])
    
    """ 1986. 完成任务的最少工作时间段 #medium
有一组任务, 完成每个任务需要一定的时间. 你每次训练可以工作 `sessionTime` 个小时. 在一个session中, 你可以完成多个任务, 但一个任务不能分割到多个session中. 要求分配任务到不同的session, 使得session总数最小.
限制: 任务数量 1 <= n <= 14; 任务时间 max(tasks[i]) <= sessionTime <= 15
注意, 不能用「尽量选择大的任务」的方法, 例如 [2,2,3,3,3,5], sessionTime=9 的情况下, 这种方案会导致 [5,3], [3,2,2], [2] 而实际答案为 2.
[here](https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/solution/wan-cheng-ren-wu-de-zui-shao-gong-zuo-sh-tl0p/)
思路1: #枚举子集 的动态规划 #DP
    f[mask] 表示mask对应子集所需的最少session.
    递归的方式: 显然有 f[mask] = min{f[mask\subset] + 1} 这里的subset要求是子集中元素和不超过 sessionTime 的.
    如何 **遍历所有子集**? 有一种经典的方式: 先初始化 `sub = mask`, 然后递归 `sub = (sub - 1) & mask` 即可保证.
    如何计算子集和? 为了避免重复, 可以预计算.
    时间复杂度: $3^n$. 在递归过程中, 我们需要遍历 mask [1: 2^n], 而每一个mask有多少非零位? 可知包含k个1的二进制表示有 $C^n_k$ 个. 因此复杂度为 $\sum_{k=0}^{n}\left(\begin{array}{l}n \\ k\end{array}\right) 2^{k}$. 正好是 $3^n = (1+2)^n$ 的二次项展开形式.
    具体见链接.
思路2: #存储两个值的动态规划
    本思路更符合直觉, 复杂度也更低, 但是比较难想清楚.
    对于某一mask表示的集合, 我们考虑最后一个加入的元素, 并且 **让之前的session都不再变化**. 这样, 可以用 (segment, currnet) 表示状态. 其中前者表示已用的session数量, 后者表示最后一个session已占用的时间.
    转移: `f[mask] = min{trans(f[mask\i], tasks[i])}` 这里的i是枚举了所有mask中包含的元素. trans是对于状态的转移, 比较简单.
    复杂度: O(n * 2^n)
"""
    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        # https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/solution/wan-cheng-ren-wu-de-zui-shao-gong-zuo-sh-tl0p/
        n = len(tasks)
        m = 1<<n
        # 预计算所有的subset是否可以放在一个session中
        valid = [False] * m
        for mask in range(1, m):
            cumT = 0
            # 得到mask所表示的所有 1 的位置的数字和
            for i in range(n):
                if 1<<i > mask: break
                if (1<<i) & mask: cumT += tasks[i]
                if cumT > sessionTime: break
            if cumT <= sessionTime: valid[mask] = True
            
        
        # DP 递归. 计算每一个子集的最小session数
        # f = defaultdict(lambda: inf)
        f = [inf] * m
        f[0] = 0
        # 注意, 这里是要遍历所有可能的子集, 而不是 1, 11, 111...
        for mask in range(1, m):
            # 遍历 mask 所表示的集合的所有子集的方式: 先将 sub 初始化为 mask, 然后依次 `sub = (sub - 1) & mask`
            sub = mask
            while sub:
                if valid[sub]: f[mask] = min(f[mask], f[mask ^ sub]+1)
                sub = (sub - 1) & mask
        return f[(1<<n)-1]

    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        """ 第一部分的计算见 [here](https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/solution/zi-ji-dong-tai-gui-hua-by-endlesscheng-wtua/)
        采取了DP的形式, 但复杂度仍然位 O(2^n)
        实际上提交的时间几乎没有变化 (因为第二部分复杂度更高?)"""
        n = len(tasks)
        m = 1<<n
        # 预计算所有的subset是否可以放在一个session中
        sums = [0] * m
        for i, task in enumerate(tasks):
            # j 从0遍历到 2^i-1, 即将第 i 位加到 tasks[:i] 的所有子集中中
            j, limit = 0, 1<<i
            while j<limit:
                sums[j | limit] = task + sums[j]
                j += 1
        f = [inf] * m
        f[0] = 0
        for mask in range(m):
            subset = mask
            while subset:
                if sums[subset] <= sessionTime:
                    f[mask] = min(f[mask], f[subset ^ mask] + 1)
                subset = (subset - 1) & mask
        return f[m-1]
    
    
    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        """ 思路2 https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/solution/wan-cheng-ren-wu-de-zui-shao-gong-zuo-sh-tl0p/
        复杂度: O(n * 2^n)"""
        n = len(tasks)
        f = [(inf, inf)] * (1<<n)
        f[0] = (1, 0)
        def add(o, x):
            if o[1] + x <= sessionTime:
                return o[0], o[1] + x
            return o[0]+1, x
        for mask in range(1, 1<<n):
            for i in range(n):
                if mask & (1<<i):
                    f[mask] = min(f[mask], add(f[mask ^ (1<<i)], tasks[i]))
        return f[(1<<n)-1][0]
    
    """ 1987. 不同的好子序列数目 #hard
给定一个二进制字符串, 一定「好子序列」为合法的二进制数(除了0本身之外不包含前导0). 求 **不同** 的好子序列的数目.
例如, binary = "101" 有5个好子序列: ["1", "0", "1", "10", "11", "101"]
约束: 1 <= binary.length <= 10^5
思路1: #倒序 DP
    为了子序列合法, 我们仅考虑「以1开头的不同子序列数量」. 最后若字符串中包含0再 +1 即可
    如何得到以1开头的子序列数量? **倒序** 看有多少以0/1结尾的子序列数量!
    令 dp[i][0/1] 表示从后往前, 直到第 i 位的字符串中, 有多少以0/1结尾的子序列数量
    转移公式: 若 `s[i]==1`, 显然 `dp[i][0] = dp[i+1][0]`, 而 `dp[i][1] = dp[i+1][0] + dp[i+1][1] + 1` 分别表示在原本的基础上加上字符1, 以及单独的一个比特1.
    from [灵神](https://leetcode.cn/problems/number-of-unique-good-subsequences/solution/jian-ji-xie-fa-by-endlesscheng-bvrx/)
    [官答](https://leetcode.cn/problems/number-of-unique-good-subsequences/solution/bu-tong-de-hao-zi-xu-lie-shu-mu-by-leetc-ej2n/) 的讨论更复杂些.
"""
    def numberOfUniqueGoodSubsequences(self, binary: str) -> int:
        """ [灵神](https://leetcode.cn/problems/number-of-unique-good-subsequences/solution/jian-ji-xie-fa-by-endlesscheng-bvrx/) """
        MOD = 10**9 + 7
        # dp[0/1] 表示「以0/1结尾的所有不同子序列数量」.
        dp = [0] * 2
        for ch in binary[::-1]:
            idx = 0 if ch=='0' else 1
            dp[idx] = (dp[0] + dp[1] + 1) % MOD
        return dp[1] + ('0' in binary)

sol = Solution()
result = [
    # sol.minimumDifference(nums = [9,4,1,7], k = 2),
    
    # sol.minSessions(tasks = [1,2,3], sessionTime = 3),
    # sol.minSessions(tasks = [3,1,3,1,1], sessionTime = 8),
    # sol.minSessions(tasks = [1,2,3,4,5], sessionTime = 15),
    # sol.minSessions([9,8,8,4,6],14),
    
    sol.numberOfUniqueGoodSubsequences(binary = "101"),
    
    
]
for r in result:
    print(r)
