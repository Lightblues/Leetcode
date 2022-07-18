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
https://leetcode.cn/contest/weekly-contest-234
@2022 """
class Solution:
    """ 1805. 字符串中不同整数的数目 """
    def numDifferentIntegers(self, word: str) -> int:
        import re
        nums = set()
        for num in re.findall("\d+", word):
            nums.add(int(num))
        return len(nums)
    
    """ 1806. 还原排列的最少操作步数 #medium
原本的长尾偶数的排列为 perm = 0,1,...n-1. 现每次进行操作: `f(i) = perm[i/2] if i%2==0 else perm[(i-2)/2 + n/2]` 问经过多少次操作后被还原.
限制: 长度 [2, 1000]
思路1: #归纳 #猜想. 
    可知, 在每一步中, 将原数组的前一半扩充到偶数位上, 后一半扩充到奇数位上.
    画出一步中每个位置的变化情况, 可见 0/n-1 位不变, 其他位置发生「轮转」.
    因此 #猜想: 其他位的轮转次数相同, 因此仅考虑其中一个即可. 定义轮转函数 f, 例如当 n=6, idx=1, 这个数字在操作中依次变为 1,2,4,3,1... 因此答案为 4.
思路2: 更为数学的 #证明
    除了0/n-1位置保持不变之外, 其他位置的变换关系可以统一写成 `f(i)≡2i mod(n-1)`, 因此有 `f^k(i) ≡ 2^k i mod(n-1)`
    为了还原, 需要满足 `2^k i mod(n-1) = i mod(n-1)` (可以看到与i无关)
"""
    def reinitializePermutation(self, n: int) -> int:
        m = [0] * n
        for i in range(n):
            if i%2 == 0: m[i] = i//2
            else: m[i] = n//2 + (i-1)//2
        cnt = 1
        init = 1; idx = 1
        while m[idx] != init:
            idx = m[idx]
            cnt += 1
        return cnt
    
    """ 1807. 替换字符串中的括号内容 #medium
字符串中以 `(key)` 的形式存储着一些待替换的key, 将这些替换为所给的 dict元素.
思路1: #模拟 遍历, 用一个变量记录本阶段的开始idx, 遇到 "()" 两个符号的时候进行替换. 注意最后加一个 `(`哨兵.
"""
    def evaluate(self, s: str, knowledge: List[List[str]]) -> str:
        knowledge = dict(knowledge)
        ans = ""
        sidx = 0
        for i,ch in enumerate(s + '('):
            if ch=='(':
                ans += s[sidx:i]
                sidx = i+1
            elif ch==')':
                key = s[sidx:i]
                ans += knowledge.get(key, '?')
                sidx = i+1
        return ans

    """ 1808. 好因子的最大数目 #hard
问题等价于: 给定一个数字 n, 可以拆分成若干个数字 (相加 =n), 要求这些数字之积最大.
限制: 所给数字 1e9
提示: 拆分出来的数字中不会出现大于等于4的. 这是因为, `2(x-2)>=x` 在 `x>=4` 时恒成立.
思路1: 根据公式计算拆分结果, 然后用 #快速幂 计算.
    根据提示, 可知最后拆分的结果一定只包含 2,3. 进一步可知: 数字2出现的次数不会超过两次: 因为若出现3次, 将其替换为两个3是更好的选择.
    综上: 计算 `a,b = divmod(n, 3)` 若余数 b==1, 说明3的数量为 a-1 (要进行拆分).
复杂度: 操作次数是常数时间的, 快速幂的复杂度为 O(log n).
关联: 「0343. 整数拆分」 see [官答](https://leetcode.cn/problems/integer-break/solution/zheng-shu-chai-fen-by-leetcode-solution/)
"""
    def maxNiceDivisors(self, primeFactors: int) -> int:
        # 特判
        if primeFactors==1: return 1
        
        mod = 10**9 + 7
        a,b = divmod(primeFactors, 3)
        r = 1
        if b == 1:
            # a个3, 剩余一个1; 应该拆成两个2.
            a = a-1; r = 4
        elif b==2:
            r = 2
        return pow(3, a, mod) * r % mod
    
    """ 0343. 整数拆分 #medium 同1808 """
    def integerBreak(self, n: int) -> int:
        # 特判: 要求拆分数量 >=2
        if n<=3: return n-1
        a,b = divmod(n, 3)
        if b==1: a-=1; b=4
        elif b==0: b=1
        return pow(3, a) * (b)
sol = Solution()
result = [
    # sol.numDifferentIntegers(word = "a123bc34d8ef34"),
    # sol.reinitializePermutation(2),
    # sol.reinitializePermutation(4),
    # sol.reinitializePermutation(6),
    # sol.reinitializePermutation(8),
    # sol.evaluate(s = "(name)is(age)yearsold", knowledge = [["name","bob"],["age","two"]]),
    # sol.evaluate(s = "hi(name)", knowledge = [["a","b"]]),
    sol.maxNiceDivisors(5),
    sol.maxNiceDivisors(8),
    sol.maxNiceDivisors(6),
]
for r in result:
    print(r)
