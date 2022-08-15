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
https://leetcode.cn/contest/weekly-contest-204
@2022 """
class Solution:
    """ 1566. 重复至少 K 次且长度为 M 的模式 """
    def containsPattern(self, arr: List[int], m: int, k: int) -> bool:
        # n = len(arr)
        mm = m * k
        for e in range(mm, len(arr)+1):
            if arr[e-mm:e] == arr[e-m:e] * k:
                return True
        return False
    
    """ 1567. 乘积为正数的最长子数组长度 #medium #题型
问一个数组中, 子数组的乘积为正数的最大长度
思路0: 尝试用几个变量来记录历史位置, 但写得乌漆麻枣... 放弃
思路1: #DP 用两个数组 `neg[i], pos[i]` 记录当前位置结束的正/负序列最长分别是多少
    转移: 1) 遇到0, 都重置; 2) 遇到正数, `pos[i] = pos[i-1]+1` 若上一个负数不为0, 则 `neg[i] = neg[i-1]+1`; 3) 遇到负数, `neg[i] = pos[i-1]+1` 若上一个负数不为0, 则 `pos[i] = neg[i-1]+1`
    see [official](https://leetcode.cn/problems/maximum-length-of-subarray-with-positive-product/solution/cheng-ji-wei-zheng-shu-de-zui-chang-zi-shu-zu-ch-3/)
"""
    def getMaxLen(self, nums: List[int]) -> int:
        # lastPos, lastNeg = -1,-1
        # flag = 0; firstNeg = -1; firstPos = -1
        # ans = 0
        # for i,a in enumerate(nums):
        #     if a==0: 
        #         flag = 0
        #         continue
        #     if flag==0:
        #         if a>0:
        #             firstPos = i-1
        #             flag = 1
        #             ans = max(ans, 1)
        #         else:
        #             firstNeg = i
        #             flag = -1
        #         continue
        #     flag *= 1 if a>0 else -1
        #     if flag==1:
        #         if firstPos==-1: firstPos = i
        #         else: ans = max(ans, i-firstPos+1)
        #     elif flag==-1:
        #         if firstNeg==-1: firstNeg = i
        #         else: ans = max(ans, i-firstNeg)
        # return ans
        pass
    def getMaxLen(self, nums: List[int]) -> int:
        # 思路1: #DP 
        n = len(nums)
        pos, neg = [0]*(n+1), [0]*(n+1)
        for i,a in enumerate(nums):
            if a==0: 
                continue
            elif a>0:
                pos[i+1] = pos[i]+1
                if neg[i]!=0: neg[i+1] = neg[i]+1
            else:
                neg[i+1] = pos[i]+1
                if neg[i]!=0: pos[i+1] = neg[i]+1
        return max(pos)
    
    
    """ 1568. 使陆地分离的最少天数 #hard see [SCC] """
    
    """ 1569. 将子数组重新排序得到同一个二叉查找树的方案数 #hard #题型
给定一个元素互不相同的数组, 顺序插入可以形成一个二叉查找树. 问有多少种数组可以形成一样的二叉查找树?
限制: 长度 1000; 对结果取模.
思路1: #组合计数
    不考虑左右子树内部的方式, 假设左右子树的大小分别为 ln, rn. 对于一个节点来说, 到达顺序是无所谓的. 因此 `f[node] = comb(ln+rn, rn) * f[left]*f[right]`. 递归求解.
    细节: 注意到递归函数需要 (组合数, 返回包含节点数). 边界: 若node为空, 则返回 (1, 0)
    复杂度: 1) 这里涉及到comb的计算. 预处理递推计算的复杂度为 `O(n^2)`; 2) 建立二叉树的平均复杂度为 `O(n logn)`, 但特殊情况下为 `O(n^2)`, 及退化为链式结构; 3) 递归求解的复杂度为 `O(n)`.
思路2: 可以将上面的部分都优化到 O(n) 左右
    首先是建树的过程: 上述讨论是对于一般的数组而言, 这里的特殊条件是数组数字构成一个排列 (离散化了). 这样, 我们可以保证对于 x 和 x+1, x-1 节点之间存在依赖关系 (根据在数组中的前后关系讨论). 这样, 我们逆序遍历数组, 并用 #并查集 来记录联通关系, 可以在 `O(n a(n))` 的时间内完成.
    然后是组合数的计算. 需要利用 #乘法逆元. 可的组合数计算公式 `comb(n,k) = n! / k!(n-k)! = fac[n] * facInv[k] * facInv[n-k] (mod m)`.
        根据 #裴蜀定理 和 #费马小定理, 这里的 `fac[i] = i! mod m; facInf[i] = (i!)^(m-2) mod m` 这样, 预处理的复杂度为 O(n logm), 对数项来自 快速乘方操作
        实际上可以进一步优化到 O(n), 见答案
    [official](https://leetcode.cn/problems/number-of-ways-to-reorder-array-to-get-same-bst/solution/jiang-zi-shu-zu-zhong-xin-pai-xu-de-dao-tong-yi-2/)
"""
    def numOfWays(self, nums: List[int]) -> int:
        class Node:
            def __init__(self, val) -> None:
                self.val = val
                self.left = self.right = None
        root = Node(nums[0])
        for a in nums[1:]:
            node = root
            while True:
                if a > node.val:
                    if node.right is None: node.right = Node(a); break
                    else: node = node.right
                else:
                    if node.left is None: node.left = Node(a); break
                    else: node = node.left
        mod = 10**9+7
        def dfs(node: Node):
            # return: ans, num_nodes
            if node is None: return 1,0
            la, ln = dfs(node.left)
            ra, rn = dfs(node.right)
            return la*ra * math.comb(ln+rn, ln) % mod, ln+rn+1
        return dfs(root)[0] - 1
        
            
    
sol = Solution()
result = [
    # sol.containsPattern(arr = [1,2,1,2,1,3], m = 2, k = 3),
    # sol.containsPattern(arr = [1,2,1,2,1,1,1,3], m = 2, k = 2),
    # sol.getMaxLen(nums = [1,-2,-3,4]),
    # sol.getMaxLen(nums = [-1,-2,-3,0,1]),
    # sol.getMaxLen(nums = [0,1,-2,-3,-4]),
    # sol.getMaxLen(nums = [1]),
    sol.numOfWays(nums = [3,1,2,5,4,6]),
    sol.numOfWays(nums = [9,4,2,1,3,6,5,7,8,14,11,10,12,13,16,15,17,18]),
]
for r in result:
    print(r)
