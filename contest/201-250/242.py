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
https://leetcode.cn/contest/weekly-contest-242
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1869. 哪种连续子字符串更长 """
    def checkZeroOnes(self, s: str) -> bool:
        last = ""; cnt = 0
        mx0= mx1 = 0
        for ch in s+" ":
            if ch==last:
                cnt += 1
            else:
                if last=='0': mx0=max(mx0, cnt)
                elif last=='1': mx1=max(mx1, cnt)
                cnt=1
                last = ch
        return mx1 > mx0
    
    """ 1870. 准时到达的列车最小时速 #medium
有一组路, 路口只能在整点出发, 要求在hour范围内到达, 问最少能够到达的速度是多少.
限制: 答案 1e7 以内的整数.
思路1: 标准的 #二分 题目. 需要注意的是要根据题意来判断边界条件.
"""
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        # 边界
        if hour<len(dist)-1+dist[-1]/1e7: return -1
        def check(speed):
            acc = 0
            for d in dist[:-1]: acc += ceil(d/speed)
            acc += dist[-1]/speed
            return acc <= hour
        ans = inf
        l,r = 1, int(1e7)
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = min(ans, mid)
                r = mid-1
            else:
                l = mid+1
        return ans
    
    """ 1871. 跳跃游戏 VII #medium
有01的路径s, 要求从开头跳到最后, 每次只能跳 `[minJump, maxJump]` 的距离并且只能跳到值为0的位置. 问能否跳到最后.
思路1: #二分
    用一个有序数组记录所有可达的0位置. 在顺序遍历s中可跳点的过程中, 要求「判断 `[idx-maxJump, idx-minJump]` 范围内是否有可达点」, 这可以通过两次二分查找得到.
    复杂度: O(n log(n))
思路2: 官答给出的是用 #DP 然后用 #前缀和 优化
    针对遍历过程中判断某一范围内是否有可达点这一问题, 用一个DP数组来记录信息. 问题是顺序判断的复杂度为 O(maxJump-minJump) = O(n), 如何优化?
    答案是利用前缀和.
    see [官答](https://leetcode.cn/problems/jump-game-vii/solution/tiao-yue-you-xi-vii-by-leetcode-solution-rsyv/)
    
"""
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        reached = [0]   # 注意到引入初始点
        for i,ch in enumerate(s):
            if ch=='1': continue
            il, ir = bisect_left(reached, i-maxJump), bisect_right(reached, i-minJump)
            if ir > il: reached.append(i)
        return reached[-1] == n-1
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        # 思路2
        n = len(s)
        f, pre = [0] * n, [0] * n
        f[0] = 1
        # 由于我们从 i=minJump 开始动态规划，因此需要将 [0,minJump) 这部分的前缀和预处理出来
        for i in range(minJump):
            pre[i] = 1
        for i in range(minJump, n):
            left, right = i - maxJump, i - minJump
            if s[i] == "0":
                total = pre[right] - (0 if left <= 0 else pre[left - 1])
                f[i] = int(total != 0)
            pre[i] = pre[i - 1] + f[i]
        return bool(f[n - 1])

    """ 1872. 石子游戏 VIII #hard #interest #博弈
有一排数量n的石子, 每个石子有一定的分数, AB轮流从左侧拿多于一颗石子, 然后分数累计为自己的分数, 然后将一个等价值的石子放回去. 两者都想 **最大化自己与对方的分数差** (也即, A想最大化 scoreA-scoreB, B则想最小化). 问都在最优策略下, scoreA-scoreB 的值.
限制: 数量 1e5
提示: 
    可以考虑 #前缀和. 问题等价于, AB轮流取下标 (每一个下标要比上一个更大, 并且第一个要求>0) 获得分数
思路1: 采用 #DP
    表示: 记 f[i] 为A在选择 [i,n) 范围内下标时可以取得的最大分差.
    递推: 两种情况: 1) 若A没选第i个石子, 则有 `f[i] = f[i+1]`; 2) 若选了i (拿到 acc[i] 分), 则对于B来说, **他要从 [i+1,n) 范围内选择, 使得分差最小, 正好等于 `-f[i+1]`**, 因此有 `f[i] = acc[i]-f[i+1]`. 因此有: `f[i] = max{ f[i+1], acc[i]-f[i+1] }`.
    因此, 从后往前 #逆序 DP即可, 最后的答案即为 f[1]
    [官答](https://leetcode.cn/problems/stone-game-viii/solution/shi-zi-you-xi-viii-by-leetcode-solution-e8dx/)
    说明: 这里的情况2比较tricky, [灵神](https://leetcode.cn/problems/stone-game-viii/solution/zai-qian-zhui-he-shang-dao-xu-dp-by-endl-jxqs/) 的解答中分别给出了AB两人的递推公式, **因为两者形式一致所以可以合并到一起**, 这样思考更顺.
总结: 在思考的时候有点被例子带歪; 考虑到用前缀和后最tricky的地方在于想到情况2的公式, 这里可以借鉴灵神的思路, 更容易想到一点.
"""
    def stoneGameVIII(self, stones: List[int]) -> int:
        n = len(stones); acc = list(accumulate(stones))
        f = [0] * n
        f[n-1] = acc[n-1]
        for i in range(n-2, 0, -1):
            f[i] = max(f[i+1], acc[i]-f[i+1])
        return f[1]

    
sol = Solution()
result = [
    # sol.checkZeroOnes(s = "1101"),
    # sol.checkZeroOnes(s = "110100010"),
    # sol.minSpeedOnTime(dist = [1,3,2], hour = 6),
    # sol.minSpeedOnTime(dist = [1,3,2], hour = 2.7),
    # sol.canReach(s = "011010", minJump = 2, maxJump = 3),
    # sol.canReach(s = "01101110", minJump = 2, maxJump = 3),
    sol.stoneGameVIII(stones = [-1,2,-3,4,-5]),
    sol.stoneGameVIII(stones = [7,-6,5,10,5,-2,-6]),
    sol.stoneGameVIII(stones = [-10,-12]),
]
for r in result:
    print(r)
