from typing import List
import bisect


class Solution272:
    """ 5956. 找出数组中的第一个回文字符串 """
    def firstPalindrome(self, words: List[str]) -> str:
        def isPalindrome(words):
            return words[::-1] == words
        for word in words:
            if isPalindrome(word):
                return word
        return ""
    """ 5957. 向字符串添加空格 """
    def addSpaces(self, s: str, spaces: List[int]) -> str:
        result = ""
        for i in spaces[::-1]:
            result = " " + s[i:] + result
            s = s[:i]
        return s + result
    
    """ 5958. 股票平滑下跌阶段的数目 
给你一个整数数组 prices ，表示一支股票的历史每日股价，其中 prices[i] 是这支股票第 i 天的价格。
一个 平滑下降的阶段 定义为：对于 连续一天或者多天 ，每日股价都比 前一日股价恰好少 1 ，这个阶段第一天的股价没有限制。

输入：prices = [3,2,1,4]
输出：7
解释：总共有 7 个平滑下降阶段：
[3], [2], [1], [4], [3,2], [2,1] 和 [3,2,1]
注意，仅一天按照定义也是平滑下降阶段。"""
    def getDescentPeriods(self, prices: List[int]) -> int:
        descentLen = []
        prices.append(float("inf"))
        i = 1
        count = 1
        while i<len(prices):
            if prices[i] != prices[i-1]-1:
                descentLen.append(count)
                count = 1
            else:
                count += 1
            i += 1
        result = 0
        f = lambda x: int((x+1)*x/2)
        for l  in descentLen:
            # result += math.factorial(l)
            result += f(l)
        return result

    """ 5959. 使数组 K 递增的最少操作次数
如果对于每个满足 k <= i <= n-1 的下标 i ，都有 arr[i-k] <= arr[i] ，那么我们称 arr 是 K 递增 的。 
输入：arr = [5,4,3,2,1], k = 1
输出：4
解释：
对于 k = 1 ，数组最终必须变成非递减的。
可行的 K 递增结果数组为 [5,6,7,8,9]，[1,1,1,1,1]，[2,2,3,4,4] 。它们都需要 4 次操作。
次优解是将数组变成比方说 [6,7,8,9,10] ，因为需要 5 次操作。
显然我们无法使用少于 4 次操作将数组变成 K 递增的。

输入：arr = [4,1,5,2,6,2], k = 2
输出：0
解释：
这是题目描述中的例子。
对于每个满足 2 <= i <= 5 的下标 i ，有 arr[i-2] <= arr[i] 。
由于给定数组已经是 K 递增的，我们不需要进行任何操作。

转化为求递增子序列, 参见 #300 https://leetcode-cn.com/problems/longest-increasing-subsequence/solution/zui-chang-shang-sheng-zi-xu-lie-by-leetcode-soluti/"""
    def kIncreasing(self, arr: List[int], k: int) -> int:
        result = 0
        for kk in range(k):
            subarr = arr[kk::k]
            result += len(subarr) - self.lengthOfLIS2(subarr)
        return result

    def lengthOfLIS(self, nums: List[int]) -> int:
        # 
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[i] >= nums[j]:
                    dp[i] = max(dp[i], dp[j]+1)
        return max(dp)
    def lengthOfLIS2(self, nums: List[int]) -> int:
        d = []
        for num in nums:
            if not d or num >= d[-1]:
                d.append(num)
            else:
                index = bisect.bisect(d, num)
                d[index] = num
        return len(d)


sol = Solution272()
res = [
    # sol.addSpaces("LeetcodeHelpsMeLearn", [8,13,15]),
    # sol.getDescentPeriods([3,2,1,4]),

    # sol.lengthOfLIS([10,9,2,5,3,7,101,18]),
    sol.kIncreasing(arr = [5,4,3,2,1], k = 1), 
    sol.kIncreasing(arr = [4,1,5,2,6,2], k = 2),
]
for r in res:
    print(r)
