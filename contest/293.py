from typing import List, Optional, Tuple
import copy
import collections
import math
import bisect
import heapq
import functools, itertools

from sortedcontainers import SortedList, SortedDict, SortedSet
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
from utils_leetcode import testClass
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 5234. 移除字母异位词后的结果数组
给定一组word, 对于相邻的两个词, 若其包含的字符相同, 则删除前一个word (这样可以保证无论删除顺序最后的结果一致). 要求 最后的结果
思路: 模拟.
"""
    def removeAnagrams(self, words: List[str]) -> List[str]:
        def check(w1, w2):
            return collections.Counter(w1) == collections.Counter(w2)
        i = 0
        while i<len(words)-1:
            if check(words[i], words[i+1]):
                words.pop(i+1)
            else: i+=1
        return words
    
    """ 6064. 不含特殊楼层的最大连续楼层数 """
    def maxConsecutive(self, bottom: int, top: int, special: List[int]) -> int:
        special.sort()
        
        ans = max(
            special[0] - bottom,
            top - special[-1]
        )
        for i in range(len(special)-1):
            ans = max(ans, special[i+1] - special[i] - 1)
        return ans
    
    """ 6065. 按位与结果大于零的最长组合 """
    def largestCombination(self, candidates: List[int]) -> int:
        maxL = len(bin(10**7))
        counter = [0] * maxL
        for n in candidates:
            idx = 0
            while n:
                counter[idx] += n & 1
                n >>= 1
                idx += 1
        return max(counter)

    def testClass(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res

""" 6066. 统计区间中的整数数目 #hard #二分
要求实现一个数据结构, 支持插入和查询两种操作. 插入的元素是一个区间, 查询返回这些区间所包含的所有整数.
思路0: 直接暴力排序 (因为两个相邻的区间一定是不相交的). 
每次插入采用二分查找. 然而, 由于采用数组存储, 这样插入的复杂度仍为 O(n).
原本修改index的方式采用了 `self.left = self.left[:idxL] + [valueL] + self.left[idxR:]` 的形式, 超时
显然 `self.left[idxL:idxR] = [valueL]` 这样的效率更高, 直接 100% 了
see [here](https://leetcode.cn/problems/count-integers-in-intervals/solution/chun-er-fen-by-migeater-t5kh/)

关联: 0715, 那题更全一点
"""
class CountIntervals:
    """ 暴力用列表+二分来做"""
    def __init__(self):
        self.left = []
        self.right = []
        self.counter = 0

    def add(self, left: int, right: int) -> None:
        idxL = bisect.bisect_left(self.right, left)
        idxR = bisect.bisect_right(self.left, right)
        for i in range(idxL, idxR):
            self.counter -= self.right[i] - self.left[i] + 1
        # 没有交集, 插入
        if idxL==idxR:
            valueL, valueR = left, right
        else:
            valueL = left if idxL == len(self.left) else min(self.left[idxL], left)
            if idxR == 0 or len(self.right)==0:
                valueR = right
            else:
                valueR = max(right, self.right[idxR-1])
        # 修改左右 index
        # self.left = self.left[:idxL] + [valueL] + self.left[idxR:]
        # self.right = self.right[:idxL] + [valueR] + self.right[idxR:]
        self.left[idxL:idxR] = [valueL]
        self.right[idxL:idxR] = [valueR]
        self.counter += valueR-valueL+1

    def count(self) -> int:
        return self.counter

class CountIntervals_0:
    def __init__(self):
        self.ints = []
        self.cnt = 0

    def add(self, left: int, right: int) -> None:
        ints = self.ints
        # 找最左侧的与[left,right]相交的区间, 受限于右端点
        lidx  = bisect.bisect_left(ints, left, key=lambda itv:itv[1])
        # 找最右侧的与[left,right]相交的区间`ints[ridx-1]`, 受限于左端点
        ridx = bisect.bisect_right(ints, right, key=lambda itv:itv[0])

        for i in range(lidx, ridx):
            left = min(left, ints[lidx][0])
            right = max(right, ints[ridx-1][1])
            self.cnt -= ints[i][1] - ints[i][0] + 1

        ints[lidx:ridx] = [(left, right)]
        self.cnt += right - left + 1

    def count(self) -> int:
        return self.cnt




sol = Solution()
result = [
    # sol.removeAnagrams(words = ["abba","baba","bbaa","cd","cd"]),
    # sol.maxConsecutive(bottom = 2, top = 9, special = [4,6]),
    # sol.maxConsecutive(6,8,[7,6,8]),
    
    # sol.largestCombination(candidates = [16,17,71,62,12,24,14]),
    # sol.largestCombination([8,8]),
    sol.testClass(inputs = """["CountIntervals","add","add","add","add","add","add","count"]
[[],[10,27],[46,50],[15,35],[12,32],[7,15],[49,49],[]]"""),
    sol.testClass("""["CountIntervals", "add", "add", "count", "add", "count"]
[[], [2, 3], [7, 10], [], [5, 8], []]"""),
    sol.testClass("""["CountIntervals","count","add","add","count","count","add","add","add","count"]
[[],[],[33,49],[43,47],[],[],[37,37],[26,38],[11,11],[]]"""),
    
    
]
for r in result:
    print(r)
