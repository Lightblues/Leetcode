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
from itertools import chain, product, permutations, combinations, combinations_with_replacement
import string
from string import ascii_lowercase, ascii_uppercase
import sys, os
# sys.setrecursionlimit(10000)

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode

""" 
题目: 
2035. 将数组分成两个数组并最小化数组和的差; 1755.最接近目标值的子序列和; 
0805.数组的均值分割; 0416.分割等和子集; 0494.目标和 
见 [总结](https://leetcode.cn/problems/closest-subsequence-sum/solution/by-mountain-ocean-1s0v/)
@2022 """


class Solution:

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
            

    """ 1755. 最接近目标值的子序列和 #hard #折半枚举
给定一个数组, 要求找到一个子序列, 它的和最接近目标值. 返回这个最小 abs
复杂度: 长度为 len<=40. 直接暴力枚举的复杂度为 O(2^n) 会超时.
思路: 折半枚举. 先枚举前一半数组的子序列可能组成的和, 排好序 sums. 然后再枚举右侧一半的和, 然后和 sums 匹配, 二分找到最接近目标的
"""
    def minAbsDifference(self, nums: List[int], goal: int) -> int:
        half = len(nums)//2
        left, right = nums[:half], nums[half:]
        sums = set()
        def dfs_left(s, i):
            if i==len(left):
                sums.add(s)
                return
            dfs_left(s+left[i], i+1)
            dfs_left(s, i+1)
        dfs_left(0, 0)
        sums = sorted(list(sums))
        
        ans = math.inf
        def dfs_right(s, i):
            if i==len(right):
                target = goal - s
                idx = bisect.bisect_left(sums, target)
                nonlocal ans
                ans = min(
                    ans, 
                    abs(target - sums[min(idx, len(sums)-1)]),
                    abs(target - sums[max(0, idx-1)])
                )
                return
            dfs_right(s+right[i], i+1)
            dfs_right(s, i+1)
        dfs_right(0, 0)
        return ans

    """ 0805. 数组的均值分割 #hard #Fraction #题型 #折半枚举
给定一个数组, 将其分为两个子数组, 问能否使得两个数组的均值相同.
因为所有的元素都已知, 因此题目等价于, 能够在一个大数组中找到一个子数组 (非空非全), 使其均值等于目标值 `target = mean(nums)`.
复杂度: n<=30
思路: #折半枚举
    直接枚举子数组的复杂度为 O(2^n) 会超时. 考虑 #折半枚举
    具体而言, 先枚举左半部分, 用 `sumLeft[i] = set()` 来记录元素数量为 i 的子数组的和. 再遍历右半部分, `pair  = target * (j + i) - sum` 在 sumLeft[j] 中存在则说明找到了.
    注意要求数组非空
注意: 要留意浮点数的问题. 因为上面的 target 的计算可能除不尽, 这样上式计算的 pair 可能是小数, 无法直接比较.
    一种解决方案是采用 Fraction, 但尝试超时.
    更方便的思路是约束 target 为整数 —— 只需要把 nums 所有元素 `*len(nums)` 这样均值必为整数
思路2: [官方](https://leetcode.cn/problems/split-array-with-same-average/solution/shu-zu-de-jun-zhi-fen-ge-by-leetcode/)
    上面要考虑左右两边的元素数量. 这里将所有元素减去了均值. 这样, 目标就变为「找到一个和为0 的子数组」. (避免了上面 target浮点数的问题)
    自己用的 DFS 进行枚举, 官方用 for 展开了可能会更快?
"""
    def splitArraySameAverage_0(self, nums: List[int]) -> bool:
        """ 超时了 """
        # epsilon = 1e-4
        from fractions import Fraction
        if len(nums) < 2: return False
        half = len(nums)//2
        left, right = nums[:half], nums[half:]
        target = Fraction(sum(nums), len(nums))
        sums = [set() for _ in range(len(nums)+1)]
        def dfs_left(s, i, count):
            if i==len(left):
                if count>0 and Fraction(s, count) == target: return True
                sums[count].add(s)
                return False
            r1 = dfs_left(s+left[i], i+1, count+1)
            if r1: return True
            return dfs_left(s, i+1, count)
        r = dfs_left(0, 0, count=0)
        if r: 
            return True
        
        def dfs_right(s, i, count):
            if i==len(right):
                if count>0 and Fraction(s, count) == target:
                    return True
                for j in range(len(nums) - count):
                    # 注意, 如果这里如果不用 Fraction, 浮点数可能有问题
                    # 当然, 也可以对于所有元素 * len(nums) 这样均值必然为整数
                    pair = target * (count + j) - s
                    if len(nums) > count + j > 0 and pair.denominator==1 and int(pair) in sums[j]: 
                        return True
                return False
            r1 = dfs_right(s+right[i], i+1, count+1)
            if r1:
                return True
            r2 =  dfs_right(s, i+1, count)
            if r2:
                return True
            return False
        return dfs_right(0, 0, 0)

    def splitArraySameAverage(self, nums: List[int]) -> bool:
        """ 相较于上一种解法, 没用 Fraction, 过了 """
        if len(nums) < 2: return False
        n = len(nums)
        # 对所有元素 * n , 这样均值肯定为整数
        nums = [i*n for i in nums]
        half = len(nums)//2
        left, right = nums[:half], nums[half:]
        target = sum(nums)// len(nums)
        sums = [set() for _ in range(len(nums)+1)]
        def dfs_left(s, i, count):
            if i==len(left):
                # 注意不能为空集
                if count>0 and s/count == target: return True
                sums[count].add(s)
                return False
            r1 = dfs_left(s+left[i], i+1, count+1)
            if r1: return True
            return dfs_left(s, i+1, count)
        r = dfs_left(0, 0, count=0)
        if r: 
            return True
        
        def dfs_right(s, i, count):
            if i==len(right):
                if count>0 and s/count == target:
                    return True
                for j in range(len(nums) - count):
                    # 注意, 如果这里如果不用 Fraction, 浮点数可能有问题
                    # 当然, 也可以对于所有元素 * len(nums) 这样均值必然为整数
                    pair = target * (count + j) - s
                    if count + j > 0 and pair in sums[j]: 
                        return True
                return False
            r1 = dfs_right(s+right[i], i+1, count+1)
            if r1:
                return True
            return dfs_right(s, i+1, count)
        return dfs_right(0, 0, 0)

    """ https://leetcode.cn/problems/split-array-with-same-average/solution/shu-zu-de-jun-zhi-fen-ge-by-leetcode/ """
    def splitArraySameAverage1(self, A):
        from fractions import Fraction
        N = len(A)
        S = sum(A)
        # 将所有元素减去均值
        A = [z - Fraction(S, N) for z in A]

        if N == 1: return False

        # Want zero subset sum
        left = {A[0]}
        for i in range(1, N//2):
            left = {z + A[i] for z in left} | left | {A[i]}
        if 0 in left: return True

        right = {A[-1]}
        for i in range(N//2, N-1):
            right = {z + A[i] for z in right} | right | {A[i]}
        if 0 in right: return True

        sleft = sum(A[i] for i in range(N//2))
        sright = sum(A[i] for i in range(N//2, N))

        return any(-ha in right and (ha, -ha) != (sleft, sright) for ha in left)
    
    
    """ 0494. 目标和 #medium #背包
给定一个整数数组, 在它们之间加 +/- 组成表达式, 要求返回结果为 target 的表达式数量.

- 方法一, DFS
    - 改进: #折半枚举 可以减少 DFS的复杂度
- 方法二, DP, see [here](https://leetcode-cn.com/problems/target-sum/solution/mu-biao-he-by-leetcode-solution-o0cp/)
    - `dp[i][j]` 为前 i 个数字中选取部分, 其和为 j 的组合数量
    - 可知, 更新公式为 `dp[i][j] = dp[i-1][j] + dp[i-1][j-nums[i]]`, 当 `j<nums[i]` 不合法, 第二项取0.
    - 优化空间, 可以用 **滚动数组**. 则更新公式为 `dp[j] += dp[j-nums[j]]`. 注意因为用了滚动数组, 内层循环需采用倒序遍历的方式.
"""
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        n = len(nums)
        if n==1:
            return 1 if nums[0]==target or nums[0]==target else 0
        
        leftList = [0]
        for i in range(n//2):
            leftList = list(itertools.chain(*[(a+nums[i], a-nums[i]) for a in leftList]))
        rightList = set([0])
        for i in range(n//2, n):
            rightList = list(itertools.chain(*[(a+nums[i], a-nums[i]) for a in rightList]))
            # rightSet = rightSet | {j+nums[i] for j in rightSet} | {j-nums[i] for j in rightSet}
        countLeft, countRight = collections.Counter(leftList), collections.Counter(rightList)
        ans = 0
        for a in countLeft:
            ans += countLeft[a] * countRight[target-a]
        return ans
    
    
    """ 0416. 分割等和子集 #背包 #medium
相较于 「0805. 数组的均值分割」这里要求两个数组的和相等.
复杂性: 数组长度 200, 每个元素大小 100.
思路1: #折半枚举
    注意本题的特殊性, 由于每个元素的数量较小, 元素和最大为 `k = 200/2 * 100` (实际上 target 也是限制, 可以剪枝), 要比枚举数量 `O(2^100)`, 因此不会超时.
    复杂度: O(n/2 * k) 注意这里的元素和限制给出了复杂度限制 k.
思路2: 建模为 #背包 问题, 然后 #DP 求解
    具体而言, 用 dp[i][j] 表示使用数组的前 i 个元素, 和为 j 的组合数量. 同样我们可以限制 j<=target.
    递推公式: 当 nums[i] 小于等于 j 时, `dp[i][j] = dp[i-1][j] or dp[i-1][j-nums[i]]`. 否则 `dp[i][j] = dp[i-1][j]`.
    复杂度: O(n * target).
"""
    def canPartition_0(self, nums: List[int]) -> bool:
        """  """
        n = len(nums)
        s = sum(nums)
        if s%2 != 0: return False
        target = s//2
        
        # left, right = nums[:n//2], nums[n//2:]
        leftSet = {0}
        for i in range(n//2):
            # 注意, 由于都是正数, 可以基于  if a+nums[i]<=target 剪枝
            leftSet = leftSet | {a+nums[i] for a in leftSet if a+nums[i]<=target}
        if target in leftSet: return True
        rightSet = {0}
        for i in range(n//2, n):
            rightSet = rightSet | {a+nums[i] for a in rightSet if a+nums[i]<=target}
        if target in rightSet: return True
        
        for a in leftSet:
            if target-a in rightSet: return True
        return False
    
    def canPartition(self, nums: List[int]) -> bool:
        """ DP
https://leetcode.cn/problems/partition-equal-subset-sum/solution/fen-ge-deng-he-zi-ji-by-leetcode-solution/"""
        n = len(nums)
        if n < 2:
            return False
        
        total = sum(nums)
        if total % 2 != 0:
            return False
        
        target = total // 2
        dp = [True] + [False] * target
        for i, num in enumerate(nums):
            for j in range(target, num - 1, -1):
                dp[j] |= dp[j - num]
        
        return dp[target]


sol = Solution()
result = [
    # sol.minimumDifference(nums = [3,9,7,3]),
    # sol.minimumDifference(nums = [2,-1,0,4,-2,-9]),

    # sol.minAbsDifference(nums = [5,-7,3,5], goal = 6),
    # sol.minAbsDifference(nums = [7,-9,15,-2], goal = -5),
    
    # sol.splitArraySameAverage([1865,2885,6227,3222,2726,1710,1775,716,8901,8283,9082,5676,5513,9462,4512,268,4636,129,8196,1722,2583,6497,5181,2333,2067,2653,5246,3676,1566,9768]),
    # sol.splitArraySameAverage(nums = [1,2,3,4,5,6,7,8]),
    # sol.splitArraySameAverage([1,3]),
    # sol.splitArraySameAverage([6,8,18,3,1]),
    # sol.splitArraySameAverage([904,8738,6439,1889,138,5771,8899,5790,662,8402,3074,1844,5926,8720,7159,6793,7402,9466,1282,1748,434,842,22]),
    
    # sol.findTargetSumWays(nums = [1,1,1,1,1], target = 3),
    # sol.findTargetSumWays([1,0],1)
    
    sol.canPartition(nums = [1,5,11,5]),
    sol.canPartition(nums = [1,2,3,5]),
]
for r in result:
    print(r)
