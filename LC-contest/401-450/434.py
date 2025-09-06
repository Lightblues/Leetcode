from typing import *


""" 
https://leetcode.cn/contest/weekly-contest-434

Easonsi @2025 """
class Solution:
    """ 3432. 统计元素和差值为偶数的分区方案 """
    def countPartitions(self, nums: List[int]) -> int:
        s = sum(nums)
        if s & 1: return 0
        return len(nums) - 1
    
    """ 3433. 统计用户被提及情况 """
    def countMentions(self, numberOfUsers: int, events: List[List[str]]) -> List[int]:
        answer = [0] * numberOfUsers
        online = [0] * numberOfUsers
        events.sort(key=lambda x: (int(x[1]), -ord(x[0][0])))  # offline 先于 message
        for event, time, x in events:
            time = int(time)
            if event == "OFFLINE":
                online[int(x)] = time + 60
            else:
                if x == "HERE":
                    for i,t in enumerate(online):
                        if t <= time: answer[i] += 1
                elif x == "ALL":
                    for i in range(numberOfUsers):
                        answer[i] += 1
                else:
                    ids = [int(i[2:]) for i in x.split(" ")]
                    for i in ids:
                        answer[i] += 1
        return answer
    
    """ 3434. 子数组操作后的最大频率 """
    def maxFrequency(self, nums: List[int], k: int) -> int:

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
