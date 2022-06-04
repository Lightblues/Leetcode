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
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-251
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1945. 字符串转化后的各位数字之和 """
    def getLucky(self, s: str, k: int) -> int:
        chs = ""
        for ch in s:
            chs += str(ord(ch) - ord('a') + 1)
        for _ in range(k):
            chs = sum(map(int, str(chs)))
        return chs
    
    """ 1946. 子字符串突变后可能得到的最大整数 """
    def maximumNumber(self, num: str, change: List[int]) -> str:
        nums = list(map(int, num))
        flag = False
        for i,a in enumerate(nums):
            if change[a] > a:
                nums[i] = change[a]
                flag = True
            if change[a] < a and flag:
                break
        return "".join(map(str, nums))
    
    """ 1947. 最大兼容性评分和 #medium
给定m个学生和m个老师, 两两匹配, 要求最大匹配分数和. 定义分数: 对于学生和老师的长度为n的0/1选择题, 分数为他们相同选项的数量.
约束: m,n < 8
思路1: 预先计算匹配矩阵. 然后DFS遍历所有可能的匹配情况
    建模为「二分图匹配问题」. 要求遍历他们之间的匹配方式.
    为了避免重复, 以idx 顺序遍历所有的学生; 维护一个remains集合记录所有未匹配的老师.
    这样, DFS的复杂度为 8x7x...x1. 时间上 `math.perm(8)=40320` 是够的.
    除了采用DFS的形式之外, [官答](https://leetcode.cn/problems/maximum-compatibility-score-sum/solution/zui-da-jian-rong-xing-ping-fen-he-by-lee-be2l/) 借用 0031 的思路得到所有的排列, 避免了递归, 形式上更为清晰.
思路2: #状态压缩 #DP
    也是顺序给学生分配老师. 用一个0/1 mask数字记录老师的匹配情况. f[mask] 表示
    递归公式: `f[mask]= max{f[mask\i]+g[c-1][i]}` 表示 c-1 转移到 c. 这里的 `mask\i` 表示将mask的第i位从1变为0.
    答案为 `f[2^m - 1]`
    see 官答
"""
    def maxCompatibilitySum(self, students: List[List[int]], mentors: List[List[int]]) -> int:
        m,n = len(students), len(students[0])
        # 预先计算匹配得分矩阵
        scores = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                scores[i][j] = sum(a==b for a,b in zip(students[i], mentors[j]))
        # DFS遍历所有匹配
        s_max = 0
        def dfs(idx, s_curr, remains: set):
            # 用 set 来存储剩余为匹配的老师
            nonlocal s_max
            if idx == m:
                s_max = max(s_max, s_curr)
                return
            for j in remains:
                dfs(idx+1, s_curr+scores[idx][j], remains - {j})
        dfs(0, 0, set(range(m)))
        return s_max
                
    """ 1948. 删除系统中的重复文件夹 #hard
背景很有意思: 对于一棵目录树, 若两个节点所包含的目录结构(文件夹名字)相同, 则认为它们是重复的. 给定一棵目录树, 要求检测删除所有重复节点.
约束: 目录树的节点数量 2e4, 路径最大深度 500, 文件夹名称不超过 10个字符.
思路1: #字典树 + #括号表示法 + 哈希表
    如何检测两棵子树结构相同? 对于树结构序列化为字符串, 判断两个字符串是否相同. (采用后续遍历DFS)
    如何保证子节点之间的顺序? 利用Trie存储子节点, 对于key排序.
    如何删除重复节点? 用一个哈希表存储节点表示到节点的映射, 将 1:n 映射的节点删除.
    [官答](https://leetcode.cn/problems/delete-duplicate-folders-in-system/solution/shan-chu-xi-tong-zhong-de-zhong-fu-wen-j-ic32/)
    复杂度: 见答案中的分析.

"""
    def deleteDuplicateFolder(self, paths: List[List[str]]) -> List[List[str]]:
        class Trie:
            def __init__(self, name) -> None:
                self.name = name
                self.children = {}  # name to node
                self.duplicated = False
        root = Trie("/")
        for path in paths:
            node = root
            for d in path:
                if d not in node.children:
                    node.children[d] = Trie(d)
                node = node.children[d]
        # 存储节点的序列化表示到节点的映射
        parse2node = defaultdict(list)
        def dfs(node: Trie) -> str:
            """ 后续遍历得到节点包含的子树的表示 """
            if len(node.children)==0:
                return ""
            # s = node.name
            s = ""
            for child in sorted(node.children):
                child = node.children[child]
                p = dfs(child)
                s += child.name + "("+p+")"
            parse2node[s].append(node)
            return s
        dfs(root)
        # 通过标记的方式删除重复节点
        for p, nodes in parse2node.items():
            if len(nodes)>1:
                for n in nodes:
                    n.duplicated = True
        # DFS遍历所有保留的节点, 返回结果
        res = []
        path = []
        def dfsOut(node: Trie):
            for childName, childNode in node.children.items():
                if childNode.duplicated: continue
                path.append(childName)
                # 对于每一个非duplicated目录都需要输出
                res.append(path[:])
                dfsOut(childNode)
                path.pop()
        dfsOut(root)
        return res

sol = Solution()
result = [
    # sol.getLucky(s = "iiii", k = 1),
    
    # sol.maximumNumber(num = "132", change = [9,8,5,0,3,6,4,2,6,8]),
    
    # sol.maxCompatibilitySum(students = [[1,1,0],[1,0,1],[0,0,1]], mentors = [[1,0,0],[0,0,1],[1,1,0]]),
    # sol.maxCompatibilitySum(students = [[0,0],[0,0],[0,0]], mentors = [[1,1],[1,1],[1,1]]),
    
    sol.deleteDuplicateFolder(paths = [["a"],["c"],["d"],["a","b"],["c","b"],["d","a"]]),
    sol.deleteDuplicateFolder(paths = [["a"],["c"],["a","b"],["c","b"],["a","b","x"],["a","b","x","y"],["w"],["w","y"]]),
]
for r in result:
    print(r)
