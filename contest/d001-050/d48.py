from time import time
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

""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-48
@2022 """
class Solution:
    """ 1796. 字符串中第二大的数字 """
    def secondHighest(self, s: str) -> int:
        nums = (int(ch) for ch in s if ch in "0123456789")
        nums = sorted(set(nums), reverse=True)
        return nums[1] if len(nums)>1 else -1
    
    """ 1798. 你能构造出连续值的最大数目 #medium
给定一组银币, 问能从这些硬币中组成 0,1,2...n-1 这样最大多少个连续数字, 返回能构成的数量n.
思路: #归纳
    根据所给的例子进行归纳猜想. 例如, 给定 `[1,4,10,3,1]`, 答案为20. 
    先将其排序 `[1,1,3,4,10]`, 第一个最多为1; 前两个最多构成2, 正好接上第三个数字3; 第四个显然可以; 然后前四个数字之和9, 可以接上数字10, 这样最大的数字为19.
    因此, 可以总结: 对于第i个数字若前缀和 acc[1...i-1] >= nums[i], 则可以使用第i个数字. 找到最大的满足条件的i, 答案即为 acc+1.
"""
    def getMaximumConsecutive(self, coins: List[int]) -> int:
        coins.sort()
        if coins[0] != 1: return 1
        acc = 0
        for c in coins:
            if c <= acc+1:
                acc += c
            else:
                break
        return acc+1
    
    """ 1799. N 次操作后的最大分数和 #hard #题型
给定一个长度为 2n 的数组, 将他们分成n组, 每组两个数字计算gcd, 然后每一组的权重为 1,2...,n, 定义分数为带权和. 求最大的分数
限制: 最大的组数为 n<=7
思路0: 尝试暴力遍历, 超时
    初步想了一下, 从所有数字中找一半作为一组, 数量最多为为 `comb(14, 7) = 3432`, 然后遍历其中一部分进行匹配, 数量为 `perm(7) = 5040`. 这样整体的尝试次数似乎在 1e7 级别?
    下面用递归形式, 结果超时了
思路1: #DP
    数组的最大长度为 14, 因此考虑用状压来进行表示. 注意这里只有mask中非零位数量为偶数时才是有效的.
    采用dp, 定义 dp[mask] 为 **采用mask所表示的大小为2a子集, 权重分别为 1...a 的最大分数**; 
    则有递推公式 `dp[mask] = max{ dp[premask] + s*gcd(mask^premask) }`. 其中第一项premask枚举mask之前的状态 (查了两个数字), 而第二项是新加的两个数字, 权重 s=mask.bit_count()//2
    复杂度: dp长度为 2^(2n); 枚举大小为2的子集的复杂度为 O(len(arr)^2). 因此总体复杂度为 O(2^(2n) * (2n)^2)
注意: 在考虑DP的时候, 之前在纠结子问题的值进行表示什么? 它们的权重是什么? 但考虑到DP其实就是暴力枚举, 在上面max的过程中自然会遍历到所有的可能, 因此直接定义submask的权重为子问题的即可, 这样, 对于新的pair赋予权重为之后的那一个即可.
"""
    def maxScore(self, nums: List[int]) -> int:
        """ 尝试暴力遍历, 超时 """
        # 预计算 gcd表
        l = len(nums)
        gcdMap = [[0]* l for _ in range(l)]
        for i in range(l):
            for j in range(i, l):
                gcdMap[i][j] = math.gcd(nums[i], nums[j])
        n = l//2
        # 遍历所有的 comb(14,7) 组合
        part1 = []
        def dfs(idx):
            if len(part1) == n:
                check(part1)
                return
            for i in range(idx, l):
                part1.append(i)
                dfs(i+1)
                part1.pop()
        ans = 0
        # 检查划分方式 part1, part2 是否满足条件: 需要遍历所有的匹配方式
        def check(part1):
            nonlocal ans
            part2 = (i for i in range(l) if i not in part1)
            for perm in itertools.permutations(part2):
                gcds = [gcdMap[i][j] for i,j in zip(part1, perm)]
                gcds.sort()
                ans = max(ans, sum(i*j for i,j in zip(range(1, n+1), gcds)))
        dfs(0)
        return ans
    
    def maxScore(self, nums: List[int]) -> int:
        l = len(nums)
        dp = [0] * (1<<l)
        for mask in range(1, 1<<l):
            if mask.bit_count() % 2 != 0: continue
            idxs = [i for i in range(l) if mask>>i&1]
            for pair in itertools.combinations(idxs, 2):
                submask = mask ^ (1<<pair[0]) ^ (1<<pair[1])
                dp[mask] = max(dp[mask], dp[submask] +mask.bit_count()//2 * math.gcd(nums[pair[0]], nums[pair[1]]) )
        return dp[(1<<l)-1]
    
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res

class AuthenticationManager:
    """ 1797. 设计一个验证系统
init: timeToLive 为验证到期时间
generate(string tokenId, int currentTime): 在currentTime生成一个验证码
renew(string tokenId, int currentTime): 如果存在tokenId并且尚未过期, 则更新其开始时间为currentTime
countUnexpiredTokens(int currentTime): 计算所有未过期的验证码数量
"""
    def __init__(self, timeToLive: int):
        self.timeToLive = timeToLive
        self.auths = {}

    def generate(self, tokenId: str, currentTime: int) -> None:
        self.auths[tokenId] = currentTime

    def renew(self, tokenId: str, currentTime: int) -> None:
        if tokenId in self.auths and currentTime - self.auths[tokenId] < self.timeToLive:
            self.auths[tokenId] = currentTime

    def countUnexpiredTokens(self, currentTime: int) -> int:
        cnt = 0
        for tokenId in self.auths:
            if currentTime - self.auths[tokenId] < self.timeToLive:
                cnt += 1
            # 否则应该删除掉; 不过调用次数最多2000没必要
        return cnt

sol = Solution()
result = [
    # sol.secondHighest(s = "abc1111"),
    # sol.secondHighest(s = "dfa12321afd"),
#     sol.testClass("""["AuthenticationManager", "renew", "generate", "countUnexpiredTokens", "generate", "renew", "renew", "countUnexpiredTokens"]
# [[5], ["aaa", 1], ["aaa", 2], [6], ["bbb", 7], ["aaa", 8], ["bbb", 10], [15]]"""),
    # sol.getMaximumConsecutive(coins = [1,3]),
    # sol.getMaximumConsecutive([1,4,10,3,1]),
    # sol.getMaximumConsecutive(coins = [1,1,1,4]),
    sol.maxScore(nums = [1,2]),
    sol.maxScore(nums = [3,4,6,8]),
    sol.maxScore(nums = [1,2,3,4,5,6]),
    sol.maxScore([39759,619273,859218,228161,944571,597983,483239,179849,868130,909935,912143,817908,738222,653224]),
]
for r in result:
    print(r)
