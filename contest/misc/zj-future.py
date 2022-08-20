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
杭州未来科技城X 力扣编程大赛集
see https://leetcode.cn/circle/article/LYt7tg/
@2022 """
class Solution:
    """ zj-future01. 信号接收 """
    def canReceiveAllSignals(self, signals: List[List[int]]) -> bool:
        signals.sort()
        lastEnd = -1
        for s,e in signals:
            if s<lastEnd: return False
            lastEnd = e
        return True
    
    """ zj-future02. 黑白棋游戏 """
    def minSwaps(self, chess: List[int]) -> int:
        target = sum(chess)
        mx = sum(chess[:target])
        cnt = mx
        for i in range(target, len(chess)):
            cnt += chess[i] - chess[i-target]
            mx = max(mx, cnt)
        return target - mx
    
    """ zj-future03. 快递中转站选址 #medium
在一个grid上有一组快递分发点, 想要加一个中转站, 问放在哪里, 它距离所有分发点的曼哈顿记录之和最小?
提示: 两个坐标的计算是可分离的!
思路1: 计算 #中位数 即可
    等价于, 在一个坐标轴上有一系列的点, 找一个点, 使其与所有点的距离之和最小. 注意到, 该问题的解就是中位数!
"""
    def buildTransferStation(self, area: List[List[int]]) -> int:
        m,n = len(area), len(area[0])
        l = 0; sx,sy = [], []
        for i in range(m):
            for j in range(n):
                if area[i][j]==1:
                    l += 1
                    sx.append(i); sy.append(j)
        # cx, cy = round(sx/l), round(sy/l)
        import numpy as np
        cx,cy = np.median(sx), np.median(sy)
        ans = 0
        for x,y in zip(sx,sy):
            ans += abs(x-cx) + abs(y-cy)
        return int(ans)
    
    """ zj-future04. 门店商品调配 #hard
问题转化: 有一组门店借出, 另一组调入. 每次操作用a转x个物品到b门店, 问最少的操作次数.
限制: 门店数量12
提示:
    对于一组大小为s的借入借出关系 (和为0), 最多的最优操作是多少次? `s-1`. (一种naive的方法是, 先将正数集中到一个人, 然后一次分配给其他的负数)
思路1: #状压 #DP
    我们考虑用DP, 记 `f[mask]` 为mask所表示的一组店, 用多少次可以平衡. 可知若该组之和≠0则不能平衡, 定义为inf.
    当所选组可以平衡的时候, 可考虑递归 `f[mask] = min{ mask.bit_count()-1, f[subset]+f[mask\subset] }`. 也即考虑最坏情况和所有的可递归子问题.
    复杂度: 枚举所有子集 `O(n^3)`. see [灵神](https://leetcode.cn/circle/discuss/3p5v9B/view/8FQhy2/)
思路2: 暴力 #DFS
    我们仅考虑没有平衡的账户. 然后遍历idx, 对于每一个idx, 检查在其后的账户, 若两者符号相反, 将idx的值加到后者上 (不管绝对值谁大谁小), 然后后移idx.
    正确性: 实际上我们利用了提示中的上界, 遍历了所有的情况.
    参见 「0465 Optimal Account Balancing 最优账户平衡」 (会员题, 见 [here](https://developer.aliyun.com/article/336702))
总结: 关键是想到提示中的上界, 然后思路1其实枚举了所有的情况; 思路2更加暴力点, 代码更简单但理解更玄学.
"""
    def minTransfers(self, distributions: List[List[int]]) -> int:
        """ 尝试启发, 失败
        错例: [3,3,5], [1,4,6] """
        cnt = [0] * 12
        for i,o, c in distributions:
            cnt[i] -= c
            cnt[o] += c
        ins = []; outs = []
        for c in cnt:
            if c>0: ins.append(c)
            elif c<0: outs.append(-c)
        ins.sort(); outs.sort()
        ans = 0
        def f1():
            nonlocal ans
            for i in ins[:]:
                if i in outs:
                    ins.remove(i); outs.remove(i)
                    ans += 1
        def f2():
            nonlocal ins, outs, ans
            if ins[-1] > outs[-1]: ins, outs = outs, ins
            outs[-1] -= ins[-1]; ins.pop()
            ans += 1
        while ins or outs:
            f1(); 
            if ins: f2()
        return ans
            
    def minTransfers(self, distributions: List[List[int]]) -> int:
        # 思路1
        n = 12
        cnt = [0] * n
        for i,o,c in distributions:
            cnt[i] -= c; cnt[o] += c
        f = [inf] * (1<<n); f[0] = 0
        for mask in range(1, 1<<n):
            sm = 0
            for j in range(n):
                if mask&(1<<j): sm += cnt[j]
            if sm != 0: continue
            f[mask] = mask.bit_count()-1
            sub = (mask-1)&mask
            while sub:
                f[mask] = min(f[mask], f[sub]+f[mask^sub])
                sub = (sub-1)&mask
        return f[-1]
    def minTransfers(self, distributions: List[List[int]]) -> int:
        # 思路2 from https://developer.aliyun.com/article/336702
        n = 12
        cnt = [0] * n
        for i,o,c in distributions:
            cnt[i] -= c; cnt[o] += c
        cnt = [i for i in cnt if i!=0]
        m = len(cnt)
        if m==0: return 0   # 边界
        ans = m-1
        def dfs(i, c):
            nonlocal ans
            # 剪枝
            if cnt >= ans: return 
            # 终止条件
            if i==m: ans = min(ans, c); return
            # i 位置已平衡
            if cnt[i]==0: dfs(i+1, c); return
            for j in range(i+1, m):
                if cnt[i]*cnt[j] < 0:
                    cnt[j] += cnt[i]
                    dfs(i+1, c+1)
                    cnt[j] -= cnt[i]
        dfs(0, 0)
        return ans
    
sol = Solution()
result = [
    # sol.canReceiveAllSignals(signals = [[0,40],[10,15],[20,30]]),
    # sol.canReceiveAllSignals(signals = [[2,8],[8,14]]),
    # sol.minSwaps(chess = [1,0,1,0,1,0]),
    # sol.minSwaps(chess = [1,1,0,1,0,1,0,0,1,0,1]),
    # sol.buildTransferStation(area = [[0,1,0,0,0],[0,0,0,0,1],[0,0,1,0,0]]),
    # sol.buildTransferStation(area = [[1,1],[1,1]]),
    # sol.minTransfers(distributions = [[0,1,5],[1,2,10],[2,0,5],[2,1,1]]),
    # sol.minTransfers(distributions = [[0,1,5],[1,4,5],[4,0,5]]),
    sol.minTransfers([[1,2,3],[1,3,3],[6,4,1],[5,4,4]]),
]
for r in result:
    print(r)
