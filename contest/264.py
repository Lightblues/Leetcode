from re import T
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
from itertools import product, permutations, combinations, combinations_with_replacement
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import sys, os
# sys.setrecursionlimit(10000)

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode

""" 
https://leetcode.cn/contest/weekly-contest-264
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 2047. 句子中的有效单词数
1月每日一题做过了, 要求的验证条件比较复杂.
"""
    def countValidWords(self, sentence: str) -> int:
        # valid = string.ascii_lowercase + '-' + '!.,'
        lowercase = string.ascii_lowercase
        sep = '-'
        special = '!.,'
        def test(token: str):
            # if not all(ch in valid for ch in token): return False
            # if '-' in token:
            #     if token.count('-') > 1: return False
            #     if token[0] == '-' or token[-1] == '-': return False
            #     idx = token.find('-')
            #     if token[idx-1] not in string.ascii_lowercase or token[idx+1] not in string.ascii_lowercase: return False
            countSep = 0
            countSpecial = 0
            for i, ch in enumerate(token):
                if ch == sep:
                    if countSep >= 1: return False
                    countSep += 1
                    if i == 0 or i == len(token)-1: return False
                    if token[i-1] not in lowercase or token[i+1] not in lowercase: return False
                elif ch in special:
                    if countSpecial >= 1: return False
                    countSpecial += 1
                    if i != len(token)-1: return False
                elif ch not in lowercase:
                    return False
            return True
        return sum(test(token) for token in sentence.split())
    
    """ 2048. 下一个更大的数值平衡数
定义「数值平衡数」为, 例如 3133, 包含了1个1, 3个3. 
现在给定一个数字, 要求返回比这个数字大的下一个数值平衡数.
复杂度: 1e6
思路1: 暴力遍历. 要test一个数字是否为平衡数是简单的. 由于数字范围不大, 可以直接暴力遍历.
思路2: 整体的数量不多, 为了加速查询, 可以 #打表 预计算范围内的所有平衡数, 然后二分查找.
"""
    def nextBeautifulNumber(self, n: int) -> int:
        # lenN = len(str(n))
        def test(n: int) -> bool:
            c = Counter(str(n))
            for k,v in c.items():
                if int(k) != v: return False
            return True
        n += 1
        while not test(n):
            n += 1
        return n
    
    
    """ 2049. 统计最高分的节点数目 #medium #题型
有一棵二叉树, 定义一个节点的分数: 移除这个节点(和相邻边) 后, 其他部分节点数量的乘积.
要求返回分数最大的节点的数量.
思路1: #DFS
对于一个节点, 先探索子节点包含的节点数量, 剩余部分的节点数量为 `n-1-nChild1-nChild2` (注意需要排除为 0 的情况), 然后计算乘积.
"""
    def countHighestScoreNodes(self, parents: List[int]) -> int:
        n = len(parents)
        g = [[] for _ in range(n)]
        for i, p in enumerate(parents):
            if p != -1:
                g[p].append(i)
        # DFS
        maxVal, count = n - 1, 0
        def dfs(i: int) -> int:
            """ 返回节点包含的数量 """
            childs = g[i]
            nonlocal maxVal, count, n
            if len(childs) == 0:
                val = n-1
                numNode = 1
            elif len(childs) == 1: 
                nChild = dfs(childs[0])
                val = nChild * max(n-1-nChild, 1)
                numNode = nChild + 1
            elif len(childs) == 2:
                nChild1 = dfs(childs[0])
                nChild2 = dfs(childs[1])
                val = nChild1 * nChild2 * max(n-1-nChild1-nChild2, 1)
                numNode = nChild1 + nChild2 + 1
            if val > maxVal: 
                maxVal, count = val, 1
            elif val==maxVal:
                count += 1
            return numNode
        dfs(0)
        return count
    
    """ 2050. 并行课程 III #hard #题型
课程之间存在DAG依赖关系, 每个课程修习需要一定的月份, 前序依赖满足的情况下, 不同课程可以同时修习. 求完成所有可能的最小时间.
复杂度: 节点/边数量 5e4, 
思路1: #拓扑排序 在遍历的过程中记录每个节点的timeLimit, 这样, 遍历每一条边的时候, 可以更新 `timeLimit[v]` 为 max(timeLimit[v], timeLimie[u]+time[v])`
"""
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        degrees = [0] * n   # in degree
        timeLimit  = time[:]
        g = [[] for _ in range(n)]
        for u, v in relations:
            g[u-1].append(v-1)
            degrees[v-1] += 1
        
        # ans = math.inf
        q = collections.deque([i for i,d in enumerate(degrees) if d==0])
        while q:
            u = q.popleft()
            t = timeLimit[u]
            for v in g[u]:
                degrees[v] -= 1
                timeLimit[v] = max(timeLimit[v], t+time[v])
                if degrees[v] == 0:
                    q.append(v)
        return max(timeLimit)

sol = Solution()
result = [
    # sol.countValidWords(" 62   nvtk0wr4f  8 qt3r! w1ph 1l ,e0d 0n 2v 7c.  n06huu2n9 s9   ui4 nsr!d7olr  q-, vqdo!btpmtmui.bb83lf g .!v9-lg 2fyoykex uy5a 8v whvu8 .y sc5 -0n4 zo pfgju 5u 4 3x,3!wl  fv4   s  aig cf j1 a i  8m5o1  !u n!.1tz87d3 .9    n a3  .xb1p9f  b1i a j8s2 cugf l494cx1! hisceovf3 8d93 sg 4r.f1z9w   4- cb r97jo hln3s h2 o .  8dx08as7l!mcmc isa49afk i1 fk,s e !1 ln rt2vhu 4ks4zq c w  o- 6  5!.n8ten0 6mk 2k2y3e335,yj  h p3 5 -0  5g1c  tr49, ,qp9 -v p  7p4v110926wwr h x wklq u zo 16. !8  u63n0c l3 yckifu 1cgz t.i   lh w xa l,jt   hpi ng-gvtk8 9 j u9qfcd!2  kyu42v dmv.cst6i5fo rxhw4wvp2 1 okc8!  z aribcam0  cp-zp,!e x  agj-gb3 !om3934 k vnuo056h g7 t-6j! 8w8fncebuj-lq    inzqhw v39,  f e 9. 50 , ru3r  mbuab  6  wz dw79.av2xp . gbmy gc s6pi pra4fo9fwq k   j-ppy -3vpf   o k4hy3 -!..5s ,2 k5 j p38dtd   !i   b!fgj,nx qgif "),
    # sol.countValidWords(sentence = "!this  1-s b8d!"),
    # sol.countValidWords(sentence = "alice and  bob are playing stone-game10"),
    
    # sol.nextBeautifulNumber(n = 3000),
    
    # sol.countHighestScoreNodes(parents = [-1,2,0,2,0]),
    # sol.countHighestScoreNodes(parents = [-1,2,0]),
    
    sol.minimumTime(n = 3, relations = [[1,3],[2,3]], time = [3,2,5]),
    sol.minimumTime(n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]),
]
for r in result:
    print(r)
