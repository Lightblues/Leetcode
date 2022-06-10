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
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-52
@2022 """
class Solution:
    """ 1859. 将句子排序 """
    def sortSentence(self, s: str) -> str:
        idx2word = {}
        for w in s.strip().split():
            idx2word[int(w[-1])] = w[:-1]
        ans = []
        for i in range(1, len(idx2word) + 1):
            ans.append(idx2word[i])
        return " ".join(ans)
    
    """ 1860. 增长的内存泄露 #meium
有一个程序每一秒新占用的内存数以 1,2,3,... 形式递增; 现有两个大小分别为 memory1, memory2, 分配策略为: 每次选择空余较多的那个分配, 如果相同则分配第一个. 要求返回内容不够分配的时刻, 以及此时两内存的剩余.
限制: 2^31-1
思路1: 模拟
    要死, 看成了大小限制为 1e31 级别, 想了半天如何找规律...
    在32进制的大小下, 可以直接模拟求解. 时间估计如下: 到时刻t分配的总内存为 1+2...n = O(n^2) 级别, 因此时间复杂度为 O(sqrt(memory1 + memory2)), 这样 `2**16 = O(5)` 没问题

"""
    def memLeak(self, memory1: int, memory2: int) -> List[int]:
        t = 1
        while max(memory1, memory2) >= t:
            if memory1 >= memory2: memory1 -= t
            else: memory2 -= t
            t += 1
        return [t, memory1, memory2]
    
    """ 1861. 旋转盒子 #medium
有一个矩形的盒子, 有两类物体: 障碍物(不会移动), 石头(占据一个格子). 要求将盒子顺时针转90度之后的物体分布.
思路: 直接 #模拟
"""
    def rotateTheBox(self, box: List[List[str]]) -> List[List[str]]:
        m, n = len(box), len(box[0])
        ans = [["."] * m for _ in range(n)]
        for i in range(m):
            tj = m - 1 - i
            lastObs = n
            for j in range(n-1, -1, -1):
                if box[i][j] == ".": continue
                elif box[i][j] == "*":
                    ti = j
                    ans[ti][tj] = "*"
                    lastObs = j
                    continue
                else:
                    ti = lastObs - 1
                    ans[ti][tj] = "#"
                    lastObs -= 1
        return ans
    
    """ 1862. 向下取整数对和 #hard #题型
给定一个整数数组 nums, 对于所有的下标组 (i,j), 计算 nums[i]//nums[j], 求和
思路0: 尝试讨巧借用 numpy, 结果发现超时了. 因为服务器是单核?
思路1: 遍历 + #前缀和 复杂度为 #调和级数
    不妨考虑从小到大排列, 对于数字 y, 我们遍历 x/y 的所有可能: `1,...,upper//y`.
    如何统计 `x//y==`a, 也即 x 在 [ay, ay+y) 范围内的个数? 可以用一个cnt数组记录所有数字出现的次数, 这样只需要对该区间求和即可; 显然用前缀和可以 O(1) 得到
    这里的复杂度分析: 假设最大值为` C, 有 C/1 + C/2 + ... C/C`, 是一个调和级数, 复杂度为 `O(C log(C))`
    [here](https://leetcode.cn/problems/sum-of-floored-pairs/solution/xiang-xia-qu-zheng-shu-dui-he-by-leetcod-u3eg/)
思路2: #二分 + #cache
    既然上述的遍历 x//y 的方式可以过 (有调和级数保障), 那么如果想不到用cnt计数, 直接排序之后二分查找也是可以的.
    为了得到 [ay, ay+y) 范围内的数字, 显然可以在排好序的数组中二分查找边界.
Note: 调和级数的边界
$\sum_{i=1}^{n} \frac{1}{i}=\ln (n+1)+\gamma$
"""
    def sumOfFlooredPairs(self, nums: List[int]) -> int:
        # 试图取巧
        import numpy as np
        a = np.array(nums).reshape((-1, 1))
        r = np.sum(np.floor(a / a.T))
        return int(r)
    
    def sumOfFlooredPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        upper = max(nums)       # 取最大值
        # nums 计数. 为了计算前缀和, 需要一个连续数组
        cnt = [0] * (upper + 1) # nums 从1开始, 方便起见前面加一个0
        for n in nums:
            cnt[n] += 1
        # 前缀和
        acc = list(itertools.accumulate(cnt, initial=0))
        ans = 0
        # 遍历 y
        for num in range(1, upper+1):
            if not cnt[num]: continue
            a = 1
            # 遍历 floor(x/y)
            while num * a <= upper:
                # 注意所求区间和为 [num*a, num*(a+1)) 左闭右开 区间, 因此公式为 sum = acc[num*(a+1)] - acc[num*a], (一般求[a,b] 范围和为 sum = acc[b+1] - acc[a])
                # 另外注意数组越界: cnt 的长度为 upper+1, 因此 acc数组的长度为 upper+2
                ans += a * (acc[min(num*a + num, upper+1)] - acc[num*a]) * cnt[num]
                a += 1
        return ans % MOD
    
    def sumOfFlooredPairs(self, nums: List[int]) -> int:
        # 采用 #二分 + #cache
        nums.sort()
        upper = nums[-1]
        @lru_cache(None)
        def f(x):
            ans = 0
            a = x
            left = bisect_left(nums, a)
            while a <= upper:
                right = bisect.bisect_left(nums, a+x)
                ans += (right - left) * a//x
                left = right
                a += x
            return ans % (10**9 + 7)
        ans = 0
        for x in nums:
            ans += f(x)
        return ans
    
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
    # sol.sortSentence(s = "is2 sentence4 This1 a3"),
    
    # sol.memLeak(memory1 = 2, memory2 = 2),
    # sol.memLeak(8, 11),
    
    # sol.rotateTheBox(box = [["#","#","*",".","*","."],
    #         ["#","#","#","*",".","."],
    #         ["#","#","#",".","#","."]]),
    # sol.rotateTheBox(box = [["#",".","*","."],
    #         ["#","#","*","."]]),
    
    sol.sumOfFlooredPairs(nums = [2,5,9]),
    sol.sumOfFlooredPairs(nums = [7,7,7,7,7,7,7]),
]
for r in result:
    print(r)
