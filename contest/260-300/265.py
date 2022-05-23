from re import S
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
import sys, os
# sys.setrecursionlimit(10000)

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
from structures import ListNode, TreeNode, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-265
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 2057. 值相等的最小索引 """
    def smallestEqual(self, nums: List[int]) -> int:
        for i,num in enumerate(nums):
            if i%10 == num:
                return i
        return -1
    
    """ 2058. 找出临界点之间的最小和最大距离 #medium #链表
给定一个链表, 定义关键点为局部(严格的)极小/极大值, 要求返回这些关键点之间距离的最小和最大值.
例如, head = [5,3,1,2,5,1,2] 这一链表的关键点位置在 2,4,5, 因此返回 [1,3]
思路1: 模拟遍历
    自己的思路是每次仅关注到当前遍历的节点, 因此需要记录上一个节点的值, 以及上一个节点与当前节点的大小比较.
    而 [answer](https://leetcode.cn/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/solution/zhao-chu-lin-jie-dian-zhi-jian-de-zui-xi-b08v/) 中, 使用 `cur.next.next.val` 来获取连续三个节点的值, 更为方便, 而不需要记录历史信息. 从代码上更为简洁.

"""
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        dMin, dMax = float("inf"), float("-inf")
        # 记录第一个和上一个关键点位置
        lastPos, firstPos = None, None
        # 上一个节点的值, 以及上一个节点与再上一个节点的大小比较
        lastVal, lastCompare = head.val, 0
        pos = 1
        head = head.next
        while head:
            newPos = None
            if head.val < lastVal:
                if lastCompare == 1: newPos = pos
                lastCompare = -1
            elif head.val > lastVal:
                if lastCompare == -1: newPos = pos
                lastCompare = 1
            else: lastCompare = 0
            if newPos:
                if lastPos:
                    dMin = min(dMin, newPos - lastPos)
                if firstPos:
                    dMax = max(dMax, newPos - firstPos)
                lastPos = newPos
                if not firstPos: firstPos = newPos 
            lastVal = head.val
            head = head.next
            pos += 1
        if not math.isfinite(dMin): return [-1, -1]
        return [dMin, dMax]
    
    """ 2059. 转化数字的最小运算数 #medium
给定一组数字nums, 要求将 start 转为 goal. 每一次操作可以从nums中选择一个与start进行 +/-/^ 操作, 每个nums中的数字可以用任意次. 问最小操作数.
限制: 0 <= x <= 1000. 当操作超过这一范围后, 无法再进行操作 (goal可以超过这一范围).
思路1: #BFS 将每一次允许的操作看作是对于当前数字/点的转移边. 因此建模为可达性问题, 用BFS求解.
    技巧: operator 包
"""
    def minimumOperations(self, nums: List[int], start: int, goal: int) -> int:
        num2step = {start: 0}
        import operator
        queue = collections.deque([start])
        while queue:
            a = queue.popleft()
            for b in nums:
                # if a+b not in num2step:
                #     if a+b==goal: return num2step[a]+1
                #     num2step[a+b] = num2step[a] + 1
                #     queue.append(a+b)
                # if a-b not in num2step:
                #     if a-b==goal: return num2step[a]+1
                #     num2step[a-b] = num2step[a] + 1
                #     queue.append(a-b)
                # if a^b not in num2step:
                #     if a^b==goal: return num2step[a]+1
                #     num2step[a^b] = num2step[a] + 1
                #     queue.append(a^b)
                for op in [operator.add, operator.sub, operator.xor]:
                    if op(a,b) not in num2step:
                        if op(a,b)==goal: return num2step[a]+1
                        if op(a,b) < 0 or op(a,b) > 1000: continue
                        num2step[op(a,b)] = num2step[a] + 1
                        queue.append(op(a,b))
        return -1

    """ 2060. 同源字符串检测 #hard
定义一种压缩字母字符串的方案: 类似将 "internationalization" 简写为 "i18n". 也即, 将整个字符串分解成若干部分, 某些部分用其长度来表示.
现给定两个压缩后的字符串, 要求判断它们是否可能同源.
复杂度: s1,s2 的长度限制 40, 最多出现的连续数字为 3.
思路1: DFS + 分类讨论
    from [here](https://leetcode.cn/problems/check-if-an-original-string-exists-given-two-encoded-strings/solution/ji-yi-hua-sou-suo-by-endlesscheng-ll3r/)
    整体是采用DFS. 分类准则: dfs[i,j,d] 表示用 s1[:i] 和 s2[:j] 子串 (部分匹配成功), 并且前者长度 - 后者长度的差值为 d.
        注意这里的 d!=0 的情况出现在, 采用了数字进行匹配, 还有剩余. (因为两者都是字母的情况下不会有剩余)
        终止条件: `i==n and j==m and d==0`
        如何检查冲突? 当 d==0 时, 若 s1[i], s2[j] 都是字母并且不相等, 则匹配失败.
        如何避免重复访问? 例如, 若两个压缩字符串的前缀均为 `a111a111xxx`, 在匹配到位置8的时候, dfs[8,8,0] 会出现很多次. 因此, 用cache记录 (i,j,d) 以避免重复访问.
    总结一下: 分类讨论的优先级是: 1) 若 d==0 且待匹配的都是字母, 则将 i, j 同时向后一位; 2) 否则, 匹配较短的字符串 (d>=0, d<=0) 这里取等号, 是为了处理 d==0 并且 i,j 位置为一个数字一个字母的情况.
    3) 在匹配较短序列的时候, 基于字母和数字进行分类讨论.
    [官答](https://leetcode.cn/problems/check-if-an-original-string-exists-given-two-encoded-strings/solution/tong-yuan-zi-fu-chuan-jian-ce-by-leetcod-mwva/) 用了DP来理解, 思路是一样的, 并进行了复杂性估计.

"""
    def possiblyEquals(self, s1: str, s2: str) -> bool:
        """ naive方法, 超时了 """
        def split(s):
            """ 将字符串分割成字母和数字 """
            res = []
            last = ""
            for ch in s + "-":
                if ch.isalpha():
                    if last and last.isalpha():
                        res[-1] += ch
                    else:
                        res.append(ch)
                elif ch.isdigit():
                    if last and last.isdigit():
                        res[-1] += ch
                    else:
                        res.append(ch)
                last = ch
            return res
        
        def possSplit(parts):
            """ 分割数字为可能的长度 """
            splits = [[]]
            for part in parts:
                if not part.isdigit():
                    splits = [s+[part] for s in splits]
                else:
                    if len(part)==1:
                        poss = [[int(part)]]
                    elif len(part)==2:
                        poss = [[int(part)], [int(part[0]), int(part[1])]]
                    elif len(part)==3:
                        poss = [[int(part[:1]), int(part[1:])], [int(part[:2]), int(part[2:])], [int(part[0]), int(part[1]), int(part[2])]]
                    splits = list(a+b for a,b in itertools.product(splits, poss))
                # splits = filter(lambda x: getLen(x)<=40, splits)
            return splits
        
        def getLen(split):
            l = 0
            for a in split:
                if isinstance(a, int):
                    l += a
                else: l+= len(a)
            return l
        
        def check(s1,s2):
            """ 检查两个序列是否可能相等
            例如 ['l', 1, 2, 3, 'e'] 和 [4, 4] 有可能
            """
            # s1, s2 = convert(split1), convert(split2)
            for c1, c2 in zip(s1, s2):
                if c1!="_" and c2!="_" and c1!=c2:
                    return False
            return True
        def convert(split):
            s = ""
            for a in split:
                if isinstance(a, str):
                    s += a
                else: s += "_" * a
            return s
        

        parts1, parts2 = split(s1), split(s2)
        poss1, poss2 = possSplit(parts1), possSplit(parts2)
        ss1, ss2 = [convert(s) for s in poss1], [convert(s) for s in poss2]
        len1, len2 = collections.defaultdict(list), collections.defaultdict(list)
        for s in ss1:
            len1[len(s)].append(s)
        for s in ss2:
            len2[len(s)].append(s)
        for l in len1:
            for s1 in len1[l]:
                for s2 in len2[l]:
                    if check(s1, s2):
                        return True
        return False
    
    def possiblyEquals(self, s1: str, s2: str) -> bool:
        """ https://leetcode.cn/problems/check-if-an-original-string-exists-given-two-encoded-strings/solution/ji-yi-hua-sou-suo-by-endlesscheng-ll3r/
        另见 https://leetcode.cn/problems/check-if-an-original-string-exists-given-two-encoded-strings/solution/tong-yuan-zi-fu-chuan-jian-ce-by-leetcod-mwva/"""
        n, m = len(s1), len(s2)
        
        # cache方式1
        # 因为数字最大长度为3, 因此长度差 d 的范围在 (-1000, 1000) 内, 用 bias都转到正常的index
        # mx, bias = 2000, 1000
        # vis = [[[None] * mx for _ in range(m+1)] for _ in range(n+1)]
        
        # cache方式2: 直接用字典
        vis = set()
        def dfs(i,j,d: int) -> bool:
            """ 匹配两字符串的 i和j 个位置元素
                d: s1[:i] 和 s2[:j] 表示的字符串长度之差
            """
            # 匹配成功
            if i==n and j==m and d==0: return True
            
            # cache. 注意这里不加cache会超时
            # if vis[i][j][d+bias]: return False
            # vis[i][j][d+bias] = True
            if (i,j,d) in vis: return False
            vis.add((i,j,d))
            
            # 原始字符串长度相同时，若 s1[i] == s2[j]，则 s1[:i] 和 s2[:j] 均可以向后扩展一个字母
            if d==0 and i<n and j<m and s1[i]==s2[j] and dfs(i+1, j+1, 0): return True
            
            if d<=0 and i<n:
                # s1[:i] 的原始字符串长度不超过 s2[:j] 的原始字符串长度时，扩展 s1[:i]
                if s1[i].isalpha():
                    # 字符，扩展一位，注意这里 d 不能为 0
                    if d<0 and dfs(i+1, j, d+1): return True
                else:   # 为数字
                    # 遍历所有可能的数字. 注意这里遍历 s[i:k], 右边界k是取不到的. 因此若连续数字最大数量为3, i:i+3. 这里的k就应该是 i+4
                    for k in range(i+1, min(i+4, n+1)):
                        if s1[k-1].isdigit():
                            v = int(s1[i:k])
                            if dfs(k, j, d+v): return True
                        else: break
            if d>=0 and j<m:
                if s2[j].isalpha():
                    if d>0 and dfs(i, j+1, d-1): return True
                else:
                    for k in range(j+1, min(j+4, m+1)):
                        if s2[k-1].isdigit():
                            v = int(s2[j:k])
                            if dfs(i, k, d-v): return True
                        else: break
            return False
        return dfs(0,0,0)
    
    
sol = Solution()
result = [
    # sol.smallestEqual(nums = [4,3,2,1]),
    
    # sol.nodesBetweenCriticalPoints(list2ListNode([5,3,1,2,5,1,2])),
    
    # sol.minimumOperations(nums = [2,4,12], start = 2, goal = 12),
    # sol.minimumOperations(nums = [3,5,7], start = 0, goal = -4),
    sol.minimumOperations([2,8,16],0,1),
    
    # sol.possiblyEquals(s1 = "l123e", s2 = "44"),
    # sol.possiblyEquals(s1 = "112s", s2 = "g841"),
    # sol.possiblyEquals(s1 = "a5b", s2 = "c5b"),     # False
    # sol.possiblyEquals("p87p739q339p","751p6p259q3p1p"),
    # sol.possiblyEquals("879w788w777w", "999w988w988w"),
]
for r in result:
    print(r)
