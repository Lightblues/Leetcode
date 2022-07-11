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
https://leetcode.cn/contest/weekly-contest-301

题解: https://leetcode.cn/circle/discuss/5t4W96/view/kJ2FEW/
@2022 """

""" 6113. 无限集中的最小数字 """
class SmallestInfiniteSet:
    def __init__(self):
        self.ava = SortedList(range(1, 10000))

    def popSmallest(self) -> int:
        return self.ava.pop(0)

    def addBack(self, num: int) -> None:
        if num not in self.ava:
            self.ava.add(num)

class Solution:
    """ 6112. 装满杯子需要的最短总时长 #easy
有三种类型的物品, 各需要一定数量, 每次操作可以 1) 获得两种物品各一; 或 2) 或者一种物品. 问最少需要多少次操作才能得到所有的物品?
思路1: #归纳 分析
    三种类型的数量排序, 假如分别是 a,b,c. 对于a+b与c的关系进行分类讨论记录. 复杂度 O(1)
思路2: #贪心 每次选择剩余数字较大的两个进行操作.
"""
    def fillCups(self, amount: List[int]) -> int:
        amount.sort()
        a,b,c = amount
        if a+b>=c:
            return c+ ceil((a+b-c)/2)
        return a+b + (c-a-b)
    
    """ 6114. 移动片段得到字符串 #medium
两个字符串包括了 `L,R,_` 类别, L只能向左, R只能向右, 不能交替. 问start能否变为target.
限制: 两字符串等长, 1e5
思路1: 字符之间存在一一对应关系, #模拟 检查即可.
    由于LR不能交错, 因此要求S,T中, 非空字符的顺序相同. 并且要求: 对应字符中, L的位置满足 `idxS>=idxT`, R的位置 `idxS<=idxT`
"""
    def canChange(self, start: str, target: str) -> bool:
        s = [ch for ch in start if ch!="_"]
        t = [ch for ch in target if ch!="_"]
        if s!=t: return False
        idxS = [i for i,ch in enumerate(start) if ch!="_"]
        idxT = [i for i,ch in enumerate(target) if ch!="_"]
        for ch,idxs,idxt in zip(s,idxS,idxT):
            if ch=="L":
                if idxs<idxt: return False
            elif ch=='R':
                if idxs>idxt: return False
        return True
    
    """ 6115. 统计理想数组的数目 #hard
定义「理想数组」: 所有元素都在 `[1...maxValue]`, `arr[i]` 都是` arr[i-1]` 的倍数 (1,2,3...倍)
限制: n,maxVal 1e4
思路0: #DP
    定义 `f[i][j]` 为长度为i的数组, 最后一个值为j的理想数组的数量.则有递推 `f[i][j] = sum{ f[i-1][k] }`, 其中k为j的因子.
    但显然复杂度不够, 需要 O(n^3).
思路1: 将数字分解 #因子, 然后利用 #排列 公式计算
    定义 `f[k]` 表示已k结尾的长度为n的合法数组数量. 则答案为 `sum{ f[k] }`.
    将问题定义为排列问题: 对于每一个质因子计算重复数, 然后进行放置. 注意, 不是 `comb(n, ...)`.
        先考虑所有的因子都相同的情况. 例如有2个因子2, 长度n=2, 可以有的排列为 `[2,4], [1,4], [4,4]`, 注意两个因子可以放在一个slot中! 因此, 实际上是将2个相同的球放在2个袋子中的数量. 可以用「挡板法」考虑, 也即将k个球放在n个篮子里, 等价在k+n-1个位置选k-1个位置放挡板, `comb(k+n-1, k-1)`
        对于不同的因子, 注意它们之间是独立的! (直观理解, 在上面的例子中加入一个重复数为1的因子3, 则答案数*2).
    总之, 对于结尾数字k, 假如k不同因子的分别有 [m1,m2,...] 个重复, 则以k结尾的合法数组数量为 `prod{ comb(n+m_i-1, m_i) }`.
    复杂度: 在遍历n的每一步, 计算质因子 O(log n), 计算组合数 O(log n) (这里直接用了math.comb, 在比较小的情况下是线性的), 因此复杂度最多 `O(n log^2(n))`
    from [灵神](https://leetcode.cn/problems/count-the-number-of-ideal-arrays/solution/shu-lun-zu-he-shu-xue-zuo-fa-by-endlessc-iouh/)
"""
    def idealArrays(self, n: int, maxValue: int) -> int:
        mod = 10**9 + 7
        ans = 1
        for i in range(2, maxValue+1):
            factors = getPrimeFactors(i)
            a = 1
            for f in factors:
                a = (a * math.comb(n+f-1, f)) % mod
            ans = (ans + a) % mod
        return ans

# 计算所有的质数
ps = [2,3]
for i in range(5, 10**4+1):
    flag = True
    for j in range(len(ps)):
        if ps[j]**2 > i: break
        if i % ps[j] == 0: flag = False; break
    if flag: ps.append(i)
# 将一个数n分解为质因子
def getPrimeFactors(n):
    idx = 0
    factors = []
    while n>1:
        cnt = 0
        while n%ps[idx]==0:
            n //= ps[idx]
            cnt += 1
        idx += 1
        if cnt: factors.append(cnt)
    return factors

sol = Solution()
result = [
    # sol.fillCups(amount = [1,4,2]),
    # sol.fillCups(amount = [5,4,4]),
#     testClass("""["SmallestInfiniteSet", "addBack", "popSmallest", "popSmallest", "popSmallest", "addBack", "popSmallest", "popSmallest", "popSmallest"]
# [[], [2], [], [], [], [1], [], [], []]"""),
    # sol.canChange(start = "_L__R__R_", target = "L______RR"),
    # sol.canChange(start = "R_L_", target = "__LR"),
    # sol.canChange(start = "_R", target = "R_"),
    # quick_matrix_pow([[1,1],[1,0]], 3),
    # getPrimeFactors(6),
    sol.idealArrays(n = 2, maxValue = 5),
    sol.idealArrays(n = 5, maxValue = 3),
]
for r in result:
    print(r)
