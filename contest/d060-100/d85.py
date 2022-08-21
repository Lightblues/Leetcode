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
https://leetcode-cn.com/contest/biweekly-contest-85
[灵神](https://leetcode.cn/circle/discuss/oZvJdG/view/lLAAmi/)

@2022 """
class Solution:
    """ 6156. 得到 K 个黑块的最少涂色次数 #easy #滑动窗口
有黑白格子, 每次操作可以涂黑一个白色, 问得到k个连续黑格的最小操作. 限制: n 100
思路0: #DP 感觉好蠢 复杂度 `O(n^2)`
    记 `f(c,i)` 表示在c次操作以内, 以i结尾的连续黑块的起始位置 (-1)
    递推: 若i为黑格, 则f(c,i) = f(c,i-1); 否则, f(c,i) = f(c-1,i-1)
    初始化: 可以用一个变量维护最近出现的白色位置
思路1: 目标是长为k的一个子数组, 因此直接 #滑动窗口 取最小值即可. 复杂度 `O(n)`
    [灵神](https://leetcode.cn/problems/minimum-recolors-to-get-k-consecutive-black-blocks/solution/on-hua-dong-chuang-kou-by-endlesscheng-s4fx/) 利用zip简化了代码.
"""
    def minimumRecolors(self, blocks: str, k: int) -> int:
        # 思路0: #DP
        n = len(blocks)
        f = [[-1]*(n+1) for _ in range(k+1)]
        # 
        preW = -1
        for idx in range(n):
            if blocks[idx]=='W': preW = idx
            f[0][idx+1] = preW
            if idx-preW >= k: return 0
        for c in range(1, k+1):
            for i in range(n):
                if blocks[i]=='B':
                    # f[c][i+1] = min(i-1, f[c][i])
                    f[c][i+1] = f[c][i]
                else:
                    f[c][i+1] = f[c-1][i]
                if i-f[c][i+1] >= k: return c
    def minimumRecolors(self, blocks: str, k: int) -> int:
        # 思路1: 滑动窗口
        ans = cnt_w = blocks[:k].count('W')
        for in_, out in zip(blocks[k:], blocks):
            cnt_w += (in_ == 'W') - (out == 'W')
            ans = min(ans, cnt_w)
        return ans

    """ 6157. 二进制字符串重新安排顺序需要的时间
给定一个二进制字符串, 在每一轮中, 将所有的 01 转换为 10. 问经过多少次操作后终止? 限制: 1000
思路1: #模拟 复杂度 O(n^2)
思路2: 一次遍历, 复杂度 O(n)
    显然, 每次操作的过程会将1往左移动. 模拟「车辆移动」的过程; 特殊在于, 只有当一辆车前面有空格时才能前进.
    用DP, 记 `f[i]` 为将前i个字符移动所需的时间. 
    递归: 若 s[i]==0, 则 `f[i] = f[i-1]`; 否则, 考虑两种情况: 1) 假如前面有 pre0 个0, 则移动的步骤至少为 pre0步; 2) 但连续的两辆车可能会「堵车」, 但 **若发生堵车, 它和前一辆车的距离最多有一个空格**, 因此这种情况下时间为 `f[i-1]+1`. 综合考虑即 `f[i] = max(pre0, f[i-1]+1)`.
"""
    def secondsToRemoveOccurrences(self, s: str) -> int:
        step = 0
        s = list(map(int, s))
        n = len(s)
        flag = True     # 标记是否发生了操作
        while flag:
            flag = False
            ns = [0] * n
            ns[0] = s[0]
            for i in range(1, n):
                if s[i-1]==0 and s[i]==1:   # 出现 01
                    ns[i-1] = 1
                    flag = True
                elif s[i] == 1:             # 未匹配到的 1
                    ns[i] = 1
            s = ns
            # 注意只有发生了操作才 +1
            if flag: step += 1
        return step
    def secondsToRemoveOccurrences(self, s: str) -> int:
        # 思路2: 一次遍历, 复杂度 O(n)
        f = pre0 = 0
        for c in s:
            if c == '0': pre0 += 1
            elif pre0: f = max(f + 1, pre0)  # 前面有 0 的时候才会移动
        return f

    """ 6158. 字母移位 II #medium 就是一道 #差分 题
限制: 序列长度, 区间操作数 5e4; 
"""
    def shiftingLetters(self, s: str, shifts: List[List[int]]) -> str:
        n = len(s)
        ords = list(map(lambda ch: ord(ch)-ord('a'), s))
        # 差分数组, 这里长度+1 是为了防止越界, 实际上还原的时候不会用到
        diff = [0] * (n+1)
        diff[0] = ords[0]
        for idx in range(1, n):
            diff[idx] = ords[idx] - ords[idx-1]
        # 记录区间操作
        for s,e,d in shifts:
            if d==0: diff[s] -= 1; diff[e+1] += 1
            else: diff[s] += 1; diff[e+1] -= 1
        ans = [0] * n
        limit = 26
        ans[0] = diff[0] % limit
        for i in range(1,n):
            ans[i] = (diff[i] + ans[i-1]) % limit
        return ''.join(map(lambda x: chr(x+ord('a')), ans))
    def shiftingLetters(self, s: str, shifts: List[List[int]]) -> str:
        # 灵神的神奇简洁写法
        c2i = {c: i for i, c in enumerate(ascii_lowercase)}

        diff = [0] * (len(s) + 1)
        for start, end, dir in shifts:
            diff[start] += dir * 2 - 1
            diff[end + 1] -= dir * 2 - 1
        return ''.join(ascii_lowercase[(c2i[c] + shift) % 26] for c, shift in zip(s, accumulate(diff)))

    """ 6159. 删除操作后的最大子段和 #hard
给定一个长n的数组, 然后给一个n的全排列, 定义了每次删除的元素顺序. 要求返回在每一步删除操作后, 剩余元素所构成的区间中的最大区间和.
思路1: #逆向 考虑, 用 #并查集 记录相连情况.
    细节: 由于逆向过程中只有一部分的点才是合法的(未被删除), 可以用一个set来记录合法的点.
    在逆向「加点」的过程中, 连接合法的左右邻居(所对应的区间), 更新全局的mx.
关联: 2334. 元素值大于变化阈值的子数组 也是逆序并查集 参见 [线段树]
from [灵神](https://leetcode.cn/problems/maximum-segment-sum-after-removals/solution/by-endlesscheng-p61j/)
"""
    def maximumSegmentSum(self, nums: List[int], removeQueries: List[int]) -> List[int]:
        n = len(nums)
        # 并查集
        fa = list(range(n))
        values = nums[:]        # 记录每个组的区间和 (只有根节点是正确的)
        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        def union(x,y):
            x = find(x)
            y = find(y)
            if x != y:
                fa[x] = y
            values[y] += values[x]
            return values[y]
        def getV(x):
            return values[find(x)]
        # 逆向加点
        ans = [0] * n
        mx = 0
        valid = set()
        for i in range(n-1,0,-1):
            a = removeQueries[i]
            if a<n-1 and a+1 in valid:
                union(a+1,a)
            if a>0 and a-1 in valid:
                union(a-1,a)
            mx = max(mx, getV(a))
            ans[i-1] = mx
            valid.add(a)
        return ans
    def maximumSegmentSum(self, nums: List[int], removeQueries: List[int]) -> List[int]:
        # 灵神的简洁写法
        n = len(nums)
        fa = list(range(n + 1))
        sum = [0] * (n + 1)
        def find(x: int) -> int:
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        ans = [0] * n
        for i in range(n - 1, 0, -1):
            x = removeQueries[i]
            # 注意这里固定将第x个元素所在组合并到右侧x+1的组中, 因此只需要往一边合并即可.
            to = find(x + 1)
            fa[x] = to  # 合并 x 和 x+1
            sum[to] += sum[x] + nums[x] # 原本的sum[x] 中还不包含 nums[x]
            ans[i - 1] = max(ans[i], sum[to])
        return ans




sol = Solution()
result = [
    # sol.minimumRecolors(blocks = "WBBWWBBWBW", k = 7),
    # sol.minimumRecolors(blocks = "WBWBBBW", k = 2),
    # sol.minimumRecolors("WWW", 2),
    # sol.secondsToRemoveOccurrences("0110101"),
    # sol.secondsToRemoveOccurrences("111000"),
    # sol.shiftingLetters(s = "abc", shifts = [[0,1,0],[1,2,1],[0,2,1]]),
    # sol.shiftingLetters(s = "dztz", shifts = [[0,0,0],[1,1,1]]),
    # sol.maximumSegmentSum(nums = [1,2,5,6,1], removeQueries = [0,3,2,4,1]),
    # sol.maximumSegmentSum(nums = [3,2,11,1], removeQueries = [3,2,1,0]),

]
for r in result:
    print(r)
