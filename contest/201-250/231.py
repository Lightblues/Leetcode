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
https://leetcode.cn/contest/weekly-contest-231
@2022 """
class Solution:
    """ 1784. 检查二进制字符串字段 """
    import re
    def checkOnesSegment(self, s: str) -> bool:
        return len(re.split("1+", '0' + s + '0')) <= 2
    
    """ 1785. 构成特定和需要添加的最少元素 """
    def minElements(self, nums: List[int], limit: int, goal: int) -> int:
        diff = abs(sum(nums) - goal)
        return math.ceil(diff/limit)
    
    """ 1786. 从第一个节点出发到最后一个节点的受限路径数 #medium #题型 #UCS
从1走到节点n, 要求「受限路径」为, 所有经过的节点距离节点n的距离依次减小 (边带权), 问所有受限路径的数量.
限制: 节点, 边 2e4. 
思路1: #UCS 即可. 除了记录每一个节点的距离, 还统计每个节点的路径数量
    正确性: 路径要求其中的每个点的到点n的距离是严格递减的, 而我们是按照节点距离从小到大反向遍历的, 因此, **我们在拓展节点u的时候, 已经将到u的所有合法路径累加好了**.
    用一个 #heap, 每次拓展距离最小的节点; 为了避免重复拓展, 用一个 visited哈希表来记录.
"""
    def countRestrictedPaths(self, n: int, edges: List[List[int]]) -> int:
        mod = 10**9 + 7
        g = [[] for _ in range(n+1)]
        for u,v,w in edges:
            g[u].append((v,w))
            g[v].append((u,w))
        # 一开始想到可以用目标节点的额距离进行剪枝, 但没必要
        # dist1 = inf
        dists = [inf] * (n+1); counts = [0] * (n+1)
        dists[n] = 0; counts[n] = 1
        q = [(0, n)]; visited = set()   # 由于一个节点可能在堆中出现多次, 用一个set记录访问过的节点
        while q:
            # 每次遍历没有遍历过的, 距离最小的节点
            dist, u = heappop(q)
            if u==1: break
            # 剪枝
            if u in visited: continue
            for v,w in g[u]:
                # 注意这里的判断: dists[u] >= dists[v] 按照题意路径不合法. 此时我们已经遍历过距离很小的 v 了
                if dist >= dists[v]: continue
                # if v in visited or dist >= dists[v]: continue
                dists[v] = min(dists[v], dist+w)
                counts[v] = (counts[v] + counts[u]) % mod
                heappush(q, (dists[v], v))
            visited.add(u)
        return counts[1]

    """ 1787. 使所有区间的异或结果为零 #hard #异或 #hardhard #题型
给定一个长n的数组和一个数字k, 要求对于数组元素做最少次数的改动, 使得所有长为k的子数组的异或和为0.
限制: n 2000; 数组元素 2^10
提示:
    最后得到的数组一定是长度为k的 **循环数组**. 证明: 因为相邻两个长k的数组的异或和都为0.
    对于所有二进制长度不超过L的一组数字, 它们的异或和一定不超过 2^L-1.
思路1
    由于结果为长k的循环数组, 我们可以将原数组划分为k个部分, 我们仅需要确定这k个部分取的数字是什么. 为此, 我们给每个部分统计出现的数字的数量.
    可以 #分类 讨论: 1) 考虑某一组数字全部发生替换. 此时, 对于其他组的数字可以 #贪心 选取数量最多的, 然后将全部替换的数字设置为相应的异或和即可; 2) 所有组的数字都采用组内原本就有的. 此时, 采用如下贪心做法:
        记 `f[i][mask]` 表示采用前i个组并且异或和为mask时, **最多可以保留的数量**. (方面起见统计最多可以保留的数量, 答案用n一减即可).
        递推: `f[i][mask] = max{ cnt[i][num] + f[i-1][mask ^ num] for num in nums }` 这里假设第i组数字包括nums, 而保留了其中的元素 num. (注意: 正因为我们假设了每组都会设置成其中已有的元素, max遍历的复杂度为 `O(n/k)`)
        边界: i=0 时, `f[i][mask] = cnt[i][mask]`
        复杂度: 根据提示, 我们mask只需要取异或和可能的最大长度即可, 因此DP数组大小 O(k * 2^L), 每次max为 O(n/k), 因此总体复杂度为 ` O(n 2^L)`
    见 [灵神](https://leetcode.cn/problems/make-the-xor-of-all-segments-equal-to-zero/solution/fen-lei-tao-lun-tan-xin-dp-by-endlessche-y14r/). 相较于 [官答](https://leetcode.cn/problems/make-the-xor-of-all-segments-equal-to-zero/solution/shi-suo-you-qu-jian-de-yi-huo-jie-guo-we-uds2/) 更为清晰.
总结: 灵神的题解真的精彩. 相较于官答, 这里通过分类讨论, 清除地将「仅考虑第i组已有的数字」这种情况分离出来 (从而将max复杂度从 n 下降为 n/k), 理解起来更为直观.
"""
    def minChanges(self, nums: List[int], k: int) -> int:
        # 统计每组中出现的数字
        cnt = [Counter() for _ in range(k)]
        for i,num in enumerate(nums):
            cnt[i%k][num] += 1
        # 分类1: 选择一个组全部进行替换
        # mx = 0
        maxs = [max(d.values()) for d in cnt]
        mx = max(sum(maxs)-maxs[i] for i in range(k))
        # 分类2: DP
        M = 2**10
        f = [cnt[0][m] for m in range(M)]
        for i in range(1,k):
            # 下面可以进行简写. 因为右侧的f没有发生修改
            # nf = [0]*M
            # for mask in range(M):
            #     nf[mask] = max(cnt[i][v] + f[mask^v] for v in cnt[i])
            # f = nf
            f = [max(f[mask^v] + cnt[i][v] for v in cnt[i]) for mask in range(M)]
        mx = max(mx, f[0])
        return len(nums) - mx   # 取反
        
sol = Solution()
result = [
    # sol.checkOnesSegment("1001"),
    # sol.checkOnesSegment("110"),
    # sol.countRestrictedPaths(n = 5, edges = [[1,2,3],[1,3,3],[2,3,1],[1,4,2],[5,2,2],[3,5,1],[5,4,10]]),
    # sol.countRestrictedPaths(n = 7, edges = [[1,3,1],[4,1,2],[7,3,4],[2,5,3],[5,6,1],[6,7,2],[7,5,3],[2,6,4]]),
    # sol.countRestrictedPaths(6, [[2,4,5],[3,4,2],[2,1,3],[3,1,3],[4,6,5],[5,1,9],[1,4,3],[2,6,5],[5,6,5],[5,3,8],[1,6,6],[3,2,8],[5,2,8]]),
    # sol.countRestrictedPaths(8, [[5,4,2],[4,6,10],[5,7,1],[8,3,3],[2,8,1],[6,8,9],[5,6,8],[3,6,10],[8,5,5],[2,4,4],[2,1,10],[1,5,6],[6,1,6],[7,3,6],[6,7,7],[3,2,5],[3,5,8],[1,4,10],[1,7,6],[7,8,9]]),
    sol.minChanges(nums = [1,2,0,3,0], k = 1),
    sol.minChanges(nums = [3,4,5,2,1,7,3,4,7], k = 3),
    sol.minChanges(nums = [1,2,4,1,2,5,1,2,6], k = 3),
    
    
]
for r in result:
    print(r)
