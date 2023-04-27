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
from functools import cache, lru_cache, reduce, partial # cache
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
https://leetcode.cn/contest/weekly-contest-245
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1897. 重新分配字符使所有字符串都相等 """
    def makeEqual(self, words: List[str]) -> bool:
        n = len(words)
        cnt = Counter(itertools.chain(*words))
        for ch, c in cnt.items():
            if c%n !=0: return False
        return True
    
    """ 1898. 可移除字符的最大数目 #medium #题型
给定两个字符串 s,p, 其中p为s的子序列; 另外有一个下标序列removable 表示s中的一些位置, 要找到最大的k使得从s中删除removable[:k]后, p仍然为s的子序列.
约束: s,p 1e5; removable 中的坐标互不相同.
思路0: 从左往右检查删除 removable[i] 后是否满足. #模拟 #超时
    用一个 pIdxs 列表记录当前p中的每一个字符在s中的匹配位置(最靠左的匹配方式), 用removed集合来记录已经删除的坐标. 每删除一个s中的字符(从左往右遍历removable)后, 检查删除的是否在pIdxs, 若在的话, 从所在的位置 pidx 开始重新匹配.
    写了一个很fancy的 `search(pidx, idx)` 函数表示新增了removed之后, 需要从pidx和idx出发重新开始匹配, 能否成功.
    这样, 每次重新检查的复杂度为 O(n), 因此极端情况的整体复杂度是 O(n^2) 会超时!!!
思路1: #二分 搜索
    忘记了一种最简单的方法 orz. 本题中, 现在答案的取值范围为 [0...len(removable)], 因此可以用二分搜索来求解.
    复杂度: `O(n log(len(removable))) = O(n log(n))`
"""
    def maximumRemovals(self, s: str, p: str, removable: List[int]) -> int:
        """ 超时了?? """
        removed = set()         # 已删除的idx
        pIdxs = [-1] * len(p)   # p中的字符对应的idx
        def search(pidx, idx):
            """ 从p的第pidx位置, s的第idx位置 开始往后匹配
            整合了一开始的匹配和之后每次删除一个点之后的重新匹配 """
            # 终止条件
            if pidx>=len(p): return True
            target = p[pidx]
            while idx < len(s):
                if idx not in removed and s[idx]==target:
                    # 找到了 pidx 对应的字符. 注意这里一定要return了不会走到while之外
                    pIdxs[pidx] = idx
                    if pidx==len(p)-1: return True
                    if pIdxs[pidx+1] > idx: return True
                    return search(pidx+1, idx+1)
                idx += 1
            # 没有找到pidx对应的字符
            return False
        search(0, 0)
        for i,ridx in enumerate(removable):
            removed.add(ridx)
            # 检查是否使用了 ridx 元素
            r = bisect.bisect_left(pIdxs, ridx)
            if r<len(pIdxs) and pIdxs[r]==ridx:
                if not search(r, ridx+1): return i  # 从 ridx+1 开始搜索
        return len(removable)
    
    def maximumRemovals(self, s: str, p: str, removable: List[int]) -> int:
        def check(k):
            removed = set(removable[:k])
            pidx = 0
            for i, ch in enumerate(s):
                if i not in removed and ch==p[pidx]:
                    pidx += 1
                    if pidx==len(p): return True
            return False
        l, r = 0, len(removable)
        ans = 0
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                l = mid+1
            else:
                r = mid-1
        return ans
    
    """ 1899. 合并若干三元组以形成目标三元组 """
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        flags = [False] * 3
        for a,b,c in triplets:
            if a>target[0] or b>target[1] or c>target[2]: continue
            if a==target[0]: flags[0] = True
            if b==target[1]: flags[1] = True
            if c==target[2]: flags[2] = True
            if all(flags): return True
        return False
    
    
    """ 1900. 最佳运动员的比拼回合 #hard #interest #题型
有 1...n 个运动员顺序排列. 在竞标赛的执行过程中, 前第i为和后第i位对决二进一 (若n为计数则中间的人轮空晋级). 假设除了两个特殊的选手 firstPlayer < secondPlayer 特别强之外, 其他人的水平都相近. 其他人相互对决时胜负均可. 问两个特殊选手对决出现的最早和最晚轮次.
限制: 2 <= n <= 28
思路1: #分类讨论 来简化分析; #DP; 并利用 #记忆化搜索
    不妨令 `F(n, f,s)` 表示数量为n个, 我们关心的两个人分别在f,s位置时的最少轮次, 用 G(n, f,s) 表示最大轮次.
    下面讨论 F的递推关系, G是完全类似的. 首先, 可以假设 f<s, 不满足的话交换即可. 在下面的讨论中, 记中间位置为 `half = (n+1)//2`
    另外, 可以使得 f<half, 不满足的话对于两个运动员 **取对称位置** `n+1-s, n+1-f` 即可. 下面分类:
    若 s<=half, 此时, 记经过一个轮次后, f前面保留的人的数量和f,s之间保留的人的数量为 i,j, 则它们分别可取 `[0...f-1], [0...s-f-1]`, 而两个人下一轮次的位置为 i+1, i+j+2. 于是有转移方程 `F(n,f,s) = min{ F(half, i+1, i+j+2) } + 1` 这里的ij取上述范围.
    若 s>half. 记s对称位置为 `s'=n+1-s`, 则根据 f, s' 的位置关系进行分类:
        若 `s'==f`, 则直接结束 F(n,f,s) = 1
        另外的情况下, 我们仍可以统一为 f<s': 若出现f>s'的情况, 类似上面的分析我们同样将两者取对称位置即可.
        总之, 有 `0<=f<s'<half`. 这样, f前面和f,s'之间保留的人的数量 i,j 分别可取 `[0...f-1], [0...s'-f-1]`; s'一定被s击败; s'...s 最中间的 n-2*s' 个人一定保留 `mid = (n-2*s'+1)//2` 个, 因此有转移方程 `F(n,f,s) = min{ F(half, i+1, i+j+mid+2) } + 1`
    代码: 在具体实现上, 如何完成这样的DP? 在Python中可以简单用 #记忆化搜索 来送上至下进行计算.
    细节: 对于两次「取对称位置」操作的条件? 第一个是 `s>f>=half`; 第二种情况是 `n+1-s==s'<f`, 于是有 `f+s>n+1`, 注意到这对于第一种情况也是成立的. 于是可以合并为同一个判断 `f+s > n+1`.
    复杂度: DP有三个维度, 每次枚举的复杂度为 O(n^2), 但我们注意到, 递推过程中数组长度n是指数下降的, 因此实际复杂度为 `O(n^4 log(n))`.
详见[官答](https://leetcode.cn/problems/the-earliest-and-latest-rounds-where-players-compete/solution/zui-jia-yun-dong-yuan-de-bi-pin-hui-he-b-lhuo/), 图文并茂.
"""
    def earliestAndLatest(self, n: int, firstPlayer: int, secondPlayer: int) -> List[int]:
        @cache
        def dp(n: int, f: int, s: int):
            assert f < s        # 可以假设 f<s. 注意在下面的转移过程中我们保持调用是满足的
            if f+s == n+1: return (1,1)
            
            # 这条整合了上面的两个需要交换的情况
            if f+s > n+1:
                return dp(n, n+1-s, n+1-f)
            
            n_half = (n+1)//2
            earliest, latest = inf, -inf
            if s<=n_half:
                # s 在左侧或者中间
                for i in range(f):
                    for j in range(s-f):
                        x,y = dp(n_half, i+1, i+j+2)
                        earliest = min(earliest, x)
                        latest = max(latest, y)
            else:
                # s 在右侧
                s_prime = n+1-s
                mid_len = (n - 2*s_prime + 1)//2
                for i in range(f):
                    for j in range(s_prime-f):
                        x,y = dp(n_half, i+1, i+j+mid_len+2)
                        earliest = min(earliest, x)
                        latest = max(latest, y)
            return (earliest+1, latest+1)
        if firstPlayer>secondPlayer:
            firstPlayer, secondPlayer = secondPlayer, firstPlayer
        return dp(n, firstPlayer, secondPlayer)

    
sol = Solution()
result = [
    # sol.makeEqual(words = ["abc","aabc","bc"]),
    # sol.mergeTriplets(triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]),
    # sol.mergeTriplets(triplets = [[3,4,5],[4,5,6]], target = [3,2,5]),
    sol.maximumRemovals(s = "abcacb", p = "ab", removable = [3,1,0]),
    sol.maximumRemovals(s = "abcbddddd", p = "abcd", removable = [3,2,1,4,5,6]),
    sol.maximumRemovals(s = "abcab", p = "abc", removable = [0,1,2,3,4]),
    # sol.earliestAndLatest(n = 11, firstPlayer = 2, secondPlayer = 4),
    # sol.earliestAndLatest(n = 5, firstPlayer = 1, secondPlayer = 5),
]
for r in result:
    print(r)
