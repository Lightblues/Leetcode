from typing import *
from collections import Counter, defaultdict

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-143

T3 两种解法: 差分和同向三指针, 非常惊艳! 理应属于常规题的
T4 数位DP, 又忘差不多了...

Easonsi @2025 """
class Solution:
    """  """
    def smallestNumber(self, n: int, t: int) -> int:
        def calc(x):
            prod = 1
            while x > 0:
                prod *= x % 10
                x //= 10
            return prod
        for i in range(n, n+10):
            if calc(i) % t == 0: return i
        return -1

    """3347. 执行操作后元素的最高频率 II #medium 对于一个数组, 需要操作 o 次, 每次选择一个不同的位置, 增加 [-k, k]. 问能得到的最大频数 
限制: n 1e5; x 1e9
思路1: #滑动窗口 + #同向三指针
    考虑最终freq最大的数字为 x, 可以分为两种情况: x 不存在 / 存在 于原本数组中的
    - x 存在于原数组: 同向三指针
        遍历x, 然后维护 left, right 分别统计 x-k, x+k 的边界
    - x 不存在: 可以用滑动窗口
        注意到, 此时答案必然 <=o, 可以维护一个宽度为 2k 的窗口, 计算最大长度!
思路2: #差分
    对于每个数字 a, 其可变换的范围为 [a-k, a+k], 可以用差分记录范围! 
    - 如何处理超大数字范围? 只统计某部分特定数字!
    - 如何处理 operation 限制? 对于目标数组 x, 取 min{ 差分和, cnt[x] + numOperations }
    - 会出现枚举遗漏吗? (关联问题1) 注意到, 答案只可能出现在 (a-k, a, a+k) 中, 不需要考虑其他数字!
[ling](https://leetcode.cn/problems/maximum-frequency-of-an-element-after-performing-operations-ii/solutions/2983355/liang-chong-fang-fa-chai-fen-hua-dong-ch-7buy/)
"""
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        freq = Counter(nums)
        freq = sorted(freq.items())
        # 情况1
        ans = 0; n = len(freq)
        l = r = 0; cnt = 0
        for m, (x, c) in enumerate(freq):
            # cnt += c  # 在 r 已经算进去了
            while freq[l][0] < x-k:
                cnt -= freq[l][1]
                l += 1
            while r < n and freq[r][0] <= x+k:
                cnt += freq[r][1]
                r += 1
            ans = max(ans, min(cnt, c + numOperations))
        # 提前结束
        if ans > numOperations: return ans
        # 情况2
        l = cnt = 0
        for x,c in freq:
            cnt += c
            while freq[l][0] < x-2*k:
                cnt -= freq[l][1]
                l += 1
            ans = max(ans, min(cnt, numOperations))
        return ans

    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        cnt = Counter(nums)
        diff = defaultdict(int)
        for x,c in cnt.items():
            diff[x]  # NOTE: 不能漏掉
            diff[x-k] += c
            diff[x+k+1] -= c
        acc = 0; ans = 0
        for x, c in sorted(diff.items()):
            acc += c
            ans = max(ans, min(acc, cnt[x] + numOperations))
        return ans

    """ 对于没有0的整数, 返回 >=num 的, 且各位数乘积可以被 t 整除的数字, 找不到则 -1.
限制: len(num) 1e5; t 1e14
思路1: 复杂的 #数位DP
    破题: 注意到, 所有个位数所能提供的质因子只有 (2,3,5,7), 因此, 若 t 中包括超过7的质因子, 则显然无解, 直接返回 -1
    接下来就是数位DP的思路: 
        用一个 ans 数组保存当前枚举的数字
        vis(i, t, is_limit) 表示枚举i位, 剩余的需要满足的乘积为 t, 是否受到 >=num 的约束.
            显然, 当我们填入x的时候, 需要更新 t <- t / gdc(t,x)
    需要考虑的特殊点: 
        - 一定有解, 但答案的长度可能超过 len(num)! 因此需要对于 num 补前导0
            至少补1个, 因为 num=99, t=2 的时候, 答案 112 也比 99 更长
            需要补 max{ cnt - len(num) + 1, 1 } 个, 其中 cnt 为t中的质因子个数.
        - 枚举前导0会有什么影响? 
            注意条件中 "非零", 也即正常数位DP过程中不会考虑0; 什么时候可以填0? 
            isLimit & i <= pad, 其中pad是补的前导0的个数
    复杂度问题? 
[ling](https://leetcode.cn/problems/smallest-divisible-digit-product-ii/solutions/2984014/bao-sou-zuo-fa-lei-si-shu-wei-dp-by-endl-nkoo/)
    """
    def smallestNumber(self, num: str, t: int) -> int:
        pass


sol = Solution()
result = [
    sol.smallestNumber(n = 10, t = 2),
    # sol.maxFrequency(nums = [1,4,5], k = 1, numOperations = 2),
    # sol.maxFrequency(nums = [5,11,20,20], k = 5, numOperations = 1),
    # sol.maxFrequency([9], 0, 0),
]
for r in result:
    print(r)
