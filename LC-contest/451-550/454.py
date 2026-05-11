from typing import *
import string
import collections
import math
import itertools

"""
https://leetcode.cn/contest/weekly-contest-454
Easonsi @2026 """


class Solution:
    """ 3582. 为视频标题生成标签 """
    def generateTag(self, caption: str) -> str:
        ans = ""
        for i, word in enumerate(caption.split()):
            if i == 0:
                ans += word.lower()
            else: ans += word.capitalize()
        ans = "".join(ch for ch in ans if ch in string.ascii_letters)
        return ("#"+ans)[:100]

    """ 3583. 统计特殊三元组 
统计 (i,j,k) 坐标数量, 满足 nums[i] = nums[k] = 2 * nums[j]
限制: n 1e5; 对结果取模
思路 1: 枚举中间
    复杂度: O(n)
    """
    def specialTriplets(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        cnt = collections.Counter(nums)
        pre_cnt = collections.defaultdict(int)
        ans = 0
        for i,x in enumerate(nums):
            if x != 0:
                ans = (ans + pre_cnt[2*x]*(cnt[2*x]-pre_cnt[2*x])) % MOD
            pre_cnt[x] += 1
        return (math.comb(cnt[0],3) + ans) % MOD

    """ 3584. 子序列首尾元素的最大乘积 
对于一个数组, 找所有长度为 m 的子序列中, 首尾元素乘积最大值
限制: n 1e5
思路 1: 
    对于 l 开头的子序列, 其匹配的最右位置为 l+m-1, ...
    因此, 可以枚举 l, 维护后缀的 min/max -- 因为乘积最大一定是在min/max 取到
思路 1: 脑筋急转弯 + #枚举右维护左 -- 代码可以更简洁!
    注意无需特判 m=1 的情况，此时答案来自 nums 的最大值与自己相乘 -- 可以枚举到!
https://leetcode.cn/problems/maximum-product-of-first-and-last-elements-of-a-subsequence/solutions/3700555/nao-jin-ji-zhuan-wan-mei-ju-you-wei-hu-z-93zo/
    """
    def maximumProduct(self, nums: List[int], m: int) -> int:
        # if m == 1:  # 不需要特判!
        #     return max(map(abs, nums))**2
        n = len(nums)
        suf_min, suf_max = nums[-1], nums[-1]
        ans = nums[n-m] * nums[-1]
        for l in range(n-m-1,-1,-1):
            x = nums[l]
            nr = nums[l+m-1]
            suf_min = min(suf_min, nr)
            suf_max = max(suf_max, nr)
            ans = max(ans, x*suf_min, x*suf_max)
        return ans

    """ 3585. 树中找到带权中位节点 #hard
给定一棵带权树, 对于每次查询 (u,v), 计算 "带权中位节点", 也即从 u 到 v 的路径上, 累计边权和 >= u到v总边权和的节点.
限制: n, q 1e5
思路 1: #最近公共祖先 LCA
    """
    def findMedian(self, n: int, edges: List[List[int]], queries: List[List[int]]) -> List[int]:


sol = Solution()
result = [
    # sol.generateTag(caption = "Leetcode daily streak achieved"),
    # sol.specialTriplets(nums = [6,3,6]),
    # sol.specialTriplets(nums = [0,1,0,0]),
    sol.maximumProduct(nums = [-1,-9,2,3,-2,-3,1], m = 1),
    sol.maximumProduct(nums = [1,3,-5,5,6,-4], m = 3),
]
for r in result:
    print(r)