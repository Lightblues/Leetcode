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
https://leetcode.cn/contest/weekly-contest-217
@2022 """
class Solution:

    """ 1672. 最富有客户的资产总量 """
    def maximumWealth(self, accounts: List[List[int]]) -> int:
        ans = map(sum, accounts)
        return max(ans)
    
    """ 1673. 找出最具竞争力的子序列 #medium #题型
从长度为k的子序列中找到字典序最小的.
思路: 采用 #最小堆. 如何保证最后剩余的堆大小至少为k? 对于长n的给定序列, 位置i往后的长度为n-i, 因此堆剩余的大小至少为 `k-(n-i)`
"""
    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        h = []
        n = len(nums)
        for i,num in enumerate(nums):
            # 保证剩余堆的大小至少为k
            while len(h) >= max(1, k-n+i + 1) and num<h[-1]:
                h.pop()
            h.append(num)
        return h[:k]
    
    """ 1674. 使数组互补的最少操作次数 #medium #题型 #差分数组
给定一个长为偶数的数组, 每次操作可以使得任一数字变为 [1...limit] 中的一个数, 要求最少操作, 使得对称元素之和都是同一个数. 这里有一个重要限制是数组内的所有元素都 <= limit.
限制: n,limit 1e5
提示
    考虑可取值的范围, 目标值在 [2...2*limit] 区间内.
    而对于一组数 (a,b) 而言, **最多修改2次**. 什么情况下可以减少修改次数? 可知在 [mn+1...mx+limit] 范围内只需修改一次, 其中特殊点 sum(a,b) 则不需要修改.
思路1: 利用 #差分数组 来记录区间信息
    根据提示, 我们可以暴力遍历所有可取范围, 但检查数对是否可行, 总体复杂度为 O(limit * n) 会超时.
    因此, 用差分数组来记录区间信息. 简单起见对于每组数字我们仅考虑 `[mn+1...mx+limit]` 这里范围, 并用 cnt 来记录不需要修改次数 (最多反向减一下即可).
    这样, 差分数组累加结果acc记录了该范围内只需要进行一次(或零次)修改即可的数组数量, 而其他数组的修改次数需要为2次. 因此, 答案就是 `[n] - acc - cnt` 的最小值. 第一项是默认全部数组修改2次, 第二项减去只需要修改一次的部分, 第三项减去不需要修改的数组.
    见 [zero](https://leetcode.cn/problems/minimum-moves-to-make-array-complementary/solution/shi-shu-zu-hu-bu-de-zui-shao-cao-zuo-ci-shu-by-zer/)
总结: 转弯有点多, 想到差分数组是关键.
"""
    def minMoves(self, nums: List[int], limit: int) -> int:
        n = len(nums)
        s = [n] * (2*limit+2)
        acc = [0] * (2*limit+2)
        cnt = [0] * (2*limit+2)
        for i in range(n//2):
            a,b = nums[i],nums[n-1-i]
            cnt[a+b] += 1
            acc[min(a,b)+1] += 1
            acc[(max(a,b)+limit)+1] -= 1
        for i in range(len(acc)-1):
            acc[i+1] += acc[i]
        ans = [a-b-c for a,b,c in zip(s,acc,cnt)]
        return min(ans)

    """ 1675. 数组的最小偏移量 #hard
数组的「偏移量」定义为其两个元素的最大差值. 现给定一个数组, 可以对其中的元素进行操作: 若为偶数可以/2, 对于奇数可以*2. 要求最少偏移量.
限制: 数组长度 5e4, 元素大小 1e9
思路1: 注意奇数最多只能*2一次, 但偶数可能可以多次/2. 先将所有所有奇数*2转为全偶数的情况. 然后用 #有序数组 来维护, 每次的差值为 mx-mn, 然后对于最大值/2放回数组. 注意若最大值为奇数, 其不可能变小了, 终止!
    复杂度: O(n logMAX)
    see [zero](https://leetcode.cn/problems/minimize-deviation-in-array/solution/shu-zu-de-zui-xiao-pian-yi-liang-by-zerotrac2/)
关联: 「0632. 最小区间」
"""
    def minimumDeviation(self, nums: List[int]) -> int:
        from sortedcontainers import SortedList
        nums = [i if i%2==0 else i*2 for i in nums]
        sl = SortedList(nums)
        ans = inf
        while sl[-1]%2==0:
            mx = sl.pop()
            ans = min(ans, mx-sl[0])
            sl.add(mx//2)
        ans = min(ans, sl[-1]-sl[0])
        return ans
            
            
    """ 0632. 最小区间 #hard
给定k个递增数组, 要求一个最小的区间, 满足对于数组至少包含其中一个元素. 「最小区间」的定义: 范围最小, 范围相等的话数字较小.
限制: 数组数量 k 3500, 数组长度 n 50, 元素范围 [-1e5, 1e5]
思路1: 维护一个 #有序数组 sl, 包含k个数组中的当前最大元素, 答案维护sl的最大差值.
    优化: 这里用到了高级的有序数组, 是否有更为简单的DS? [官答](https://leetcode.cn/problems/smallest-range-covering-elements-from-k-lists/solution/zui-xiao-qu-jian-by-leetcode-solution/) 从小到大遍历, 维护当前关注的一个 #最小堆, 只用一个maxValue记录当前的最大值. DS更简单.
    复杂度: `O(nk logk)`, 所有数字的数量为 nk, 每次堆操作 logk.
思路2: 记所有元素的范围为 [mn,mx], 我们在这一范围内 #滑动窗口 来解决, 参见「0076. 最小覆盖子串」.
    具体而言, 用一个cnt记录当前窗口内的数字所覆盖的数组 (辅助哈希表 `{num:arrsContaining[]}` 每个数字所出现的递增数组). 在滑动窗口的过程中检查是否包含所有递增数组.
    复杂度: `O(nk + |V|)`, 前者是滑动窗口时所有数字只会用到2次, 后者是数组数值范围.
关联: 1675. 数组的最小偏移量
"""
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        # 边界: k==1
        if len(nums)==1:
            return [nums[0][0], nums[0][0]]
        
        from sortedcontainers import SortedList
        sl = SortedList()
        k = len(nums)
        for i in range(k):
            sl.add((nums[i].pop(), i))
        mx,idx = sl.pop()       # 边界: k==1
        minD = mx - sl[0][0]
        ans = (sl[0][0], mx)
        while nums[idx]:
            sl.add((nums[idx].pop(), idx))
            mx,idx = sl.pop()
            if mx-sl[0][0] <= minD:
                minD = mx-sl[0][0]
                ans = (sl[0][0], mx)
        return ans

    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        # 思路2 #滑动窗口
        mn,mx = inf, -inf
        num2arrs = defaultdict(list)
        for i,arr in enumerate(nums):
            for a in arr:
                mn = min(mn, a)
                mx = max(mx, a)
                num2arrs[a].append(i)
        # 
        k = len(nums)
        cnt = [0]*k
        containedArrCnt = 0     # 记录当前包含的数组数量
        l = mn
        ansLen = inf; ans = (0,0)
        for r in range(mn,mx+1):
            for idx in num2arrs[r]:
                # 包含了了新的arr
                if cnt[idx]==0: containedArrCnt += 1
                cnt[idx] += 1
            while containedArrCnt==k:
                if r-l<ansLen:
                    ansLen = r-l
                    ans = (l,r)
                for idx in num2arrs[l]:
                    cnt[idx] -= 1
                    if cnt[idx]==0: containedArrCnt -= 1
                l += 1
        return ans

    
sol = Solution()
result = [
    # sol.mostCompetitive(nums = [3,5,2,6], k = 2),
    # sol.mostCompetitive(nums = [2,4,3,3,5,4,9,6], k = 4),
    # sol.minMoves(nums = [1,2,4,3], limit = 4),
    # sol.minMoves(nums = [1,2,2,1], limit = 2),
    # sol.minMoves(nums = [1,2,1,2], limit = 2),
    # sol.minimumDeviation(nums = [1,2,3,4]),
    # sol.minimumDeviation(nums = [4,1,5,20,3]),
    
    # sol.smallestRange(nums = [[4,10,15,24,26], [0,9,12,20], [5,18,22,30]]),
    # sol.smallestRange(nums = [[1,2,3],[1,2,3],[1,2,3]]),
    # sol.smallestRange([[1]])
    

]
for r in result:
    print(r)
