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
from functools import lru_cache, reduce, partial, cache
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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    """ 6108. 解密消息 """
    def decodeMessage(self, key: str, message: str) -> str:
        chs = []
        for ch in key:
            if ch==' ' or ch in chs: continue
            chs.append(ch)
        keymap = dict(zip(chs, string.ascii_lowercase[:len(chs)]))
        keymap[' '] = ' '
        return "".join(keymap[ch] for ch in message)
            
    """ 6111. 螺旋矩阵 IV #medium
给定一个 (M,N) 的gird, 顺时针方向往里面填数字, 数字由一个头为head的链表提供. 剩余的空格填入-1.
思路0: 用一个函数 `f(m,n, idx)` 统一计算在一个 (m,n) 的圆环中第idx个位置的坐标.
    每一圈的周长为 (2m+2n-4), 从外往里一圈一圈填充, 每填一圈, m,n 减去2, 同时 bias 增加1.
    注意, 在上面周长计算公式中, 当 m==n==1 时结果为0, 而实际上有一个点需要填充! 在下面的代码中进行了特判
思路2: 按层 #模拟
    和上面的思路一样, 不过维护了每层上下左右点位置, 然后便利右下左上四条边即可.
    见 0059题 [官答](https://leetcode.cn/problems/spiral-matrix-ii/solution/luo-xuan-ju-zhen-ii-by-leetcode-solution-f7fp/
思路1: #模拟 轮转前进方向
    同 0059题, 这里可以利用 -1 特殊变量以及四个方向的轮转, 来更新每一次的前进方向.
    具体而言, 四个方向 右下左上 轮转 (可以用一个iDirection来表示, 每次 `(iDirection+1)%4` 更新), 当更新后的位置不合法或者遇到-1时, 更新方向.
"""
    def spiralMatrix(self, m: int, n: int, head: Optional[ListNode]) -> List[List[int]]:
        grid = [[-1] * n for _ in range(m)]
        def f(m,n, idx):
            circle = 2 * (m+n-2)
            assert idx < circle
            if idx<n-1:
                return 0, idx
            elif idx<m+n-2:
                return idx-n+1, n-1
            elif idx<2*n+m-3:
                return m-1, 2*n+m-3-idx
            else:
                return circle-idx, 0
        bias = 0
        while m>0 and n>0 and head:
            # 特判! 此时 2*(m+n-2)==0 !
            if m==n==1:
                grid[bias][bias] = head.val
                return grid
            for i in range(2*(m+n-2)):
                x, y = f(m,n, i)
                grid[x+bias][y+bias] = head.val
                head = head.next
                if head is None: return grid
            bias += 1
            m, n = m-2, n-2
        return grid

    def generateMatrix(self, n: int) -> List[List[int]]:
        """ 思路2: 按层 #模拟
        [官答](https://leetcode.cn/problems/spiral-matrix-ii/solution/luo-xuan-ju-zhen-ii-by-leetcode-solution-f7fp/) """
        matrix = [[0] * n for _ in range(n)]
        num = 1
        left, right, top, bottom = 0, n - 1, 0, n - 1

        while left <= right and top <= bottom:
            for col in range(left, right + 1):
                matrix[top][col] = num
                num += 1
            for row in range(top + 1, bottom + 1):
                matrix[row][right] = num
                num += 1
            if left < right and top < bottom:
                for col in range(right - 1, left, -1):
                    matrix[bottom][col] = num
                    num += 1
                for row in range(bottom, top, -1):
                    matrix[row][left] = num
                    num += 1
            left += 1
            right -= 1
            top += 1
            bottom -= 1

        return matrix

    
    def spiralMatrix(self, m: int, n: int, head: Optional[ListNode]) -> List[List[int]]:
        # 思路1
        grid = [[-1] * n for _ in range(m)]
        directions = [(0,1), (1,0), (0, -1), (-1,0)]    # 右下左上
        x,y = 0,0; didx = 0
        while head:
            grid[x][y] = head.val
            head = head.next
            dx,dy = directions[didx]
            nx, dy = x+dx, y+dy
            if nx<0 or nx>=m or dy<0 or dy>=n or grid[nx][dy]!=-1:
                didx = (didx+1)%4
            dx,dy = directions[didx]
            x, y = x+dx, y+dy
        return grid
    
    """ 6109. 知道秘密的人数 #medium #interest #题型
第1天有1个人知道秘密, 在经过delay天之后, 他会每天告诉一个新人, 直到经过forget天之后他忘记秘密. 问经过n天之后多少人知道秘密
限制: n 1e3; 对结果取模
思路1: #模拟 计算; 理解为 #DP
    记 f[i] 为第i天知道的人, 可知递推公式 `f[i+1] = f[i] - forgets[i] + news[i]`, 其中 `forgets[i]` 为第i天忘记的人, `news[i]` 为第i天新加的人
    我们用一个哈希表 news[i] 记录当天新知道秘密的人的数量, 可知有递推关系 `news[i] = sum{ news[i-forget+1]+...+news[i-delay] }`
    对于忘记的人显然有 `forgets[i] = news[i-forget]`
    复杂度: `O(n^2)`
    灵神总结这种方法为「填表法」; 注意到, 上面的 news 计算可以利用前缀和优化到 `O(n)`
思路2: 刷表法
    上面的这种是从当前日向前找, 还可以对当前日期影响的人往后「刷表」.
    注意到, 当天知道秘密的人可以分为 A「知道秘密，但还不能分享」和 B「知道秘密，且可以分享」两类.
    用一个 f 列表记录该天 B「知道秘密，且可以分享」的人. 则当前i可以影响的范围为 [i+delay...i+forget]; 另外统计日期n时的 A类人即可.
    [灵神](https://leetcode.cn/problems/number-of-people-aware-of-a-secret/solution/by-endlesscheng-2x0z/)
"""
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        MOD = 10**9 + 7
        news = defaultdict(int)
        news[1] = 1
        f = 1
        for i in range(2, n+1):
            nf = sum(news[j] for j in range(i-forget+1, i-delay+1)) % MOD
            news[i] = nf
            f = (f + nf - news[i-forget]) % MOD
        return f
    
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        """ 上面的算法可以利用前缀和油画到 O(n)
        from [here](https://leetcode.cn/problems/number-of-people-aware-of-a-secret/solution/by-endlesscheng-2x0z/) """
        MOD = 10 ** 9 + 7
        sum = [0] * (n + 1)
        sum[1] = 1
        for i in range(2, n + 1):
            f = sum[max(i - delay, 0)] - sum[max(i - forget, 0)]
            sum[i] = (sum[i - 1] + f) % MOD
        return (sum[n] - sum[max(0, n - forget)]) % MOD
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        """ 思路2: 刷表法. 注意遍历的边界
        O(n^2) """
        MOD = 10**9 + 7
        typeBs = [0] * (n + 1); typeBs[1] = 1
        cntA = 0
        for i in range(1, n+1):
            if i+delay > n:
                cntA += typeBs[i]
            for j in range(i+delay, min(i+forget, n+1)):
                typeBs[j] += typeBs[i]
        return (cntA + typeBs[n]) % MOD
    
    """ 6110. 网格图中递增路径的数目 #hard
给定一个grid, 问网格中有多少严格递增的路径. 对结果取模
约束: m,n <=1e3; 网格点 1e5
思路1 对于网格值 #排序 之后 #DP
    注意看例子 [[1,1],[3,4]], 以1结尾的路径有1条; 以3结尾的路径有 `[3],[1,3]` 2条; 以4结尾的路径有 `[4],[1,4],[1,3,4]` 3条
    可知, 以某点结尾的路径数量可由周围点的路径书递归计算.
    因此, 先构建 {value: idxs} 的哈希表, 然后对于值排序后进行上面的DP计算.
思路2: #记忆化搜索
    相较于上面排序后再DP, 也可以写成记忆化搜索, 代码会更加简洁.
"""
    def countPaths(self, grid: List[List[int]]) -> int:
        MOD = 10**9 + 7
        m,n = len(grid), len(grid[0])
        key2idxs = defaultdict(list)
        for i in range(m):
            for j in range(n):
                key2idxs[grid[i][j]].append((i,j))
        cnts = [[1]*n for _ in range(m)]
        for v in sorted(key2idxs.keys()):
            for x,y in key2idxs[v]:
                if x>0 and grid[x-1][y]<v:
                    cnts[x][y] = (cnts[x][y] + cnts[x-1][y]) % MOD
                if y>0 and grid[x][y-1]<v:
                    cnts[x][y] = (cnts[x][y] + cnts[x][y-1]) % MOD
                if x<m-1 and grid[x+1][y]<v:
                    cnts[x][y] = (cnts[x][y] + cnts[x+1][y]) % MOD
                if y<n-1 and grid[x][y+1]<v:
                    cnts[x][y] = (cnts[x][y] + cnts[x][y+1]) % MOD
        return sum(sum(r) for r in cnts) % MOD
    
    def countPaths(self, grid: List[List[int]]) -> int:
        """ 记忆化搜索 from https://leetcode.cn/problems/number-of-increasing-paths-in-a-grid/solution/ji-yi-hua-sou-suo-pythonjavacgo-by-endle-xecc/ """
        MOD = 10 ** 9 + 7
        m, n = len(grid), len(grid[0])
        @cache
        def dfs(i: int, j: int) -> int:
            res = 1
            for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):
                if 0 <= x < m and 0 <= y < n and grid[x][y] > grid[i][j]:
                    res += dfs(x, y)
            return res % MOD
        return sum(dfs(i, j) for i in range(m) for j in range(n)) % MOD

    
sol = Solution()
result = [
    # sol.decodeMessage(key = "the quick brown fox jumps over the lazy dog", message = "vkbs bs t suepuv"),
    # 注意链表不太好本地调试
    # sol.spiralMatrix(m = 3, n = 5, head = [3,0,2,6,8,1,7,9,4,2,5,5,0]),
    # sol.spiralMatrix(m = 1, n = 4, head = [0,1,2]),
    # sol.peopleAwareOfSecret(n = 6, delay = 2, forget = 4),
    # sol.peopleAwareOfSecret(n = 4, delay = 1, forget = 3),
    # sol.countPaths(grid = [[1,1],[3,4]]),
    # sol.countPaths(grid = [[1],[2]]),
    
]
for r in result:
    print(r)
