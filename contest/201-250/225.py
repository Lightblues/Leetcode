import random
import time
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
https://leetcode.cn/contest/weekly-contest-225
@2022 """
class Solution:
    """ 1736. 替换隐藏数字得到的最晚时间 #easy #题型 
给定一个字符串表示时间, 其中一些位用 `?` 表示未知, 问填充得到最大的时间.
思路1: 纯粹基于规则.
    [官答](https://leetcode.cn/problems/latest-time-by-replacing-hidden-digits/solution/ti-huan-yin-cang-shu-zi-de-dao-de-zui-wa-0s7r/) 中的逻辑更清楚一点.
"""
    def maximumTime(self, time: str) -> str:
        # 实际上的判断不必这么复杂: 按照 0,1,2,3 位分别判断即可
        ans = ""
        if time[:2]=="??": ans += "23"
        elif time[0]=='?':
            if time[1]>'3': ans += '1'+time[1]
            else: ans += '2'+time[1]
        elif time[1]=='?':
            if time[0]=='2': ans += '23'
            else: ans += time[0]+'9'
        else: ans += time[:2]
            
        ans += ":"
        if time[-2:]=="??": ans += '59'
        elif time[-2]=='?':
            ans += '5'+time[-1]
        elif time[-1]=='?':
            ans += time[-2]+'9'
        else:
            ans += time[-2:]
        return ans
    
    
    """ 1737. 满足三条件之一需改变的最少字符数 #medium
给定两个字符串, 每次操作可以修改其中的任一字符为小写字母. 问得到以下三种状态之一, 最少步数. 条件: a的每个字母严格小于b的任意字母; 或者b的每个字母严格大于a的任意字母; 或者a和b都由同一个字母构成.
思路1: #计数, 然后考虑每一种情况.
    debug: 原本直接 [a,z] 遍历了, 但有问题. 因为是 **严格小于关系**, 因此遍历分割字符x的过程中, 要求一个字符串都小于等于x, 另一个都大于x; 因此, 这里的x的实际范围是 `[a,z)`
"""
    def minCharacters(self, a: str, b: str) -> int:
        ca, cb = Counter(a), Counter(b)
        ans = inf
        for ch in string.ascii_lowercase:
            ans = min(ans, len(a)+len(b)-ca[ch]-cb[ch])
        for ch in string.ascii_lowercase[:-1]:
            ans = min(ans,
                sum(v for k,v in ca.items() if k<=ch) + sum(v for k,v in cb.items() if k>ch),
                sum(v for k,v in cb.items() if k<=ch) + sum(v for k,v in ca.items() if k>ch)
            )
        return ans
    
    """ 1738. 找出第 K 大的异或坐标值 #medium #题型
对于一个二维矩阵, 对于每一个 (a,b) 坐标计算的score为, 以 (0,0)和(a,b) 两点确定的矩阵的所有值的异或. 求这些分数中第 K 大的值.
思路1: 采用二维 #前缀和 来存储每个位置的score. 
    需要注意这里前缀和的计算方式: `pre(i,j)=pre(i-1,j) ^ pre(i,j-1) ^ pre(i-1,j-1) ^ matrix(i,j)`. 利用了 x^x=0 这一性质.
    然后要返回第K大的元素, 参见「0215. 数组中的第K个最大元素」.
    [官答](https://leetcode.cn/problems/find-kth-largest-xor-coordinate-value/solution/zhao-chu-di-k-da-de-yi-huo-zuo-biao-zhi-mgick/)
"""
    def kthLargestValue(self, matrix: List[List[int]], k: int) -> int:
        m,n = len(matrix), len(matrix[0])
        xor = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                xor[i][j] = xor[i][j-1]^matrix[i][j] if j>0 else matrix[i][j]
                # if i>0: xor[i][j] ^= xor[i-1][j]
        for i in range(1,m):
            for j in range(n):
                xor[i][j] ^= xor[i-1][j]
        print(xor)
        return sorted(itertools.chain(*xor))[-k]
    
    """ 1739. 放置盒子 #hard #interest #题型
在一个房间放置n个正方体盒子. 只有当底部盒子的四个侧面都是墙壁/其他盒子的情况下, 才能在上面堆叠了. 问最少接触地面的盒子的数量. 图见 [题](https://leetcode.cn/problems/building-boxes/)
提示: 最优的堆叠方式正如题目所示.
思路1: #模拟 堆叠过程, #二分
    先来看最优堆叠情况下, 底层三角形的边长和体积的关系: 
        从上到下每一层的边长分别为 1,2,...,n. 每一层面积为 `s[i] = i*(i+1)/2`. 因此, 体积为 `v[n] = sum{ s[1...n] }` (也可以推导出公式).
    在给定正方形数量n的情况下, 计算最大的满足 `v[j] <= n`  的边长. 然后在其上添加 `remain = n - v[j]` 个正方体即可.
    如何计算需要增加多少个地面元素? 参见下面的演示, 增加关系同样按照三角形面积 s 的方式进行增长. 二分找到最小满足 `remian <= s[j]` 的下标即可.
    
# 底边边长为3的最优堆叠体的顶视图
000
00
0
# 底面增加两个, 可以在上面堆一个. 共 3个
00XX
00X
0
# 再增加一个, 可以另外堆叠两个. 共 6个
0XXX
0XX
0X
"""
    def minimumBoxes(self, n: int) -> int:
        MAX = 10**5
        s = [i*(i+1)//2 for i in range(MAX)]
        v = list(accumulate(s))
        idx = bisect.bisect_right(v, n)
        ans = s[idx-1]
        remain = n - v[idx-1]
        idx = bisect_left(s, remain)
        return ans + idx


    """ 0215. 数组中的第K个最大元素 #medium #题型 #star
给定一个数组, 要求返回其中第k大的元素.
限制: 数组长度 1e5
思路1: 维护一个大小为k 的 最小 #堆
    复杂度: O(n logk)
思路2: #快速选择, 基于 #快速排序
    基本思路是, 每次选择一个pivot, 将数组元素按照相较pivot的大小关系分成两边.
    具体而言, 需要实现 `partition(arr, l,r)` 在 `arr[l...r]` 中随机选择一个pivot, 并返回其下标.
    复杂度: 平均复杂度 `O(n)`, 最坏情况下 `O(n^2)`. 为此, 在选择pivot的时候可以增加 random.
    具体见 [官答](https://leetcode.cn/problems/kth-largest-element-in-an-array/solution/shu-zu-zhong-de-di-kge-zui-da-yuan-su-by-leetcode-/)
总结: 
"""
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # 推排序
        h = nums[:k]
        heapify(h)
        for num in nums[k:]:
            if num>h[0]:
                heappushpop(h, num)
        return h[0]
            
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # 快速选择
        random.seed(time.time())
        def partition(arr, l,r):
            # 选择 arr[r] 作为 pivot, 进行划分.
            x = arr[r]  # pivot
            i = l-1     # 记录最右边的 <=x 的位置
            for j in range(l, r):
                if arr[j]<=x:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            i += 1
            arr[i], arr[r] = arr[r], arr[i]
            return i
        def randomPartition(arr, l, r):
            # 在partition的基础上, 随机选择一个位置作为 pivot.
            idx = random.randint(l, r)
            arr[idx], arr[r] = arr[r], arr[idx]
            return partition(arr, l, r)
        
        def quickselect(arr, l, r, k):
            # 返回arr中第k大的元素
            # i = partition(arr, l, r)
            i = randomPartition(arr, l, r)
            if i==k:
                return arr[i]
            elif i<k:
                return quickselect(arr, i+1, r, k)
            else:
                return quickselect(arr, l, i-1, k)
        
        return quickselect(nums, 0, len(nums)-1, len(nums)-k)
    
sol = Solution()
result = [
    # sol.minimumBoxes(3),
    # sol.minimumBoxes(4),
    # sol.minimumBoxes(6),
    # sol.minimumBoxes(10),
    sol.findKthLargest([3,2,1,5,6,4], k = 2)
    
]
for r in result:
    print(r)
