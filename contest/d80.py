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
https://leetcode-cn.com/contest/biweekly-contest-80
@2022 """
class Solution:
    """ 2299. 强密码检验器 II #easy #题型
要求: 至少8位; 相邻位不同字符; 至少包含一个数字; 至少包含一个小写字母; 至少包含一个大写字母; 至少包含一个特殊字符"!@#$%^&*()-+";
思路1: 用集合 intersection 判断是否包含某一类字符
思路2: 用位运算来记录是否包含某一类字符
    例如: 大/小写/数字/特殊字符分别表示1-4位, 对于所有的字符求或, 则包括所有的类型等价于, 最后的运算结果为 15.
    see [灵神](https://leetcode.cn/problems/strong-password-checker-ii/solution/go-jian-ji-xie-fa-by-endlesscheng-w3lu/)

"""
    def strongPasswordCheckerII(self, password: str) -> bool:
        if len(password) < 8: return False
        s = set(password)
        if not s.intersection(set(string.ascii_lowercase)): return False
        if not s.intersection(set(string.ascii_uppercase)): return False
        if not s.intersection(set(string.digits)): return False
        if not s.intersection(set("!@#$%^&*()-+")): return False
        for i in range(len(password)-1):
            if password[i] == password[i+1]:
                return False
        return True
    
    """ 2300. 咒语和药水的成功对数 """
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort()
        n = len(potions)
        ans = []
        for s in spells:
            ans.append(n-bisect.bisect_left(potions, success/s))
        return ans
    
    """ 2301. 替换字符后匹配 #hard #题型
给定一个替换列表 mappings, 对于每一组字符 (old, new), 可以将待处理字符串中的任意字符 old 替换为 new. 现给定两个字符串 s, sub, 问能否通过替换操作将sub转化为s的某一子串?
复杂度: 两个字符串长度 5e3, 映射数量 1e3
思路1: 暴力枚举
    直接用一个哈希表记录一个字符串所有可能的原始字符, 然后暴力枚举s所有可能的子串, 看是否匹配
    复杂度: 每次检查是否可以替换得到的复杂度为 O(1), 因此总的复杂度为 O(n^2), 大概是1e7 够了
思路2: #正则
    暴力得到正则表达式, see [here]*(https://leetcode.cn/problems/match-substring-after-replacement/solution/-by-migeater-gdqi/)
哈哈, 大佬认真考虑了这题[为什么标成了hard](https://leetcode.cn/problems/match-substring-after-replacement/solution/shu-ju-fan-wei-geng-da-de-hua-zen-yao-zu-d9es/), 是我不懂的
"""
    def matchReplacement(self, s: str, sub: str, mappings: List[List[str]]) -> bool:
        new2olds = defaultdict(list)
        for o,n in mappings:
            new2olds[n].append(o)
        for start in range(len(s)-len(sub)+1):
            flag = True
            for i,ch in enumerate(sub):
                if ch!=s[start+i] and ch not in new2olds[s[start+i]]: 
                    flag = False
                    break
            if flag: return True
        return False
    
    def matchReplacement(self, s: str, sub: str, mappings: List[List[str]]) -> bool:
        # 思路2, 暴力用 re
        d = {}
        for k,v in mappings:
            d[k] = d.get(k, k) + v
        return bool(re.search("".join(f"[{d.get(c, c)}]" for c in sub), s))

    
    """ 2302. 统计得分小于 K 的子数组数目 #hard 
定义一个连续子数组的分数: 数组和*长度. 现给定一个数组, 求分数小于k的子数组数量.
约束: 数组长度 1e5
思路1: #双指针
    遍历子数组的右端点 idx, 只需要求出最左边的满足条件的位置即可.
    注意到: 维护一个全局的左端点left, 当 idx右移的过程中, left也一定是右移的.
    因此, 双指针的复杂度为 O(n)
    see [灵神](https://leetcode.cn/problems/count-subarrays-with-score-less-than-k/solution/by-endlesscheng-b120/)
思路2: 傻叉的 #二分
    一开始没考虑清楚双指针的复杂度, 仅仅利用了left是肯定不断右移的性质, 考虑每次在 [left, idx+1] 区间内二分找到满足条件的最有位置
    结果, 采用了bisect库中的 `key` 参数, 结果用错了Orz, 浪费了好久...
        因为, `bisect_right(a, x, lo=0, hi=None, *, key=None)` 中的key作用对象是 `key(a[mid])` 而不是idx!!!
    后面手写了二分, 结果速度比思路1慢了很多. 因为这里的复杂度变为 O(n log(n))

"""
    def countSubarrays(self, nums: List[int], k: int) -> int:
        """ 一开始尝试二分, 不过用错了 bisect_right 函数, 会越界:
        错了!!!"""
        n = len(nums)
        acc = list(accumulate(nums, initial=0))
        left = 0
        ans = 0
        for i in range(n):
            idx = bisect_right(acc, 0, lo=left, hi=i+2, 
                              key=lambda x: 1 - ((acc[i+1] - acc[x]) * (i+1-x) >= k))
            ans += i-idx+1
            left = idx
        return ans

    def countSubarrays(self, nums: List[int], k: int) -> int:
        """ 思路1: 双指针 """
        n = len(nums)
        acc = list(accumulate(nums, initial=0))
        left = 0
        ans = 0
        for i in range(n):
            while (acc[i+1]-acc[left]) * (i+1-left) >= k:
                left += 1
            ans += i-left+1
        return ans

    def countSubarrays(self, nums: List[int], k: int) -> int:
        """ 思路2: 傻叉二分 """
        n = len(nums)
        acc = list(accumulate(nums, initial=0))
        def test(l,r):
            return (acc[r+1]-acc[l]) * (r-l+1) < k
        def bisectRight(lo, hi, idx):
            while lo<hi:
                mid = (lo+hi)//2
                if test(mid, idx):
                    hi = mid
                else:
                    lo = mid+1
            return lo
        left = 0
        ans = 0
        for i in range(n):
            # idx = bisect_right(acc, 0, lo=left, hi=i+2, 
            #                   key=lambda x: 1 - ((acc[i+1] - acc[x]) * (i+1-x) >= k))
            # 注意, 二分搜索的右边界是 i+1, 也即单独一个i也无法满足条件
            idx = bisectRight(left, i+1, i)
            ans += i-idx+1
            left = idx
        return ans

sol = Solution()
result = [
    # sol.strongPasswordCheckerII(password = "IloveLe3tcode!"),
    # sol.strongPasswordCheckerII(password = "Me+You--IsMyDream"),
    # sol.strongPasswordCheckerII(password = "1aB!"),
    # sol.successfulPairs(spells = [5,1,3], potions = [1,2,3,4,5], success = 7),
    # sol.countSubarrays(nums = [2,1,4,3,5], k = 10),
    # sol.countSubarrays(nums = [1,1,1], k = 5),
    
    sol.matchReplacement(s = "fool3e7bar", sub = "leet", mappings = [["e","3"],["t","7"],["t","8"]]),
    sol.matchReplacement(s = "fooleetbar", sub = "f00l", mappings = [["o","0"]]),
]
for r in result:
    print(r)
