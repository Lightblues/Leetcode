from logging import root
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
from itertools import product, permutations, combinations, combinations_with_replacement
import string
from string import ascii_lowercase, ascii_uppercase
import sys, os
# sys.setrecursionlimit(10000)

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)

# from utils_leetcode import testClass
from structures import ListNode, TreeNode

""" 
https://leetcode.cn/contest/weekly-contest-261
@2022 """
class Solution:
    """ 2027. 转换字符串的最少操作次数 """
    def minimumMoves(self, s: str) -> int:
        ans = 0
        i = 0
        while i<len(s):
            if s[i] == "X":
                ans += 1
                i += 3
            else: i+=1
        return ans
    
    """ 2028. 找出缺失的观测数据 """
    def missingRolls(self, rolls: List[int], mean: int, n: int) -> List[int]:
        missing = mean * (len(rolls)+n) - sum(rolls)
        if missing < n or missing > 6*n: return []
        div, mod = divmod(missing, n)
        ans = [div+1] * mod + [div] * (n-mod)
        return ans
    
    """ 2029. 石子游戏 IX 
- 2029. 石子游戏 IX #medium #博弈论
    - 有一组数字, AB依次取数字, A先手. 胜利条件:
        - 若两人取的数字之和可以被3整除, 则A获胜.
        - 除此之外, 若数字全部被取走A还未获胜, 则B获胜.
    - 一月的每日一题做过了, 但还是debug了挺久. 这里记录更为 naive 的思路
    - 思路: 模拟判断
        - 显然, 可以将数字根据除3的余数分成三类. 能够被3整除的数字可以起到「交换」的作用.
        - 先不考虑整除的数字, 剩余的两类地位是等价的. 例如, 在数字数量足够的情况下, 两人的最优序列形如 `112121...`. 注意到, **B所取的数字都是一样的**. 一下根据数量分类讨论 A 的胜利与否
            - 计两类数字的数量为 cmin, cmax; 方便起见假设1的数量更少
            - 若 cmin=0 (所给的数字数量 >0), 则无论是 cmax=2时B取完数字, 还是 cmax>=3 时A取数字后总和能够被3整除, 均为 False;
            - 若 cmin=1, A取 `1` 之后, B只能取2, 因此 True;
            - 若 cmin=2, AB取完 `112` 之后, B只能取2, 因此 True;
            - 若 cmin<=3, 胜利条件是 `112121...2` 之后, B只能取2, 因此数量条件时 `count[2] >= count[1]`, 也即 cmax>=cmin, 始终成立, 因此 True.
            - 综上所述, 官答给了一个更好的总结: **A的策略始终为取数量较少的那类数字**; 只要cmin>= 均为 True
        - 考虑可以被3整除的数字的影响: 当数量为偶数时不影响; 以下分析数量为奇数时:
            - 这一情况下, 相当于B获得了一次「换手」的机会.
            - 对于 cmin=0,1,2 进行讨论, 易知此时A均为 False;
            - A获胜的条件只可能为 `221021...2` (这里0表示B换手, 可知在哪个位置换手不影响AB所取的数字数量) 之后, B只能取1, 因此数量条件为 `count[2] - count[1] >= 3`. 也即 `cmax-cmin >= 3` 注意允许一次「换手」之后, A的最后策略变为取数量较多的那一类数字.


"""
    def stoneGameIX(self, stones: List[int]) -> bool:
        counts = [0] * 3
        for stone in stones:
            counts[stone%3] += 1
        def game(count1, count2):
            """ 不考虑 3 的情况下, Alice 的获胜条件 """
            if min(count1, count2) == 0: return False
            if min(count1, count2) == 1: return True
            if min(count1, count2) == 2: return True
            if max(count1, count2) >= 3: return True
            return False
        def game2(count1, count2):
            cmin, cmax = min(count1, count2), max(count1, count2)
            # if min(count1, count2) <= 1: return False
            if cmax - cmin >= 3: return True
            return False
        if counts[0] %2 == 0:
            return game(counts[1], counts[2])
        return game2(counts[1], counts[2])
    
    """ 2030. 含特定字母的最小子序列 #单调栈 #hard #题型
给定一个字符串s要求找到一个长度为k的子序列 (不要求连续), 使得: 1) 其中包含至少 repetition 个特定字符 letter; 2) 子序列字典序最小.
关联: 0316. 去除重复字母; 另有基本题型「求长为 k 的字典序最小子序列」
本题的限制包括 1) 子序列长度为 k; 2) 子序列中包含至少 repetition 个特定字符 letter.
思路: 单调栈, 注意判断这些限制条件!
单调栈相关问题思路: 
- 注意空栈 pop 的错误;
- 限制子序列长度为 k: 1) 在push的时候判断时候超过限制; 2) pop时判断剩余的是否够, 即使 break;
- 限制栈内元素数量 (比如要求ch的数量至少为repetition): 1) pop的时候检查剩余是否够; 2) 另外需要检查, 若栈内元素不足以放剩余的ch (repetition-countInStack), 则需要push.
"""
    def smallestSubsequence(self, s: str, k: int, letter: str, repetition: int) -> str:
        countLetter = collections.Counter(s)[letter]
        stack = []
        n = len(s)
        # 允许从栈中弹出的 letter 数量
        # possPop = counter[letter] - repetition
        # 
        cInStack = 0 # 当前栈中的字符 letter 数量
        cPop = 0     # 弹出的 letter数量
        for i, ch in enumerate(s):
            """ 单调栈的 pop 条件: 递归弹出比当前判断元素大的栈顶元素 """
            # 注意防止 stack 空
            while stack and ch < stack[-1]:
                # 条件1: 长度k的约束不允许弹出
                if len(stack) + (n-i) <= k:
                    break
                if stack[-1]==letter:
                    # 条件2: 不允许弹出 letter 了
                    if countLetter - cPop - 1 < repetition:
                        break
                    cPop += 1
                    cInStack -= 1
                    stack.pop()
                else:
                    stack.pop()
            # 条件2: 剩余空间不足以放剩下的 letter
            # while k - len(stack) < repetition-cInStack: 
            #     c = stack.pop()
            #     # cInStack -= c==letter
            # 每次压入栈一个元素的时候检查即可, 不需要用到while
            if k-len(stack) < repetition-cInStack:
                stack.pop()
            # 条件1: 长度k约束. 当前栈已经超过 k 了, 不在压入栈
            if len(stack) >= k:
                cPop += ch==letter
                continue
            stack.append(ch)
            if ch==letter:
                cInStack += 1
        return "".join(stack)

sol = Solution()
result = [
    # sol.minimumMoves(s = "XXOX"),
    
    # sol.missingRolls(rolls = [1,5,6], mean = 3, n = 4),
    # sol.missingRolls(rolls = [1], mean = 3, n = 1),
    
    # sol.stoneGameIX([20,3,20,17,2,12,15,17,4]),
    # sol.stoneGameIX([10,2,7,8]),
    # sol.stoneGameIX([19,2,17,20,7,17]),
    # sol.stoneGameIX(stones = [2,1]),
    # sol.stoneGameIX(stones = [2]),
    # sol.stoneGameIX(stones = [5,1,2,4,3]),
    
    sol.smallestSubsequence(s = "bba", k = 1, letter = "b", repetition = 1),
    sol.smallestSubsequence("facfffkfnffoppfffzfz",9,"f",9),
    sol.smallestSubsequence("aaabbbcccddd",3,"b",2),
    sol.smallestSubsequence(s = "leet", k = 3, letter = "e", repetition = 1),
    sol.smallestSubsequence(s = "leetcode", k = 4, letter = "e", repetition = 2),
]
for r in result:
    print(r)
