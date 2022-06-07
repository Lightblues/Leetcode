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
# from structures import ListNode, TreeNode

""" 
https://leetcode.cn/contest/weekly-contest-266
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 2062. 统计字符串中的元音子字符串 #easy #题型
要求统计连续子序列的数量. 条件为: 1) 所有元素为元音字符 2) 包含所有aeiou五个元素.
思路1: 暴力检索. 时间复杂度 O(n^2)
    技巧: 这里要检查数组包括的所有元素, 天然就是 set 问题.
思路2: #双指针.
    先用re抽取所有仅由元音组成的子串, 对于每一个符合要求的子串, 双指针遍历.
    具体而言, 存储左右指针内包含的元音数量. 遍历有指针的过程中, 维护左指针使得「左右指针包含的包含所有元音的最短序列」, 这样, 以右指针结尾的包含左右元音的子串数量为 left+1.
"""

    def countVowelSubstrings(self, word: str) -> int:
        """ navie 方式. 遍历所有子序列, 对每个子串检测, 时间复杂度为 O(n^3)
        官方给了个简化的 O(n^2) 代码 [here](https://leetcode.cn/problems/count-vowel-substrings-of-a-string/solution/tong-ji-zi-fu-chuan-zhong-de-yuan-yin-zi-evp9/) """
        vowels = "aeiou"
        # def test(s):
        #     for ch in s:
        #         if ch not in vowels: return False
        #     for v in vowels:
        #         if v not in s: return False
        #     return True
        vowelSet = set(vowels)
        def test(s):
            s = set(s)
            return s&vowelSet == vowelSet and s|vowelSet == vowelSet
        ans = 0
        for i in range(len(word)):
            for j in range(i, len(word)):
                if test(word[i:j+1]): ans += 1
        return ans

    def countVowelSubstrings(self, word: str) -> int:
        """ 双指针 O(n)
[here](https://leetcode.cn/problems/count-vowel-substrings-of-a-string/solution/on-shuang-zhi-zhen-xie-fa-by-endlesschen-6dkt/)
"""
        vowelSubs = re.findall(r'[aeiou]+', word)
        ans = 0
        ch2idx = {ch:i for i,ch in enumerate("aeiou")}
        for sub in vowelSubs:
            left = 0
            count = [0] * 5
            for ch in sub:
                count[ch2idx[ch]] += 1
                while count[ch2idx[sub[left]]]>1:
                    count[ch2idx[sub[left]]] -= 1
                    left += 1
                if all(c>0 for c in count):
                    ans += left+1
        return ans


    """ 2063. 所有子字符串中的元音
返回所有子字符串中, 出现的voweld的个数"""
    def countVowels(self, word: str) -> int:
        wList = [1 if ch in "aeiou" else 0 for ch in word]
        n = len(wList)
        ans = 0
        for i,isVowel in enumerate(wList):
            if isVowel:
                ans += (i+1) * (n-i)
        return ans
    
    """ 2064. 分配给商店的最多商品的最小值 #medium #二分
将一组商品分配给n家商店, 每家店只能有一种商品 (也可以没有商品). 要求一种最「平均」的分配方式, 也即这些店中的商品数量最大值达到最小.
限制: 商品种类 m = 1e5, 每一种的最大数量 a = 1e5
思路1: #二分查找 每次检查的复杂度为 m, 二分的范围最大为 a, 因此时间复杂度为 O(m*log(a)).
    左右边界: sum(quantities)/n), quantities[-1]+1
    注意二分的边界: 这里的题型是「满足条件的最小值」. 因此不满足时缩小左边界 `left = mid+1`, 最后返回 `left`.
说明: 出了手动写二分算法之外, [here](https://leetcode.cn/problems/minimized-maximum-of-products-distributed-to-any-store/solution/er-fen-da-an-by-endlesscheng-aape/)
    直接调用了 go 中的 `sort.Search` 函数, 简化了代码. 
    类似的, 在 Python 中可采用 `bisect.bisect_left`, 语法有所不同, 思路是一样的 (其实都是在一个range数组中二分查找).
"""
    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        # s = sum(quantities)
        # avg = s//n
        
        # q = len(quantities)
        quantities.sort()
        # cumsum = itertools.accumulate(quantities, initial=0)
        left, right = math.ceil(sum(quantities)/n), quantities[-1]
        def check(a):
            remain = n
            for q in quantities:
                remain -= math.ceil(q/a)
                if remain < 0: return False
            return True
        while left < right:
            mid = (left+right)//2
            if not check(mid):
                left = mid+1
            else:
                right = mid
        return left

    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        """ 参考 [here](https://leetcode.cn/problems/minimized-maximum-of-products-distributed-to-any-store/solution/er-fen-da-an-by-endlesscheng-aape/)
        相较于 go 中的 `sort.Search` 函数, 采用了 `bisect.bisect_left`, 语法有所不同, 思路是一样的. """
        def check(a):
            remain = n
            for q in quantities:
                remain -= math.ceil(q/a)
                if remain < 0: return False
            return True
        idx = bisect.bisect_left(list(1, range(int(1e5))), 1, key=check)
        return idx+1
    
    """ 2065. 最大化一张图中的路径价值 #hard #DFS
给定带权图, 每个节点有分数. 在 maxTime 时限下, 从0回到0, 找到最大分数的路径. 注意, 节点可以重复访问
限制: 每个节点的相连边最多为4; 由于 `10 <= time_j, maxTime <= 100`, 所以最大搜索深度为 10. 
思路1: 暴力DFS, 注意是可重复访问的
    本题的特殊之处在于节点可重复访问. 
    题中对于图有着较多的限制, 采用最暴力的 DFS, `4**10` 也不超时.
"""
    def maximalPathQuality(self, values: List[int], edges: List[List[int]], maxTime: int) -> int:
        """ 一开始用 deepcopy 超时了, 性能比较低; 换成手动复制就OK """
        n = len(values)
        g = [[] for _ in range(n)]
        for u,v,w in edges:
            g[u].append((v,w))
            g[v].append((u,w))
        
        target = 0 # 回到原点

        ans = values[target]
        def dfs(u: int, remain: int, visited: set):
            nonlocal ans
            for v,w in g[u]:
                # 注意避免 deepcopy! 效率很低
                # newVisited = deepcopy(visited)
                newVisited = set(visited)
                if w > remain: continue
                newVisited.add(v)
                if v==target:
                    ans = max(ans, sum(values[i] for i in newVisited))
                dfs(v, remain-w, newVisited)
        dfs(0, maxTime, {0})
        return ans

    def maximalPathQuality(self, values: List[int], edges: List[List[int]], maxTime: int) -> int:
        n = len(values)
        g = [[] for _ in range(n)]
        for u,v,w in edges:
            g[u].append((v,w))
            g[v].append((u,w))
        
        target = 0 # 回到原点

        ans = values[target]
        def dfs(u: int, remain: int):
            nonlocal ans
            for v,w in g[u]:
                if w > remain: continue
                path.append(v)
                if v==target:
                    ans = max(ans, sum(values[i] for i in set(path)))
                dfs(v, remain-w)
                path.pop()
        path  = [0]
        dfs(0, maxTime)
        return ans

sol = Solution()
result = [
    sol.countVowelSubstrings(word = "aeiouu"),
    sol.countVowelSubstrings("cuaieuouac"),
    
    # sol.countVowels(word = "aba"),
    # sol.countVowels(word = "noosabasboosa"),
    
    # sol.minimizedMaximum(n = 6, quantities = [11,6]),
    # sol.minimizedMaximum(n = 7, quantities = [15,10,10]),
    
    # sol.maximalPathQuality(values = [0,32,10,43], edges = [[0,1,10],[1,2,15],[0,3,10]], maxTime = 49),
    # sol.maximalPathQuality(values = [5,10,15,20], edges = [[0,1,10],[1,2,10],[0,3,10]], maxTime = 30),
    
]
for r in result:
    print(r)
