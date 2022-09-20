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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
    
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 6181. 最长的字母序连续子字符串的长度 """
    def longestContinuousSubstring(self, s: str) -> int:
        s = list(ord(c)-ord('a') for c in s+"0")
        ans = 0
        idx = 0
        for i,ch in enumerate(s):
            if i>0 and ch!=s[i-1]+1:
                ans = max(ans, i-idx)
                idx = i
            ans = max(ans, i-idx)
        return ans
    
    """ 6182. 反转二叉树的奇数层 #medium 给定一颗完全二叉树, 要求翻转其第 1,3,5... 层. 限制: 节点数量 2^14
思路1: 暴力求解, 记录每一层的节点序列.
    空间复杂度: O(n) 这里的n是每层的最大节点数.
"""
    def reverseOddLevels(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        s = [root]
        flip = True
        while s[0]:
            nxt = list(itertools.chain(*[[t.left, t.right] for t in s]))
            # print(list(t.val for t in s))
            # print([t.val for t in nxt])
            if flip:
                n = len(s)
                for i,node in enumerate(s):
                    node.left = nxt[2*n-1-i*2]
                    node.right = nxt[2*n-1-i*2-1]
            else:
                n = len(s)
                for i in range(n):
                    s[n-1-i].left = nxt[i*2]
                    s[n-1-i].right = nxt[i*2+1]
            flip = False if flip else True
            s = nxt
        return root

    
    """ 6183. 字符串的前缀分数和 #hard 简单考察 #Trie 字典树 """
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        class Node():
            def __init__(self, ch) -> None:
                self.ch = ch
                self.cnt = 0    # 当前前缀出现的次数.
                self.childs = defaultdict(Node)
        root = Node(" ")
        def add(word: str, root: Node):
            # 加word
            for ch in word:
                if ch not in root.childs: root.childs[ch] = Node(ch)
                root = root.childs[ch]
                root.cnt += 1
        def cnt(word: str, root: Node):
            # 查询题目要求
            ans = 0
            for ch in word:
                root = root.childs[ch]
                ans += root.cnt
            return ans
        for word in words: add(word, root)
        ans = []
        for word in words: ans.append(cnt(word, root))
        return ans

    
sol = Solution()
result = [
    # sol.longestContinuousSubstring("abacaba"),
    # sol.longestContinuousSubstring("abcde"),
    # sol.longestContinuousSubstring("a"),
    sol.sumPrefixScores(["abc","ab","bc","b"]),
    sol.sumPrefixScores(["abcd"])
]
for r in result:
    print(r)
