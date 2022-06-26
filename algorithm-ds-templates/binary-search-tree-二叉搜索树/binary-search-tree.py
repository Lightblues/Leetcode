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

# 二叉树
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

""" 二叉搜索树
1932. 合并多棵二叉搜索树  #hard #二叉搜索树 #树 #题型
    给定n棵(合法的) 二叉搜索树,  每棵树最多两层 (也即最多root+left+right三个节点), 按照下面的方式进行合并, 问能否经过n-1 合并后成为一个合法的二叉搜索树.
    合并方式为: 找到 (i,j) 对, 满足第j棵树的root值等于第i棵树的leave节点的值, 然后将这个节子节点替换为第j棵树, 并且整棵二叉搜索树仍然是合法的.
    提示: 重点在于, 想到构造的唯一性.
 """
class Solution:
    """ 1932. 合并多棵二叉搜索树  #hard #二叉搜索树 #树 #题型
给定n棵(合法的) 二叉搜索树,  每棵树最多两层 (也即最多root+left+right三个节点), 按照下面的方式进行合并, 问能否经过n-1 合并后成为一个合法的二叉搜索树.
合并方式为: 找到 (i,j) 对, 满足第j棵树的root值等于第i棵树的leave节点的值, 然后将这个节子节点替换为第j棵树, 并且整棵二叉搜索树仍然是合法的.
约束: 所给的n棵树的根节点值唯一
提示: **构造的唯一性**
    最重要的一点观察: 根据上述规则最终得到的结果是唯一的.
    题目保障了所有跟节点的值是唯一的, 我们可以知道, 若某一个树不是最终的root, 那么它对应的合并节点是唯一的. 
        反证法: 设该树的根值为x, 若有两个叶子节点的值均为x, 这棵树只能合并到其中一个叶子节点上, 那么最终还会有两个值相同的节点, 与最终得到一棵二叉搜索树矛盾.
    进一步有: 所有叶子节点的值也是唯一的 (因为最终二叉搜索树的节点值唯一, 而合并过程中最多只能消去一个叶子节点).
    这样, 构造就是唯一的. 遍历所有跟节点和叶节点, 我们可以找到那个唯一的跟节点 (其值不出现在叶节点的值中), 而其他树都可以与某一个叶子节点唯一对应起来.
思路1: 从上往下遍历
    关键是要找到某一节点的值的范围约束. 如果不按照特定顺序进行合并, 则较难维护叶子节点的range.
    而根据构造的唯一性, 我们可以从跟节点出发, 这样, 我们在遍历过程中可以维护新增节点的范围约束
        例如, 假设当前节点node的范围约束为 `range = (l, r)`, 我们在根节点中找到 node.val 所对应的那一棵树 replaceNode(由于我们的构造顺序, 其最多root+left+right三个节点), 我们很容易检查是否满足条件
        然后, 更新replaceNode的叶子节点的 range.
    综上, 我们维护一个queue记录从跟节点出发的树中所包含的所有叶节点, 遍历过程中, 将会发生合并的根节点替换该叶节点, 然后将新加入节点的叶节点加入queue. 最后, 若今剩下唯一的合法二叉搜索树, 则构造成功.
思路2: 直接 #中序遍历
    官答给出了一种更妙的思路: **既然构造是唯一的, 并且我们可以按照从上往下的顺序来合并, 那么直接中序遍历即可.**
    这样, 相较于思路1, 我们可以简化节点范围约束的检查: 因为中序遍历天然要求节点的值递增, 我们仅需要维护一个全局的 prev 变量, 记录上一个节点的值即可.
    [官答](https://leetcode.cn/problems/merge-bsts-to-create-single-bst/solution/he-bing-duo-ke-er-cha-sou-suo-shu-by-lee-m42t/)
"""
    def canMerge(self, trees: List[TreeNode]) -> Optional[TreeNode]:
        """ https://leetcode.cn/problems/merge-bsts-to-create-single-bst/solution/he-bing-duo-ke-er-cha-sou-suo-shu-by-lee-m42t/ """
        # 存储所有叶节点值的哈希集合
        leaves = set()
        # 存储 (根节点值, 树) 键值对的哈希映射
        candidates = dict()
        for tree in trees:
            if tree.left:
                leaves.add(tree.left.val)
            if tree.right:
                leaves.add(tree.right.val)
            candidates[tree.val] = tree
        
        # 存储中序遍历上一个遍历到的值，便于检查严格单调性
        prev = float("-inf")
        
        # 中序遍历，返回值表示是否有严格单调性
        def dfs(tree: Optional[TreeNode]) -> bool:
            if not tree:
                return True
            
            # 如果遍历到叶节点，并且存在可以合并的树，那么就进行合并
            if not tree.left and not tree.right and tree.val in candidates:
                tree.left = candidates[tree.val].left
                tree.right = candidates[tree.val].right
                # 合并完成后，将树丛哈希映射中移除，以便于在遍历结束后判断是否所有树都被遍历过
                candidates.pop(tree.val)
            
            # 先遍历左子树
            if not dfs(tree.left):
                return False
            # 再遍历当前节点
            nonlocal prev
            if tree.val <= prev:
                return False
            prev = tree.val
            # 最后遍历右子树
            return dfs(tree.right)
        
        for tree in trees:
            # 寻找合并完成后的树的根节点
            if tree.val not in leaves:
                # 将其从哈希映射中移除
                candidates.pop(tree.val)
                # 从根节点开始进行遍历
                # 如果中序遍历有严格单调性，并且所有树的根节点都被遍历到，说明可以构造二叉搜索树
                return tree if dfs(tree) and not candidates else None
        
        return None
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
