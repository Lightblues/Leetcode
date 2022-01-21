from operator import ne
from typing import List
import collections
import math
import bisect
import heapq

""" 
每日一题 """

class Solution:
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
            if (typ := val % 3) == 0:
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

sol = Solution()
rels = [
    sol.minJumps2(arr = [100,-23,-23,404,100,23,23,23,3,404])
]
for r in rels:
    print(r)