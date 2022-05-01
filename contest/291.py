from typing import List, Optional
import collections
import math
import bisect
import heapq
import functools, itertools
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
from utils_leetcode import (
    testClass,
)
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """

class Solution:
    """ 6047. 移除指定数字得到的最大结果
给定一个字符串num, 可以删除指定的一个数字d, 要求删除后的数字最大
思路: 从左往右遍历, 对于位置i的数组d满足 num[i]<num[i+1], 则显然可以删除该数字. 否则, 应该删除最后一个数字d所在的位置.

输入：number = "1231", digit = "1"
输出："231"
解释：可以移除第一个 '1' 得到 "231" 或者移除第二个 '1' 得到 "123" 。
由于 231 > 123 ，返回 "231" 。
    """
    def removeDigit(self, number: str, digit: str) -> str:
        lastIdx = -1
        for i,ch in enumerate(number):
            if ch!= digit: continue
            if i<len(number)-1 and number[i+1] > digit:
                return number[:i] + number[i+1:]
            lastIdx = i
        return number[:lastIdx] + number[lastIdx+1:]
    
    """ 6048. 必须拿起的最小连续卡牌数
求一数组中一对相同元素的最近距离

输入：cards = [3,4,2,3,4,7]
输出：4
解释：拿起卡牌 [3,4,2,3] 将会包含一对值为 3 的匹配卡牌。注意，拿起 [4,2,3,4] 也是最优方案。
"""
    def minimumCardPickup(self, cards: List[int]) -> int:
        if collections.Counter(cards).__len__()==len(cards): return -1
        ans = len(cards)
        d = collections.defaultdict(list)
        for i,c in enumerate(cards):
            if d[c]:
                ans = min(ans, i-d[c][-1]+1)
            d[c].append(i)
        return ans
    
    
    """ 6049. 含最多 K 个可整除元素的子数组
条件: 子数组中能够被数字 p 整除的元素的个数最多为 k
对一个数组的所有 **连续非空** 子数组, 计算满足条件的不同的数组数量.

思路: 本题复杂度为 `1 <= nums.length <= 200`, 因此用一个 isPdivisible 数组记录每个数字是否可被整出, 然后用一个set记录出现的不重复子数组即可.

输入：nums = [2,3,3,2,2], k = 2, p = 2
输出：11
解释：
位于下标 0、3 和 4 的元素都可以被 p = 2 整除。
共计 11 个不同子数组都满足最多含 k = 2 个可以被 2 整除的元素：
[2]、[2,3]、[2,3,3]、[2,3,3,2]、[3]、[3,3]、[3,3,2]、[3,3,2,2]、[3,2]、[3,2,2] 和 [2,2] 。
注意，尽管子数组 [2] 和 [3] 在 nums 中出现不止一次，但统计时只计数一次。
子数组 [2,3,3,2,2] 不满足条件，因为其中有 3 个元素可以被 2 整除。
    """
    def countDistinct(self, nums: List[int], k: int, p: int) -> int:
        isPdivisible = [i%p==0 for i in nums]
        results = set()
        for i in range(1, len(nums)+1):
            for start in range(len(nums)-i+1):
                if sum(isPdivisible[start:start+i])<=k:
                    results.add(tuple(nums[start:start+i]))
        return len(results)
    
    """ 6050. 字符串的总引力
定义一个字符串的引力: 不同字符的数量. 要求所有子字符串的引力只和.
复杂度: 1 <= s.length <= 105
尝试了对于每一个长度进行「滑动窗口」, 复杂度为 O(n^2), 显然会超时.

输入：s = "abbca"
输出：28
解释："abbca" 的子字符串有：
- 长度为 1 的子字符串："a"、"b"、"b"、"c"、"a" 的引力分别为 1、1、1、1、1，总和为 5 。
- 长度为 2 的子字符串："ab"、"bb"、"bc"、"ca" 的引力分别为 2、1、2、2 ，总和为 7 。
- 长度为 3 的子字符串："abb"、"bbc"、"bca" 的引力分别为 2、2、3 ，总和为 7 。
- 长度为 4 的子字符串："abbc"、"bbca" 的引力分别为 3、3 ，总和为 6 。
- 长度为 5 的子字符串："abbca" 的引力为 3 ，总和为 3 。
引力总和为 5 + 7 + 7 + 6 + 3 = 28 。
"""
    def appealSum0(self, s: str) -> int:
        """ 滑动窗口. 显然会超时 """
        n = len(s)
        ans = n
        for i in range(2, n+1):
            c = collections.Counter(s[:i])
            ans += len(c)
            for j in range(i, n):
                c[s[j]] += 1
                c[s[j-i]] -= 1
                if c[s[j-i]]==0: del c[s[j-i]]
                ans += len(c)
        return ans
    """ 思路: 遍历累计
考虑序列中某一个ch会在多少个子串中出现?
不考虑本题, 一般情况下, 对于位置idx的ch, 序列 ...xxx[ch]xxx... 的子串中出现ch的个数为: `(idx+1) * (len-idx+1)`
本题中, 只有在子串中第一次出现的ch才计数假设. 因此假设出现的位置分别为 `i_1, i_2,...i_j, i_k, ...`. 对于 ik, 其 **作为第一个ch出现在子串中** 的数量为 `(i_k-i_j) * (len-i_j+1)`. 注意左边界进行了限制.
因此, 在遍历过程中, 对于不同的ch分别记录出现的 idx, 并累计计数.

思路二: 类似DP.
考虑从长度为 i 的前缀字符串拓展到 i+1 的变化情况. 增加了 i+1 个子串, 分别是 s[1:i+1], s[2:i+1]...s[i+1:i+1]. 我们要计算这些新子串所包括的引力值: 两部分
- 末尾字符的: `idx[i+1]-idx[i]`
- 其他字符的引力值 等价于 **所有以第i个字符结尾的子串的引力值**. 记这个值为 `sum_g`, 易知迭代公式 `sum_g[i+1] = sum_g[i] + (idx[i+1]-idx[i])`

see [here](https://leetcode-cn.com/problems/total-appeal-of-a-string/solution/by-endlesscheng-g405/) 
"""
    def appealSum(self, s: str) -> int:
        # ch2lastIdx = collections.defaultdict(lambda : -1)
        # ans = 0
        # for i,ch in enumerate(s):
        #     ans += i - ch2lastIdx[ch]
        #     ch2lastIdx[ch] = i
        # return ans
        
        ch2idx = collections.defaultdict(lambda: [-1])  # 注意defaultdict的初始化
        for i,ch in enumerate(s):
            ch2idx[ch].append(i)
        ans = 0
        for ch, idx in ch2idx.items():
            idx.append(len(s))
            for i in range(1, len(idx)-1):
                ans += (idx[i]-idx[i-1]) * (idx[-1]-idx[i])
        return ans

        ans, sum_g, pos = 0, 0, [-1] * 26
        for i, c in enumerate(s):
            c = ord(c) - ord('a')
            sum_g += i - pos[c]
            ans += sum_g
            pos[c] = i
        return ans

sol = Solution()
result = [
    # sol.removeDigit(number = "1231", digit = "1"),
    # sol.removeDigit(number = "551", digit = "5"),
    # sol.removeDigit("123", "3"),
    
    # sol.minimumCardPickup(cards = [3,4,2,3,4,7]),
    # sol.minimumCardPickup(cards = [1,0,5,3]),
    
    # sol.countDistinct(nums = [2,3,3,2,2], k = 2, p = 2),
    # sol.countDistinct(nums = [1,2,3,4], k = 4, p = 1),
    
    sol.appealSum(s = "code"),
    sol.appealSum(s = "abbca"),
]
for r in result:
    print(r)
