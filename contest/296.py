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

from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-296
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 6090. 极大极小游戏 #easy 模拟即可 """
    def minMaxGame(self, nums: List[int]) -> int:
        while len(nums) > 1:
            newNums = []
            for i in range(len(nums)//2):
                if i%2==0:
                    newNums.append(min(nums[2*i], nums[2*i+1]))
                else:
                    newNums.append(max(nums[2*i], nums[2*i+1]))
            nums = newNums
        return nums[0]
    
    """ 6091. 划分数组使最大差为 K """
    def partitionArray(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = 0
        last  = -inf
        for num in nums:
            if num - last > k:
                ans += 1
                last = num
        return ans
    
    
    """ 6092. 替换数组中的元素 #medium
给定一个长度为n的数组, 其中每个元素都不相同. 然后给定长为m的操作序列 (顺序执行), 每次将数组中的元素完成 (a->b) 的映射, 这里的操作有限制: 保证了a出现在数组中, 而b不出现在数组中.
限制: 1 <= n, m <= 10**5.
思路: #哈希表
    注意这里的操作是顺序执行的, 因此会有  1->2->3 这样的多次映射关系.
    这里保证了数组元素互不相同, 而每次操作执行后也能保证形成的数组元素互不相同. 因此, **我们只需要记录从一开始到最后的映射即可**.
    具体而言, 用 `numMap` 哈希表记录顺序遍历操作后, 形成的最终的映射表; 再用一个 `numMapBack` 哈希表记录回链.
        对于每个映射 `(a->b)`, 如果 `a` 出现在 `numMapBack` 哈希表中, 则利用回链来更新映射表 `numMap[numMapBack[a]] = b`; 
        之前纠结的点在于, 上述映射链条之后, 是否需要删除回链 `numMapBack[a]`? 没必要, 因为根据题意, 在生成 (a->b) 映射的时候数组中是不包含b的, 因此再经过 (b->c) 之后数组中又不存在b了; 删除与否无所谓.
        
"""
    def arrayChange(self, nums: List[int], operations: List[List[int]]) -> List[int]:
        numMap = {}
        numMapBack = {}
        for a,b in operations:
            if a not in numMapBack:
                numMap[a] = b
                numMapBack[b] = a
            else:
                numMap[numMapBack[a]] = b
                numMapBack[b] = numMapBack[a]
        ans = [None] * len(nums)
        for a, num in enumerate(nums):
            ans[a] = numMap[num] if num in numMap else num
        return ans

    def testClass(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res


""" 6093. 设计一个文本编辑器 #hard 不太符合? 可能是 Python 字符串操作太方便了
模拟一个文本编辑器, 要求实现 添加、删除、光标移动操作.
限制: 1 <= text.length, k <= 40 其中text为添加的字符串的长度, k为删除和移动光标距离. 操作次数 2e4
思路: 直接用str操作即可.
"""
class TextEditor:

    def __init__(self):
        self.text = ""
        self.cursor = 0

    def addText(self, text: str) -> None:
        self.text = self.text[:self.cursor] + text + self.text[self.cursor:]
        self.cursor += len(text)

    def deleteText(self, k: int) -> int:
        dLen = min(k, self.cursor)
        self.text = self.text[:self.cursor-dLen] + self.text[self.cursor:]
        self.cursor -= dLen
        # retLen = min(10, self.cursor)
        # return self.text[self.cursor-retLen:self.cursor]
        return dLen

    def cursorLeft(self, k: int) -> str:
        self.cursor = max(self.cursor-k, 0)
        retLen = min(10, self.cursor)
        return self.text[self.cursor-retLen:self.cursor]

    def cursorRight(self, k: int) -> str:
        self.cursor = min(self.cursor+k, len(self.text))
        retLen = min(10, self.cursor)
        return self.text[self.cursor-retLen:self.cursor]

sol = Solution()
result = [
    # sol.minMaxGame(nums = [1,3,5,2,4,8,2,2] ),
    # sol.partitionArray(nums = [1,2,3], k = 1),
    # sol.partitionArray(nums = [3,6,1,2,5], k = 2),
    
    # sol.arrayChange(nums = [1,2], operations = [[1,3],[2,1],[3,2]]),
    # sol.arrayChange(nums = [1,2,4,6], operations = [[1,3],[4,7],[6,1]]),
    
    sol.testClass("""["TextEditor", "addText", "deleteText", "addText", "cursorRight", "cursorLeft", "deleteText", "cursorLeft", "cursorRight"]
[[], ["leetcode"], [4], ["practice"], [3], [8], [10], [2], [6]]"""),
]
for r in result:
    print(r)
