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
import random

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
https://leetcode.cn/contest/weekly-contest-248
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1920. 基于排列构建数组 """
    def buildArray(self, nums: List[int]) -> List[int]:
        ans = [0] * len(nums)
        for i,num in enumerate(nums):
            ans[i] = nums[num]
        return ans
    
    """ 1921. 消灭怪物的最大数量 #medium #题型
题目设置很有意思(类似植物大战僵尸): 对于长度n的一个列表, 每一行有一个距离 dist[i] 的怪物以速度 speed[i] 移动, 每次可以选择一行击毙敌人. 问最多可以坚持多长时间.
约束: 数组长度 1e5
思路1: #模拟
    题目其实比较简单, 关键是需要注意边界情况. 
"""
    def eliminateMaximum(self, dist: List[int], speed: List[int]) -> int:
        avaTime = defaultdict(int)
        for d,s in zip(dist, speed):
            avaTime[ceil(d/s)] += 1
        acc = 0
        for t, multi in sorted(avaTime.items()):
            # 注意 = 的情况是可取的.
            if acc+multi > t:
                return t
            acc += multi
        return acc
    
    """ 1922. 统计好数字的数目 #medium #快速幂
问满足一定条件的数字的个数. 总而言之, 计算公式为 5^(ceil(n/2)) * 4^(floor(n/2))
约束: 数字范围为 1e15, 对结果取模
思路1: 利用 #快速幂 计算
    对于这么大的数字, 可知算法必然是要求在 O(log(n)) 级别的
总结: 注意数字范围那么大, 应该马上联想到快速幂的.
"""
    def countGoodNumbers(self, n: int) -> int:
        MOD = 10**9 + 7
        multi, rem = divmod(n, 2)
        return pow(20, multi, MOD) * 5**rem % MOD
    
    
    """ 1923. 最长公共子路径 #hard
给定n个长度至多为n的序列, 问这些序列的最长公共子数组. 相较于 「0718 题」, 从2个数组变为n个.
约束: n <= 1e5, 所有数组的长度之和L <= 1e5
思路1: #字符串哈希 + #二分
    思路和0718一样, 不过这里检查长度k是否满足的时候, 需要依次比较所有数组所包含的哈希值集合之交集是否非空.
    复杂度: O(L * log(n)) 其中计算所有哈希值需要 L, 二分搜索的范围为 `[0, min(len_i)]` 即所有数组的最小长度.
    关于参数的选择: 官答中的分析很赞!
        #生日悖论: 若随机选择 23个人则两个人生日相同的概率大于 50%. 一般而言, 从 N个数字中随机选择K个, 当 K=O(log(N)) 时, 出现重复(碰撞)的概率很大.
        本题中, 所有长度为k的子串的数量级在 `L=O(1e5)` 级别, 因此选择的模应该远大于 1e10 级别.
            因此, 答案中选择 (10**9+7) * (10**9+9) 将两个大质数相乘.
            Python中不用考虑大数字的问题, 在其他语言中, 可以分别求这两个数字的模, 都不想相等时才认为子串不同.
        另外, 关于base的选择: 可能的公共子串的长度在 1e5 级别, 题目中随机选取了 `[1e6, 1e7]` 范围内的随机数, 发现确实比较容易过 (而 1e5 以下的冲突概率较大).
总结: 在 Rabin-Karp 算法的基础上, 更多考察了 base, mod 的选择问题, 通过 #生日悖论 理论计算了所需的mod.
[官答](https://leetcode.cn/problems/longest-common-subpath/solution/zui-chang-gong-gong-zi-lu-jing-by-leetco-ypip/)

"""
    def longestCommonSubpath(self, n: int, paths: List[List[int]]) -> int:
        """ https://leetcode.cn/problems/longest-common-subpath/solution/zui-chang-gong-gong-zi-lu-jing-by-leetco-ypip/ """
        # 考虑到最多有 L = O(1e5) 级别的不同子串, 需要用的 mod 数量级应该远大于 1e10
        mod = (10**9+7) * (10**9+9)
        # base = 113 
        # base 的选择: 因为数组长度最大为 1e5, 所以 base 取值范围大一些.
        # 官答用了随机策略 (说是一种「调参」的方法), 但拍脑袋尝试应该也没问题
        base = random.randint(10**6, 10**7)
        base = 176483
        
        limit = min(len(i) for i in paths)
        # 注意到, 由于 base 1e6, limit 1e5, 因此要采用快速幂算法
        # bases = [base**i % mod for i in range(limit)]
        bases = [pow(base, i, mod) for i in range(limit)]
        def f(k) -> bool:
            hashs = set()
            path = paths[0]
            hash = sum(bases[k-i-1] * path[i] for i in range(k)) % mod
            hashs.add(hash)
            for i in range(1, len(path) -k+1):
                hash = ((hash - bases[k-1]*path[i-1]) * base + path[i+k-1]) % mod
                hashs.add(hash)
            # 
            for path in paths[1:]:
                newHashs = set()
                hash = sum(bases[k-i-1] * path[i] for i in range(k)) % mod
                if hash in hashs: newHashs.add(hash)
                for i in range(1, len(path) -k+1):
                    hash = ((hash - bases[k-1]*path[i-1]) * base + path[i+k-1]) % mod
                    if hash in hashs: newHashs.add(hash)
                if not newHashs: return False
                hashs = newHashs
            return True
        
        l, r = 0, limit
        ans = 0
        while l<=r:
            mid = (l+r) >> 1
            if f(mid):
                ans = mid
                l = mid+1
            else:
                r = mid-1
        return ans
    
    
    """ 0718. 最长重复子数组 #medium #题型 Rabin-Karp
给定两个数组, 求出最长公共子数组的长度.
限制: 两数组长度都小于 1e3
思路0: #暴力 方法. 枚举所有的 (i,j) 开始匹配位置, 尝试匹配. 注意这样的时间复杂度为 O(n^3) 会超时!
思路1: 用 #DP 进行优化
    注意, 思路0中哪里出现了重复比较? 在尝试匹配 (i,j), (i-1, j-1), (i-2, j-2)... 的过程中, 都会比较 nums[i:] 和 nums[j:]
    实际上, 我们可以避免这样的重复. 记 `f[i][j]` 表示nums[i:] 和 nums[j:]的最大匹配长度, 则仅当 nums1[i]==nums2[j] 时有 `f[i][j] = f[i-1][j-1] + 1`, 否则为0.
    这样, 时间复杂度为 O(MN)
思路2: #字符串哈希 + #二分
    考虑子问题: 判断两数组是否有长度为k的公共子数组. 可以采用 Rabin-Karp 计算字符串哈希, 若两字符串有相同哈希值则认为有 (当然有几率发生碰撞).
    滚动计算哈希值: 可以采用 #滑动窗口 的策略
        有递推公式: `hash(s[i+1:i+1+len]) = (hash(i:i+len) - base^(len-1)*s[i]) * base + s[i+len]`
    复杂度: O((M+N) log(min(M,N)))
思路3: #滑动窗口
    题解2中说的很好: 「想象两把尺子，错开之后比较相同的部分，找最长相同的串就好了」; 很符合实际拿到两个纸质列表的直观解法.
    复杂度: O((M+N) min(M,N))
总结: 从复杂度上来说, 还是字符串哈希是最快的, 因为没有尝试进行两字符串之间的比较.
[官答](https://leetcode.cn/problems/maximum-length-of-repeated-subarray/solution/wu-li-jie-fa-by-stg-2/)
"""
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        # 思路1: 用 #DP. O(MN)
        m,n = len(nums1), len(nums2)
        f = [[0] * n for _ in range(m)]
        ans = 0
        for i in range(n):
            if nums1[-1]==nums2[i]:
                f[-1][i] = 1
                ans = 1
        for j in range(m):
            if nums1[j]==nums2[-1]:
                f[j][-1] = 1
                ans = 1
        for i in range(m-2, -1, -1):
            for j in range(n-2, -1, -1):
                if nums1[i]==nums2[j]:
                    f[i][j] = f[i+1][j+1] + 1
                    ans = max(ans, f[i][j])
        return ans

    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        """ 思路2: #字符串哈希 + #二分
        hash(s[i+1:i+1+len]) = (hash(i:i+len) - base^(len-1)*s[i]) * base + s[i+len]
        """
        base = 113
        mod = 10**9 + 7
        
        m, n = len(nums1), len(nums2)
        bases = [base**i %mod for i in range(min(m,n))]
        def check(k):
            hash1s = set()
            hash1 = sum(bases[k-i-1] * nums1[i] for i in range(k)) % mod
            hash1s.add(hash1)
            for i in range(1, m-k+1):
                hash1 = ((hash1 - bases[k-1] * nums1[i-1]) * base + nums1[i+k-1]) % mod
                hash1s.add(hash1)
            hash2 = sum(bases[k-i-1] * nums2[i] for i in range(k)) % mod
            if hash2 in hash1s: return True
            for i in range(1, n-k+1):
                hash2 = ((hash2 - bases[k-1] * nums2[i-1]) * base + nums2[i+k-1]) % mod
                if hash2 in hash1s: return True
            return False
        # bisect
        l, r = 0, min(m, n)
        ans = 0
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                l = mid+1
            else:
                r = mid-1
        return ans
        
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        """ 思路3: #滑动窗口  O((M+N) log(min(M,N))) """
        m, n = len(nums1), len(nums2)
        def f(i,j):
            t = 0; ans = 0
            while i<m and j<n:
                if nums1[i]==nums2[j]:
                    t += 1
                    ans = max(ans, t)
                else:
                    t = 0
                i += 1; j += 1
            return ans
        ans = 0
        # 想象两把尺子交错, 比较重叠部分中的最大重复子串.
        for j in range(n-1, -1, -1):
            ans = max(ans, f(0, j))
        for i in range(1, m):
            ans = max(ans, f(i, 0))
        return ans
        
        
sol = Solution()
result = [
    # sol.buildArray(nums = [0,2,1,5,3,4]),
    # sol.eliminateMaximum(dist = [1,3,4], speed = [1,1,1]),
    # sol.eliminateMaximum(dist = [1,1,2,3], speed = [1,1,1,1]),
    # sol.eliminateMaximum(dist = [3,2,4], speed = [5,3,2]),
    # [sol.countGoodNumbers(i) for i in range(1, 20)],
    
    # sol.findLength(nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]),
    # sol.longestCommonSubpath(n = 3, paths = [[0],[1],[2]]),
    sol.longestCommonSubpath(n = 5, paths = [[0,1,2,3,4],
                     [4,3,2,1,0]]),
    sol.longestCommonSubpath(n = 5, paths = [[0,1,2,3,4],
                     [2,3,4],
                     [4,0,1,2,3]]),
]
for r in result:
    print(r)
