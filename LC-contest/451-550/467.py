from typing import *

"""
https://leetcode.cn/contest/weekly-contest-467
3. 含上限元素的子序列和 #背包 DP 的拓展题目, 看了讲解思路清晰了很多!
    DP 问题还是非常有意思!
4. 稳定子序列的数量 #背包
    回头来看, 有思路的话其实不复杂! 关键是要有分析 DP 的思路!
Easonsi @2026 """


class Solution:
    """ 3683. 完成一个任务的最早时间 """
    def earliestTime(self, tasks: List[List[int]]) -> int:
        return min(a+b for a,b in tasks)

    """ 3684. 至多 K 个不同元素的最大和 """
    def maxKDistinct(self, nums: List[int], k: int) -> List[int]:
        return sorted(set(nums), reverse=True)[:k]

    """ 3685. 含上限元素的子序列和 #medium 
给定一个大小 n 的数组, 对于每个 x=1,2,...n, 可生成一个被 x 限制 (capped) 的数组 -- 也即每个元素变为 min(mins[i], x)
    对于每个 x, 判断其限制得到的数组, 子数组和是否可位 k
限制: n 4e3, k 4e3, 元素 1<=x<=n
思路 1: 0-1 背包 + 双指针
    考虑 x 固定的情况, 就是问对于变换后的数组, 是否有子数组和位 k -- 标准 0/1 背包
        复杂度? 每个 0/1 背包 O(nk), 则整体 O(n^2k)
    如何优化? 
        (固定 x) 考虑给数组排序, 数组被分为两部分 (<x 的那些, 其他都变成了 x), 我们可以枚举 x 出现的次数 -- 也即只需要计算前半部分数组的 0/1 背包 f
        优化完整问题: 我们可以 "增量" 地计算排序后数组的 f -- 这样这部分的整体复杂度就只有 O(nk)
    复杂度: 更新 f 数组 O(nk) -- 注意三层训练中, 外层的 for, while 整体贡献 O(n)
        枚举 j 的部分, 若 k 很大, 则循环 O(n^2), 否则是 k/1 + k/2 + ... + k/n -> O(k logn), 两者取 min
https://leetcode.cn/problems/subsequence-sum-after-capping-elements/solutions/3781344/0-1-bei-bao-shuang-zhi-zhen-pythonjavacg-j4ca/
bonus: bitset 优化!
    复杂度: 若使用位运算来优化, 则复杂度变为 O(nk/w), 其中 w 为位宽 (64 or 32)
    """
    def subsequenceSumAfterCapping(self, nums: List[int], k: int) -> List[bool]:
        nums.sort()
        n = len(nums)
        ans = [False] * n
        f = [False] * (k+1)  # f[i] 表示 (前缀数组) 能够构成和 i
        f[0] = True

        i = 0
        for x in range(1, n+1):
            while i<n and nums[i]==x:
                # 拓展左半部分数组 (考虑进背包的部分)
                for j in range(k, nums[i]-1, -1):  # 倒序考虑新增元素的影响
                    f[j] = f[j] or f[j-nums[i]]  # 0-1 背包：不选 or 选
                i += 1
            # 考虑选择 0, 1, ..., min(k//x,n-i) 个 x
            for j in range(min(k//x,n-i) + 1):
                if f[k - j*x]:
                    ans[x-1] = True
                    break
        return ans

    """ 3686. 稳定子序列的数量 #hard
对于一个数组的所有子序列, "稳定" 定义为 " 子序列 中 不存在连续三个 元素奇偶性相同", 求所有稳定数量
限制: n 1e5; 对结果取模
思路 1: DP
    考虑 f[i+1][x][j] 表示在前i 个元素中, 末尾元素为 x (0/1), 且末尾有连续 j+1 个奇偶性都为 x 的数 (0,1)
    考虑 nums[i] 选或不选
    - 不选, 变为 f[i][x][j] 
    - 选, 
        - 单独构成一个长度为 1 的稳定子序列, 个数为 1
        - 当 j=0, 也即 nums[i] 添加到一个末尾奇偶性为 x^1 的稳定子序列后面, f[i][x^1][0] + f[i][x^1][1]
        - 当 j=1, 说明 nums[i] 添加到一个末尾奇偶性相同的子序列后, f[i][x][0]
    因此有:
        f[i+1][x][0] = f[i][x][0] + f[i][x^1][0] + f[i][x^1][1] + 1
        f[i+1][x][1] = f[i][x][1] + f[i][x][0]
    初始值: f[0][x][j] = 0
    答案: f[n][0][0] + f[n][0][1] + f[n][1][0] + f[n][1][1]
    优化: 在递推过程中, 第一个维度可去掉!
https://leetcode.cn/problems/number-of-stable-subsequences/solutions/3781347/he-fa-zi-xu-lie-dppythonjavacgo-by-endle-7sz0/
     """
    def countStableSubsequences(self, nums: List[int]) -> int:
        MOD = 10**9+7
        f00 = f01 = f10 = f11 = 0
        for x in nums:
            if x % 2 == 0:
                f01 = (f01+f00) % MOD  # NOTE: 这里的更新有依赖关系! 两行不能交换!
                f00 = (f00+f10+f11+1) % MOD
            else:
                f11 = (f11+f10) % MOD
                f10 = (f10+f00+f01+1) % MOD
        return (f00+f01+f10+f11) % MOD




sol = Solution()
result = [
    # sol.maxKDistinct(nums = [1,1,1,2,2,2], k = 6),
    # sol.subsequenceSumAfterCapping(nums = [4,3,2,4], k = 5),
    # sol.countStableSubsequences(nums = [1,3,5]),
    sol.countStableSubsequences([1,19,14,30,1,28,36])
]
for r in result:
    print(r)
