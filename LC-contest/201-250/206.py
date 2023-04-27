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
https://leetcode.cn/contest/weekly-contest-206
@2022 """
class Solution:
    """ 1582. 二进制矩阵中的特殊位置 #easy 找到一个01矩阵中, 「某个1是该行和该列中唯一的1」条件的元素数量 """
    def numSpecial(self, mat: List[List[int]]) -> int:
        m,n = len(mat),len(mat[0])
        rowsum = map(sum, mat)
        colsum = [sum(mat[i][c] for i in range(m)) for c in range(n)]
        ans = 0
        for r,ss in enumerate(rowsum):
            if ss!=1: continue
            c = mat[r].index(1)
            if colsum[c]==1: ans += 1
        return ans
    
    
    """ 1583. 统计不开心的朋友 #medium #读题
题目好难读Orz... 有偶数个人两两配对. 一个人之对其他人有偏好性排序, 对于x来说, 假如有某个匹配u, 在配对 `(x,y), (u,v)` 的情况下, 有 `x_u > x_v and u_x > u_v`, 则x是不开心的. 现给定一个匹配, 问不开心的人数.
思路1: 枚举. 注意虽然存在一定的对称关系, 但令x不开心的对象u可能有多个, 因此需要分别判断. 复杂度: O(n^2)
"""
    def unhappyFriends(self, n: int, preferences: List[List[int]], pairs: List[List[int]]) -> int:
        pa = {}
        for a,b in pairs:
            pa[a] = b; pa[b] = a
        pre = defaultdict(dict)
        for i,p in enumerate(preferences):
            for j,q in enumerate(p):
                pre[i][q] = j
        ans = 0
        for i in range(n):
            for j in range(n):
                if i==j: continue
                pi,pj = pa[i],pa[j]
                if pi==j: continue
                if pre[i][j]<pre[i][pi] and pre[j][i]<pre[j][pj]: ans += 1; break
        return ans
    
    """ 1584. 连接所有点的最小费用 #medium #题型 可以有更巧妙的 #hard 解法
平面上有一组点, 问将所有点都联通所需的最小距离和. 也即, 求 #最小生成树.
思路1: 经典的 #Kruskal 算法. 对于所有的边排序, 从小到大遍历, 若 **当前边连接了两个联通分支**, 则将其加入.
    这样, 每次联通一个分支(这个分支和其他分支的最小距离)的代价是最小的, 因此最优.
    为了维护联通性, 用一个 #并查集 来记录.
    复杂度: O(n^2 logn)
思路2: #Prim 算法. 一开始想到的, 但懒得实现了. 基本思路是: 随机选一个点进行初始化; 从当前树结构的相邻节点中选择代价最小的边连接, 直到构成生成树. see [here](https://leetcode.cn/problems/min-cost-to-connect-all-points/solution/prim-and-kruskal-by-yexiso-c500/)
思路3: 建图优化的 Kruskal #hard
    基本思想是, 思路1的复杂度高是因为边过多 (全联通图). 这里利用了一个intuition将每个点连接的边的数量限制到8, 从而将复杂度降为 `O(n logn)`
    intuition: 对于一个点x, 哪些匹配点与其的边会出现在最小生成树中? 将这个点x的四周分成8个45度角的空间, 则在每个区间中最多有一个点与x的边会出现在最小生成树中. 这是因为, 三角形的最长边不可能出现在生成树中.
    如何找到区间内的距离最小的点? 以P1区间内的点为力, 相较于基准点 (x,y), 该区间内的点满足 `x1>=x; y1-x1>=y-x`, 我们的目标是要找到该区间内的 x1+y1 最小值.
        我们按照横坐标从大到小加入, 这样之前加入的点满足第一个条件; 用树状数组记录每个点的 y+x 的最小值信息, 每次在条件二所在的范围内查询最小值. (对于y-x进行离散化操作)
        对于其他区间, 可以巧妙的利用 #坐标变换 转到P1中.
    具体见 [官答](https://leetcode.cn/problems/min-cost-to-connect-all-points/solution/lian-jie-suo-you-dian-de-zui-xiao-fei-yo-kcx7/) 太复杂了.

"""
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        dist = [[inf]*n for _ in range(n)]
        for i,(x,y) in enumerate(points):
            for j,(a,b) in enumerate(points):
                if i==j: continue
                dist[i][j] = abs(x-a) + abs(y-b)
        
        fa = [i for i in range(n)]
        def find(x):
            if fa[x]!=x:
                fa[x] = find(fa[x])
            return fa[x]
        def union(x,y):
            fx,fy = find(x),find(y)
            if fx==fy: return
            fa[fx] = fy
        
        dists = [(dist[i][j],i,j) for i,j in combinations(range(n), 2)]
        dists.sort()
        cost = 0
        for d,i,j in dists:
            if find(i)==find(j): continue
            cost += d
            union(i,j)
        return cost
    
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        # 思路3: https://leetcode.cn/problems/min-cost-to-connect-all-points/solution/lian-jie-suo-you-dian-de-zui-xiao-fei-yo-kcx7/
        n = len(points)
        edges = list()

        def build(pos: List[Tuple[int, int, int]]):
            """ 在相对于 (x,y) 的P1区间内的点满足 `x1>=x; y1-x1>=y-x`, 我们要找到该区间内的 x1+y1 最小值.
            我们按照横坐标从大到小加入, 这样之前加入的点满足第一个条件; 用树状数组记录每个点的 y+x 的最小值信息, 每次在条件二所在的范围内查询最小值."""
            # pos: [(x,y,idx)]
            pos.sort()
            a = [y - x for (x, y, _) in pos]
            b = sorted(set(a))      # 离散化
            num = len(b)

            bit = BIT(num + 1)
            # x坐标 从大到小加入, 确保
            for i in range(n - 1, -1, -1):
                poss = bisect.bisect(b, a[i])
                j = bit.query(poss)
                if j != -1:     # 找到了, 建边
                    dis = abs(pos[i][0] - pos[j][0]) + abs(pos[i][1] - pos[j][1])
                    edges.append((dis, pos[i][2], pos[j][2]))
                bit.update(poss, pos[i][0] + pos[i][1], i)
        
        def solve():
            # 分别对于四个区间计算最近的点. BIT 基于区间P1实现, 下面的三个区间进行了坐标变换.
            pos = [(x, y, i) for i, (x, y) in enumerate(points)]
            build(pos)
            pos = [(y, x, i) for i, (x, y) in enumerate(points)]
            build(pos)
            # 例如 P1 的点满足 0<x<y. 而 P3 的点满足 0<x<(-y). 为了坐标符合要求转为 (-y,x) 即可.
            pos = [(-y, x, i) for i, (x, y) in enumerate(points)]
            build(pos)
            pos = [(x, -y, i) for i, (x, y) in enumerate(points)]
            build(pos)
        
        solve()
        dsu = DisjointSetUnion(n)
        edges.sort()
        
        ret, num = 0, 1
        for length, x, y in edges:
            if dsu.unionSet(x, y):
                ret += length
                num += 1
                if num == n:
                    break
        return ret


    """ 1585. 检查字符串是否可以通过排序子字符串得到另一个字符串 #hard #题型 #冒泡排序
对于一个字符串, 每次可以对于某一子字符串进行排序操作. 问能否经过若干操作变为目标字符串.
限制: 字符串长度 1e5; 所有元素为 0-9
思路0: 
    intuition: 画出例子中从s变为t的位置变化关系. 猜测对于s中某一字符迁移到t中的某一位置, 与其发生交叉的数字都要比它大.
    问题变为, 如何检查「交叉」? 一开始想从s变为到t来考虑, 结果想不明白, 放弃
思路1: #冒泡排序
    证明了题目中的操作类似冒泡排序, 并且只需要长为2的相邻元素排序即可.
    那么, 如何检查是否合法? 我们遍历t, 对于当前的元素, 需要s中目标位置之前的元素都比它大 (去掉之前已经用过的元素). 注意到, 题目中的字符数量仅为10, 我们用一个 defaultdict(deque) 记录每个数字出现的位置. 对于t中当前数字x, 需要判断0...x-1的剩余数字中是否有index比x的首个位置更小的. 用完了x之后 popleft 即可. 具体见 [官答](https://leetcode.cn/problems/check-if-string-is-transformable-with-substring-sort-operations/solution/jian-cha-zi-fu-chuan-shi-fou-ke-yi-tong-guo-pai-2/)
    复杂度: O(C n) 这里的C为字符集的大小.
总结: 上面的intuition其实挺正确的. 但没有根据字符集的数量较小这一特点记录想下去, 有点可惜.
"""
    def isTransformable(self, s: str, t: str) -> bool:
        # 思路1: #冒泡排序
        pos = defaultdict(deque)
        for i,digit in enumerate(s):
            pos[int(digit)].append(i)
        for digit in t:
            d = int(digit)
            if not pos[d]: return False
            if any(pos[i] and pos[i][0] < pos[d][0] for i in range(d)): return False
            pos[d].popleft()
        return True

""" 按秩启发的并查集 """
class DisjointSetUnion:
    def __init__(self, n):
        self.n = n
        self.rank = [1] * n
        self.f = list(range(n))
    
    def find(self, x: int) -> int:
        if self.f[x] == x:
            return x
        self.f[x] = self.find(self.f[x])
        return self.f[x]
    
    def unionSet(self, x: int, y: int) -> bool:
        fx, fy = self.find(x), self.find(y)
        if fx == fy:
            return False

        if self.rank[fx] < self.rank[fy]:
            fx, fy = fy, fx
        
        self.rank[fx] += self.rank[fy]
        self.f[fy] = fx
        return True

""" 树状数组. 维护该数组的前缀最小值 """
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [float("inf")] * n      # 树状数组
        self.idRec = [-1] * n               # 记录树中最小值出现的位置 (原数组中的位置信息)
        self.lowbit = lambda x: x & (-x)        # 辅助函数: 取最小位
    
    def update(self, pos: int, val: int, identity: int):
        # 更新离散化后的位置pos的最小值为val, 该数据的实际序号为identity
        while pos > 0:
            if self.tree[pos] > val:
                self.tree[pos] = val
                self.idRec[pos] = identity
            pos -= self.lowbit(pos)

    def query(self, pos: int) -> int:
        # 查询小于pos的记录中的最小值
        minval, j = float("inf"), -1
        while pos < self.n:
            if minval > self.tree[pos]:
                minval = self.tree[pos]
                j = self.idRec[pos]
            pos += self.lowbit(pos)
        return j


    
sol = Solution()
result = [
    # sol.unhappyFriends(n = 4, preferences = [[1, 2, 3], [3, 2, 0], [3, 1, 0], [1, 2, 0]], pairs = [[0, 1], [2, 3]]),
    # sol.unhappyFriends(n = 4, preferences = [[1, 3, 2], [2, 3, 0], [1, 3, 0], [0, 2, 1]], pairs = [[1, 3], [0, 2]]),
    # sol.minCostConnectPoints(points = [[0,0],[2,2],[3,10],[5,2],[7,0]]),
    sol.isTransformable(s = "34521", t = "23415"),
    sol.isTransformable(s = "12345", t = "12435"),
]
for r in result:
    print(r)
