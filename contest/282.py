from typing import List, Optional
import collections
import math
import bisect
import heapq

from structures import ListNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 6008. 统计包含给定前缀的字符串 """
    def prefixCount(self, words: List[str], pref: str) -> int:
        return sum(1 for w in words if w.startswith(pref))

    """ 6009. 使两字符串互为字母异位词的最少步骤数 """
    def minSteps(self, s: str, t: str) -> int:
        m,n = len(s) , len(t)
        cs, ct = collections.Counter(s), collections.Counter(t)
        cnt = 0
        for k,v in cs.items():
            cnt += min(v, ct[k])
        return m + n - 2 * cnt

    """ 6010. 完成旅途的最少时间
给一组公交车运行一轮的用时: `time[i]` 表示第 `i` 辆公交车完成 一趟旅途 所需要花费的时间。
要求计算所有公交车运行至少 totalTrips 圈所需的最少时间。

思路: 二分查找
对于运行时间排序, 在一定区间内二分查找最短时间
初始化: 考虑左边界, 假设所有车运行一圈都为最小的那一辆, 则最短时间 T 需要满足 `T//min(time) * n >= totalTrips`, 则最小为 T = min(time) * math.ceil(totalTrips/n)
这里复习一下二分: 循环 `l < r`, 每次查找的 `mid = (l + r) // 2` 有可能为 l. 因此在检查条件后, 根据是否满足分别设置 `r = mid, l = mid + 1` 从而保证不会死循环.
具体而言, 这里要求最小的满足条件的数字, 则可以: 每次检查成功收缩右边界, 令 `r = mid`; 失败则拓展左边界 `l = mid + 1`, 从下一个点开始搜索.
 """
    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        time.sort()
        n = len(time)

        def check(t):
            # 检查时间 t 是否满足条件: 所有车的运行轮次之和 cnt >= totalTrips
            cnt = 0
            for i in range(n):
                cnt += t // time[i]
            return cnt >= totalTrips

        l, r = time[0]*math.ceil(totalTrips/n), time[-1]*math.ceil(totalTrips/n)
        while l < r:
            mid = (l + r) // 2
            if check(mid):
                r = mid
            else:
                l = mid + 1
        return l

    """ 6011. 完成比赛的最少时间
给定一组轮胎, `tires[i] = [fi, ri]` 表示第 `i` 种轮胎如果连续使用，第 `x` 圈需要耗时 `fi * ri ** (x-1)` 秒。
同时给你一个整数 `changeTime` 和一个整数 `numLaps` , 表示换轮胎的时间和总圈数. 要求最短用时.

输入：tires = [[1,10],[2,2],[3,4]], changeTime = 6, numLaps = 5
输出：25
解释：
第 1 圈：使用轮胎 1 ，耗时 2 秒。
第 2 圈：继续使用轮胎 1 ，耗时 2 * 2 = 4 秒。
第 3 圈：耗时 6 秒换一条新的轮胎 1 ，然后耗时 2 秒完成这一圈。
第 4 圈：继续使用轮胎 1 ，耗时 2 * 2 = 4 秒。
第 5 圈：耗时 6 秒换成轮胎 0 ，然后耗时 1 秒完成这一圈。
总耗时 = 2 + 4 + 6 + 2 + 4 + 6 + 1 = 25 秒。
完成比赛的最少时间为 25 秒。

思路: DP
对于dp[i], 考虑两种情况: 1. 用一种轮胎, 则用时为 `f * (r**laps -  1) / (r-1)` (等比数列); 2. 递推, 则用时为 `dp[i] + dp[i-j] + changeTime` (j = 1...i-1).
注意对于第一种情况, 次题中 numLaps=1e3, len(tires)=1e5, 直接暴力会超时. 因此需要对每一轮次可能达到最短时间的 tires 进行筛选, 
这里用了简单的策略: 计算换一个轮胎跑一圈的最短用时 `min0 = min(i[0] for i in tires) + changeTime`, 如果此时继续用轮胎i `i[0]*(i[1]**(laps-1))>= min0` 则不需要考虑了.
 """
    def minimumFinishTime0(self, tires: List[List[int]], changeTime: int, numLaps: int) -> int:
        # 超时了
        # n = len(tires)
        dp = [0] * (numLaps + 1)
        def singleTire(tire, laps):
            f,r = tire
            return f * (r**laps -  1) // (r-1)
        
        for i in range(1, numLaps + 1):
            dp[i] = min(singleTire(tire, i) for tire in tires)
            for j in range(1, i):
                dp[i] = min(dp[i], dp[j] + dp[i-j] + changeTime)
        return dp[-1]


    def minimumFinishTime(self, tires: List[List[int]], changeTime: int, numLaps: int) -> int:
        def singleTire(tire, laps):
            f,r = tire
            return f * (r**laps -  1) // (r-1)
        
        tires.sort()
        possMin = tires
        min0 = min(i[0] for i in tires) + changeTime
        def filter(possMin, laps):
            return [i for i in possMin if i[0]*(i[1]**(laps-1)) < min0]
        
        dp = [0] * (numLaps + 1)
        for i in range(1, numLaps + 1):
            possMin = filter(possMin, i)
            dp[i] = min(singleTire(tire, i) for tire in possMin) if possMin else float('inf')
            for j in range(1, i//2+1):
                dp[i] = min(dp[i], dp[j] + dp[i-j] + changeTime)
        return dp[-1]
sol = Solution()
result = [
    # sol.minSteps(s = "leetcode", t = "coats"),

    # sol.minimumTime(time = [1,2,3], totalTrips = 5),
    # sol.minimumTime(time = [2], totalTrips = 1),
    # sol.minimumTime([2,7,3,4,5], 1),

    sol.minimumFinishTime(tires = [[2,3],[3,4]], changeTime = 5, numLaps = 4),
    sol.minimumFinishTime(tires = [[1,10],[2,2],[3,4]], changeTime = 6, numLaps = 5),
]
for r in result:
    print(r)