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
https://leetcode.cn/contest/weekly-contest-244
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1886. 判断矩阵经轮转后是否一致 #easy
给定两个方阵, 判断经过旋转后是否一致.
思路1: 分别计算每种旋转的坐标变换公式 (推了好久Orz), 如下. 例如顺时针90度变换, 坐标从 (i,j) 变为 `(j, n-1-i)`. 具体可以参见 0048 的[官答](https://leetcode.cn/problems/rotate-image/solution/xuan-zhuan-tu-xiang-by-leetcode-solution-vu3m/)
思路2: 看了官答的解法, 还真就原地旋转了三次, 更为粗暴.
"""
    def findRotation(self, mat: List[List[int]], target: List[List[int]]) -> bool:
        n = len(mat)
        if all(mat[i][j]==target[i][j] for i in range(n) for j in range(n)): return True
        if all(mat[i][j]==target[j][n-1-i] for i in range(n) for j in range(n)): return True
        if all(mat[i][j]==target[n-1-i][n-1-j] for i in range(n) for j in range(n)): return True
        if all(mat[i][j]==target[n-1-j][i] for i in range(n) for j in range(n)): return True
        return False
    
    """ 1887. 使数组元素相等的减少操作次数 #medium 
定义了一种操作, 问将数组最终变为所有元素相等的操作次数. 直接推公式就行 """
    def reductionOperations(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        # ans = 0
        # for num in sorted(cnt.keys(), reverse=True):
        keys = sorted(cnt.keys())
        cnts = [cnt[c] for c in keys]
        return sum(c*i for i, c in enumerate(cnts))
    
    """ 1888. 使二进制字符串字符交替的最少反转次数 #medium
对于一个01字符串, 可以采取两种操作: 1) 将第一个字符移到最后; 2) 反转任意一位. 问要将某一字符串变为「交替」的操作序列中, 类型2操作的最小次数.
思路1: #分析 归纳不同的类别. 具体需要分别计算 #前缀 和 #后缀, 然后匹配.
    提示: 1) 可以将所有的操作1安排在操作2后面; 2) 操作1起作用的情况, 只可能是操作2之后变为 `101|10` 这种; 注意到, 此时字符串一定是奇数长度, 并在某一位置前后出现了两个连续的比特. 并且, 在上例中, 左侧是以1结尾的交替串, 右侧是以1开头的交替串 (都是0也可).
    因此, 我们考虑将字符串转为 1) 0101或1010; 2) 转为上述情况 (仅当长度为奇数) 这写情况中, 所需的翻转步骤最小的.
    为此, 可以 `pre[i][0/1]` 表示将前i位变为以 0/1 结尾的交替串所需的翻转数. 则有递推: `pre[i][0] = pre[i-1][1] + (s[i]==1)`; `pre[i][1] = pre[i-1][0] + (s[i]==0)`;
    同样, 用后缀 `suf[j][0/1]` 表示将j位之后的串变为以 0/1 开头的交替串所需翻转数. 递推 `suf[j][0] = suf[j+1][1] + (s[j]==1)`; `suf[j][1] = suf[j+1][0] + (suf[j]==0)`;
    see [官答](https://leetcode.cn/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/solution/shi-er-jin-zhi-zi-fu-chuan-zi-fu-jiao-ti-i52p/) 思路很清晰.
    灵神给出了一个类似的, 更fancy的, 也更难理解的 [方法](https://leetcode.cn/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/solution/cong-qian-wang-hou-pi-pei-cong-hou-wang-uiq6a/).
思路2: 利用 #滑动窗口
    提示: 由于最后的结果只有01/10序列两种情况, 因此假如变为某一类型需要x次翻转, 则变为另一种类型需要 n-x 次翻转.
    按照思路1的分析, 主要考虑的是奇数时从哪个位置分成左右两段? 注意到, 若将左半部分接到右边是合法的. 因此, 我们double字符串 (从而避免边界判断), 然后用 #滑动窗口 扫描每一种情况需要翻转的次数.
    具体看 [here](https://leetcode.cn/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/solution/minimum-number-of-flips-by-ikaruga-lu32/) 的图更为直观.
总结: 上面 `101|10` 这种情况叫做「循环同构」; 思路1虽然复杂但其实是更容易想到的; 思路2更为巧妙但其实绕了很多弯.
"""
    def minFlips(self, s: str) -> int:
        """ 尝试贪心: 所有的操作1可以在一开始执行. 
        需要考虑的情况是 `"01001001101"` 这样的, 因此, 在下面的处理中将 `010` 搬到最后, 但证明这一启发是错的! """
        s = list(map(int, s))
        def f(s, first=0):
            acc = 0
            for i in s:
                if i==first: acc += 1
                first = 1-first
            return acc
        ans = min(f(s, 0), f(s, 1))
        if s[0] + s[-1] == 1:
            i = 1
            while i <= len(s)-1 and s[i]+s[i-1]==1: i += 1
            s = s[i:] + s[:i]
            ans = min(ans, min(f(s, 0), f(s, 1)))
        return ans
    def minFlips(self, s: str) -> int:
        """ [官答](https://leetcode.cn/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/solution/shi-er-jin-zhi-zi-fu-chuan-zi-fu-jiao-ti-i52p/) """
        s = list(map(int, s)); n = len(s)
        pre = [[0,0] for _ in range(n)]
        pre[0] = [int(s[0]==1), int(s[0]==0)]
        for i in range(1, n):
            pre[i][0] = pre[i-1][1] + (s[i]==1)
            pre[i][1] = pre[i-1][0] + (s[i]==0)
        ans = min(pre[-1])
        if n&1 == 0: return ans
        suf = [[0,0] for _ in range(n)]
        suf[-1] = [int(s[-1]==1), int(s[-1]==0)]
        for j in range(n-2, -1, -1):
            suf[j][0] = suf[j+1][1] + (s[j]==1)
            suf[j][1] = suf[j+1][0] + (s[j]==0)
        for idx in range(1,n):
            ans = min(ans, pre[idx-1][0]+suf[idx][0], pre[idx-1][1]+suf[idx][1])
        return ans
    
    """ 1889. 装包裹的最小浪费空间 #hard
需要将n个物品装到包裹中, 一个包裹只能装一个体积更小的物品; 对于一组固定大小的包裹, 定义score为所有包裹浪费的空间之和; 现在要从m个供应商中选一组提供包裹, 使得score最小.
限制: m,n 1e5; 每个供应商提供的不同尺寸的包裹数量 1e5
思路1: 排序 之后 #二分计算. 用到 #前缀和 加速计算
    思路比较简单: 就是先分别对于物品和提供的包裹体积排序, 然后依次二分找到该体积的包裹对应了哪一部分的物品, 利用前缀和加速计算.
    复杂度: $O(n \log n+l \log l+l \log n)$ 这里的l为所有供应商提供的箱子的数量之和, 参见 [官答](https://leetcode.cn/problems/minimum-space-wasted-from-packaging/solution/zhuang-bao-guo-de-zui-xiao-lang-fei-kong-90lk/#comment).
"""
    def minWastedSpace(self, packages: List[int], boxes: List[List[int]]) -> int:
        mod = 10**9 + 7
        packages.sort()
        acc = list(accumulate(packages, initial=0))
        ans = inf
        for suppliers in boxes:
            suppliers.sort()
            if suppliers[-1] < packages[-1]: continue
            lastidx = 0; waste = 0 
            for box in suppliers:
                idx = bisect_right(packages, box)
                waste += box * (idx - lastidx) - (acc[idx] - acc[lastidx])
                # 先取 mod 的话可能解答错误 
                # waste %= mod
                lastidx = idx   # 注意这里的index使用.
            ans = min(ans, waste)
        return ans %mod if ans != inf else -1
    
sol = Solution()
result = [
    # sol.findRotation(mat = [[0,1],[1,0]], target = [[1,0],[0,1]]),
    # sol.findRotation(mat = [[0,1],[1,1]], target = [[1,0],[0,1]]),
    # sol.findRotation(mat = [[0,0,0],[0,1,0],[1,1,1]], target = [[1,1,1],[0,1,0],[0,0,0]]),
    # sol.reductionOperations(nums = [5,1,3]),
    # sol.reductionOperations(nums = [1,1,2,2,3]),
    # sol.minWastedSpace(packages = [2,3,5], boxes = [[4,8],[2,8]]),
    # sol.minWastedSpace(packages = [2,3,5], boxes = [[1,4],[2,3],[3,4]]),
    # sol.minWastedSpace(packages = [3,5,8,10,11,12], boxes = [[12],[11,9],[10,5,14]]),
    # sol.minFlips(s = "111000"),
    # sol.minFlips(s = "010"),
    # sol.minFlips(s = "1110"),
    sol.minFlips("01001001101"),
    sol.minFlips("1"),
]
for r in result:
    print(r)
