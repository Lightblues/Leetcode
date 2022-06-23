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

""" 
https://leetcode.cn/contest/weekly-contest-298
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 5242. 兼具大小写的最好英文字母 """
    def greatestLetter(self, s: str) -> str:
        sset = set(s)
        ans = ""
        for ch in string.ascii_uppercase:
            if ch in sset and ch.lower() in sset:
                ans = ch
        return ans
    
    """ 5218. 个位数字为 K 的整数之和 #medium
约束: 一个多重集中的数字个位数都是k, 多重集中的元素之和为num. 现在给定k和num, 问满足条件的多重集的大小最小是多少?
例子: num = 38, k = 9 时, 一种情况是 `{19,19}`. 定义空集的元素和为0.
思路1: 记录每一个末尾元素的最小值.
    注意, 集合中用到的仅仅是个位数字, 高位是可以任意指定的
    因此, 我们仅需要考虑, **对于末位数字k, 其的倍数可以取到ll时的最小值是多少**.
    例如, 对于9来说, num=18是可以满足的, 但 num=8 则不可以, 这是因为9的倍数的个位取到8时的最小值为18.
    因此, 我们用一个哈希表 `mmap` 记录 k 的倍数取到ll时的最小值即可. 显然k的末位数字能取到哪些值, 只需要遍历其与 `1...10` 的乘积即可.
    注意: 当num=0时, 答案直接为空集; 但比如num=10时, 需要从 mmap 表中查找.
"""
    def minimumNumbers(self, num: int, k: int) -> int:
        # 思路1: 记录每一个末尾元素的最小值.
        if num==0: return 0
        # 记录 k 的倍数中, 末位取到 ll 时的最小值
        mmap = collections.defaultdict(lambda: inf)
        for i in range(1, 11):
            ll = (i * k) % 10
            mmap[ll] = min(mmap[ll], i)
        a = mmap[num%10]
        if a*k<=num: return a
        return -1
        
    """ 6099. 小于等于 K 的最长二进制子序列 #medium #DP
对于一个二进制序列, 要求返回一个小于等于K的所有子序列中, 长度最大的那一个.
思路1: #DP
    定义 `f[i, l]` 表示序列的前i的元素的子序列中, 长度为l的子序列的最小值
    显然有递推公式: `f[i, l] = min(f[i-1, l], (f[i-1, l-1]<<1) + bits[i])`
    答案: f[-1,l] 中, 满足小于等于K的最大l.
    复杂度: O(n^2)
思路2: #贪心
    上述解法的复杂度是O(n^2), 实际上贪心可以做到 O(n).
    重点: 我们可以判断 **序列中的0均可以保留**. 证明: 假设剩余0的一个解法为x, 则我们将0插入任意位置, 替换掉最高位的1, 一定可以得到一个更小的数字.
    贪心算法: 从低到高位遍历, 记录当前的数字大小, 遇到0直接加到高位, 遇到1则判断当前数字是否超过了K (当然, 实际上可以提前终止).
    见 [here](https://leetcode.cn/problems/longest-binary-subsequence-less-than-or-equal-to-k/solution/by-flix-lb02/)
    进一步简化: 从上面的贪心过程中可以发现, 我们选择1的区间只能在最后的 `K.bit_length()` 范围内. 对于左侧部分, 我们仅需要记录 0 的个数即可.
        参见 [灵神](https://leetcode.cn/problems/longest-binary-subsequence-less-than-or-equal-to-k/solution/fen-lei-tao-lun-tan-xin-by-endlesscheng-vnlx/)
"""
    def longestSubsequence(self, s: str, k: int) -> int:
        n = len(s)
        f = [inf] * (n+1)
        f[0] = 0
        for i, ch in enumerate(s):
            for l in range(i+1, 0, -1):
                f[l] = min(f[l], (f[l-1]<<1) +int(ch))
        for l in range(n, -1, -1):
            if f[l]<=k: return l
        return 0
    
    """ 5254. 卖木头块 #hard #题型
给一组木头定价: (h,w, price). 现在给定一个高宽分别为 (m,n) 的整块木头, 每次分割只能对于整体进行横/竖的切割. 求最多能获得的价值.
约束: 木头长宽 200, 不同大小的可售木头数量 2e4
总结: 典型想复杂了, 没有考虑清楚DP
思路0: 记忆化搜索
    显然直接分割木块就得到两个子问题, 因此考虑采用 #cache 来搜索 `dfs(height, width)` 问题的解.
    直接采用搜索的方式求解, 用 #cache 避免重复. 子问题的分解见思路1中的讨论.
    采用DFS, 执行时间和空间比较下面的DP展开形式要高一点, 但整体的复杂度是一致的.
    see [here](https://leetcode.cn/problems/selling-pieces-of-wood/solution/python-ji-yi-hua-shen-sou-by-qin-qi-shu-ty3cy/)
思路1: 线性 #DP
    定义: f[h,w] 表示可以得到的最大价格
    递归形式: 对于一个大小为 (h,w) 的木块, 有三种情况: 直接出售, 从两个方向分割成两块, 变为两个子问题.
        三种情况分别对应, `min{ prices.get((h,w), 0); f[i, w]+f[h-i, w]; f[h, j]+f[h, w-j] }`. 其中第一项是看整块木球是否可以出售; 后两项分别对于高宽进行遍历.
        复杂度: 每次分割的复杂度为 O(h+w)
    复杂度: O(mn * (m+n))
    from [灵神](https://leetcode.cn/problems/selling-pieces-of-wood/solution/by-endlesscheng-mrmd/)
"""
    def sellingWood(self, m: int, n: int, prices: List[List[int]]) -> int:
        """ 自己的实现, 超时了!
一种贪心策略是: 尽量选择单位价格最高的切割方式. 但这样的策略有问题: 例如 `[(3,3,10), (2,2,4)]` 的价格表, 对于大小为 (4,4) 的木头.
在一开始的实现中, 尝试对于每中木块大小都尝试切割出最多的数量 (根据单位价格进行 prune, 还自己为妙), 然后再递归剩余的小块; 但这样显然是有问题的.
因此, 最后的实现是, 得到一个大致解之后, 再遍历每一种切割方式 —— 然后理所当然的超时了.
"""
        sl = SortedList()
        for h,w,p in prices:
            avgP = p / (h*w)
            sl.add((-avgP, (h,w,p)))
        @lru_cache(maxsize=None)
        def dfs(height, width):
            if height==0 or width==0: return 0
            res = 0
            for avg, (h,w,p) in sl:
                # 
                if -avg * (height*width) <= res: break
                if h>height or w>width: continue
                a, rh = divmod(height, h)
                b, rw = divmod(width, w)
                total = a*b*p + max(
                    dfs(rh, width)+dfs(a*h, rw), dfs(height, rw)+dfs(rh, b*w)
                )
                res = max(res, total)
            for h in range(1, height//2+1):
                res = max(res, dfs(h, width) + dfs(height-h, width))
            for w in range(1, width//2+1):
                res = max(res, dfs(height, w) + dfs(height, width-w))
            return res
        return dfs(m, n)

    def sellingWood(self, m: int, n: int, prices: List[List[int]]) -> int:
        """ 思路1: 记忆化搜索
        from [here](https://leetcode.cn/problems/selling-pieces-of-wood/solution/python-ji-yi-hua-shen-sou-by-qin-qi-shu-ty3cy/) """
        @lru_cache(None)
        def dfs(x, y):
            res = d.get((x, y), 0)  # 如果木头块价格不在价格列表中则为0
            for i in range(1, x):   # 高度切割
                res = max(res, dfs(i, y) + dfs(x - i, y))
            for i in range(1, y):   # 宽度切割
                res = max(res, dfs(x, i) + dfs(x, y - i))
            return res
        d = {(h, w):p for h, w, p in prices}    # 木头块高宽和价格映射表
        return dfs(m, n)


    def sellingWood(self, m: int, n: int, prices: List[List[int]]) -> int:
        """ from [灵神](https://leetcode.cn/problems/selling-pieces-of-wood/solution/by-endlesscheng-mrmd/) """
        pr = {(h, w): p for h, w, p in prices}
        f = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                f[i][j] = max(pr.get((i, j), 0),
                              max((f[i][k] + f[i][j - k] for k in range(1, j)), default=0),
                              max((f[k][j] + f[i - k][j] for k in range(1, i)), default=0))
        return f[m][n]


    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [
    # sol.greatestLetter(s = "arRAzFif"),
    # sol.greatestLetter(s = "AbCdEfGhIjK"),
    # sol.minimumNumbers(num = 37, k = 2),
    # sol.minimumNumbers(num = 58, k = 9),
    # sol.minimumNumbers(8,9),
    # sol.minimumNumbers(num = 0, k = 7),
    # sol.longestSubsequence(s = "1001010", k = 5),
    # sol.longestSubsequence(s = "00101001", k = 1),
    sol.sellingWood(m = 3, n = 5, prices = [[1,4,2],[2,2,7],[2,1,3]]),
    sol.sellingWood(m = 4, n = 6, prices = [[3,2,10],[1,4,2],[4,1,3]]),
    sol.sellingWood(5,9,[[2,3,15],[5,2,10],[1,3,27],[1,2,23],[5,1,11],[4,7,23]])
]
for r in result:
    print(r)
