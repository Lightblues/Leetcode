from time import time
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

from utils_leetcode import testClass
# from structures import ListNode, TreeNode
""" 
https://leetcode.cn/contest/weekly-contest-262
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 2032. 至少在两个数组中出现的值 """
    def twoOutOfThree(self, nums1: List[int], nums2: List[int], nums3: List[int]) -> List[int]:
        s1, s2, s3 = set(nums1), set(nums2), set(nums3)
        return list(
            s1.intersection(s2).union(
                s2.intersection(s3).union(
                    s3.intersection(s1)
                )
            )
        )
        
    """ 2033. 获取单值网格的最小操作数 #medium #题型
给定一个grid, 每次操作可以对于其中的每个元素加减x, 要求使得所有元素相同的最小操作数.
思路: #中位数
    注意, 这里不应该算mean, 而是中位数!!
    考虑一个反例: [1,1,1,1,100] 将小元素移动到mean的成本要高于移动较大值.
    中位数的逻辑在于, 每修改一次target都会对于所有的元素产生影响: 要么都加x, 要么都减x. 因此要将左右元素数量均衡.
    from [here](https://leetcode.cn/problems/minimum-operations-to-make-a-uni-value-grid/solution/zhong-wei-shu-by-endlesscheng-p0vj/): 假设要让所有元素均为 y，设小于 y 的元素有 p 个，大于 y 的元素有 q 个.
        则 y 每增加一个 x, 都会使得操作数增加 p - q; (或者说, 每减少 x, 都会使得操作数减少 q - p). 因此取最小值的条件是 `p=q`.
"""
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        # 注意不是 mean!!
        # m,n = len(grid), len(grid[0])
        # import numpy as np
        # mean = np.sum(grid) / (m*n)
        # a1 = (grid[0][0] - mean) // x
        # a2 = a1 + 1
        # t1, t2 = grid[0][0] - a1 * x, grid[0][0] - a2 * x
        # target = t1 if abs(t1-mean) < abs(t2-mean) else t2
        # ans = 0
        # for row in grid:
        #     for ele in row:
        #         if (ele-target) % x != 0:
        #             return -1
        #         ans += int(abs((ele-target) // x))
        # return ans
        
        nums = list(itertools.chain(*grid))
        nums.sort()
        target = nums[len(nums)//2]
        ans = 0
        for ele in nums:
            if (ele-target) % x != 0:
                return -1
            ans += abs((ele-target) // x)
        return ans
    
    """ 2034. 股票价格波动 #medium #题型
(timestamp, price) 定义股票价格, 进来的timestamp是乱序的. 注意, **价格可能出现错误, 假设后到的是对于该时刻价格的修正**.
要求实现一个类, 有操作
    int current() 返回股票 最新价格. 
        这个比较简单, 维护一个最大时间戳即可
    void update(int timestamp, int price) 在时间点 timestamp 更新股票价格为 price.
        实现更新, 主体逻辑
    int maximum() 返回股票 最高价格 (相应的还有最低价格)
        本题的特殊点即在于有修正错误值的操作, 因为需要用一定的数据结构来存储这一信息
每日一题做过了, 这里再记录一下思路:
时间戳到价格的存储肯定用一个map, 关键在于如何实现更新操作?
思路1: #有序集合 为了快速得到最大最小值, 显然可以维护一个有序结构. 注意: **有序集合的插入(更新)和最大最小查询复杂度均为 `O(log(n))`**
    官答用了 SortedList. 尝试了用 slice 语法实现更新, 发现 O(n) 的复杂度还是会超时.
思路2: 最大最小的查询, 另外的一种思路自然是 #堆 结构. 
    这里多了数据可能无效这一限制, 则可以将 (price, timestamp) 当做一个元素, 从堆顶取出元素的时候, 只需要在 priceMap 中查询数据是否仍有效即可.
    这样在没有太多错误数据情况下, 查询的时间复杂度为 `O(1)`
[here](https://leetcode.cn/problems/stock-price-fluctuation/solution/gu-piao-jie-ge-bo-dong-by-leetcode-solut-rwrb/)
"""
    def test_class(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
    
    """ 2035. 将数组分成两个数组并最小化数组和的差 #hard #题型
将长度为 2n 的数组分成等长的两部分, 要求两个数组和相差最小.
复杂度: n<=15
思路: #折半枚举 +排序+ #二分
    这里用的思路是 #折半枚举. 具体而言, 本题需要从 2n个数字从取 n个. 折半枚举的思路是分别从左侧的一半和右侧的一般数组中取 i, n-i 个.
    计算复杂度: 直接枚举的复杂度为 `math.comb(2n, n)`; 折半枚举每一边的复杂度为 `O(2**n)`. 例如在 n=15 时差了好几个数量级
    用数组(集合)记录在left中取i个数字可能得到的和, 并排序; 然后在右侧枚举取n-i个数字, 两者匹配计算.
    [here](https://leetcode.cn/problems/partition-array-into-two-arrays-to-minimize-sum-difference/solution/zhe-ban-mei-ju-pai-xu-er-fen-by-endlessc-04fn/)

关联: 1755.最接近目标值的子序列和; 0805.数组的均值分割; 0416.分割等和子集; 0494.目标和
见 [总结](https://leetcode.cn/problems/closest-subsequence-sum/solution/by-mountain-ocean-1s0v/)
"""
    def minimumDifference(self, nums: List[int]) -> int:
        n = len(nums)//2
        sumNums = sum(nums)
        target = sumNums // 2
        
        left = nums[:n]
        # 记录左边的一半数字中, 选择 0-n 个数字组成的和; 排序
        count2sum = [set() for _ in range(n+1)]
        for i in range((1<<n)):
            count = 0
            s = 0
            for j in range(n):
                if i&(1<<j):
                    count += 1
                    s += left[j]
            count2sum[count].add(s)
        for i in range(n+1):
            count2sum[i] = sorted(list(count2sum[i]))
        
        ans = math.inf
        right = nums[n:]
        # 防止重复二分
        cache = [set() for _ in range(n+1)]
        for i in range((1<<n)):
            count = 0
            s = 0
            for j in range(n):
                if i&(1<<j):
                    count += 1
                    s += right[j]
            if s in cache[count]: continue
            cache[count].add(s)
            # 从右侧取 count 个数字, 匹配左侧的 countLeft 个; 左右两部分的目标和为 target
            countLeft = n - count
            targetLeft = target - s
            pairs = count2sum[countLeft]
            # 二分, 若 targetLeft在两个数字之间, 则左右的点都有可能是答案
            idx = bisect.bisect_left(pairs, targetLeft)
            ans = min(ans, 
                      abs(sumNums - 2*(pairs[min(idx, len(pairs)-1)]+s)),
                      abs(sumNums - 2*(pairs[max(0, idx-1)]+s))
                    )
        return ans
            


class StockPrice:
    """ 尝试用 Python 切片, 还是超时了 """
    def __init__(self):
        self.maxTime = 0
        self.priceMap = {}
        self.priceList = []

    def update(self, timestamp: int, price: int) -> None:
        self.maxTime = max(self.maxTime, timestamp)
        # 若是price修正, 删除原来的记录
        if timestamp in self.priceMap: #  and self.priceMap[timestamp] != price
            idx = bisect.bisect_left(self.priceList, self.priceMap[timestamp])
            self.priceList = self.priceList[:idx] + self.priceList[idx+1:]
        self.priceMap[timestamp] = price
        # 将记录插入到priceList中
        idx = bisect.bisect_left(self.priceList, price)
        self.priceList = self.priceList[:idx] + [price] + self.priceList[idx:]

    def current(self) -> int:
        return self.priceMap[self.maxTime]

    def maximum(self) -> int:
        return self.priceList[-1]

    def minimum(self) -> int:
        return self.priceList[0]

sol = Solution()
result = [
    # sol.twoOutOfThree(nums1 = [1,1,3,2], nums2 = [2,3], nums3 = [3]),
    
    sol.minOperations([[931,128],[639,712]],73),
    sol.minOperations(grid = [[2,4],[6,8]], x = 2),
    sol.minOperations(grid = [[1,2],[3,4]], x = 2),
    
#     sol.test_class("""["StockPrice", "update", "update", "current", "maximum", "update", "maximum", "update", "minimum"]
# [[], [1, 10], [2, 5], [], [], [1, 3], [], [4, 2], []]"""),

    # sol.minimumDifference(nums = [3,9,7,3]),
    # sol.minimumDifference(nums = [2,-1,0,4,-2,-9]),
]
for r in result:
    print(r)
