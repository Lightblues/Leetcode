from typing import List, Optional
import collections
import math
import bisect
import heapq

from structures import ListNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@202203 """
class Solution:
    """ 2206. 将数组划分成相等数对 """
    def divideArray(self, nums: List[int]) -> bool:
        counter = collections.Counter(nums)
        for k,v in counter.items():
            if v%2:
                return False
        return True
    
    """ 2207. 字符串中最多数目的子字符串
有可以字符串 text 和长度为 2 的 pattern (记为字符 a 和 b), 可以对 text 插入一个字符 a/b.
要求计算操作后 text 的子字符串恰好是 pattern 的数量. 注意「子字符串」的定义不要求连续, 因此 `aabb` 包括 四个子字符串 `ab`.
思路: 注意到, 这里插入的字符最优解为在最前面插入a 或最后插入b (取决于text中a/b的数量). 而原本text自身的子字符串数量可以 O(n) 求解 (记录 countA, countB).
特殊情况: a==b

输入：text = "aabb", pattern = "ab"
输出：6
解释：
可以得到 6 个 "ab" 子序列的部分方案为 "aaabb" ，"aaabb" 和 "aabbb" 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximize-number-of-subsequences-in-a-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def maximumSubsequenceCount(self, text: str, pattern: str) -> int:
        a,b = pattern
        if a==b:
            count = sum(1 for i in text if i==a)
            return count * (count+1) // 2 # 注意返回整数
        countA, countB = 0, 0
        ans = 0
        for ch in text:
            if ch==a:
                countA += 1
            elif ch==b:
                ans += countA
                countB += 1
        return ans + max(countA, countB)
    
    """ 2208. 将数组和减半的最少操作次数
每次选择数组中的一个元素减半, 要求使得数组和减半需要的次数.
思路: 每次选最大的即可. 采用 heap 实现. 注意 heapify 默认是最小堆, 因此需要取反.
    """
    def halveArray(self, nums: List[int]) -> int:
        nums = [-i for i in nums]
        heapq.heapify(nums)
        target = sum(nums) / 2
        cumsum = 0
        count = 0
        while cumsum > target:
            i = heapq.heappop(nums)
            cumsum += i/2
            heapq.heappush(nums, i/2)
            count += 1
        return count
    
    
    """ 2209. 用地毯覆盖后的最少白色砖块
给一条黑白地板 floor 铺地毯, 要求剩余最少的白色. 给定 numCarpets 条长度为 carpetLen 的黑色地毯.

思路: DP
定义状态: dp[i][j] 表示用 i 条铺 **前面 j 个地砖**, 剩余的最少白色砖块数.
状态转移: dp[i][j] = min(dp[i][j-1]+(floor[j]=="1"), dp[i-1][j-carpetLen]). 其中第一式表示不用地毯.
参见 [here](https://leetcode-cn.com/problems/minimum-white-tiles-after-covering-with-carpets/solution/by-endlesscheng-pa3v/)
    """
    def minimumWhiteTiles(self, floor: str, numCarpets: int, carpetLen: int) -> int:
        """ 注意这里维度为 (numCarpets+1, len(floor)+1)
        第一维遍历地毯数量 0~numCarpets, 第二维遍历地砖长度 0~len(floor). 注意 dp[i][0] = 0."""
        dp = [[0] * (len(floor)+1) for _ in range(numCarpets+1)]
        # 初始条件
        for i,f in enumerate(floor):
            dp[0][i+1] = dp[0][i] + 1 if f=='1' else dp[0][i]
        # DP迭代
        for i in range(1, numCarpets+1):
            # 更好的遍历策略为
            # for j in range(carpetLen * i, len(floor)+1):
            for j in range(1, len(floor)+1):
                dp[i][j] = min(
                    dp[i][j-1]+(floor[j-1]=='1'), 
                    dp[i-1][max(0, j-carpetLen)]
                )
        return dp[-1][-1]
    
sol = Solution()
result = [
    # sol.maximumSubsequenceCount(text = "abdcdbc", pattern = "ac"),
    # sol.halveArray(nums = [5,19,8,1]),
    sol.minimumWhiteTiles(floor = "10110101", numCarpets = 2, carpetLen = 2),
    sol.minimumWhiteTiles(floor = "11111", numCarpets = 2, carpetLen = 3),
]
for r in result:
    print(r)