from operator import ne
from os import times
from turtle import st
from typing import List
import collections
import math
import bisect
import heapq

""" 
每日一题 1 @2201
start from 20220119
 """

class Solution:
    """ 219. 存在重复元素 II
给你一个整数数组 nums 和一个整数 k ，判断数组中是否存在两个 不同的索引 i 和 j ，满足 nums[i] == nums[j] 且 abs(i - j) <= k 。如果存在，返回 true ；否则，返回 false 。
输入：nums = [1,2,3,1], k = 3
输出：true """
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        num2idx = collections.defaultdict(list)
        for i,num in enumerate(nums):
            num2idx[num].append(i)
        for num, idxs in num2idx.items():
            for i in range(len(idxs)-1):
                if idxs[i+1]-idxs[i] <= k:
                    return True
        return False


    """ 2029. 石子游戏 IX
Alice 和 Bob 再次设计了一款新的石子游戏。现有一行 n 个石子，每个石子都有一个关联的数字表示它的价值。给你一个整数数组 stones ，其中 stones[i] 是第 i 个石子的价值。
Alice 和 Bob 轮流进行自己的回合，Alice 先手。每一回合，玩家需要从 stones 中移除任一石子。

如果玩家移除石子后，导致 所有已移除石子 的价值 总和 可以被 3 整除，那么该玩家就 输掉游戏 。
如果不满足上一条，且移除后没有任何剩余的石子，那么 Bob 将会直接获胜（即便是在 Alice 的回合）。

假设两位玩家均采用 最佳 决策。如果 Alice 获胜，返回 true ；如果 Bob 获胜，返回 false 。

输入：stones = [2,1]
输出：true
解释：游戏进行如下：
- 回合 1：Alice 可以移除任意一个石子。
- 回合 2：Bob 移除剩下的石子。 
已移除的石子的值总和为 1 + 2 = 3 且可以被 3 整除。因此，Bob 输，Alice 获胜。

- 2029. 石子游戏 IX `中` 但实际上可以说很难!
  - 分别取石子, A优先, 两条规则
    - 当某个人取出后总和为 3的倍数时, 其失败;
    - 当取完所有的石子, 条件1不成立, 则 A 失败(不管最后一个是谁取的).
  - 博弈, 参见 [官方解答](https://leetcode-cn.com/problems/stone-game-ix/solution/shi-zi-you-xi-ix-by-leetcode-solution-kk5f/).
  - 首先的失败条件是取出的石子总和为 3, 因此可将石子除以3的余数为 0,1,2 分成三类
  - 先不考虑 0, 假设只有 1,2. 由于每个人都是最佳决策, 因此只会出现
    - `1,1,2,1,2,1,...` 或者 `2,2,1,2,1,2,...` 的序列. 也即除了第一颗, 两个都回去相同的石子. 
    - 条件 1 的失败条件为对方没有可取的石子, 因此 A 的策略是取数量少的那一类. 
      - 以 `1,1,2,1,2,1,...` 序列为例, A 获胜条件为: 有类型 1 的石子并且数量少于类型 2, `0 < cn1 <= cn2`
    - 综合两种情况, A 获胜条件为 `cnt1 >= 1 and cnt2 >= 1`
  - 还要考虑 1, 当 0 的数量为偶数时, 条件不改变. 考虑 0 有奇数个
    - A 的策略仍然是选择较少的类, 然而此时 B 可以有一次选类型 0 石子的机会, 因此条件变为
      - `cnt1 - cnt2 > 2 or cnt2 - cnt1 > 2`

     """
    #  https://leetcode-cn.com/problems/stone-game-ix/solution/shi-zi-you-xi-ix-by-leetcode-solution-kk5f/
    def stoneGameIX(self, stones: List[int]) -> bool:
        cnt0 = cnt1 = cnt2 = 0
        for val in stones:
            typ = val % 3
            if typ == 0:
                cnt0 += 1
            elif typ == 1:
                cnt1 += 1
            else:
                cnt2 += 1
        if cnt0 % 2 == 0:
            return cnt1 >= 1 and cnt2 >= 1
        return cnt1 - cnt2 > 2 or cnt2 - cnt1 > 2


    """ 1345. 跳跃游戏 IV
给你一个整数数组 arr ，你一开始在数组的第一个元素处（下标为 0）。

每一步，你可以从下标 i 跳到下标：

i + 1 满足：i + 1 < arr.length
i - 1 满足：i - 1 >= 0
j 满足：arr[i] == arr[j] 且 i != j
请你返回到达数组最后一个元素的下标处所需的 最少操作次数 。

输入：arr = [100,-23,-23,404,100,23,23,23,3,404]
输出：3
解释：那你需要跳跃 3 次，下标依次为 0 --> 4 --> 3 --> 9 。下标 9 为数组的最后一个元素的下标。 """
    # 超时了, 问题在于, 当存在大量点的数字相同, 变为稠密图, BFS 复杂度为 O(n^2)
    def minJumps(self, arr: List[int]) -> int:
        # 建图
        n = len(arr)
        val2index = collections.defaultdict(list)
        g = collections.defaultdict(set)
        val2index[arr[0]].append(0)
        for i in range(1, n):
            val2index[arr[i]].append(i)
            g[i-1].add(i)
            g[i].add(i-1)
        for val,indexs in val2index.items():
            if len(indexs) > 1:
                for i in range(len(indexs)):
                    for j in range(i+1, len(indexs)):
                        g[indexs[i]].add(indexs[j])
                        g[indexs[j]].add(indexs[i])
        # BFS
        target = n-1
        cost = 0
        visited = set([0])
        q = collections.deque()
        q.append(0)
        while q:
            newq = collections.deque()
            for index in q:
                if index == target:
                    return cost
                for next in g[index]:
                    if next not in visited:
                        visited.add(next)
                        newq.append(next)
            cost += 1
            q = newq
        return -1

    # 考虑这一问题的特殊性: 所有相同元素构成稠密图, 因此没有必要遍历改子图上所有的边 —— 递归一遍这些节点后, 没有必要在这一稠密图上搜索了
    # 因此, 直接不构建这一部分的图
    def minJumps2(self, arr: List[int]) -> int:
        n = len(arr)
        val2index = collections.defaultdict(list)
        for i,val in enumerate(arr):
            val2index[val].append(i)
        visited = set()
        # BFS
        target = n-1
        cost = 0
        q = collections.deque()
        q.append(0)
        visited.add(0)
        while q: # [答案](https://leetcode-cn.com/problems/jump-game-iv/solution/tiao-yue-you-xi-iv-by-leetcode-solution-zsix/) 同时保存了 cost 更简洁
            newq = collections.deque()
            for index in q:
                if index==target:
                    return cost
                for next in val2index[arr[index]]:
                    if next not in visited:
                        visited.add(next)
                        newq.append(next)
                # 删掉 相同值 的节点集合, 就不会再遍历到该子图了
                del val2index[arr[index]]
                # 还要考虑前后两个点
                if index<n-1 and index+1 not in visited:
                    visited.add(index+1)
                    newq.append(index+1)
                if index >0 and index-1 not in visited:
                    visited.add(index-1)
                    newq.append(index-1)
            cost += 1
            q = newq
        return -1

    """ 1332. 删除回文子序列
给你一个字符串 s，它仅由字母 'a' 和 'b' 组成。每一次删除操作都可以从 s 中删除一个回文 子序列。
s 仅包含字母 'a'  和 'b'

输入：s = "baabb"
输出：2
解释："baabb" -> "b" -> "". 
先删除回文子序列 "baab"，然后再删除 "b"。 

注意删除的是 子序列 """
    def removePalindromeSub(self, s: str) -> int:
        if s[::-1]==s:
            return 1
        return 2

""" 2034. 股票价格波动
股票数据可能会更新，已后到的为准，要求实现
- 更新
- 找到最高/最低价格
- 返回最近时间的价格

方法一：哈希表 + 有序集合
用 map 存储每个时间对应的价格；有序列表存储所有的价格（要求最大最小直接返回列表的首尾元素即可）
`from sortedcontainers import SortedList`

方法二：哈希表 + 两个优先队列
用两个优先队列分别存储最大的最小值， (price,timestamp)；在返回时，将存储的 price 和 map 中对应时刻的价格比较，若不一致则说明过期了
 """
from sortedcontainers import SortedList
class StockPrice:
    def __init__(self):
        self.priceMap = {}
        self.priceList = SortedList()
        self.ccurrent = 0

    def update(self, timestamp: int, price: int) -> None:
        if timestamp in self.priceMap:
            self.priceList.discard(self.priceMap[timestamp])
        self.priceList.add(price)
        self.priceMap[timestamp] = price
        self.ccurrent = max(self.ccurrent, timestamp)

    def current(self) -> int:
        return self.priceMap[self.ccurrent]

    def maximum(self) -> int:
        return self.priceList[-1]

    def minimum(self) -> int:
        return self.priceList[0]

class StockPrice2:
    def __init__(self):
        self.maxPrice = []
        self.minPrice = []
        self.timePriceMap = {}
        self.maxTimestamp = 0
    def update(self, timestamp, price) -> None:
        heapq.heappush(self.maxPrice, (-price, timestamp))
        heapq.heappush(self.minPrice, (price, timestamp))
        self.timePriceMap[timestamp] = price
        self.maxTimestamp = max(self.maxTimestamp, timestamp)
    def current(self):
        return self.timePriceMap[self.maxTimestamp]
    def maximum(self):
        while True:
            price, timestamp = self.maxPrice[0]
            if -price == self.timePriceMap[timestamp]:
                return -price
            heapq.heappop(self.maxPrice)
    def minimum(self):
        while True:
            price, timestamp = self.minPrice[0]
            if price== self.timePriceMap[timestamp]:
                return price
            heapq.heappop(self.minPrice)


# Your StockPrice object will be instantiated and called as such:
# obj = StockPrice()
# obj.update(timestamp,price)
# param_2 = obj.current()
# param_3 = obj.maximum()
# param_4 = obj.minimum()

""" 2045. 到达目的地的第二短时间
给定一张图，求从 1 到 n 的第二短路径；在这些节点上定义了红绿灯，每条边的开销是一样的，当到达节点时，次节点是红灯状态下无法离开，需要等待到下一次绿灯；所有节点的红绿灯变化是一样的，求第二短时间。
see [here](https://leetcode-cn.com/problems/second-minimum-time-to-reach-destination/solution/dao-da-mu-de-di-de-di-er-duan-shi-jian-b-05i0/) 
第一步，计算次短路径。直接暴力 BFS 会超时，注意到 仅需要记录一个节点的最短和次短路径，因此可以剪枝
第二布，计算时间。迭代的方式求解，当 time_j % (change*2) >= change 时需要等待 change*2 - time_j % (change*2)
"""
class Solution2:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:
        g = collections.defaultdict(list)
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # BFS 严格次短路径
        def dfs():
            q = collections.deque()
            shortest = 0
            q.append((1,0))
            while q:
                u, d = q.popleft()
                for v in g[u]:
                    if v==n:
                        if shortest>0 and d+1>shortest:
                            return d+1
                        shortest = d+1
                    q.append((v,d+1))
        # 直接无脑 BFS 会超时
        def dfs2():
            dist = [[float('inf')]*2 for _ in range(n+1)]
            dist[1][0] = 0
            q = collections.deque([(1,0)])
            while dist[n][1] == float('inf'):
                p = q.popleft()
                for y in g[p[0]]:
                    d = p[1]+1
                    if d < dist[y][0]:
                        dist[y][0] = d
                        q.append((y,d))
                    elif dist[y][0] < d < dist[y][1]:
                        dist[y][1]= d
                        q.append((y,d))
            return dist[n][1]
        subShortest = dfs2()
        # 计算所需时间
        ans = 0
        for _ in range(subShortest):
            if ans % (change*2) >= change:
                ans += change*2 - ans%(change*2)
            ans += time
        return ans


    def numberOfMatches(self, n: int) -> int:
        result = 0
        while n>1:
            result += n//2
            n = n/2 if n%2 == 0 else n//2+1
        return int(result)

""" 2013. 检测正方形
实现一个类，实现 count：输入一个坐标，返回这个点和已有的点能够组成正方形（平行坐标轴的）的数量
注意审题，因为是正方形所以遍历的复杂度不是很高，所以逻辑实现在 count 函数中即可
用一个 `map{x:[ys]}` 记录每一行出现过的列（或者 [官答](https://leetcode-cn.com/problems/detect-squares/solution/jian-ce-zheng-fang-xing-by-leetcode-solu-vwzs/) 中直接 `map{[x][y]:count}` 记录每一个点出现的次数，数据结构 `defaultdict(Counter)`）遍历所有可能的正方形即可

["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
[[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]
 """

class DetectSquares:
    def __init__(self):
        self.x2y = collections.defaultdict(list)
    def add(self, point:List[int]):
        xi,yi = point
        self.x2y[xi].append(yi)
    def count(self, point:List[int]):
        # 理解错了，以为是长方形
        # result = 0
        # xi,yi = point
        # possibleXj = [x for x,ys in self.x2y.items() if len(ys)>1 and yi in ys and x!=xi]
        # for yj in self.x2y[xi]:
        #     if yj==yi:
        #         continue
        #     for xj in possibleXj:
        #         if yj in self.x2y[xj]:
        #             count = self.x2y[xj].count(yi) * self.x2y[xj].count(yj)
        #             result += count
        # return result
        # 正方形
        result = 0
        xi,yi = point
        possibleYj = set([y for y in self.x2y[xi] if y!=yi])
        for yj in possibleYj:
            d = yj-yi
            for d in [d, -d]:
                if yi in self.x2y[xi+d] and yj in self.x2y[xi+d]:
                    result += self.x2y[xi+d].count(yi) * self.x2y[xi+d].count(yj) * self.x2y[xi].count(yj)
        return result

def test2013():
    obj = DetectSquares()
    obj.add([3,10])
    obj.add([11,2])
    obj.add([3,2])
    print(obj.count([11,10]))
    print(obj.count([14,8]))
    obj.add([11,2])
    print(obj.count([11,10]))

# test2013()

# Your DetectSquares object will be instantiated and called as such:
# obj = DetectSquares()
# obj.add(point)
# param_2 = obj.count(point)

# sol = Solution()
# rels = [
#     sol.containsNearbyDuplicate(nums = [1,2,3,1], k = 3),
#     # sol.minJumps2(arr = [100,-23,-23,404,100,23,23,23,3,404])
# ]

# sol = Solution2()
# rels = [
#     # sol.secondMinimum(n = 5, edges = [[1,2],[1,3],[1,4],[3,4],[4,5]], time = 3, change = 5), 
#     # sol.secondMinimum(n = 2, edges = [[1,2]], time = 3, change = 2),
#     sol.numberOfMatches(7)
# ]
# for r in rels:
#     print(r)
