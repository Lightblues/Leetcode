"""
给你一个整数数组 arr 和一个整数 difference，请你找出并返回 arr 中最长等差子序列的长度，该子序列中相邻元素之间的差等于 difference 。

子序列 是指在不改变其余元素顺序的情况下，通过删除一些元素或不删除任何元素而从 arr 派生出来的序列。

输入：arr = [1,5,7,8,5,3,4,2,1], difference = -2
输出：4
解释：最长的等差子序列是 [7,5,3,1]。

关键在想好 DP 的形式：这里记录arr每个位置的

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-arithmetic-subsequence-of-given-difference
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

from typing import List

class Solution:
    def longestSubsequence(self, arr: List[int], difference: int) -> int:
        dp = {}     # defaultdict(int)
        for i in arr:
            if i - difference in dp:
                dp[i] = 1 + dp[i - difference]
            else:
                dp[i] = 1
        return max(dp.values())

        
print(Solution().longestSubsequence([1,5,7,8,5,3,4,2,1], -2))