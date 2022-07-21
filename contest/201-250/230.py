from turtle import st
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
https://leetcode.cn/contest/weekly-contest-230
@2022 """
class Solution:
    """ 1773. 统计匹配检索规则的物品数量 """
    def countMatches(self, items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
        ruleIdx = dict(zip(['type', 'color', 'name'], [0,1,2]))[ruleKey]
        return sum(1 for item in items if item[ruleIdx] == ruleValue)
    
    """ 1774. 最接近目标价格的甜点成本 #medium
需要从n种冰激凌基料中选择一种, 还可以选择添加m种配料,每种最多2个. 给定目标价格, 返回根据上述规则的配置方案下最接近的总价格.
限制: n,m 10, 价格数量级 1e4
思路1: 基料有n种选择, 配料有 3^m 种选择, 两两匹配计算与target的差值.
"""
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        # itertools.product
        toppings = [[0,p,2*p] for p in toppingCosts]
        topingCosts = [sum(p) for p in itertools.product(*toppings)]
        ans = 0; d = inf
        for b,t in itertools.product(baseCosts, topingCosts):
            # 差值更小, 相同时选择较小的
            if abs(b+t-target) < d or (abs(b+t-target) == d and b+t < ans):
                d = abs(b+t-target)
                ans = b+t
        return ans
        
    
    """ 1775. 通过最少操作次数使数组的和相等 #medium
给定两个所有元素在 [1,6] 之间的数组, 每次可以修改任意一个元素, 问两者之和相等的最少操作数.
思路1: #贪心
    不妨令两数组的和满足 s1 < s2. 记 `diff = s2-s1`, 目标是用最少操作使其变为0. #贪心 选择最快的即可
    对于 nums1,nums2 分别计数, 从大到小考虑每次可以减少的差值 (`i = 5,4,3,2,1`), 每次从nums1中取 i+1, 从nums2中取 6-i.

"""
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        s1, s2 = sum(nums1), sum(nums2)
        if s1 == s2:
            return 0
        elif s1 > s2:
            nums1, nums2 = nums2, nums1
            s1, s2 = s2, s1
        # 
        # 
        cnt1, cnt2 = Counter(nums1), Counter(nums2)
        diff = s2-s1
        acc = 0
        for i in range(6):
            c1 = cnt1[i+1]
            if diff <= c1 * (5-i):
                return acc + ceil(diff/(5-i))
            diff -= c1 * (5-i)
            acc += c1
            c2 = cnt2[6-i]
            if diff <= c2 * (5-i):
                return acc + ceil(diff/(5-i))
            diff -= c2 * (5-i)
            acc += c2
        if diff >0: return -1
        elif diff ==0: return acc

        

    """ 1776. 车队 II #hard #题型 #单调栈
有一组车 (position, speed) 相同方向行驶. 当两辆车相遇时, 它们按照较低速度组成「车队」. 问所有车与下一辆车相遇的时间 (不相遇则为 -1).
限制: 数组长度 1e5;  位置,速度 1e6
提示: 一定是速度快的车从后面追上前一辆车.
    这题的难点在于, 虽然idx可以追上idx+1车, 但idx+1的速度可能会被更前面的车所「拖慢」, 因此实际上相遇时间是需要计算得失idx和idx+x的相遇所需时间.
思路0: WA
    考虑, **对于速度从小到大处理 (相同速度不考虑), 它一定会追上前一辆更慢的车**.
思路0: 从右往左遍历, WA
    从右往左遍历(距离从大到小), 则idx车只能可能和idx+1发生碰撞, 碰撞后速度降为前一辆车. 因此, 非发生碰撞的车的速度一定是递减的. 所以可以用一个「单调递减栈」来维护. (进一步, 根本不需要用栈, 记录当前最慢速度即可.)
    但这样是错的, 因为如提示, **idx追上的不一定是idx+1** !
思路1: 用 #单调栈 递增栈, 来记录可能会被追到的车
    还是从右往左遍历. 用一个「单调递增栈」进行记录.
    #分类: 1) 若栈顶速度更快, 追不上, 而idx后面的车一定会被idx拖慢, 所以栈顶元素没用了, pop; 2) 否则, 说明idx可以追上栈顶元素, 但时间怎么算? 我们 计算idx追上栈顶所需的时间, 若该时间小于栈顶元素追上下一车的时间, 则直接利用两者计算; 否则, 我们递归栈内下一个元素, 直到找到满足条件的车. 注意到, 对于不满足要求的, **栈顶元素会在下一辆车追到之前撞上栈内下一个元素, 因此没有用了**, 可以pop. (从而将复杂度从 `O(n^2)` 降为 `O(n)`)
    参见 [here](https://leetcode.cn/problems/car-fleet-ii/solution/dan-diao-zhan-xiang-xi-jie-fa-by-2018272-5ff7/)
总结: 初看似乎从右往左用单调递减栈, 但实际上记录更高的速度是没有意义的 (会被前面更慢的所拖累, 永远不会发生碰撞); 反而 **用一个单调递增栈来记录可能发生碰撞的元素**. 对于「idx车可能实际上碰撞的是idx+x」这一难点, 遍历栈内元素的碰撞时间来求解, 利用了上述性质将没必要记录的元素直接pop掉, 从而降低了时间复杂度.
思路2: 相较于上面 O(n) 的单调栈「标准解法」, 这里用 #优先队列 来实现一种更为直观的思路, 复杂度 O(n logn). 更符合我刚开始的想法.
    核心: 根据相撞时间维护一个优先队列, 从小到大遍历.
    一开始, 假设所有车都与前一辆相撞. 由于我们按照碰撞时间排序, 假设当前x撞到了y, 则之后x不会被碰撞, 排除. 需要「修正」x之前的车的碰撞对象为y.
    如何维护x「之前」的车? 我们用一个pre数组, 一开始初始化为邻近的前一辆车, 碰撞时更新 `pre[y] = pre[x]`
    from [here](https://leetcode.cn/problems/car-fleet-ii/solution/ji-yu-you-xian-dui-lie-de-jie-fa-by-arse-tji2/)
"""
    def getCollisionTimes(self, cars: List[List[int]]) -> List[float]:
        # 思路0, 尝试打补丁, 失败. 因此无法判断idx车撞到了哪一辆
        from sortedcontainers import SortedList
        speed2ps = defaultdict(list)
        for i,(p,s) in enumerate(cars):
            speed2ps[s].append((p,i))
        positions = SortedDict()
        ans = [-1] * len(cars)
        # 
        n = len(cars)
        fa = [i for i in range(n)]
        def find(i):
            if fa[i] != i:
                fa[i] = find(fa[i])
            return fa[i]
        def union(i,j):
            fi,fj = find(i), find(j)
            if fi==fj: return
            if fi>fj:
                fi,fj = fj,fi
            fa[fi] = fj
        for s,ps in sorted(speed2ps.items(), key=lambda i: i[0]):
            for p,i in ps[::-1]:
                idx = positions.bisect_left(p)
                if idx != len(positions):
                    # 这辆车会追上 SL 中的第idx车
                    idxNext = positions[positions.iloc[idx]]
                    # 采用并查集搜索
                    idxNext = find(idxNext)
                    pnext, snext = cars[idxNext]
                    ans[i] = (pnext-p)/(s-snext)
                    # if ans[idxNext]!=-1:
                    #     ans[i] = min(ans[i], (pnext+snext*ans[idxNext] -p)/s)
                    union(i,idxNext)
                # positions.update(p=i)
                positions[p] = i
        return ans
    def getCollisionTimes(self, cars: List[List[int]]) -> List[float]:
        # 距离从小到大遍历 (从左往右), 不对
        n = len(cars)
        ans = [-1] * n
        stack = []
        for i,(p,v) in enumerate(cars):
            while stack and stack[-1][0]>v:
                vpre, ppre, idx = stack.pop()
                ans[idx] = (p-ppre)/(vpre-v)
            stack.append((v,p,i))
        return ans
    def getCollisionTimes(self, cars: List[List[int]]) -> List[float]:
        # 思路1
        n = len(cars)
        ans = [-1] * n
        stack = []
        for i in range(n-1, -1, -1):
            p,v = cars[i]
            while stack:    # (p,v,i)
                # 栈顶元素更快, 则左侧的车都不会与它发生碰撞, 没用了.
                if stack[-1][1]>=v:
                    stack.pop()
                else:
                    # 栈顶尚未发生碰撞 (它是从左往右目前最快的), 则一定会撞到它
                    if ans[stack[-1][-1]] == -1:
                        ans[i] = (stack[-1][0]-p)/(v-stack[-1][1])
                        break
                    # 否则, 需要判断在栈顶元素发生碰撞 (速度被拖慢) 之前, 能否追到它. 
                    # 若可以追到, 则结束; 否则, 继续考察栈内下一个元素.
                    # 下面注释部分没有pop不需要的元素, 复杂度 O(n^2)
                    # idx = len(stack)-1
                    # while ans[stack[idx][-1]]>0 and (stack[idx][0]-p)/(v-stack[idx][1]) > ans[stack[idx][-1]]:
                    #     idx -= 1
                    # ans[i] = (stack[idx][0]-p)/(v-stack[idx][1]) 
                    # break
                    # 思路1
                    t = (stack[-1][0]-p) / (v-stack[-1][1])
                    if t < ans[stack[-1][-1]]:
                        ans[i] = t
                        break
                    else:
                        stack.pop()

            stack.append((p,v,i))
        return ans
    
    
    def getCollisionTimes(self, cars: List[List[int]]) -> List[float]:
        # 思路2, 复杂度 O(n logn)
        n = len(cars)
        pre = [i-1 for i in range(n)]
        q = []
        for i in range(1, n):
            if cars[i][1]>=cars[i-1][1]: continue
            heappush(q, 
                     ((cars[i][0]-cars[i-1][0]) / (cars[i-1][1]-cars[i][1]), i-1,i))
        ans = [-1] * n
        visited = set()
        while q:
            t, x,y = heappop(q)
            # 碰撞对象已被删除
            if y in visited: continue
            # x被删除
            visited.add(x)
            ans[x] = t
            # 
            if pre[x]>=0 and cars[pre[x]][1] > cars[y][1]:
                tt = (cars[y][0] - cars[pre[x]][0]) / (cars[pre[x]][1]-cars[y][1])
                heappush(q, (tt, pre[x], y))
            pre[y] = pre[x] # 更新前驱
        return ans
            
            
        
sol = Solution()
result = [
    # sol.closestCost(baseCosts = [2,3], toppingCosts = [4,5,100], target = 18),
    # sol.minOperations(nums1 = [1,2,3,4,5,6], nums2 = [1,1,2,2,2,2]),
    # sol.minOperations(nums1 = [1,1,1,1,1,1,1], nums2 = [6]),
    # sol.getCollisionTimes(cars = [[1,2],[2,1],[4,3],[7,2]]),
    # sol.getCollisionTimes(cars = [[3,4],[5,4],[6,3],[9,1]]),
    sol.getCollisionTimes([[1,2],[2,1],[4,3],[7,2]]),
    
]
for r in result:
    print(r)
