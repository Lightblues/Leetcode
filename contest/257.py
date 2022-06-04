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
from functools import lru_cache, reduce, partial # cache
cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, ne, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
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
https://leetcode.cn/contest/weekly-contest-257
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 1995. 统计特殊四元组 #easy #题型
给定一个数组, 找出其中满足 a,b,c 位置元素之和 = d 位置元素的四元祖的数量 (a<b<c<d)
思路1: 暴力枚举.
    直接枚举所有的(a<b<c<d) 四元祖, 如果满足条件, 则 ans += 1
    官答用了for, 我一开始用了dfs, 时间复杂度上应该差不多. 都是 `O(n^4)`
思路2: 用哈希表存储 nums[d] 的频次, `O(n^3)`
    在思路1中, 对于每一个 `s = nums[a] + nums[b] + nums[c]`, 我们都需要从 `nums[c+1:n-1]` 中统计 `s` 的频次.
    在这里, 我们可以用哈希表来存储 `s` 的频次. 这样可以降低一个量级.
    具体而言, 如何依次统计 `nums[c+1:n-1]` 范围内的数字? 可以对 c 从大到小遍历 [n-2...2], 每次将 c+1 假如到Counter中. 对于ab的遍历还是和之前一样, 只需要满足 `a<b<c`
思路3: 用哈希表存储 nums[d]-nums[c] 的频次
    将原等式转为 `nums[a] + nums[b] = nums[d] - nums[c]`, 然后遍历 a<b.
    关键是如何统计 `nums[d] - nums[c]` 的频次? 同样是对于b从大到小遍历 [n-3...1], 每次b减小1, 我们可以将 `nums[d] - nums[c:=b+1]` 加入Counter, 这里d范围 [b+1:n-1].
    这样, 我们从大到小遍历b, 第二层遍历中, a遍历b的左侧, d遍历b的右侧. 总的复杂读为 `O(n^2)`
[官答](https://leetcode.cn/problems/count-special-quadruplets/solution/tong-ji-te-shu-si-yuan-zu-by-leetcode-so-50e2/)
"""
    def countQuadruplets(self, nums: List[int]) -> int:
        n = len(nums)
        s = []
        ans = 0
        def dfs(idx):
            # search from idx
            nonlocal ans
            if len(s)==3:
                for i in range(idx, n):
                    if nums[i]==sum(s): ans += 1
                return
            for i in range(idx, n):
                s.append(nums[i])
                dfs(i+1)
                s.pop()
        dfs(0)
        return ans
    
    
    def countQuadruplets(self, nums: List[int]) -> int:
        # 思路1, 暴力枚举 O(n^4)
        n = len(nums)
        ans = 0
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        if nums[i]+nums[j]+nums[k] == nums[l]:
                            ans += 1
        return ans
        
        
    def countQuadruplets(self, nums: List[int]) -> int:
        # 思路2: 用哈希表存储 nums[d] 的频次, O(n^3)
        n = len(nums)
        ans = 0
        cnt = Counter()
        for c in range(n-2, 1, -1):
            cnt[nums[c+1]] += 1
            for b in range(c-1, 0, -1):
                for a in range(b):
                    if (s := nums[a] + nums[b] + nums[c]) in cnt:
                        ans += cnt[s]
        return ans
    
    def countQuadruplets(self, nums: List[int]) -> int:
        # 思路3: 用哈希表存储 nums[d]-nums[c] 的频次
        n = len(nums)
        cnt = Counter()
        ans = 0
        for b in range(n-3, 0, -1):
            for d in range(b+2, n):
                cnt[nums[d] - nums[b+1]] += 1
            for a in range(b):
                if (s:= nums[a] + nums[b]) in cnt:
                    ans += cnt[s]
        return ans
    
    """ 1996. 游戏中弱角色的数量 #medium #题型 #复杂排序
定义“弱角色”：包括攻击和防御两个属性，两个指标都严格小于另一个角色的角色. 要求返回一组人物中弱角色的数量.
本题需要注意的是只有当两个属性都严格小的情况下才是弱角色. [here](https://leetcode-cn.com/problems/the-number-of-weak-characters-in-the-game/solution/you-xi-zhong-ruo-jiao-se-de-shu-liang-by-3d2g/)
思路1: #排序
    首先, 按照攻击X 从大到小排序. 然后, 我们可以维护一个「最大防御值」maxY. 这样若当前遍历角色的防御值小于最大防御值, 则该角色「可能是」弱角色.
    需要注意点在于, 对于攻击值相同的角色 `p, q`, 若「最大防御值」刚好是q产生的, 这里不满足严格小的关系. 例如 `[10, 10], [10, 9]` 的情况下第二个不是弱角色.
        一种思路对于攻击值相同的元素分为一组, 用上一轮的 maxY来比较, 当一组遍历结束后再更新 maxY.
        另一种更优雅的, 可 **进一步对于防御值Y从小到大排序**. 我们仍然维护的 maxY, 此时, 若出现 `y<maxY`, 则这里的 maxY 一定是在上一个轮次 (也即攻击值严格大的角色)产生的.
思路2: #单调栈
    思路其实差不多, 区别在于, 思路1是从大到小遍历, 看每个角色是否为弱角色. 而这里时从小到大遍历, 用单调栈保存尚无法判定的角色, 利用出栈操作决定弱角色.
    具体而言, 这里先按照 攻击值从小到大, 防御值从大到小排序. 然后用一个单调递减栈保存防御值, 同样可以避免上面提到的问题.
    单调栈保存元素防御值. 由于攻击值相同的元素, 防御值从大到小排序, 因此 1. 相同攻击值最大防御值的角色最先入栈, 将此前轮次的弱角色弹出; 2. 元素不会被相同攻击值的(同一轮次)另一个角色所弹出
"""
    def numberOfWeakCharacters(self, properties: List[List[int]]) -> int:
        # 按照攻击从大到小, 防御从小到大排序
        properties.sort(key=lambda x: (-x[0], x[1]))
        result = 0
        maxY = 0
        for x,y in properties:
            # 由于我们是按照防御从小到大排序的, 因此当出现 y<maxY 时, 这里的 maxY 必然不是在本轮出现的 (防止攻击值相同的情况). 
            # 说明攻击值更高并且防御值maxY也更高的角色
            if y<maxY:
                result += 1
            # 更新遍历过程中, 最大的防御值
            else:
                maxY = y
        return result
    # 单调递增栈。(x[0], -x[1]) 排序。也即，按照递增次序遍历攻击值，栈内元素为尚无法成为弱角色的；为了处理相同攻击值的情况，采用防御值倒序作为第二排序指标
    def numberOfWeakCharacters(self, properties: List[List[int]]) -> int:
        # 攻击值从小到大, 防御值从大到小
        properties.sort(key = lambda x: (x[0], -x[1]))
        ans = 0
        # 单调栈保存元素防御值. 由于攻击值相同的元素, 防御值从大到小排序, 因此 1. 相同攻击值最大防御值的角色最先入栈, 将此前轮次的弱角色弹出; 2. 元素不会被相同攻击值的(同一轮次)另一个角色所弹出
        st = []
        for _, defence in properties:
            while st and st[-1] < defence:
                st.pop()
                ans += 1
            st.append(defence)
        return ans
    
    
    """ 1997. 访问完所有房间的第一天 #medium #DP
有n个房间, 有一个 nextVisit 数组. 你在第一天访问房间0, 按照下面的规则访问下一个房间, 问经过多少天后访问完所有房间.
    算上本次访问, 若访问房间i的总次数为奇数, 则下一次访问 `nextVisit[i]` 所指定的房间，其中 `0 <= nextVisit[i] <= i`; 
    否则, 访问 `(i + 1) mod n` 号房间 (也即下一个房间).
约束: n的长度 1e5. 对于结果取 mod
思路1: #前缀和 优化 #DP
    注意到, nextVisit 所能访问的都是i之前的房间, 因此一定是顺序从 0...n 访问房间的.
    如何从 i-1 访问到 i? 需要访问两次i-1号房间, 第二次的时候按照规则2 访问下一个房间.
    也即, 从第一次访问房间 i, 到从房间i 跳转到 i+1, 需要经历多少天? 核心: 需要依次访问 nextVisit[i]...i-1 号房间.
    因此有递推公式 `dp[i] = dp[nextVisit[i]] +...+ dp[i-1] + 2 = cumsum[i] - cumsum[nextVisit[i]] + 2` 这里的2是需要访问两次 i 号房间, cumsum[0] = 0.
    因此, 可以依次计算, dp[0]...dp[n-2], 这样第一次访问到最后一个房间的天数是 dp[n-2]+1-1, 这里+1是要跳转到最后一个房间, -1 是因为天数从0开始计算.
    [here](https://leetcode.cn/problems/first-day-where-you-have-been-in-all-the-rooms/solution/qian-zhui-he-you-hua-dp-by-endlesscheng-j10b/)
"""
    def firstDayBeenInAllRooms(self, nextVisit: List[int]) -> int:
        # https://leetcode.cn/problems/first-day-where-you-have-been-in-all-the-rooms/solution/qian-zhui-he-you-hua-dp-by-endlesscheng-j10b/
        MOD = 10**9 + 7
        n = len(nextVisit)
        # 状态 f[i] 表示从首次访问房间 i 到访问房间 i+1 之前所需要的天数. 
        # 另外注意这里的DP数组 f 实际上是可以省略的, 直接记录到 cumsum 中.
        f = [0] * n
        cumsum = [0] * (n+1)
        f[0] = 2        # 实际上直接 range(0, n-1) 即可
        cumsum[1] = 2
        for i in range(1, n-1):
            f[i] = (cumsum[i] - cumsum[nextVisit[i]] + 2) % MOD
            cumsum[i+1] = (cumsum[i] + f[i]) % MOD
        return cumsum[n-1]
            
    """ 1998. 数组的最大公因数排序 #hard
给定一个数组, 对于任意两个位置 i,j, 若他们存在公共因子 (`gcd(nums[i], nums[j]) > 1`) 则可进行交换. 问数组是否可以按照上述规则进行交换后, 变为递增数组.
约束: 数组长度 3e4, 数字大小 1e5
思路1: 分解 #质因子 的 #并查集
    结论: 对于有公共因子的数字之间连边, 可知, 在一个连通分量上, 经过交换操作可以得到任意的数字顺序. 例子:  `[10,5,9,3,15]` 两个因子 3,5 通过 15 连接, 这个数组可以得到任意顺序
    因此, 就是并查集的思路. 但是元素之间两两查询的复杂度不够. 因此, 我们引入 prime 数字构成的节点.
    这样, 对于一个数字num, 我们得到所有的质因子 factors, 将 num 连到任意质因子上, 然后将 factors[1:n-1] 都连到 factors[0] 上即可.
    判断: 最后, 将 nums, sorted(nums) 的每一位比较, 两元素相同则不需要交换; 否则, 查询 x,y 是否在同一集合中, 只有在同一集合中才能交换得到.
    下面预先计算的所有可能的质因子, 但实际上可以简化, 见 [here](https://leetcode.cn/problems/gcd-sort-of-an-array/solution/bing-cha-ji-fen-jie-zhi-yin-shu-by-xin-x-ylsz/)
"""
    def gcdSort(self, nums: List[int]) -> bool:
        sortedNums = sorted(nums)
        # 预计算所有的质数因子
        primes = [2]
        for i in range(3, sortedNums[-1]+1):
            flag = True
            limit = int(math.sqrt(i))
            for j in primes:
                if j>limit: break
                if i%j==0:
                    flag = False
                    break
            if flag: primes.append(i)
        
        def getFactors(x):
            """ 得到 x 的所有因子 """
            factors = []
            for i in primes:
                if x%i==0:
                    factors.append(i)
                    x //= i
                    while x%i==0:
                        x //= i
                if x==1: break
            return factors
        
        # 并查集
        n = len(set(nums))
        num2dix = {num:i for i, num in enumerate(set(nums))}
        prime2idx = {prime:i+n for i, prime in enumerate(primes)}
        fa = list(range(n + len(primes)))
        def find(x):
            path = []
            while fa[x] != x:
                path.append(x)
                x = fa[x]
            for i in path:
                fa[i] = x
            return x
        def merge(x, y):
            """ 将 x, y 合并到一个集合中; 令 x 是 y 的父节点 """
            fa[find(y)] = find(x)
            
        for num in nums:
            if num==1: continue
            factors = getFactors(num)
            # 将 num 合并到最小的因子上去
            merge(prime2idx[factors[0]], num2dix[num])
            # 将各个因子之间进行合并
            for i in range(1, len(factors)):
                # 按照merge的规则, 尽量让小的数字作为父节点
                merge(prime2idx[factors[0]], prime2idx[factors[i]])
        
        # 检查. 判断 idx 位置的数字能否从x变为y (也即在一个并查集中)
        for x,y in zip(nums, sortedNums):
            if x==y: continue
            if find(num2dix[x]) != find(num2dix[y]): return False
        return True

    
sol = Solution()
result = [
    # sol.countQuadruplets(nums = [1,2,3,6]),
    # sol.countQuadruplets(nums = [1,1,1,3,5]),
    
    # sol.numberOfWeakCharacters(properties = [[5,5],[6,3],[3,6]]),
    # sol.numberOfWeakCharacters(properties = [[1,5],[10,4],[4,3]]),
    # sol.numberOfWeakCharacters([[7,9],[10,7],[6,9],[10,4],[7,5],[7,10]])
    
    # sol.firstDayBeenInAllRooms(nextVisit = [0,0]),
    # sol.firstDayBeenInAllRooms(nextVisit = [0,0,2]),
    
    sol.gcdSort(nums = [7,21,3]),
    sol.gcdSort(nums = [5,2,6,2]),
    sol.gcdSort(nums = [10,5,9,3,15])
]
for r in result:
    print(r)
