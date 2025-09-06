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
    
    """ 3434. 子数组操作后的最大频率 #medium 对于一个字符串, 最多可以对于一个子数组的每个元素增加x. 问经过一次操作后, 数组中最多有多少个k?
限制: n 1e5; 数字范围 U 50
思路1: 枚举所有的初始数字 s
    对于每个子问题, 变为 "选择一个区间, 其中出现s贡献1, k贡献-1, 求区间和最大值"
        -- 子数组最大和问题有 #Kadane 算法 https://en.wikipedia.org/wiki/Maximum_subarray_problem
    复杂度: O(n U)
思路2: #状态机DP
    同样也是枚举 s, 但对于子问题采用 #DP 思路求解:
    - 题目可以选择一个区间操作, 因此将整体区间分为 左/中/右 三部分!
    - 从左到右枚举, 分别记 f0, f1, f2 为三个状态: 0...i 范围内的对应的是, 区间左 / 区间左+中 / 区间左+中+右, 情况下的最大值.
    - 转移关系
        f0 = f0 + (x==k)
        f1 = max(f0, f1) + (x==s)
        f2 = max(f1, f2) + (x==k)
    拓展: 对于 "选择一个子数组" 这一类的问题, 可以采用 #状态机DP 来进行处理
        对于这道题, 可以拓展到 "允许修改两个子数组" 的情况
    [ling](https://leetcode.cn/problems/maximum-frequency-after-subarray-operation/solutions/3057702/mei-ju-zhuang-tai-ji-dp-by-endlesscheng-qpt0/)
    """
    def maxFrequency(self, nums: List[int], k: int) -> int:
        ks = nums.count(k)

        mx = 0
        for s in set(nums):
            if s == k: continue
            # Kadane 算法
            acc = 0
            for x in nums:
                if x == s: acc += 1
                elif x== k: acc -= 1
                acc = 0 if acc < 0 else acc
                mx = max(mx, acc)
        return mx + ks

    """ 3435. 最短公共超序列的字母出现频率 #medium 给定一组 """

    
sol = Solution()
result = [
    sol.maxFrequency(nums = [1,2,3,4,5,6], k = 1),
    sol.maxFrequency(nums = [10,2,3,4,5,5,4,3,2,2], k = 10),
]
for r in result:
    print(r)
