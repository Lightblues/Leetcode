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
https://leetcode.cn/contest/weekly-contest-247
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1913. 两个数对之间的最大乘积差 """
    def maxProductDifference(self, nums: List[int]) -> int:
        nums.sort(reverse=True)
        return nums[0]*nums[1] - nums[-1]*nums[-2]
    
    """ 1914. 循环轮转矩阵 #medium
给定一个 (M,N) 大小的矩阵, 从外到内分成一圈一圈的圆周, 要求把每个元素沿着圆周转动k步.
限制: M,N <= 50; k <= 1e9
思路: 简单计算公式
    实现一个函数 `f(m,n,i)`, 计算「对于长宽为 (m,n) 的环的第i个位置的元素坐标」.
    然后从外到内移动每一层上的所有元素即可
"""
    def rotateGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m,n = len(grid), len(grid[0])
        def f(m,n,i):
            """ 对于长宽为 (m,n) 的环, 计算第i个位置的元素坐标 """
            circle = 2*(m+n-2)
            i %= circle
            # 分别在四条边上, 可以拿个例子验证一下
            if i < m-1:
                return i,0
            elif i < m+n-2:
                return m-1, i-(m-1)
            elif i < 2*m+n-3:
                return 2*m+n-3-i, n-1
            else:
                return 0, 2*m+2*n-4 - i
        ans = [[0]*n for _ in range(m)]
        bias = 0    # 坐标偏移
        while m>0 and n>0:
            # 当前环的周长, 对于每一个元素移动到新的位置上
            circle = 2*(m+n-2)
            dd = k%circle
            for i in range(circle):
                x,y = f(m,n,i)
                nx,ny = f(m,n,i+dd)
                ans[nx+bias][ny+bias] = grid[bias+x][bias+y]
            bias += 1
            m,n = m-2, n-2
        return ans
    
    """ 1915. 最美子字符串的数目 #medium #题型 #前缀和
定义「美子串」为: 字符串中, 字符的数量为奇数的字符最多出现一个. 现给定一个字符串, 求其所有的连续子串中「美子串」的数量.
约束: 字符串长度 1e5, 字符只包含 a-j 10种.
思路1: 枚举 #前缀和 #状压
    利用字符种类最多只有10个的限制, 可以用一个长度为10的二进制数表示这些数字的奇偶状态. 例如 aba 所对应 `...010` 表示b出现了奇数次
    对于当前枚举的位置j, 假设其前缀和为s[j], 若对于位置对 (i,j) 而言,
        若 `s[i]==s[j]`, 则说明 `word[i+1:j+1]` 这一子串中所有的字符都出现了偶数次.
        若 `s[i]^s[j]` 的结果仅包含一个非零位, 说明 `word[i+1:j+1]` 范围内有仅有一个字符出现了奇数次.
    因此, 我们在遍历字符串计算前缀和的过程中, 用一个计数器记录之前前缀和出现次数, 按照上面的规则累计即可.
    注意: 空字符串的前缀和定义为0
    复杂度: O(n)
    from [灵神](https://leetcode.cn/problems/number-of-wonderful-substrings/solution/qian-zhui-he-chang-jian-ji-qiao-by-endle-t57t/)
总结: 对于 (i,j) 对匹配计数的问题, 这里需要遍历的过程中直接进行累计计算, 而不是遍历完得到完整的cnt再处理. 这是两种不同的思路, 需要加强前一种方式的思维.
    
"""
    def wonderfulSubstrings(self, word: str) -> int:
        cnt = [0] * 2**10
        cnt[0] = 1  # 初始前缀和为 0，需将其计入出现次数
        ans = 0
        s = 0
        for ch in word:
            s ^= 1 << (ord(ch)-ord('a'))    # 更新前缀和
            ans += cnt[s]       # (i,j) 区间内的字符个数均为偶数
            for i in range(10): # 允许出现一个字符个数为奇数
                ans += cnt[s^(1<<i)]
            cnt[s] += 1     # 更新前缀和出现次数
        return ans
    
    
    """ 1916. 统计为蚁群构筑房间的不同顺序 #hard
归纳为, 给定一个树, 从根节点出发从上往下不断增加节点, 只有当父节点已有的时候才能构造孩子节点. 问有多少种构造方式.
限制: 节点数量 1e5, 对于结果取模
思路1: #DFS
    归纳过程: 对于某一节点, 假设有两个孩子节点
        先不考虑孩子节点内部的顺(看作是唯一的), 若两孩子的size分别为s1,s2, 这两棵子树构造过程中需要保证内部的顺序一致, 因此共有 comb(s1+s2, s2) 种构造方式.
        一般地, 对于一组孩子, 若其孩子包含节点数量为childSizes, 则构造方法共有 `ans' = prod{ comb(s[...i], childSizes[i]) }`, 其中s[...i]是前缀和.
        再考虑每个孩子内部的顺序分别为nums, 则构造方法共有 `ans = ans' * prod{nums}` 种
    按照上述公式, DFS 即可. 注意DFS函数需要返回当前节点的构造方法数和子树大小两个值.
"""
    def waysToBuildRooms(self, prevRoom: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(prevRoom)
        g = [[] for _ in range(n)]
        for i in range(1,n):
            g[prevRoom[i]].append(i)
        # 
        def dfs(root):
            if len(g[root]) == 0:
                return 1,1
            ans = 1
            childSizes = []
            for child in g[root]:
                a,s = dfs(child)
                ans = ans * a % MOD
                childSizes.append(s)
            s = childSizes[0]
            for i in range(1, len(childSizes)):
                cs = childSizes[i]
                s += cs
                ans = ans * math.comb(s, cs) % MOD
            return ans,s+1
        ans, _ = dfs(0)
        return ans
    

    
sol = Solution()
result = [
    # sol.rotateGrid(grid = [[40,10],[30,20]], k = 1),
    # sol.rotateGrid(grid = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], k = 2),
    
    sol.wonderfulSubstrings(word = "aba"),
    sol.wonderfulSubstrings(word = "aabb"),
    # sol.waysToBuildRooms(prevRoom = [-1,0,1]),
    # sol.waysToBuildRooms(prevRoom = [-1,0,0,1,2]),
]
for r in result:
    print(r)
