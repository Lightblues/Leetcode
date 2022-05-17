from typing import List, Optional
import collections
import math
import bisect
import heapq
import functools, itertools
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
# from utils_leetcode import testClass
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-65
@20220223 补 """
class Solution:
    """ 2068. 检查两个字符串是否几乎相等 """
    def checkAlmostEquivalent(self, word1: str, word2: str) -> bool:
        c1, c2 = collections.Counter(word1), collections.Counter(word2)
        for k in set(c1).union(set(c2)):
            if abs(c1[k]-c2[k])>3: return False
        return True
    
    """ 2069. 模拟行走机器人 II #medium
模拟一个机器人沿着矩形的边缘行走, 每次下一步要出边界的时候, 进行右转. 要求实现一个类, 可以 1) 查询机器人的位置和方向; 2) 要求机器人前进 num步.
初始状态为 (0,0)点, 方向向右.
思路1: 直接模拟.
然后, 由于矩形的范围不是很大, 而前进的步数可能很高, 因此需要避免重复走圈 (`num = num%self.circleLen`)
这样就遇到一个边界情况: 当机器人到达边界点的时候方便不变, 要走下一步方向才会变化; 因此其实状态的方向为向右, 但下一次机器人到达该 (0,0) 点时的方向应该是向下. 需要特殊处理一下
思路2: 直接记录位置到方向的映射
如[官方答案](https://leetcode.cn/problems/walking-robot-simulation-ii/solution/mo-ni-xing-zou-ji-qi-ren-ii-by-leetcode-lhf24/) 所言, 可以直接得到位置到行动方向的映射
这样, 对于矩形的每一个位置建立 index, 然后在行动的时候根据前进方向整除得到机器人的 index 即可.

"""
    def test_robot(self, inputs):
        s_res = []
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
    
    """ 2070. 每一个查询的最大美丽值 #题型 #索引 #二分 #medium
有一组 (price, beauty) 所定义的商品. 要求在小于 O(n) 的复杂度内查询价格在 p 以下的商品中, beauty 的最大值.
复杂度: 物品数量 1e5, price/beauty 值 1e9.
不能直接对于每一个价格建立到最大美丽值的映射, 因此考虑只对出现过的价格建立映射, 然后二分查找答案即可.
具体而言, 对于出现过的所有价格, 预计算 (price, maxBeauty) 的索引, 表示在price以下的所有价格中, 最大的美丽值. 
查询时, 对于所要差的 p, 在price中二分搜索 index, 然而返回对应的 maxBeauty 即可.
"""
    def maximumBeauty(self, items: List[List[int]], queries: List[int]) -> List[int]:
        price2max_beauty = collections.defaultdict(int)
        for price, beauty in items:
            price2max_beauty[price] = max(price2max_beauty[price], beauty)
        dp = []
        dp2 = []
        maxb = 0
        for i, price in enumerate(sorted(price2max_beauty)):
            maxb = max(maxb, price2max_beauty[price])
            dp.append(price)
            dp2.append(maxb)
        ans = []
        for q in queries:
            idx = bisect.bisect_left(dp, q)
            if idx>=len(dp) or dp[idx]>q: 
                idx -= 1
            if idx <0:
                ans.append(0)
                continue
            ans.append(dp2[idx])
        return ans
    
    
    """ 2071. 你可以安排的最多任务数目 #题型 #二分
给定一组任务和工人, 当工人的分数高于任务分数时可以完成; 另外给 k 个药丸可以增加单个工人的 strength 点能力值 (一个人只能用一次). 求最多匹配的数量.
复杂度: n 个任务和 m 个工人为 5e4, 能力值大小 1e9
思路: #二分搜索.
匹配的数量范围为 [0, min(m,n)]. 关键在于如何检查是否可以得到 k 个匹配?
用贪心: 如果可以有 k 个匹配, 显然是 k个能力最大的工人和 k个所需点最小的任务. 排序, 然后对任务从高到低遍历: 1) 能力值最大工人可以胜任, 则直接匹配; 2) 否则, 从吃了药丸可以胜任的功能中找到能力值最小的, 小号一颗药丸.
终止条件: 药丸用完了, 或者加上 strength 也没有人可以胜任.
注意复杂度分析: 每一次检测, 最多需要再 min(m,n) 个候选工人中进行二分搜索, 因此为 `O(min(m,n) * log(min(m,n)))`. 整体二分的复杂度为 `O(min(m,n) * log^2(min(m,n)))`.
事实上可以优化: 用「双端队列」来维护所有可以（在使用药丸的情况下）完成任务的工人，此时要么队首的工人被选择（删除），要么队尾的工人被选择（删除），那么单次删除操作的时间复杂度由 O(log(min(m,n))) 降低为 O(1)
see [here](https://leetcode.cn/problems/maximum-number-of-tasks-you-can-assign/solution/ni-ke-yi-an-pai-de-zui-duo-ren-wu-shu-mu-p7dm/)

技巧: 二分查找时, 可以额外用一个 ans 记录二分的结果, 而不需要纠结最后返回 l or l-1
"""
    def maxTaskAssign(self, tasks: List[int], workers: List[int], pills: int, strength: int) -> int:
        tasks.sort()
        workers.sort()
        
        def test(k, workers=workers, tasks=tasks, pills=pills, strength=strength):
            """ 测试是否可以安排 """
            workers = workers[-k:]
            tasks = tasks[:k]
            for t in tasks[::-1]:
                if workers[-1] >= t: 
                    workers.pop()
                    continue
                if pills < 1: return 0
                idx = bisect.bisect_left(workers, t-strength)
                if idx > len(workers)-1: return False
                workers.pop(idx)
                pills -= 1
            return True
        
        # 二分查找
        l, r = 0, min(len(workers), len(tasks))
        ans = 0 # 技巧: 二分查找时, 可以额外用一个 ans 记录二分的结果, 而不需要纠结最后返回 l or l-1
        while l<=r:
            mid = (l+r)//2
            if not test(mid, workers): r = mid-1
            else: 
                l = mid+1
                ans = mid
        return ans


class Robot:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pos = [0, 0]
        self.direction = (1,0)
        self.d2word = {(1,0):'East', (0,1):'North', (-1,0):'West', (0,-1):'South'}
        self.circleLen = 2*(width+height-2)
        # self.moved = False

    def step(self, num: int) -> None:
        num = num%self.circleLen
        # if num==0: return
        if self.direction == (1,0):
            if self.pos[0] + num > self.width-1:
                s = self.width - self.pos[0] - 1
                self.pos[0] += s
                self.direction = (0,1)
                self.step(num-s)
            else:
                self.pos[0] += num
                # 特殊情况: 当机器人正好走了一圈时, 方向应该变为向下! 而不是初始时的向右
                if self.pos[0] == 0:
                    self.direction = (0, -1)
        elif self.direction == (0,1):
            if self.pos[1] + num > self.height-1:
                s = self.height - self.pos[1] - 1
                self.pos[1] += s
                self.direction = (-1,0)
                self.step(num-s)
            else: self.pos[1] += num
        elif self.direction == (-1,0):
            if self.pos[0] - num < 0:
                s = self.pos[0]
                self.pos[0] = 0
                self.direction = (0,-1)
                self.step(num-s)
            else: self.pos[0] -= num
        elif self.direction == (0,-1):
            if self.pos[1] - num < 0:
                s = self.pos[1]
                self.pos[1] = 0
                self.direction = (1,0)
                self.step(num - s)
            else: self.pos[1] -= num

    def getPos(self) -> List[int]:
        # 注意要复制!!!
        return self.pos[:]

    def getDir(self) -> str:
        return self.d2word[self.direction]

sol = Solution()
result = [
    # sol.checkAlmostEquivalent(word1 = "abcdeef", word2 = "abaaacc"),
    # sol.checkAlmostEquivalent(word1 = "aaaa", word2 = "bccb"),
    
#     sol.test_robot(
#         """["Robot", "step", "step", "getPos", "getDir", "step", "step", "step", "getPos", "getDir"]
# [[6, 3], [2], [2], [], [], [2], [1], [4], [], []]"""
#     ),
#     sol.test_robot(
#         """["Robot","step","step","step","getPos","getDir","step","getPos","getDir","step","step","step","getPos","getDir","step","step","step","getPos","getDir","step","step","step","step","step","getPos","getDir","step","step","step","step","step","getPos","getDir","step","step","getPos","getDir","step","step","getPos","getDir","step","step","getPos","getDir","step","step"]
# [[20,14],[32],[18],[18],[],[],[18],[],[],[45],[37],[39],[],[],[8],[11],[18],[],[],[3],[39],[7],[31],[42],[],[],[35],[11],[36],[29],[10],[],[],[49],[31],[],[],[31],[47],[],[],[29],[1],[],[],[5],[44]]"""
#     ),

    # sol.maximumBeauty(items = [[1,2],[3,2],[2,4],[5,6],[3,5]], queries = [1,2,3,4,5,6]),
    
    sol.maxTaskAssign(tasks = [3,2,1], workers = [0,3,3], pills = 1, strength = 1),
    sol.maxTaskAssign(tasks = [5,4], workers = [0,0,0], pills = 1, strength = 5),
]
for r in result:
    print(r)
