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
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
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
300. 最长递增子序列 #medium #题型
    给定一个序列, 要求计算这个序列的最长递增子序列的长度.(严格)
1964. 找出到每个位置为止最长的有效障碍赛跑路线 #hard #DP
    问题定义: 给定一个序列, 对于其中的每一个值, 计算以其结尾的递增序列的最大长度

== 子集遍历的动态规划 (遍历子集通过状压)
1986. 完成任务的最少工作时间段 #medium
    有一组任务, 完成每个任务需要一定的时间. 你每次训练可以工作 `sessionTime` 个小时. 在一个session中, 你可以完成多个任务, 但一个任务不能分割到多个session中. 要求分配任务到不同的session, 使得session总数最小.
    f[mask] 表示mask对应子集所需的最少session.
    递归的方式: 显然有 f[mask] = min{f[mask\subset] + 1} 这里的subset要求是子集中元素和不超过 sessionTime 的.
1655. 分配重复整数 #hard
    有一组需求, 每一个要 quantity[i] 个相同的物品. 现有一组商品, 每种商品的数量为 nums[j]. 问是否可以满足所有需求.
    `dp[i][j]` 表示利用前i个物品, 分配前j个人是否可能.
    递推: `dp[i][j] = any(dp[i-1][i\subset] and nums[i] >= sum(quantity[subset]))` 
1494. 并行课程 II #hard
    有DAG课程序列, 每学期最后可修k门, 要求最少时间.
    注意有简单的剪枝策略: `numLessons = min(k, todo.bit_count())`, 也即在可选课程中, 尽量选择最多数量的课程.

"""
class Solution:
    """ 300. 最长递增子序列 #medium #题型
给定一个序列, 要求计算这个序列的最长递增子序列的长度.(严格)
思路1: #DP #二分
    dp[i] 记录长度为 i+1 的序列中, 结尾元素的最小值
    可知, 这样的dp数组必然是递增的.
    每到一个新的数字, 若其比 dp[-1] 更大, 则append到末尾; 否则, 更新相应bisect位置的最小值

输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
"""
    def lengthOfLIS(self, nums: List[int]) -> int:
        # dp[i] 记录长度为 i+1 的序列中, 结尾元素的最小值
        dp = []
        for num in nums:
            if not dp or dp[-1]<num:
                dp.append(num)
            else:
                idx = bisect.bisect_left(dp, num)
                dp[idx] = num
        return len(dp)

    """ 1964. 找出到每个位置为止最长的有效障碍赛跑路线 #hard #DP
问题定义: 给定一个序列, 对于其中的每一个值, 计算以其结尾的递增序列的最大长度
思路1: #线段树
    我们用一个哈希表记录num结尾的递增序列的最大长度
    这样, 对于每一个元素, 我们需要查询「小于等于当前元素的数字中, 长度最大的那一个」. 因此可以用线段树来解决
思路2: #DP
    基本和 0300 「最长递增子序列」完全一致.
    核心是: dp[i] 记录长度为 i+1 的序列中, 结尾元素的最小值
"""
    def longestObstacleCourseAtEachPosition(self, obstacles: List[int]) -> List[int]:
        # 果然被线段树祸害了……
        # 直接套「序列最长递增序列」的思路 见 0300 题
        dp = []
        ans = []
        for i,height in enumerate(obstacles):
            if (not dp) or dp[-1]<=height:
                dp.append(height)
                ans.append(len(dp))
            else:
                idx = bisect.bisect_right(dp, height)
                ans.append(idx+1)
                dp[idx] = height
        return ans

    """ 1986. 完成任务的最少工作时间段 #medium
有一组任务, 完成每个任务需要一定的时间. 你每次训练可以工作 `sessionTime` 个小时. 在一个session中, 你可以完成多个任务, 但一个任务不能分割到多个session中. 要求分配任务到不同的session, 使得session总数最小.
限制: 任务数量 1 <= n <= 14; 任务时间 max(tasks[i]) <= sessionTime <= 15
注意, 不能用「尽量选择大的任务」的方法, 例如 [2,2,3,3,3,5], sessionTime=9 的情况下, 这种方案会导致 [5,3], [3,2,2], [2] 而实际答案为 2.
[here](https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/solution/wan-cheng-ren-wu-de-zui-shao-gong-zuo-sh-tl0p/)
思路1: #枚举子集 的动态规划 #DP
    f[mask] 表示mask对应子集所需的最少session.
    递归的方式: 显然有 f[mask] = min{f[mask\subset] + 1} 这里的subset要求是子集中元素和不超过 sessionTime 的.
    如何 **遍历所有子集**? 有一种经典的方式: 先初始化 `sub = mask`, 然后递归 `sub = (sub - 1) & mask` 即可保证.
    如何计算子集和? 为了避免重复, 可以预计算.
    时间复杂度: $3^n$. 在递归过程中, 我们需要遍历 mask [1: 2^n], 而每一个mask有多少非零位? 可知包含k个1的二进制表示有 $C^n_k$ 个. 因此复杂度为 $\sum_{k=0}^{n}\left(\begin{array}{l}n \\ k\end{array}\right) 2^{k}$. 正好是 $3^n = (1+2)^n$ 的二次项展开形式.
    具体见链接.
思路2: #存储两个值的动态规划
    本思路更符合直觉, 复杂度也更低, 但是比较难想清楚.
    对于某一mask表示的集合, 我们考虑最后一个加入的元素, 并且 **让之前的session都不再变化**. 这样, 可以用 (segment, currnet) 表示状态. 其中前者表示已用的session数量, 后者表示最后一个session已占用的时间.
    转移: `f[mask] = min{trans(f[mask\i], tasks[i])}` 这里的i是枚举了所有mask中包含的元素. trans是对于状态的转移, 比较简单.
    复杂度: O(n * 2^n)
"""
    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        # https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/solution/wan-cheng-ren-wu-de-zui-shao-gong-zuo-sh-tl0p/
        n = len(tasks)
        m = 1<<n
        # 预计算所有的subset是否可以放在一个session中
        valid = [False] * m
        for mask in range(1, m):
            cumT = 0
            # 得到mask所表示的所有 1 的位置的数字和
            for i in range(n):
                if 1<<i > mask: break
                if (1<<i) & mask: cumT += tasks[i]
                if cumT > sessionTime: break
            if cumT <= sessionTime: valid[mask] = True
            
        
        # DP 递归. 计算每一个子集的最小session数
        # f = defaultdict(lambda: inf)
        f = [inf] * m
        f[0] = 0
        # 注意, 这里是要遍历所有可能的子集, 而不是 1, 11, 111...
        for mask in range(1, m):
            # 遍历 mask 所表示的集合的所有子集的方式: 先将 sub 初始化为 mask, 然后依次 `sub = (sub - 1) & mask`
            sub = mask
            while sub:
                if valid[sub]: f[mask] = min(f[mask], f[mask ^ sub]+1)
                sub = (sub - 1) & mask
        return f[(1<<n)-1]

    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        """ 第一部分的计算见 [here](https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/solution/zi-ji-dong-tai-gui-hua-by-endlesscheng-wtua/)
        采取了DP的形式, 但复杂度仍然位 O(2^n)
        实际上提交的时间几乎没有变化 (因为第二部分复杂度更高?)"""
        n = len(tasks)
        m = 1<<n
        # 预计算所有的subset是否可以放在一个session中
        sums = [0] * m
        for i, task in enumerate(tasks):
            # j 从0遍历到 2^i-1, 即将第 i 位加到 tasks[:i] 的所有子集中中
            j, limit = 0, 1<<i
            while j<limit:
                sums[j | limit] = task + sums[j]
                j += 1
        f = [inf] * m
        f[0] = 0
        for mask in range(m):
            subset = mask
            while subset:
                if sums[subset] <= sessionTime:
                    f[mask] = min(f[mask], f[subset ^ mask] + 1)
                subset = (subset - 1) & mask
        return f[m-1]
    
    
    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        """ 思路2 https://leetcode.cn/problems/minimum-number-of-work-sessions-to-finish-the-tasks/solution/wan-cheng-ren-wu-de-zui-shao-gong-zuo-sh-tl0p/
        复杂度: O(n * 2^n)"""
        n = len(tasks)
        f = [(inf, inf)] * (1<<n)
        f[0] = (1, 0)
        def add(o, x):
            if o[1] + x <= sessionTime:
                return o[0], o[1] + x
            return o[0]+1, x
        for mask in range(1, 1<<n):
            for i in range(n):
                if mask & (1<<i):
                    f[mask] = min(f[mask], add(f[mask ^ (1<<i)], tasks[i]))
        return f[(1<<n)-1][0]
    
    
    """ 1494. 并行课程 II #hard
有DAG课程序列, 每学期最后可修k门, 要求最少时间.
注意, 本题不可采用拓扑排序(+贪心), 因为要考虑后续课程的数量, 见 [here](https://leetcode.cn/problems/parallel-courses-ii/solution/yu-niang-niang-1494-bing-xing-ke-cheng-i-duny/).
思路1: #子集遍历 的DP
    注意, 这里因为有课程约束关系, 因此应该「从前往后」考虑: 每次从 1. 尚未学的; 2. 前置课程已完成 的课程todo中进行选择.
    因此, 这里递推的方式略有不同: 假设学好的课程为 learned, 我们每次应该从计算好的todo集合中选取课程subset (不超过门), 递推公式 `f[learned | sub] = min(f[learned | sub], f[learned] + 1)`
    一开始直接转为 Python版本超时了. 后来 `numLessons = min(k, todo.bit_count())` 剪枝之后过了! 见思路2
    zero 神也给了一种 #子集遍历 的DP, 不过在 Python中也超时了
思路2: DFS 形式的状压 DP
    from [here](https://leetcode.cn/problems/parallel-courses-ii/solution/by-iancn-kcpq/)
    被子集遍历的路子带歪了, 忘记了一种最简单的剪枝策略: 考虑每次最多选 k门课, 但是我们没必要选择 少于 `min(k, len(todo))` 门, 这是显然的. (虽然完全贪心是错误的, NP hard)

"""
    def minNumberOfSemesters(self, n: int, dependencies: List[List[int]], k: int) -> int:
        """ https://leetcode.cn/problems/parallel-courses-ii/solution/yu-niang-niang-1494-bing-xing-ke-cheng-i-duny/
        一开始在 15,[],4 这样的例子上超时了
        加了 `numLessons = min(k, todo.bit_count())` 剪枝之后过.
        """
        # 计算所有课程的前置需求
        preRequire = [0] * n
        for i,j in dependencies:
            preRequire[j-1] |= 1<<(i-1)   # 节点序号从1开始
        
        # DP. f[mask] 表示学完mask至少需要多少学期
        f = [inf] * (1<<n)
        f[0] = 0
        # 遍历子集
        for learned in range(0, 1<<n):
            todo = 0        # 下一步可学的课程子集
            for i in range(n):
                # 未学习的, 并且前置需求已经满足
                if (1<<i & learned == 0) and (preRequire[i]|learned == learned):
                    todo |= 1<<i
            sub = todo  # sub是遍历所有可学子集
            # !!!! 剪枝. 每次尽量选择最多的课程.
            numLessons = min(k, todo.bit_count())
            while sub:
                # if int.bit_count(sub) <= k:
                if int.bit_count(sub) == numLessons:
                    # 注意这里的更新公式: 我们在已有的基础上, 新学了sub子集.
                    f[learned | sub] = min(f[learned | sub], f[learned] + 1)
                # 遍历子集
                sub = (sub - 1) & todo
        return f[(1<<n)-1]
    
    def minNumberOfSemesters(self, n: int, dependencies: List[List[int]], k: int) -> int:
        """ from [zero](https://leetcode.cn/problems/parallel-courses-ii/solution/zhuang-tai-ya-suo-dong-tai-gui-hua-mei-ju-zi-ji-by/)
        超时了 """
        # 计算所有课程的前置需求
        preRequire = [0] * n
        for i,j in dependencies:
            preRequire[j-1] |= 1<<(i-1)   # 节点序号从1开始
        
        MASKS = 1<<n
        setPreReq = [0] * MASKS # 这里记录 mask 集合内部没有依赖关系 (可以一次一起学习)
        valid = [0] * MASKS
        for mask in range(MASKS):
            if mask.bit_count() > k: continue
            for i in range(n):
                if mask & (1<<i):
                    setPreReq[mask] |= preRequire[i]
            valid[mask] = setPreReq[mask] & mask == 0
            
        dp = [inf] * MASKS
        dp[0] = 0
        for mask in range(1, MASKS):
            sub = mask
            while sub:
                # mask^sub (也即已经学过的课程) 覆盖了 sub 的前置课程; 并且 sub 可以一次学习
                if valid[sub] and (mask^sub) & setPreReq[sub] == setPreReq[sub]:
                    dp[mask] = min(dp[mask], dp[mask^sub] + 1)
                sub = (sub-1) & mask
        return dp[MASKS-1]

    def minNumberOfSemesters(self, n: int, dependencies: List[List[int]], k: int) -> int:
        """ https://leetcode.cn/problems/parallel-courses-ii/solution/by-iancn-kcpq/
        思路2: DFS
        最重要的应该是下面 `combinations(cands, min(k, len(cands)))` 语句中的剪枝
        Q: 是因为硬件问题吗? 这种算法在本地跑很慢, 但是在LeetCode的服务器上跑很快不到 1s.
        """
        @lru_cache(None)
        def dfs(st):
            # dfs(st) 代表已经选了 st 包含的课程，剩下课程所需的最少学期
            if st==(1<<n)-1:
                return 0
            res = float('inf')
            # 所有能选的课程 cands
            cands = [i for i in range(n) if not st&(1<<i) and D[i]&st==D[i]]
            # 显然选得越多越好，因此遍历 cands 所有 min(k, len(cands)) 大小的子集作为这学期的课程
            for sub in combinations(cands, min(k, len(cands))):
                res = min(res, 1+dfs(st|sum(1<<i for i in sub)))
            return res

        D = [0]*n
        for x, y in dependencies:
            D[y-1] |= 1<<(x-1)
        return dfs(0)
    
    """ 1655. 分配重复整数 #hard
有一组需求, 每一个要 quantity[i] 个相同的物品. 现有一组商品, 每种商品的数量为 nums[j]. 问是否可以满足所有需求.
类似「1986. 完成任务的最少工作时间段」, 本题也不能贪心将剩余最多的分配给要求最多的人. 例子: 剩余数量 [10,10,8], 需求 [9,8,5,5], 若贪心分配则错误返回 False.
思路1:  #枚举子集 的动态规划 #DP
    `dp[i][j]` 表示利用前i个物品, 分配前j个人是否可能.
    递推: `dp[i][j] = any(dp[i-1][i\subset] and nums[i] >= sum(quantity[subset]))` 
    也即, 遍历所有子集, 只有当 1. 利用前i-1个数字可以满足subset之外的人; 2. 第i个数字可以满足subset 时, `dp[i][j]` 才可行.
    [here](https://leetcode.cn/problems/distribute-repeating-integers/solution/zi-ji-mei-ju-jing-dian-tao-lu-zhuang-ya-dp-by-arse/)
"""
    def canDistribute(self, nums: List[int], quantity: List[int]) -> bool:
        nums = list(collections.Counter(nums).values())
        # 预先计算所有子集的需求和
        n = len(quantity)
        sums = [0] *  (1<<n)
        for i, num in enumerate(quantity):
            pre = 1<<i
            for j in range(pre):
                sums[pre+j] = sums[j] + num
        # 子集枚举DP
        m = len(nums)
        dp = [[False] * (1<<n) for _ in range(m+1)]
        dp[0][0] = True
        for i in range(1, m+1):
            dp[i][0] = True
            for mask in range(1, 1<<n):
                # 注意这一行!! 假如前 i-1 个数字已经可以满足, 就不用再检查了
                # 实际上根本的原因在于, 下面遍历的subset没有考虑到 subset=0 的情况.
                if dp[i-1][mask]:
                    dp[i][mask] = True
                    continue
                # 只有在 前 i-1 个数字无法满足的情况下, 才遍历所有子集
                subset = mask
                while subset:
                    if sums[subset] <= nums[i-1] and dp[i-1][mask ^ subset]:
                        dp[i][mask] = True
                        break
                    subset = (subset - 1) & mask
        return dp[m][(1<<n)-1]
        
sol = Solution()
result = [
    sol.minNumberOfSemesters(n = 4, dependencies = [[2,1],[3,1],[1,4]], k = 2),
    sol.minNumberOfSemesters(n = 5, dependencies = [[2,1],[3,1],[4,1],[1,5]], k = 2),
    sol.minNumberOfSemesters(15,[],4),
    
    # sol.canDistribute(nums = [1,2,3,4], quantity = [2]),
    # sol.canDistribute(nums = [1,2,3,3], quantity = [2]),
    # sol.canDistribute([357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357,357], [1,2,3,4,5,6,7,8,9,10]),
]
for r in result:
    print(r)
