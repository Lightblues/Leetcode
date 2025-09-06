from typing import *


""" 
https://leetcode.cn/contest/weekly-contest-434
T3 的 Kadane 算法需要想到转化! 另外 #状态机DP 也很有意思
T4 一道巨难的题
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

    """ 3435. 最短公共超序列的字母出现频率 #medium 给定一组长度为2的字符串 words, 求它们的 "最短公共超序列" -- 也即所有的给定字符串都是该超序列的子序列. 
数量很多, 只需要返回所有超序列中出现的字母频率即可. 限制: n 256; 所有的字母数量不超过 16个
思路1: 贪心构造 + 枚举子集 + 有向图判环
    观察1: 超序列中每个字母出现的频次至多是2 -- 考虑把a放在两端, 则可满足左右的 a*, *a 的情况
        - 因此, 我们可以枚举所有子集, 判断哪些字母出现 1/2 次!
    给定一个划分 (char_set1, char_set2) 如何判断它是否可满足所有 words?
        对于words中, 出现在 char_set2 里面的要求, 显然都是满足的! 
        因此, 只需要看 char_set1 这些字母构成的要求是否满足! 
        观察2: 这个问题等价于, 每个word构成一个有向边, 判断图是否有环!
            - 有向图是否有环的问题, 可以通过 #拓扑排序 或者 #三色标记 来解决
    复杂度: O(n 2^k) 需要枚举所有出现字母的子集, 每次检查的复杂度为 O(n) 
    [ling](https://leetcode.cn/problems/frequencies-of-shortest-supersequences/solutions/3057743/mei-ju-zi-ji-jian-tu-pan-duan-shi-fou-yo-n43u/)
    """

    
sol = Solution()
result = [
    sol.maxFrequency(nums = [1,2,3,4,5,6], k = 1),
    sol.maxFrequency(nums = [10,2,3,4,5,5,4,3,2,2], k = 10),
]
for r in result:
    print(r)
