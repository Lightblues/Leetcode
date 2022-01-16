from typing import List
import collections
import random
import heapq


""" @220116
https://leetcode-cn.com/contest/weekly-contest-275
 """
class Solution276:
    """ 5980. 将字符串拆分为若干长度为 k 的组 """
    def divideString(self, s: str, k: int, fill: str) -> List[str]:
        result = []
        n = len(s)
        for i in range(n//k):
            result.append(s[i*k:(i+1)*k])
        if n%k != 0:
            result.append(s[k*(n//k):] + fill*(k-n%k))
        return result

    """ 5194. 得到目标值的最少行动次数
    给定一个目标数, 从 1 开始 +1, *2 两种操作, 限定了倍乘的次数 maxDoubles
    贪心, 从 target 往下 """
    def minMoves(self, target: int, maxDoubles: int) -> int:
        def dfs(target, doubleNum, count):
            if target==1:
                return count
            if doubleNum==0:
                return count + target-1
            if target%2:
                return dfs(target-1, doubleNum, count+1)
            else:
                return dfs(target//2, doubleNum-1, count+1)
        return dfs(target, maxDoubles, 0)

    """ 5982. 解决智力问题
    给定一系列的题目, questions[i] = [pointsi, brainpoweri], 你选择做某一题的代价是只能跳过后面 brainpower 题
    DP, 从后往前 """
    def mostPoints(self, questions: List[List[int]]) -> int:
        n = len(questions)
        dp = [0] * n
        dp[-1] = questions[-1][0]
        for i in range(n-2,-1,-1):
            point, skip = questions[i]
            if i+skip+1<n:
                dp[i] = max([dp[i+1], point+dp[i+skip+1]])
            else:
                dp[i] = max(dp[i+1], point)
        return dp[0]

    """ 5983. 同时运行 N 台电脑的最长时间
    给定一组电池 batteries, 每个电池可以给一台电脑运行一定的时间. 可以把一个电池替换给不同的电脑, 要求让所有电脑同时运行的最长时间
    这里的限制条件为电量最大的 n 个电池, 小的电池看作对它们的补充. 
    注意到: 一个电池的电量可以以任意的比例分到若干块电池上.
    因此, 可以将最大的 n 个电池看成一个「阶梯」, 其余的小电池理解为在这个池子里注水, 求高度 """
    def maxRunTime(self, n: int, batteries: List[int]) -> int:
        if len(batteries)<n:
            return 0
        batteries.sort()
        """ 
        有问题: 因为电池不一定要一次性加上去 """
        # computers, ava = batteries[-n:], batteries[:-n]
        # heap = heapq.heapify(computers)
        # for battery in ava[::-1]:
        #     new = heapq.heappop(heap) + battery
        #     heapq.heappush(heap, new)
        # return heapq.heappush(heap)

        computers = batteries[-n:]
        avaTotal = sum(batteries[:-n])
        gaps = []
        for i in range(len(computers)-1):
            gaps.append(computers[i+1]-computers[i])
        def fillGaps(index, ava):
            if index==n-1:
                return sum(gaps) + ava//n
            if ava < (index+1)*gaps[index]:
                return sum(gaps[:index]) + ava//(index+1)
            else:
                return fillGaps(index+1, ava-(index+1)*gaps[index])
        return fillGaps(0, avaTotal) + computers[0]
        


sol = Solution276()
res = [
    # sol.divideString(s = "abcdefghij", k = 3, fill = "x"),
    # sol.minMoves(target = 19, maxDoubles = 2),
    # sol.mostPoints([[1,1],[2,2],[3,3],[4,4],[5,5]]),

    # sol.maxRunTime(n = 2, batteries = [3,3,3]),
    # sol.maxRunTime(n = 2, batteries = [1,1,1,1]),
    sol.maxRunTime(n=3, batteries = [10,10,3,5]),
]
for r in res:
    print(r)