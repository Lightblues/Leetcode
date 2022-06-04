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
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # pow 与基本环境下的 pow 冲突
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
https://leetcode.cn/contest/weekly-contest-255
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1979. 找出数组的最大公约数 """
    def findGCD(self, nums: List[int]) -> int:
        nums.sort()
        return math.gcd(nums[0], nums[-1])

    """ 1980. 找出不同的二进制字符串 #题型 #二进制
- 注意熟悉二进制字符串与整数 (以及格式化) 的方式
"""
    def findDifferentBinaryString(self, nums: List[str]) -> str:
        n = len(nums[0])
        nums = [int(i,2) for i in nums]
        nums.sort()
        for i in range(1<<n):
            if i>=len(nums) or nums[i] != i:
                """ 注意这种格式化方式 """
                return f"{i:0{n}b}"
            
    """ 1981. 最小化目标值与所选元素的差 #medium
给定一个grid, 可以从每一行选择一个元素, 要求与目标值 target 的绝对差最小.
约束: 行列数量不超过70, 元素大小70, 目标值不超过800
思路1: #DP 
    从下往下遍历, 我们维护到目前为止的行, 每行选取一个元素, 可以构成的所有数字 (利用set进行去重)
    本质上也是动态规划: f[i][j] 表示到第i行为止, 每行选择一个元素, 是否可以得到和 j
    dp的思路可以枚举j, 也即 $f[i][j]=f[i][j] \vee f[i-1][j-x]$; 而下面代码中的思路则是维护一个set来保存所有出现的j; 两种方式在不同的约束下应该各有好坏.
    另外, 注意到下面进行filter操作! 可以有效减小搜索空间. 但要注意最后nums可能为空, 因此需要判断 (或者像官答一样计算一个 minSum)
    参见 [here](https://leetcode.cn/problems/minimize-the-difference-between-target-and-chosen-elements/solution/zui-xiao-hua-mu-biao-zhi-yu-suo-xuan-yua-mlym/)
    
"""
    def minimizeTheDifference(self, mat: List[List[int]], target: int) -> int:
        # m,n = len(mat), len(mat[0])
        nums = set(mat[0])
        f = lambda x: x<=800
        # f = lambda x: True
        for row in mat[1:]:
            nums = set(filter(
                f, [i+j for i,j in product(nums, row)]
            ))
        # 注意, 由于进行了filter操作, 数组可能为空!
        if len(nums)==0:
            return abs(target - sum(min(r) for r in mat))
        nums = sorted(list(nums))
        idx = bisect.bisect_left(nums, target)
        ans = inf
        if idx>0:
            ans = min(ans, abs(target-nums[idx-1]))
        if idx<len(nums):
            ans = min(ans, abs(nums[idx])-target)
        return ans
    
    """ 1982. 从子集的和还原数组 #hard #题型 #数学
给定数组的长度n和所有的 2^n 个子集的和, 要求还原原来的数组.
约束: n<=15, 子集和 -1e4~1e4
[官答](https://leetcode.cn/problems/find-array-given-subset-sums/solution/cong-zi-ji-de-he-huan-yuan-shu-zu-by-lee-aj8o/)
思路1: #递归 求解, 每次还原一个数字
    结论1: 对于所有的子集和排序, 记最小和次小元素为 `x,y`, 则 `x-y, y-x` 之一一定在原数组中.
        (假如有负数) 考虑次小元素是如何产生的? 要么是少了一个负元素, 要么是多了一个非负元素. (没有负数的情况下, 则一定是 y-x)
    提示2: 记差值 `d = y-x` (这样我们知道了 d, -d 之一一定在原数组中). 我们可以将 2^n 个子集和分成两部分 `S,T`, (一一对应) 使得每个 s[i] + d = t[i]
        可以采用双指针
        这样, 即可递归求解 —— 因为 S,T 之一一定是一个大小为 n-1 的子问题. 但注意到其中一个可能是非法的, 因此两个分支都要进行搜索, 需要DFS尝试回退.
    结论3: 事实上, 对于 S,T 的选择, 我们只需要选择包含0 的那一个即可. 这样避免了DFS.
        注意到, 一个数组的子集和中一定包含0 (空集).
        那么, 如果 S,T都包含0呢? 结论是选择哪一个都行. 例如, 假设原数组A 中包括 d, 而我们选择了 S.
            此时, S中的元素为原数组的所有子集和都 -d.
            由于 S包含0. 可知原数组中有一个集合O, 使得 `sum(O) - d = 0`.
            这样, 我们只需要对 O的元素都取反 O', 原数组A中其他元素不变, 这样变换后的数组B的所有子集和就是S.
            证明: 对于S中的任意元素 `s[i] = t[i] - d` 假设 t[i] 由原数组A中, 在O之外的X集合和O之内的Y集合构成. 我们在变换后的数组B中, 选择 `X` 和 `O'\Y`. 这样, 我们正好就是在 t[i] 的基础上减去了所有的O元素 (也即d).

"""
    def recoverArray(self, n: int, sums: List[int]) -> List[int]:
        # https://leetcode.cn/problems/find-array-given-subset-sums/solution/cong-zi-ji-de-he-huan-yuan-shu-zu-by-lee-aj8o/
        def recover(sums):
            n = len(sums)
            if len(sums)==2:
                # 数组长度为1, 则子集和一个包含0, 另一个就是元素值
                ans.append(sum(sums))
                return 
            d = sums[1] - sums[0]
            arr1, arr2 = [None] * (n//2), [None] * (n//2)
            used = [False] * n
            arr1Had0 = False
            i1, i2 = 0, 1
            for i in range(n//2):
                while used[i1]: i1 += 1
                while i2<=i1 or sums[i1] + d != sums[i2]: i2 += 1
                # 此时一定满足
                # if not used[i1] and not used[i2] and sums[i1] + d == sums[i2]:
                arr1[i] = sums[i1]
                arr2[i] = sums[i2]
                used[i1] = True
                used[i2] = True
                if sums[i1] == 0:
                    arr1Had0 = True
                used[i1] = used[i2] = True
                i1, i2 = i1+1, i2+1
            if arr1Had0:
                ans.append(d)
                recover(arr1)
            else:
                ans.append(-d)
                recover(arr2)
        sums.sort()
        ans = []
        recover(sums)
        return ans

sol = Solution()
result = [
    # sol.findGCD(nums = [2,5,6,9,10]),
    # sol.findDifferentBinaryString(nums = ["01","10"]),
    
    # sol.minimizeTheDifference([[1,2,3],[4,5,6],[7,8,9]], target = 13),
    # sol.minimizeTheDifference(mat = [[1],[2],[3]], target = 100),
    
    # sol.recoverArray(n = 3, sums = [-3,-2,-1,0,0,1,2,3]),
    # sol.recoverArray(n = 4, sums = [0,0,5,5,4,-1,4,9,9,-1,4,3,4,8,3,8]),
    sol.recoverArray(3, [365,44,-355,399,409,764,10,0]),
]
for r in result:
    print(r)
