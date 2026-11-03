from typing import *
from math import ceil, floor

"""
https://leetcode.cn/contest/weekly-contest-466
3. 碗子数组的数目
    区分 l,r 之间的大小关系, 然后用单调栈来分析;
    妙的是在出栈过程中即可判断另一种情况!
4. 统计二进制回文数字的数目 #hard 
    基本思路 "枚举二进制长度" 还是比较顺的 -- 重要的是思路要清楚!
    据说可以用数位 DP 来做, 可学习 (不过有点复杂化了?)
Easonsi @2026 """


class Solution:
    """ 3674. 数组元素相等的最小操作次数 """
    def minOperations(self, nums: List[int]) -> int:
        return 0 if len(set(nums))==1 else 1

    """ 3675. 转换字符串的最小操作次数 """
    def minOperations(self, s: str) -> int:
        chs = set(c for c in s if c!='a')
        if not chs: return 0
        mn = min(ord(c)-ord('a') for c in chs)
        return 26 - mn

        # from ling, 1. 利用了 default 语法; 2. 'z' 的下一个字符是 '{'
        min_c = min((c for c in s if c != 'a'), default='{')
        return ord('{') - ord(min_c)

    """ 3676. 碗子数组的数目 #medium 给定一个数组, 求所有满足 "两侧元素 > 中间元素最大值" 的子数组数量 (len >= 3) 
思路 1: #单调栈
    考虑 l>=r 的情况, 此时, 问题变为, 对于 r 元素, "找左侧第一个 >= 的位置"
        - 为什么是 "第一个"? 因为第二个的话就不满足 "碗条件"
        - 若 l <= r-1, 则构成一个解
        - 这一问题可用单调栈!
    那么对于 l<r 的情况呢? 妙的是, 在上述维护单调递减栈的出栈过程中, 我们即可直接判断! -- 若出栈元素位置 <= r-1, 说明它们中间的元素比它们都小!
https://leetcode.cn/problems/count-bowl-subarrays/solutions/3774499/dan-diao-zhan-pythonjavacgo-by-endlessch-y64n/
    """
    def bowlSubarrays(self, nums: List[int]) -> int:
        ans = 0
        st = []
        for i,x in enumerate(nums):
            # 维护单调递减栈
            while st and nums[st[-1]]<x:
                # 是否构成情况 2
                if i - st.pop() > 1: ans += 1
            # 是否构成情况 1
            if st and i - st[-1] > 1: ans += 1
            st.append(i)
        return ans

    """ 3677. 统计二进制回文数字的数目 #hard 给出 <=n 的, 且其二进制表示为回文数的数字数量. 0 也算.
限制: n 1e15
思路 1: 枚举二进制长度
    对于 n 其二进制长度为 m
    - 对于长度 i=1,2,...m-1 的情况, 考虑左半边 ceil(i/2) 位, 最高位只能填 1, 其他的 k=ceil(i/2)-1 随便填, 因此有 2^k 种情况 (右半边不需要考虑)
    - 对于长度 =m 的情况, 依次考虑其左半边的位, 也即 m-2,m-3...floor(m/2)
        最高位 m-1 只能是 1
        枚举其他位, 若 n 的那一位是 1:
            - 填入 0, 则其他的 k=i-floor(m/2) 位随便填
            - 填入 1, 继续往下
        枚举完成后, 将 n 的左半边翻转拼接, 如得到的数 pal <=n 则 +1
https://leetcode.cn/problems/count-binary-palindromic-numbers/solutions/3774534/olog-n-zuo-fa-pythonjavacgo-by-endlessch-1ggp/
    """
    def countBinaryPalindromes(self, n: int) -> int:
        if n==0: return 1
        ans = 1  # 
        m = n.bit_length()
        for i in range(1, m):
            k = ceil(i/2) - 1
            ans += 1<<k
        for i in range(m-2, m//2-1, -1):  # 第一位 m-1 只能填 1, 后面开始枚举
            if n>>i & 1:
                ans += 1<<(i-m//2)
        # 
        pal = n >> (m//2)
        v = pal >> (m%2)
        while v:
            pal = pal * 2 + v % 2
            v //= 2
        if pal <= n: ans += 1
        return ans

sol = Solution()
result = [
    # sol.minOperations(s = "yz"),
    # sol.bowlSubarrays(nums = [2,5,3,1,4]),
    sol.countBinaryPalindromes(9)
]
for r in result:
    print(r)
