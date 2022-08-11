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
https://leetcode.cn/contest/weekly-contest-212
@2022 """
class Solution:
    """ 1629. 按键持续时间最长的键 """
    def slowestKey(self, releaseTimes: List[int], keysPressed: str) -> str:
        lastT, mxLen, mxKey = 0, 0, None
        for t,k in zip(releaseTimes, keysPressed):
            dur = t - lastT
            if dur>mxLen or dur==mxLen and k>mxKey:
                mxLen, mxKey = dur, k
            lastT = t
        return mxKey
    
    """ 1630. 等差子数组 """
    def checkArithmeticSubarrays(self, nums: List[int], l: List[int], r: List[int]) -> List[bool]:
        def check(arr:list):
            if len(arr)==1: return True
            d = arr[1]-arr[0]
            for i in range(len(arr)-1):
                if arr[i+1]-arr[i]!=d:
                    return False
            return True
        ans = [False] * len(l)
        for i, (ll,rr) in enumerate(zip(l,r)):
            if check(sorted(nums[ll:rr+1])):
                ans[i] = True
        return ans
    
    """ 1631. 最小体力消耗路径 见「并查集」 """
    
    """ 1632. 矩阵转换后的秩 #hard #反思
输出矩阵中所有位置元素对应的秩. 秩的定义为: 从1开始, 尽可能小, 同行/同列的两元素p,q, 若 `p<q` 则 `rank(p)<rank(q)`.
限制: 矩阵 500*500
思路0: 对于所有元素排序, 从小到大确定秩. 遍历过程中维护行/列约束. #TLE 补救回来了
    补丁: 注意这样有问题: **相同值的关联元素之间存在依赖关系**. 例如同行的两个相同元素 (i,j) 但是两个位置在列上的rank不同, 则两个元素的秩应该都取较大的那个rank.
        因此, 对于同值元素根据依赖关系「分组」, 同组元素的rank取最大值. 如何分组? 根据行列依赖, 构建 #并查集 来记录.
    补丁1: 结果TLE了, 这里的原因在于, 一开始分组(连边)的时候, 我通过遍历所有行/列来找到找到连接关系, 这样复杂度就是 `((m+n) * |nodes|) = O((m+n) * (mn))` 超时.
        参考 [here](https://leetcode.cn/problems/rank-transform-of-a-matrix/solution/python-bing-cha-ji-tuo-bu-pai-xu-by-qin-lv6kx/) 同更为简单的方式分组: 建立 row2idx, col2idx 记录该行/列的第一个值为x的点, 对于同值点 (r,c) 只需要与该点连接即可.
    这样, 时间复杂度 O(mn logmn) 就是排序时间.
思路1: 总结一些上面记录, 补充更 #优雅 的一份代码. 总体就是用了 并查集 + 拓扑排序
    重新来看这一问题, 每个元素仅依赖于同行/列中的次小元素 (和同值元素), 若没有同值元素就是简单的 #拓扑排序. 特殊情况是, 同值元素所带来的依赖关系, **具有依赖关系的同值元素可以作为一个节点**, 我们用 #并查集 来记录组关系.
    
"""

    def matrixRankTransform(self, matrix: List[List[int]]) -> List[List[int]]:
        # 思路0
        m,n = len(matrix), len(matrix[0])
        row2info = {i: [-inf, 0] for i in range(m)}
        col2info = {i: [-inf, 0] for i in range(n)}
        v2idx = [(matrix[x][y], x*n+y) for x,y in product(range(m), range(n))]
        # v2idx.sort(key=lambda x: x[0])
        v2idxs = defaultdict(list)
        for v,idx in v2idx:
            v2idxs[v].append(idx)
        for v in sorted(v2idxs):
            nodes = []  # (tmpRank, idx)
            for idx in v2idxs[v]:
                x,y = divmod(idx,n)
                rank = max(
                    row2info[x][1]+1 if v>row2info[x][0] else row2info[x][1],
                    col2info[y][1]+1 if v>col2info[y][0] else col2info[y][1]
                )
                nodes.append((rank,idx))

            fa = {i:i for _,i in nodes}
            def find(x):
                # if fa[x] != x:
                #     fa[x] = find(fa[x])
                # return fa[x]
                path = [] 
                while fa[x]!=x:
                    path.append(x); x = fa[x]
                for a in path: fa[a] = x
                return x
            def merge(x,y):
                if x<y:
                    x,y = y,x
                fx,fy = find(x), find(y)
                if fx==fy: return
                fa[fx] = fy
            # 反思 #TLE 的原因: 这里分组的时候, 每次都需要遍历同组元素nodes. 这里的复杂度为 O((m+n) * |nodes|) = O((m+n) * (mn))
            # for r in range(m):
            #     node = None
            #     for _,idx in nodes:
            #         if idx//n!=r: continue
            #         if node is None: node = idx
            #         else: merge(node, idx)
            # for c in range(n):
            #     node = None
            #     for _,idx in nodes:
            #         if idx%n!=c: continue
            #         if node is None: node = idx
            #         else: merge(node, idx)
            
            col2idx = {}; row2idx = {}
            for _,idx in nodes:
                r,c = divmod(idx,n)
                if r not in row2idx: row2idx[r] = idx
                else: merge(row2idx[r], idx)
                if c not in col2idx: col2idx[c] = idx
                else: merge(col2idx[c], idx)
                
            
            groups = defaultdict(list)
            for r,idx in nodes:
                groups[find(idx)].append((r,idx))
            for g,ns in groups.items():
                rank = max(r for r,_ in ns)
                for _,idx in ns:
                    x,y = divmod(idx,n)
                    matrix[x][y] = rank
                    row2info[x] = [v, rank]
                    col2info[y] = [v, rank]
        return matrix

    def matrixRankTransform2(self, matrix: List[List[int]]) -> List[List[int]]:
        # 思路1, 其实和思路0一样. from https://leetcode.cn/problems/rank-transform-of-a-matrix/solution/python-bing-cha-ji-tuo-bu-pai-xu-by-qin-lv6kx/
        def find(x):
            if x not in cache:
                cache[x] = x
            if cache[x] != x:
                cache[x] = find(cache[x])
            return cache[x]
        def merge(x, y):
            cache[find(x)] = cache[find(y)]
        m, n = len(matrix), len(matrix[0])
        cache = {}

        dc = [{} for i in range(n)]     # 存储每列中 num2idxs
        dr = [{} for i in range(m)]
        s = set()   # all values
        d = {}      # value2idx
        for i in range(m):
            for j in range(n):
                num = matrix[i][j]
                # 更新 d, s
                if num not in d:
                    d[num] = []
                    s.add(num)
                d[num].append((i, j))
                # 对于在相同 行/列 的同值元素, 连起来.
                if num in dc[j]:
                    merge((i, j), (dc[j][num], j))
                else:
                    dc[j][num] = i
                if num in dr[i]:
                    merge((i, j), (i, dr[i][num]))
                else:
                    dr[i][num] = j

        c = [0 for i in range(n)]   # 记录当前col的已经用到的rank
        r = [0 for i in range(m)]
        s = sorted(s)
        res = [[-1 for i in range(n)] for j in range(m)]
        for num in s:
            # 对于具有相同值的元素, 根据并查集分组.
            dic = {}        # group2maxRank 注意相同值的元素根据并查集关系可能有好多组
            for i, j in d[num]:
                k = max(c[j], r[i]) + 1
                x = find((i, j))
                dic[x] = max(dic.get(x, 0), k)
            for i, j in d[num]:
                k = dic[find((i, j))]
                res[i][j] = k
                r[i] = k
                c[j] = k
        return res


    def matrixRankTransform3(self, matrix: List[List[int]]) -> List[List[int]]: 
        # 补充一个fancy的写法 https://leetcode.cn/problems/rank-transform-of-a-matrix/solution/python3-mei-sha-ji-zhu-han-liang-de-ti-jie-by-simp/
        LIM = 512
        R, C = len(matrix), len(matrix[0])
        res = [[0]*C for _ in range(R)]
        countR, countC = [0]*R, [0]*C
        
        # 按元素大小分别存储元素坐标
        ls = collections.defaultdict(list)
        for r, row in enumerate(matrix): 
            for c, val in enumerate(row): 
                ls[val].append((r, c))
                
        # 并查集用于合并行或列相同的元素
        union = list(range(LIM*2))
        def find(i): 
            if union[i] == i: return i
            union[i] = find(union[i])
            return union[i]
        
        # 按val从小到大遍历
        pool = collections.defaultdict(list)
        for val in sorted(ls.keys()): 

            # 用并查集合并行和列相同的元素并分组
            for r, c in ls[val]: 
                union[find(r)] = find(c+LIM)
            pool.clear()
            for r, c in ls[val]: 
                pool[find(r)].append((r, c))

            # 行和列相同的元素，共享相同的rank
            for group in pool.values(): 
                rank = max(max((countR[r], countC[c])) for r, c in group) + 1
                for r, c in group: 
                    countR[r] = countC[c] = res[r][c] = rank
                    # 重置并查集
                    union[r] = r
                    union[c+LIM] = c+LIM
        return res


sol = Solution()
result = [
    # sol.slowestKey(releaseTimes = [9,29,49,50], keysPressed = "cbcd"),
    # sol.checkArithmeticSubarrays(nums = [4,6,5,9,3,7], l = [0,0,2], r = [2,3,5]),
    # sol.matrixRankTransform(matrix = [[1,2],[3,4]]),
    # sol.matrixRankTransform(matrix = [[20,-21,14],[-19,4,19],[22,-47,24],[-19,4,19]]),
    sol.matrixRankTransform([[-37,-50,-3,44],[-37,46,13,-32],[47,-42,-3,-40],[-17,-22,-39,24]]),
]
for r in result:
    print(r)
