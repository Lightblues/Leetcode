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
https://leetcode.cn/contest/weekly-contest-190

T3 直接给 copilot 补出来了就离谱... 然后 T4 立马又被坑, 主要是边界问题, 居然 WA了好多次, DP 还是不熟.
@2022 """

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 1455. 检查单词是否为句中其他单词的前缀 """
    def isPrefixOfWord(self, sentence: str, searchWord: str) -> int:
        for i,word in enumerate(sentence.split()):
            if word.startswith(searchWord): return i+1
        return -1
    
    """ 1456. 定长子串中元音的最大数目 """
    def maxVowels(self, s: str, k: int) -> int:
        vowels = set('aeiou')
        acc = 0
        for i in range(k):
            if s[i] in vowels: acc += 1
        ans = acc
        for i in range(k, len(s)):
            if s[i] in vowels: acc += 1
            if s[i-k] in vowels: acc -= 1
            if acc>ans: ans = acc
        return ans
    
    """ 1457. 二叉树中的伪回文路径 #medium #题型 #copilot
给定一个二叉树, 定义一条从根节点到叶子结点的路径是「伪回文路径」的, 要求路径上的数字经过重排列为回文. 给定树, 求「伪回文路径」的数量.
限制: 节点数 1e5; 节点值的范围 1~9
思路1: #DFS, 记录当前遍历的路径
    提示: 「伪回文路径」的定义等价于, 奇数个的数字最多只能有一个!
        由于本题中节点值范围有限, 可以用二进制进行表示 (异或操作). 则条件变为: 二进制表示中1的次数不超过一次.
        可以用 `path & (path-1) == 0` 检查.
"""
    def pseudoPalindromicPaths (self, root: TreeNode) -> int:
        # from copilot. 被AI教代码...
        def dfs(node, path):
            if node is None: return 0
            path ^= 1 << node.val
            if node.left is None and node.right is None:
                return int(path & (path-1) == 0)
            return dfs(node.left, path) + dfs(node.right, path)
        return dfs(root, 0)


    """ 1458. 两个子序列的最大点积 #hard #题型 给定两个数组, 要求他们的一对相同长度的非空子序列的最大点积. 限制: 长度n 500, 数值范围 -100~100
思路1: #DP 记 `f(i,j)` 为用两个数组的前 i,j 个元素, 并且 arr1[i] * arr2[j] 进行匹配的最大分数.
    则有递推: `f(i,j) = arr1[i]*arr2[j] + max{ f(0...i-1, 0...j-1), 0 }` (注意若该区间f取值都为负数, 则可以选择不用)
        为了求区域极大值, 在遍历第i行过程中, 可以用一个 `mx[i,j]` 记录 f(0...i, 0...j-1) 的最大值.
思路2: 实际上上面第二个辅助元素可以省略. 定义 `f(i,j)` 为用两个数组的前 i,j 个元素 可以得到的最大分数.
    递推: 考虑 1) arr1[i] * arr2[j] 匹配, 2) 没有用到 arr1[i], 则为 f(i-1,j); 没用到 arr2[j] 为 f(i, j-1).
    因此有 `f(i,j) = max{ f(i-1,j), f(i,j-1), max{ 0, f(i-1,j-1) } + arr1[i]*arr2[j] }`
    复杂度: O(mn).
细节: 注意边界!. 在 i,j 进行匹配的时候, 若前序分数都是负数, 可以选择不用! (对应上面两个思路中和0取max).
"""
    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
        m,n = len(nums1), len(nums2)
        f = [[-inf]*(n) for _ in range(m)]
        mx = [[-inf]*(n) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                f[i][j] = nums1[i]*nums2[j]
                # 注意下面和 0 取max! 因为不一定要用到前面的序列和.
                if i>0 and j>0: f[i][j] += max(mx[i-1][j-1], 0)
                mx[i][j] = max(f[i][j], mx[i][j-1] if j>0 else -inf, mx[i-1][j] if i>0 else -inf)
        return mx[-1][-1]
    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:        
        m,n=len(nums1),len(nums2)
        dp=[[-inf]*(n+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                v=nums1[i]*nums2[j]
                dp[i+1][j+1] = max(max(0,dp[i][j])+v, dp[i+1][j], dp[i][j+1])
        return dp[-1][-1]

sol = Solution()
result = [
    sol.maxVowels(s = "abciiidef", k = 3),
    sol.maxDotProduct(nums1 = [2,1,-2,5], nums2 = [3,0,-6]),
    sol.maxDotProduct(nums1 = [3,-2], nums2 = [2,-6,7]),
    sol.maxDotProduct([-1,-1], [1,1]),
    sol.maxDotProduct([5,-4,-3], [-4,-3,0,-4,2]),
    sol.maxDotProduct([-3,-8,3,-10,1,3,9], [9,2,3,7,-9,1,-8,5,-1,-1])
]
for r in result:
    print(r)
