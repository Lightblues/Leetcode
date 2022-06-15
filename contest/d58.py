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

""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-58
@2022 """
class Solution:
    """ 1957. 删除字符使字符串变好 """
    def makeFancyString(self, s: str) -> str:
        last = ""
        cnt = 0
        ans = ""
        for ch in s:
            if ch!=last:
                last, cnt = ch, 1
                ans += ch
            else:
                if cnt >=2: continue
                cnt += 1
                ans += ch
        return ans
    
    """ 1958. 检查操作是否合法 """
    def checkMove(self, board: List[List[str]], rMove: int, cMove: int, color: str) -> bool:
        n = 8
        opps = "W" if color=='B' else "B"
        directions = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]
        def inBoard(r, c):
            return 0<=r<n and 0<=c<n
        for dr,dc in directions:
            r,c = rMove, cMove
            nr,nc = r+dr, c+dc
            if not inBoard(nr,nc) or board[nr][nc] != opps: continue
            while inBoard(nr,nc) and board[nr][nc] == opps:
                nr,nc = nr+dr, nc+dc
            if inBoard(nr,nc) and board[nr][nc] == color:
                return True
        return False
    
    """ 1959. K 次调整数组大小浪费的最小总空间 #medium #题型
题目的背景是动态内存分配: 对于一个数组, 可以在其中调整k的所分配的内存, 要求最小的总空间浪费.
抽象: 对于一个数组, 将其分成 k+1 个部分, 每个部分取最大值矩形进行覆盖, 要求所有矩形的面积和最小.
限制: 数组长度 n<=200, 调整次数 0<=k<n
思路1: #DP
    考虑采用动态规划求解. 每次利用之前状态的记录.
    具体而言, 记 `dp[i][j]` 表示 **覆盖数组的前i个元素, 使用j次调整(j+1个区间)所浪费的最小空间**.
        于是, 有 `dp[i][j] = min_ii { dp[ii][j] + g[ii+1][i] }`
        对于每个 `dp[i][j]`, 我们将 0...i 区间根据 ii 进行拆分, 将右边分成一个区间, 左边进行 j-1 次调整.
        这里的 `g[a][b]` 表示区间 [a,b] 分成一组的空间浪费, 可以预先双重遍历计算出来.
        具体实现中, 可以将更新公式中的 j维度省略.
    说明: 为了要求 num[0...ii] 被分成 j 个区间, 显然 ii 必须小于 j. 但实际上由于 ii<=j-1 时空间浪费必然为0, 因此在下面的代码中没有考虑这一边界情况.
    [官答](https://leetcode.cn/problems/minimum-total-space-wasted-with-k-resizing-operations/solution/k-ci-diao-zheng-shu-zu-da-xiao-lang-fei-wxg6y/)
"""
    def minSpaceWastedKResizing(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # g[i][j] 表示 nums[i:j] 作为一个组需要多少代价
        g = [[0] * n for _ in range(n)]
        acc = list(accumulate(nums, initial=0))
        for i in range(n):
            mx = nums[i]
            for j in range(i, n):
                mx = max(mx, nums[j])
                g[i][j] = mx * (j-i+1) - (acc[j+1] - acc[i])
        # 初始化: 只有一个组 (k=0)
        dp = g[0][:]
        # 遍历 k = 1...k
        for _ in range(1, k+1):
            new = dp[:]
            # update dp[i]
            for i in range(n):
                # dp[i][j] = min_ii { dp[ii][j] + g[ii+1][i] } 遍历 ii=0...i-1 尝试对于 nums[:i+1] 进行分割
                # 这里将 j维度省略.
                for ii in range(i):
                    new[i] = min(new[i], dp[ii] + g[ii+1][i])
            dp = new
        return dp[-1]
        
    
    """ 1960. 两个回文子字符串长度的最大乘积 #hard #题型
给定一个字符串, 要求找到两个连续的不相交子串 (0 <= i <= j < k <= l < s.length), 都是长度为奇数的回文串, 使得两者的乘积最大.
限制: 长度 1e5
思路1: #Manacher 算法计算所有回文串长度, 然后分别计算左右两侧的最大回文串长度, 遍历匹配.
    [here](https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-substrings/solution/ma-la-che-suan-fa-xiang-xi-tu-jie-by-new-m2zj/)
    首先, 利用 Manacher 马拉车算法计算所有位置为中心的回文串长度. 算法概要:
        初始化: 遍历 i=0...n-1 为当前位置; 初始化 mx=-1 表示之前的回文串拓展到达的最右边界, j=-1 表示mx所对应的中心位置.
        拓展: 当 i<=mx 时, 我们可以利用已有信息, 初始化 `plen[i] = min(plen[2*j-i], mx-i)`; 否则初始化为 1 (仅包括i位置)
            从 plen[i] 出发, 向两侧检测拓展回文串
        更新: 若本次拓展的位置超过了之前的边界 `i+plen[i]>mx` 则更新 mx, j.
        说明: plen[i] 表示一半的长度, 可以从0开始也可以从1开始, 需要注意代码.
    然后, 如何保证两个子串不相交?
        我们分别从左右两侧遍历, 例如 left[i] 表示 nums[:i+1] 中所包含的最大回文长度. 然后根据分割点, 匹配左右位置即可.
        思路: #DP 在遍历 i=0...n-1 的过程中, 维护一个此前的中心位置 l 和最大长度 mx.
            当进入下一个位置i时, 不断尝试右移l, 直到 `l + plen[l] -1 >= i`. 
            l+plen[l] 可能会超过当前位置i, 此时需要进行裁剪. 这需要和 l+=1 以及 mx 的计算相匹配.
        注意: 这里维护的指针 l 的更新公式中, 确保了 (l, i) 范围内不会出现更长的合法回文串. 其实和 Manacher 算法中的思想类似.
        这里看上去简单, 实际折腾了很久 —— 主要写之前没有考虑dp的更新公式.
"""
    def maxProduct(self, s: str) -> int:
        # 计算每个位置的回文串长度
        n = len(s)
        plen = [1] * n
        j, mx = -1, -1
        for i in range(n):
            if i<=mx:
                plen[i] = min(plen[2*j-i], mx-i)
            while 0<=i-plen[i] and i+plen[i]<n and s[i+plen[i]]==s[i-plen[i]]:
                plen[i] += 1
            if i+plen[i]>mx:
                j, mx = i, i+plen[i]
        # 计算 nums[0...i] 范围内的最长回文串长度
        leftLens = [1] * n
        l, mx = 0, 1
        for i in range(1, n):
            # while l+1<n-1 and l + plen[l+1] <= i:
            #     l += 1
            #     mx = max(mx, 2*plen[l]-1)
            while l + plen[l] -1 < i: l += 1
            mx = max(mx, 2*(i-l)+1)
            leftLens[i] = mx
        rightLens = [1] * n
        r, mx = n-1, 1
        for i in range(n-2, -1, -1):
            while r - plen[r] + 1 > i:
                r -= 1
            mx = max(mx, 2*(r-i)+1)
            rightLens[i] = mx
        # 遍历匹配两部分
        ans = 1
        for i in range(n-1):
            ans = max(ans, leftLens[i]*rightLens[i+1])
        return ans
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [
    # sol.makeFancyString(s = "aaabaaaa"),
    # sol.checkMove(board = [[".",".",".",".",".",".",".","."],[".","B",".",".","W",".",".","."],[".",".","W",".",".",".",".","."],[".",".",".","W","B",".",".","."],[".",".",".",".",".",".",".","."],[".",".",".",".","B","W",".","."],[".",".",".",".",".",".","W","."],[".",".",".",".",".",".",".","B"]], rMove = 4, cMove = 4, color = "W"),
    # sol.checkMove(board = [[".",".",".","B",".",".",".","."],[".",".",".","W",".",".",".","."],[".",".",".","W",".",".",".","."],[".",".",".","W",".",".",".","."],["W","B","B",".","W","W","W","B"],[".",".",".","B",".",".",".","."],[".",".",".","B",".",".",".","."],[".",".",".","W",".",".",".","."]], rMove = 4, cMove = 3, color = "B"),
    # sol.minSpaceWastedKResizing(nums = [10,20], k = 0),
    # sol.minSpaceWastedKResizing(nums = [10,20,30], k = 1),
    # sol.minSpaceWastedKResizing(nums = [10,20,15,30,20], k = 2),
    sol.maxProduct(s = "ababbb"),
    sol.maxProduct(s = "zaaaxbbby"),
    sol.maxProduct("ggbswiymmlevedhkbdhntnhdbkhdevelmmyiwsbgg")
    
]
for r in result:
    print(r)
