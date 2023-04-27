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
from functools import lru_cache, reduce, partial # cache
cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-258
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 2000. 反转单词前缀 """
    def reversePrefix(self, word: str, ch: str) -> str:
        # if ch not in word: return word
        # i = word.index(ch)
        # 相较于index若没有出现回报错, find 会返回 -1
        i = word.find(ch)
        return word[:i+1][::-1] + word[i+1:]
    
    """ 2001. 可互换矩形的组数 """
    def interchangeableRectangles(self, rectangles: List[List[int]]) -> int:
        cnt = Counter()
        for w,h in rectangles:
            # 用 Fraction 计数
            cnt[Fraction(w,h)] += 1
        ans = 0
        for c in cnt.values():
            # comb 得到组合数量
            ans += math.comb(c, 2)
        return ans
    
    """ 2002. 两个回文子序列长度的最大乘积 #medium
约束: 字符串长度最大为 12
思路1: #暴力 划分, 搜索
    对于idx字符而言, 将其划分到 字符串1/2/不使用 3中状态, 每次检查的复杂为子串长度. 因此复杂度为 O(n * 3^n)
    [灵神](https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/solution/go-bao-sou-by-endlesscheng-ivn0/)
思路2: 状态压缩
    先进行状态压缩. 对于每一个子序列计算是否为回文串(及其长度), 复杂度为 O(n * 2^n)
    注意, 这里所有回文串的数量最坏情况下是 m = 2^n 量级的.
    然后, 可以对于m个回文串两两匹配, 判断是否有重复使用的字符, 但注意最坏情况下是 `m^2 = 4^n` 级别的; 反而更差.
总结: 1. 在本题数量级较小的情况下, 暴力划分是可选的一种方案; 2. 不要无脑想到状态压缩等方案, 应该先进行复杂度的分析.
        
"""
    def maxProduct(self, s: str) -> int:
        """ 暴力搜索
        [灵神](https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/solution/go-bao-sou-by-endlesscheng-ivn0/) """
        def isPalindromic(s: list) -> bool:
            return s == s[::-1]
        stra = []
        strb = []
        ans = 0
        def dfs(i):
            nonlocal ans
            if i == len(s):
                if isPalindromic(stra) and isPalindromic(strb):
                    ans = max(ans, len(stra) * len(strb))
                return
            stra.append(s[i])
            dfs(i+1)
            stra.pop()
            
            strb.append(s[i])
            dfs(i+1)
            strb.pop()
            
            dfs(i+1)
        dfs(0)
        return ans
    
    
    """ 2003. 每棵子树内缺失的最小基因值 #hard #题型 #启发式合并
给定一棵家族树, 每个人的基因都是独特的. 基因值在 [1, 1e5] 区间内. 现在要求家族树上每个人的子树中, 「缺失的最小基因值」. 例如, 若子树包含 `1,2,3,5,6...` 那个就要返回 4
限制: 家族树大小 1e5
[here](https://leetcode.cn/problems/smallest-missing-genetic-value-in-each-subtree/solution/go-qi-fa-shi-he-bing-by-endlesscheng-kmff/)
思路1: #启发式合并 [OI wiki](https://oi-wiki.org/graph/dsu-on-tree/)
    基本的思路是, 在DFS的过程中, 返回子树所含含的数字集合, 遍历所有子节点之后对这些集合求union, 然后计算 `mex`. 计算情况下, 每一个节点都包含 n 个数字, 合并这些子树(并找到mex)的代价是 `O(n)`, 这样, 整体的复杂度 `O(n^2)` 不行
    这里 #启发式合并 的意思是, 在选择数组合并的过程中, 尽量选择将小集合合并到大集合中 (类似并查集中启发式选秩更大的作为root). 这样, 大的子节点返回的集合将不会进行合并操作 (只会合并其他小集合)
    可以证明这样贪心之后的复杂度是 `O(n log(n))`
    另外, 在递归dfs子节点的时候, 利用子节的mex值作为下届, 由此出发, 每次+1来搜索当前节点的mex. 这样可以避免链式的节点都包括 `1,2,...,n-k` 导致搜索需要 O(n) 时间的情况.
思路2: 利用基因值不同的特点
    由于要求mex并且基因值的范围在 [1, 1e5], 因此若子树不包含1则答案就是1. 利用基因值都不相同的特点, 我们 **只需要考虑基因值为1的节点往上的祖先节点**.
    这样, 我们维护一个全局的 `inSet` 记录子树上所有的基因值. 先找到基因值1的节点x, 在依次遍历其祖先的过程中, 加入祖先所包含的其他子树的数字到 `inSet`, 然后更新mex即可. 并且注意到, 沿着该路径往上的过程中, 节点的mex是递增的.
    复杂度: 我们最多遍历一次节点; 并且在尝试mex的过程中也是递增的. 所以总的复杂度是 `O(n)`
"""
    def smallestMissingValueSubtree(self, parents: List[int], nums: List[int]) -> List[int]:
        """ #启发式合并
        [here](https://leetcode.cn/problems/smallest-missing-genetic-value-in-each-subtree/solution/go-qi-fa-shi-he-bing-by-endlesscheng-kmff/) """
        n = len(parents)
        g = [[] for _ in range(n)]
        for i,p in enumerate(parents):
            # 注意避免root节点
            if i==0: continue
            g[p].append(i)
        # 
        mex = [1] * n
        def dfs(idx):
            inSet = set()
            inSet.add(nums[idx])
            for child in g[idx]:
                childSet = dfs(child)
                if len(childSet) > len(inSet):
                    inSet, childSet = childSet, inSet
                """ 注意, union 操作会开辟新的set出来, 复杂度是 len(s1) + len(s2)
                而将小集合合并到大集合的复杂度为 len(s2) """
                # inSet = inSet.union(childSet)
                for c in childSet:
                    inSet.add(c)
                mex[idx] = max(mex[idx], mex[child])
            # 从子节点的最大mex出发, 搜索当前节点的mex
            while mex[idx] in inSet:
                mex[idx] += 1
            return inSet
        dfs(0)
        return mex


    def smallestMissingValueSubtree(self, parents: List[int], nums: List[int]) -> List[int]:
        """ 思路2: 利用基因值不同的特点 """
        n = len(parents)
        g = [[] for _ in range(n)]
        for i,p in enumerate(parents):
            # 注意避免root节点
            if i==0: continue
            g[p].append(i)
        # 
        mex = [1] * n
        inSet = set()   # 全局的set, 记录了访问过的 (并且我们关心) 的节点. 利用了基因值不同的特点
        def f(idx):
            """ 递归访问idx节点, 记录所有访问过的节点的基因值 """
            inSet.add(nums[idx])
            for child in g[idx]:
                # 避免重复访问
                if nums[child] in inSet: continue
                f(child)
        # idx = nums.find(1) # 注意list没有find操作
        # if idx==-1: return mex
        if 1 not in nums: return mex
        idx = nums.index(1)
        curr = 2
        while idx >= 0:
            f(idx)
            while curr in inSet:
                curr += 1
            mex[idx] = curr
            idx = parents[idx]
        return mex

sol = Solution()
result = [
    # sol.interchangeableRectangles(rectangles = [[4,8],[3,6],[10,20],[15,30]]),
    # sol.interchangeableRectangles(rectangles = [[4,5],[7,8]]),
    
    # sol.maxProduct(s = "leetcodecom"),
    # sol.maxProduct(s = "bb"),
    
    sol.smallestMissingValueSubtree(parents = [-1,0,0,2], nums = [1,2,3,4]),
    sol.smallestMissingValueSubtree(parents = [-1,0,1,0,3,3], nums = [5,4,6,2,1,3]),
]
for r in result:
    print(r)
