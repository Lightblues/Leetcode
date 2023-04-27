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
from unicodedata import digit

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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 6148. 矩阵中的局部最大值 """
    def largestLocal(self, grid: List[List[int]]) -> List[List[int]]:
        m,n = len(grid), len(grid[0])
        ans = [[0] * (n-2) for _ in range(m-2)]
        for i in range(1,m-1):
            for j in range(1,n-1):
                for ii,jj in product([-1,0,1], [-1,0,1]):
                    ans[i-1][j-1] = max(ans[i-1][j-1], grid[i+ii][j+jj])
        return ans
    
    """ 6149. 边积分最高的节点 """
    def edgeScore(self, edges: List[int]) -> int:
        n = len(edges)
        scores = defaultdict(int)
        for u,v in enumerate(edges):
            scores[v] += u
        mx = -inf; ans = 0
        for u in sorted(scores):
            if scores[u] > mx:
                mx = scores[u]; ans = u
        return ans
            
    """ 6150. 根据模式串构造最小数字 #medium #题型 #构造
给定一个长度为n的I/D表示相邻元素的大小关系; 要求返回一个 **字典序最小的** 并且数字为两两不同的1-9数字的序列 (长度为n+1).
限制: 长度 8
思路1: #回溯 用一个有序数组记录还可用的数字, 每次尽量选择最小的那一个. 复杂度: O(n!), 本题由于最大为9 大概在1e6级别所以还行.
思路2: #贪心
    如何最小化字典序? 每次尽量填较小的数字. 为此, **每次考虑 `I..ID..D` 这样先上升后下降的片段**, 例如IIDDD可以填入45321.
    在扫描输入序列的过程中, 每次找上述特征片段 (假设长度为x), 然后填入可以数字中最小的x个数字.
    复杂度: O(n) from [灵神](https://leetcode.cn/problems/construct-smallest-number-from-di-string/solution/by-endlesscheng-8ee3/)
"""
    from sortedcontainers import SortedList
    def smallestNumber(self, pattern: str) -> str:
        # 思路1: #回溯
        n = len(pattern)
        chars = list('123456789')
        sl = SortedList(chars)
        def dfs(idx, s):
            if idx==n: return s
            if pattern[idx]=='I':
                ii = sl.bisect(s[-1])
                if ii==len(sl): return -1
                for i in range(ii, len(sl)):
                    ch = sl.pop(i)
                    r = dfs(idx+1, s+ch)
                    if r!=-1: return r
                    sl.add(ch)
            else:
                ii = sl.bisect(s[-1])
                if ii==0: return -1
                for i in range(ii):
                    ch = sl.pop(i)
                    r = dfs(idx+1, s+ch)
                    if r!=-1: return r
                    sl.add(ch)
            return -1
        for ch in chars:
            sl.remove(ch)
            r = dfs(0, ch)
            if r!=-1: return r
            sl.add(ch)
    def smallestNumber(self, pattern: str) -> str:
        # 思路2: #贪心
        digits = string.digits      # 012...9 因此下面cur从1开始
        i, cur, n = 0, 1, len(pattern)
        ans = [''] * (n + 1)
        while i < n:
            if i and pattern[i] == 'I':
                i += 1
            while i < n and pattern[i] == 'I':
                ans[i] = digits[cur]
                cur += 1
                i += 1
            i0 = i
            while i < n and pattern[i] == 'D':
                i += 1
            for j in range(i, i0 - 1, -1):
                ans[j] = digits[cur]
                cur += 1
        return ''.join(ans)
    def smallestNumber(self, pattern: str) -> str:
        # 更优雅的写法 采用翻转.
        n = len(pattern)
        ans = list(string.digits[1:n+2])
        i = 0
        while i<n:
            if pattern[i]=='I':
                i+= 1; continue
            i0 = i        # D 的起点
            i += 1
            while i<n and pattern[i]=='D':
                i+=1
            # 翻转. 下降了 i-i0 步, 需要翻转的长度 +1
            ans[i0:i+1] = ans[i0:i+1][::-1]
        return ''.join(ans)


    """ 6151. 统计特殊整数 #hard
给定上限n, 要求从 1...n 的数字中, 没有相同元素的数字. 限制: 2e9
思路1: #分类 讨论 + 模拟
    首先, 观察长度为1/2/...的数字中的特殊正数有多少? 分别有 9, 9*9, 9*9*8, ... 注意首位不能是0.
    对于长度为l的目标数字, 分成长度小于l的数字和长度等于l的数字进行讨论. 主要是第二种情况, 每次维护可用的数字列表, 假设剩余ava个可用数字, 要构造长l的子序列, 数量有 `math.perm(ava, l)` 个. 注意首位不能为0.
    写起来比较繁琐, 见code.
思路2: 通用的 #数位 DP
    写成了规范的递归函数形式 `f(i: int, mask: int, isLimit: bool, isNum: bool)`.
        这里的i是当前位, mask表示约束条件;
        isLimit 表示当前位是否受到约束. 例如本题中, 一般情况下可以取所有非冲突位, 而当前缀和n相同时, 只能取更小值;
        isNum 表示 当前位之前是否已有了非零数字, 否则首位不能填0.
    见 [灵神](https://leetcode.cn/problems/count-special-integers/solution/shu-wei-dp-mo-ban-by-endlesscheng-xtgx/)
"""
    def countSpecialNumbers(self, n: int) -> int:
        def f(ava, l):
            # 剩余可用数字有ava个 (不用考虑), 要构造的数字长度为l
            return math.perm(ava, l)
            # if l==0: return 1
            # ans = 1
            # while l:
            #     ans *= ava
            #     l-=1; ava-=1
            # return ans
        @lru_cache(None)
        def remain(ll):
            # 长度为ll 的无约束特殊数字数量. 例如长度为·1 的特殊数字有9个.
            if ll==0: return 0
            if ll==1: return 9
            mul = 9; l=ll-1; ava = 9
            while l>0:
                mul*=ava
                l-=1; ava-=1
            return mul + remain(ll-1)
        
        num = list(map(int, str(n)))
        if len(num)==1: return num[0]
        ans = remain(len(num)-1)
        # 首位不能是 0
        l = len(num)-1
        ans += (num[0]-1) * f(9, l)
        ava = set(range(10)); ava.remove(num[0])
        l -= 1
        # 枚举其他位
        for i in num[1:]:
            aa = [a for a in ava if a<i]
            ans += len(aa) * f(len(ava)-1, l); l-=1
            if i not in ava: return ans
            ava.remove(i)
        return ans + 1
    def countSpecialNumbers(self, n: int) -> int:
        # 思路2: 通用的 #数位 DP
        s = str(n)
        @lru_cache(None)
        def f(i: int, mask: int, is_limit: bool, is_num: bool) -> int:
            # isLimit 表示当前是否受到了 n 的约束。若为真，则第 i 位填入的数字至多为 s[i]，否则可以是 9。
            # isNum 表示 i 前面的位数是否填了数字。若为假，则或者要填入的数字至少为 1 (或当前位可以跳过)；若为真，则要填入的数字可以从 0 开始。
            if i == len(s):
                return int(is_num)
            
            res = 0
            # 1) 首位留空, 注意这里递归调用的 is_num=False
            if not is_num:  # 可以跳过当前数位
                res = f(i + 1, mask, False, False)
            # 2) 填数字, is_num 决定了是否为首位, 注意递归调用 is_num=True
            up = int(s[i]) if is_limit else 9   # 注意「isLimit 表示当前是否受到了 n 的约束」, 因此递归的参数是 is_limit and d == up
            for d in range(0 if is_num else 1, up + 1):  # 枚举要填入的数字 d
                if mask >> d & 1 == 0:  # d 不在 mask 中
                    res += f(i + 1, mask | (1 << d), is_limit and d == up, True)
            return res
        return f(0, 0, True, False)




sol = Solution()
result = [
    # sol.largestLocal(grid = [[9,9,8,1],[5,6,2,6],[8,2,6,4],[6,2,2,2]]),
    # sol.edgeScore(edges = [1,0,0,0,0,7,7,5]),
    sol.smallestNumber(pattern = "IIIDIDDD"),
    sol.smallestNumber(pattern = "DDD"),
    # sol.countSpecialNumbers(20),
    # sol.countSpecialNumbers(5),
    # sol.countSpecialNumbers(135),
]
for r in result:
    print(r)
