from typing import *
from math import inf
from collections import Counter
from functools import lru_cache

""" 
https://leetcode.cn/contest/biweekly-contest-149
T3 需要转换思维;
T4 的DP重构问题很复杂! 需要细品! 
Easonsi @2025 """
class Solution:
    """ 3438. 找到字符串中合法的相邻数字 """
    def findValidPair(self, s: str) -> str:
        cnt = Counter(s)
        for i in range(len(s)-1):
            if s[i] == s[i+1]: continue
            if cnt[s[i]] == int(s[i]) and cnt[s[i+1]] == int(s[i+1]):
                return s[i:i+2]
        return ""

    """ 3439. 重新安排会议得到最多空余时间 I #medium 在 [0,T] 范围内有一组会议, 可以最多移动k个, 保持相对顺序, 要求不重叠, 求移动后最长空余
限制: n 1e5
思路1: 
    NOTE: 平移操作可以合并相邻的区间! 因此等价于最大化相邻的 k+1 个空格长度
    """
    def maxFreeTime(self, eventTime: int, k: int, startTime: List[int], endTime: List[int]) -> int:
        startTime.sort(); endTime.sort()
        n = len(startTime)
        spans = [startTime[0]] + [startTime[i]-endTime[i-1] for i in range(1,n)] + [eventTime-endTime[-1]]
        ans = acc = sum(spans[:k+1])
        for i in range(k+1, len(spans)):
            acc += spans[i] - spans[i-k-1]
            ans = max(ans, acc)
        return ans

    """ 3440. 重新安排会议得到最多空余时间 II #medium 相较于上一题, 至多移动一个, 但可以改变会议的相对顺序 
思路1: 维护最大3个空格
    对于一个会议和临近的两个空格 (s1,x,s2), 
        - 若可以找到其他的位置放置x, 则可以构成 s1+x+s2
        - 否则, 移动x得到 s1=s2
    如何判断 "其他的大于x的空格" 呢? 
    1. 动态维护 "除s1,s2外最大空格", 比较复杂;
        可以左右两次遍历, 分别找 "x左侧最大空格" 和 "x右侧最大空格", 合起来判断是否满足条件!
        https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-ii/solutions/3712358/zhong-xin-an-pai-hui-yi-de-dao-zui-duo-k-tx57/
    2. 维护 "最大3个空格"! 若 s1/s2 出现在其中, 则排除它们后, 比较x是否比剩余的最大空格还大
    3. 直接维护 "最大3个空格出现的位置", 记作 a,b,c (注意可以是相同!) 
        对于x, 若相邻没有a则尝试将其放到a; 没有b则尝试将其放到b; 最差情况尝试放到c
        参见 [ling](https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-ii/solutions/3061629/wei-hu-qian-san-da-de-kong-wei-mei-ju-fe-xm2f/)
    复杂度: O(n)
    """
    def maxFreeTime(self, eventTime: int, startTime: List[int], endTime: List[int]) -> int:
        n = len(startTime)
        # startTime.sort(); endTime.sort()  # 实际上已经排好序
        spans = [startTime[0]] + [startTime[i]-endTime[i-1] for i in range(1,n)] + [eventTime-endTime[-1]]
        most_long_spans = sorted(spans, reverse=True)[:3]
        ans = 0
        def check(s1, s2, x):  # 相当不优雅的check函数, 但完全能过
            # 不满足的情况: x 比除了s1,s2外最大空格还大
            ava = most_long_spans[:]
            if s1 in ava: ava.pop(ava.index(s1))
            if s2 in ava: ava.pop(ava.index(s2))
            return x <= ava[0]
        for i,s1 in enumerate(spans[:-1]):
            s2 = spans[i+1]
            x = endTime[i]-startTime[i]
            if check(s1, s2, x):
                ans = max(ans, s1+s2+x)
            else:
                ans = max(ans, s1+s2)
        return ans

    """ 3441. 变成好标题的最少代价 #hard 给定一个字符串, 每个操作和将其中某一字符c变为 c+1 / c-1 (在a-z范围内). 要求变为 "所有连续相同字符的组长度>=3"
问最少操作所得到的字符串; 若有多种可能则返回字典序最小的
限制: n 5e4
思路1: #DP
    记 f[i,c] 表示前i个字符符合要求, 且最后一个字符为c的最小代价. 则有转移
        - f[i-1, c] + d[c, i:i]
        - min{f[i-3, .]} + d[c, i-2:i]
        取较小; 其中 d[c, i1:i2] 表示将 i1:i2 范围内变为 c 的代价
    复杂度: O(n C^2), 若采用递推的形式并将内部的min函数做记录, 则复杂度为 O(n C)
    复杂的问题在于: 如何重构字符串?
        我们需要记录 f[i,c] 的来源! 假设记作 nxt[i,c]
            若为情况1, 则设置 nxt[i,c] = i, 填入c并前向转移到 i-1
            若为情况2, 则设置 nxt[i,c] = i-3, 填入连续3个c并前向转移到 i-3
        如何得到字典序最小? 
            需要逆序! 实际上要求的 (cost, dict_order) 双重排序! 外层循环考虑cost的时候, 若遇到cost相同再考虑字典序! 
[ling](https://leetcode.cn/problems/minimum-cost-good-caption/solutions/3061609/zhuang-tai-ji-dp-shu-chu-ju-ti-fang-an-p-kjry/)
思路2: #中位数贪心
    TODO
    """
    def minCostGoodCaption(self, caption: str) -> int:
        # 简化问题: 只需要输出最少操作! 
        if len(caption) < 3: return -1
        n = len(caption)
        caption = [ord(c)-ord('a') for c in caption]
        def d(c, i1, i2):
            return sum(abs(c-caption[i]) for i in range(i1,i2+1))
        @lru_cache(None)
        def f(i:int, c:int) -> int:
            if i<2: return inf
            elif i==2: return d(c, 0, 2)
            return min(
                f(i-1,c)+d(c,i,i),
                # f(i-2,c)+d(c,i-1,i),  # NOTE: 不用考虑这种情况
                min(f(i-3,ch) for ch in range(26)) + d(c,i-2,i)
            )
        return min(f(n-1,c) for c in range(26))

    def minCostGoodCaption(self, caption: str) -> str:
        # TODO: 增加用于重构的 nxt 数组
        if len(caption) < 3: return ""
        n = len(caption)
        caption = [ord(c)-ord('a') for c in caption]
        def d(c, i1, i2):
            return sum(abs(c-caption[i]) for i in range(i1,i2+1))

        min_j = [-1]*n
        nxt = [[-1]*26 for _ in range(n)]
        # @lru_cache(None)
        # def f(i:int, c:int) -> int:
        #     if i==n: return 0  # 哨兵 for condition 1
        #     # condition 1
        #     res = f(i+1,c) + d(c,i,i)
        #     nxt[i][c] = i+1
        #     # condition 2
        #     if i<=n-6:
        #         if min_j[i+3]==-1:
        #             mn = inf
        #             for ch in range(26):
        #                 if f(i+3,ch)<mn: mn = f(i+3,ch)
        #             min_j[i+3] = mn
        #         res2 = min_j[i+3]+d(c,i,i+2)
        #         if res2<res:
        #             nxt[i][c] = i+3
        #             res = res2
        #     return res
        # _ = min(f(0,c) for c in range(26))

        # rebuild
        ans = [''] * n
        # i, j = 


    """ 1092. 最短公共超序列 #hard 给定两个字符串 s1, s2, 找到最短的字符串, 使得两个字符串均为其子序列
限制: n 1e3
    """

sol = Solution()
result = [
    # sol.findValidPair(s = "2523533"),
    # sol.maxFreeTime(eventTime = 5, k = 1, startTime = [1,3], endTime = [2,5]),
    # sol.maxFreeTime(eventTime = 10, k = 1, startTime = [0,2,9], endTime = [1,4,10]),

    # sol.maxFreeTime(eventTime = 10, startTime = [0,3,7,9], endTime = [1,4,8,10]),
    # sol.maxFreeTime(eventTime = 5, startTime = [0,1,2,3,4], endTime = [1,2,3,4,5]),
    sol.minCostGoodCaption(caption = "cdcd"),
    sol.minCostGoodCaption(caption = "aca"),
]
for r in result:
    print(r)