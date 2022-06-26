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
0300. 最长递增子序列 #medium #题型
    给定一个序列, 要求计算这个序列的最长递增子序列的长度.(严格)
1964. 找出到每个位置为止最长的有效障碍赛跑路线 #hard #DP
    问题定义: 给定一个序列, 对于其中的每一个值, 计算以其结尾的递增序列的最大长度


== 构造DP数组
1959. K 次调整数组大小浪费的最小总空间 #medium #题型
    题目的背景是动态内存分配: 对于一个数组, 可以在其中调整k的所分配的内存, 要求最小的总空间浪费.
    抽象: 对于一个数组, 将其分成 k+1 个部分, 每个部分取最大值矩形进行覆盖, 要求所有矩形的面积和最小.
    记 `dp[i][j]` 表示 **覆盖数组的前i个元素, 使用j次调整(j+1个区间)所浪费的最小空间**.
1977. 划分数字的方案数 #hard #题型 #LCP
    给定一个数字串, 问有多少种分割方式, 使其变为非递减的正数序列, 要求数字没有前导零.
    约束: 数字长度 n<=3500. 注意最多支持 O(n^2) 复杂度.
    形式: `f[i][j]` 表示对于序列nums[0...j]的分割方案中, 最后一个数字为 nums[i...j] 的方案数.
    迭代: 既然最后一个数字为 nums[i...j] 其要满足条件要求上一个数字 nums[k...i-1] 更小, 因此迭代公式为 `f[i][j] = sum{ f[k][i-1] }` 这里的k的范围为上面的约束
    除此之外, 还需要利用 LCP来快速判断 `nums[2i-j-1...i-1], nums[i...j]` 两个数字的大小

== 状压DP
1931. 用三种不同颜色为网格涂色 #hard
    给定一个 (m,n) 的网格, 用三种颜色涂, 要求相邻的颜色不同, 问有多少种方案.
    约束: 1 <= m <= 5, 1 <= n <= 1000
    用 `f[i][mask]` 表示遍历到第i行, 并且最后一行的颜色为mask的涂色方案数.
    状态转移: `f[i+1][mask] = sum{ f[i][mask2] }` 这里要求 mask, mask2 所对应的行涂色都是合法的, 并且两者同一列的颜色都不同.
6107. 不同骰子序列的数目 #hard
    投骰子n次, 问满足条件的序列数量. 条件: 相邻数字的最大公约数为1, 两个相同数字之间的间距至少为3.
    用 `f[i][mask]` 表示长度为i, 最后两位为mask的序列数量.

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
    """ 0300. 最长递增子序列 #medium #题型
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


    """ 1959. K 次调整数组大小浪费的最小总空间 #medium #题型
题目的背景是动态内存分配: 对于一个数组, 可以在其中调整k的所分配的内存, 要求最小的总空间浪费.
抽象: 对于一个数组, 将其分成 k+1 个部分, 每个部分取最大值矩形进行覆盖, 要求所有矩形的面积和最小.
限制: 数组长度 n<=200, 调整次数 0<=k<n
思路1: #DP
    考虑采用动态规划求解. 每次利用之前状态的记录.
    具体而言, 记 `dp[i][j]` 表示 **覆盖数组的前i个元素, 使用j次调整(j+1个区间)所浪费的最小空间**.
        于是, 有 `dp[i][j] = min_ii { dp[ii][j] + g[ii+1][i] }`
        对于每个 `dp[i][j]`, 我们将 0...i 区间根据 ii 进行拆分, 将右边分成一个区间, 左边进行 j-1 次调整.
        这里的 `g[a][b]` 表示区间 [a,b] 分成一组的空间浪费, 可以预先双重遍历计算出来.
        具体实现中, 可以将更新公式中的 j维度省略.
    说明: 为了要求 num[0...ii] 被分成 j 个区间, 显然 ii 必须小于 j. 但实际上由于 ii<=j-1 时空间浪费必然为0, 因此在下面的代码中没有考虑这一边界情况.
    [官答](https://leetcode.cn/problems/minimum-total-space-wasted-with-k-resizing-operations/solution/k-ci-diao-zheng-shu-zu-da-xiao-lang-fei-wxg6y/)
"""
    def minSpaceWastedKResizing(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # g[i][j] 表示 nums[i:j] 作为一个组需要多少代价
        g = [[0] * n for _ in range(n)]
        acc = list(accumulate(nums, initial=0))
        for i in range(n):
            mx = nums[i]
            for j in range(i, n):
                mx = max(mx, nums[j])
                g[i][j] = mx * (j-i+1) - (acc[j+1] - acc[i])
        # 初始化: 只有一个组 (k=0)
        dp = g[0][:]
        # 遍历 k = 1...k
        for _ in range(1, k+1):
            new = dp[:]
            # update dp[i]
            for i in range(n):
                # dp[i][j] = min_ii { dp[ii][j] + g[ii+1][i] } 遍历 ii=0...i-1 尝试对于 nums[:i+1] 进行分割
                # 这里将 j维度省略.
                for ii in range(i):
                    new[i] = min(new[i], dp[ii] + g[ii+1][i])
            dp = new
        return dp[-1]



    """ 1977. 划分数字的方案数 #hard #题型
给定一个数字串, 问有多少种分割方式, 使其变为非递减的正数序列, 要求数字没有前导零.
约束: 数字长度 n<=3500. 注意最多支持 O(n^2) 复杂度.
思路1:
    DP框架
        形式: `f[i][j]` 表示对于序列nums[0...j]的分割方案中, 最后一个数字为 nums[i...j] 的方案数.
        迭代: 既然最有一个数字为 nums[i...j] 其要满足条件要求上一个数字 nums[k...i-1] 更小, 因此迭代公式为 `f[i][j] = sum{ f[k][i-1] }` 这里的k的范围为上面的约束
            注意数字不包含前导零, 因此若 `j-i > i-1 - k` 则一定满足, 反之则不满足. 两者相等时的情况需要另外讨论 (见下).
            因此, 求和范围为 `2i-j(or -1) ... i-1`.
        边界: f[0][...] = 1; 要求的答案为 sum{f[...][n-1]}
        前缀和优化: 直接求和复杂度 O(n^3) 不够. 可以采用前缀和计算. 记 pre[k][i-1] 为上一迭代中的前缀和, 则有 `f[i][j] = pre[i][i-1] - pre[2i-j(or -1)]` 其实是否有 2i-j-1 项根据 nums[2i-j-1...i-1] <=nums[i...j] 判断.
            观察: 实际上不用前缀和利用迭代也可. 假如我们按照 i,j 的前后顺序来进行两次枚举, 根据 j, j+1 两个相邻状态的元素, 发现后者只多了1/2项, 因此用一个idx记录累计的元素即可.
        LCP: 预计算 #最长公共前缀, 快速比较两个数的大小
            上述过程中, 还需要比较 `nums[2i-j-1...i-1], nums[i...j]` 两个数字的大小, 但直接算的复杂度为 O(k), 会超时
            用 DP 预计算LCP, 形式为: lcp[i][j] 表示分别从 i,j 位置出发向右的最长公共串长度.
            显然有递推公式: 若num[i]==num[j] 则有 `lcp[i][j] = lcp[i+1][j+1] + 1`, 否则为 0.
            在此基础上, 比较 `nums[2i-j-1...i-1], nums[i...j]` 的大小就很简单: 若 lcp[i][2i-j-1] >= j-i+1, 说明公共部分比比较的部分更长, 满足大于等于; 否则, 直接比较 num[i+ll], num[2i-j-1+ll] 即可.
[官答](https://leetcode.cn/problems/number-of-ways-to-separate-numbers/solution/hua-fen-shu-zi-de-fang-an-shu-by-leetcod-env6/)
总结: 想到DP迭代公式就挺难的; 更为复杂的是之后的LCP等技巧. 本题比较综合.
"""
    def numberOfCombinations(self, num: str) -> int:
        """ [官答](https://leetcode.cn/problems/number-of-ways-to-separate-numbers/solution/hua-fen-shu-zi-de-fang-an-shu-by-leetcod-env6/) """
        MOD = 10**9 + 7
        # 边界: 第一个数字为0
        if num[0] == '0': return 0
        n = len(num)
        
        # DP计算 LCP矩阵
        lcp = [[0]*n for _ in range(n)]
        # 仅计算 i>j 的下三角部分
        for j in range(n-1):
            if num[j]==num[n-1]: lcp[n-1][j] = 1
        for i in range(n-2, -1, -1):
            for j in range(i):
                if num[i]==num[j]:
                    lcp[i][j] = lcp[i+1][j+1] + 1
        # 封装比较 nums[2i-j-1...i-1], nums[i...j] 两数字大小的函数
        def compare(a,b, c,d):
            # test num[c...d] >= num[a...b]
            assert b-a == d-c
            ll = lcp[c][a]
            if ll>=b-a+1: return True
            return num[c+ll] >= num[a+ll]
        
        f = [[0] * n for _ in range(n)]
        for j in range(n):
            f[0][j] = 1
        for i in range(1, n):
            s = 0
            # 边界情况: 不能有前缀 0
            if num[i]=='0': continue
            left = i
            # range of sum: 2i-j(or -1) ... i-1
            for j in range(i, n):
                newLeft = max(2*i-j, 0)
                if newLeft > 0:
                    if compare(2*i-j-1,i-1, i,j):
                        newLeft -= 1
                for ii in range(newLeft, left):
                    s += f[ii][i-1]
                    s %= MOD
                left = newLeft
                f[i][j] = s
        return sum(l[-1] for l in f) % MOD


    """ 6107. 不同骰子序列的数目 #hard
投骰子n次, 问满足条件的序列数量. 条件: 相邻数字的最大公约数为1, 两个相同数字之间的间距至少为3.
约束: n的数量级1e4
思路1: #状压 #DP
    可知, 第idx位置的数字可取的值仅由前两个数字决定, 只需要满足上述条件即可.
    考虑状态压缩, 用mask表示相邻两个数字, 采用6进制. 预计算: 所有合法的长度为2的序列, 合法的转移序列.
    用 `f[i][mask]` 表示长度为i, 最后两位为mask的序列数量.
    状态转移: `f[i+1][mask] = sum{ f[i][newmask] }`, 其中 newmask 表示第一位等于mask第二位并且符合条件的所有情况.
"""
    def distinctSequences(self, n: int) -> int:
        MOD = 10**9 + 7
        if n==1: return 6
        def valid(mask):
            a,b = divmod(mask, 6)
            return a!=b and math.gcd(a+1, b+1)==1
        def validTranstion(mask):
            a,b = divmod(mask, 6)
            ans = []
            for c in range(6):
                if c!=a and c!=b and math.gcd(b+1, c+1)==1:
                    ans.append(6*b + c)
            return ans
        validPairs = [i for i in range(6**2) if valid(i)]
        validTrans = {i:validTranstion(i) for i in validPairs}
        # 
        cnt = Counter(validPairs)
        for _ in range(n-2):
            newCnt = Counter()
            for u,vs, in validTrans.items():
                for v in vs:
                    newCnt[v] += cnt[u]
                    newCnt[v] %= MOD
            cnt = newCnt
        return sum(cnt.values()) % MOD

    """ 1931. 用三种不同颜色为网格涂色 #hard
给定一个 (m,n) 的网格, 用三种颜色涂, 要求相邻的颜色不同, 问有多少种方案.
约束: 1 <= m <= 5, 1 <= n <= 1000
思路1: #状压 #DP
    重点是grid的维度一比较小: 这样我们可以枚举所有的涂色可能性. 这样, 再遍历每一行的过程中, 仅需要考虑和上一行每一列的相邻颜色不同即可.
    考虑状压: 0,1,2 表示三种颜色, 则我们可以用 [0, 3^m) 范围内的数字表示每一行的涂色情况.
    用 `f[i][mask]` 表示遍历到第i行, 并且最后一行的颜色为mask的涂色方案数.
    状态转移: `f[i+1][mask] = sum{ f[i][mask2] }` 这里要求 mask, mask2 所对应的行涂色都是合法的, 并且两者同一列的颜色都不同.
    预处理: 可以预先计算所有合法的行涂色方案 validLines; 并且计算合法的相邻行 transMap, 其中 transMap[mask] 是所有合法的相邻行列表.
"""
    def colorTheGrid(self, m: int, n: int) -> int:
        MOD = 10**9 + 7
        def valid(mask: int) -> bool:
            pre = 3
            # while mask:
            for _ in range(m):
                mask, color = divmod(mask, 3)
                if color == pre: return False
                pre = color
            return True
        def validNeihbour(mask1, mask2):
            # while mask1 or mask2:
            for _ in range(m):
                mask1, color1 = divmod(mask1, 3)
                mask2, color2 = divmod(mask2, 3)
                if color1==color2: return False
            return True
        transMap = {}
        validLines = [i for i in range(3**m) if valid(i)]
        for line in validLines:
            transMap[line] = [l for l in validLines if validNeihbour(line, l)]
        # 
        cnt = Counter(validLines)
        for _ in range(n-1):
            newCnt = Counter()
            for line, nextLines in transMap.items():
                for nextLine in nextLines:
                    newCnt[nextLine] += cnt[line]
                    newCnt[nextLine] %= MOD
            cnt = newCnt
        return sum(cnt.values()) % MOD
    

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
