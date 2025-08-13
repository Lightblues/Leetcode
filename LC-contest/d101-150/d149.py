from typing import *
from collections import Counter

""" 
https://leetcode.cn/contest/biweekly-contest-149
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

    """ 3440. 重新安排会议得到最多空余时间 II #medium 相较于上一题, 至多移动一个, 但可以改变会议的相对顺序 """
    def maxFreeTime(self, eventTime: int, startTime: List[int], endTime: List[int]) -> int:
        n = len(startTime)
        startTime.sort(); endTime.sort()
        spans = [startTime[0]] + [startTime[i]-endTime[i-1] for i in range(1,n)] + [eventTime-endTime[-1]]
        most_long_spans = sorted(spans, reverse=True)[:3]
        ans = 0
        for i,s1 in enumerate(spans[:-1]):
            s2 = spans[i+1]
            x = endTime[i]-startTime[i+1]
            if x > most_long_spans[3] or sorted([])



sol = Solution()
result = [
    # sol.findValidPair(s = "2523533"),
    sol.maxFreeTime(eventTime = 5, k = 1, startTime = [1,3], endTime = [2,5]),
    sol.maxFreeTime(eventTime = 10, k = 1, startTime = [0,2,9], endTime = [1,4,10]),
]
for r in result:
    print(r)