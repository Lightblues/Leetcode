from typing import *
from math import inf
from functools import cache
from collections import defaultdict
import heapq

""" 
https://leetcode.cn/contest/weekly-contest-443
T3 两个字符串的子串连接构成回文字符串, 经典DP和中心扩展法结合应用, 需要细致的分析 #star
T4 外层划分型 DP, 内层使用懒删除堆维护滑动窗口中位数, 计算代价, 综合应用 #star
Easonsi @2025 """
class Solution:
    """ 3502. 到达每个位置的最小费用 """
    def minCosts(self, cost: List[int]) -> List[int]:
        pre = inf
        for i,x in enumerate(cost):
            pre = min(pre, x)
            cost[i] = pre
        return cost
    
    """ 3503. 子字符串连接后的最长回文串 I """

    """ 3504. 子字符串连接后的最长回文串 II #hard 给定两个字符串 s,t 从中选两个 (连续) 子串连接, 求得到的最长回文子串的长度
限制: n 2e3
--- 理解错题目了: 等价于给定一个字符串, 找到最大回文子串的长度
思路1: #DP 
    记 f[i,j] 为 s[i:j] 范围内的最长回文子串的长度, 则有
        f[i,j] = f[i+1,j-1]+2 if s[i]==s[j-1] else max(f[i+1,j], f[i,j-1])
        边界: j=i+1 / i

--- from ling
思路1:
    假设两字符串中取的分别为 x,y, 考虑长度
        |x| == |y|, 则 y = rev(x)
        |x| > |y|, 则x有一个长 |x|-|y| 的后缀回文串, 其前缀串满足 y = rev(x_prefix)
        |x| < |y|, 同理
    考虑 |x| == |y| 的情况, 使用 DP:
        记 f[i,j] 表示以 s[i] 结尾, t[j] 开头的两子串的最长匹配长度, 则有
            s[i] != t[j] 时, =0
            否则, f[i,j] = f[i-1,j+1] + 1
        最后答案为 max(2*f[i,j])
    再考虑 |x| > |y| 的情况, 采用 "0005. 最长回文子串" 的中心扩展法, 枚举所有回文中心 (长度1或者2)
        枚举中心, 假设得到的最长回文串为 s[l...r], 则匹配的y为 max{ f[l-1,:] }, 不妨记作 mx[l-1]
        注意, 这一利用了贪心的性质: 若最长回文串为 s[l...r], 则在t中找匹配的reverse子串, 一定可以用更少的前缀 s[...l-1]
    复杂度: O(n^2)
思路2: #Manacher + #后缀数组
ling: https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-ii/solutions/3633596/mei-ju-hui-wen-zhong-xin-dppythonjavacgo-kpxn/
    """
    def longestPalindrome_error(self, s: str, t: str) -> int:
        # 理解错题目了, 以为是子序列
        s = s + t
        n = len(s)
        @cache
        def f(i:int, j:int) -> int:
            if j <= i:
                return 0
            if j == i+1:
                return 1 if s[i] != s[j] else 2
            if s[i] == s[j]:
                return f(i+1, j-1) + 2
            else:
                return max(f(i+1, j), f(i, j-1))
        return f(0, n-1)

    def longestPalindrome(self, s: str, t: str) -> int:
        # NOTE: 下面用了cache形式, 不clear的话容易OOM! 可以写成递推的形式
        def calc(s:str, t:str) -> int:
            n,m = len(s),len(t)
            @cache
            def f(i:int, j:int) -> int:
                if i<0 or j>=m:
                    return 0
                if s[i] == t[j]:
                    return f(i-1, j+1) + 1
                else:
                    return 0
            @cache
            def mx(i:int) -> int:
                if i<0:
                    return 0
                return max(f(i,j) for j in range(m))
            
            ans = max(mx(i) for i in range(n)) * 2
            # 枚举回文中心
            for i in range(2*n-1):
                l,r = i//2, (i+1)//2
                while l>=0 and r<n and s[l]==s[r]:
                    l -= 1
                    r += 1
                ans = max(ans, (r-l-1) + 2*mx(l))
            # clear cache, 不然会OOM
            f.cache_clear()
            mx.cache_clear()
            return ans
        return max(calc(s,t), calc(t[::-1], s[::-1]))  # 颠倒 s,t


    """ 3505. 使 K 个子数组内元素相等的最少操作数 #hard 对于一个数组num, 每次操作可以将元素 +/-1, 为了使得出现k个长度恰好为x的不重叠子数组, 其元素都相同, 最小操作次数
限制: n 1e5
思路1: #DP (划分型 DP)
    记 f[i,j] 表示从 0...j-1 中选择i个要求的子数组的最小操作数, 分类:
        不包含 nums[j-1], 则 f[i,j] = f[i,j-1]
        包含 nums[j-1], 则 nums[j-x...j-1] 构成一个要求的区间, 有 f[i,j] = f[i-1,j-x] + cost[j-x], 其中 cost[j-x] 表示将 nums[j-x...j-1] 变为相同元素的最小操作数
        两者取 min
    边界: 
        f[0,:] = 0; 
        f[i,i*x-1] = inf, 注意不需要初始化前面的, 因为不会访问到
    如何高效计算 cost[j]? 参见 "0480. 滑动窗口中位数"
        对于 "给定一个数组, 将所有元素变为相同元素的最小操作数", 最优解是变为中位数
        如何增量计算中位数? 滑动窗口! 需要维护一个支持删除操作的最大和最小堆 -- #懒删除堆
        如何计算cost? 需要计算两个堆中元素到中位数的距离和 (面积)
ling: https://leetcode.cn/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/solutions/3633641/hua-dong-chuang-kou-zhong-wei-shu-hua-fe-e9cn/
    """
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        def medianSlidingWindow(nums: list[int], k: int) -> list[int]:
            """ 返回每个长度为k的滑动窗口的中位数 """
            left = LazyHeap()   # 最大堆, 维护前 (k+1)//2 个元素
            right = LazyHeap()  # 最小堆, 维护后 k//2 个元素
            ans = [0] * (len(nums)-k+1)
            
            for i,x in enumerate(nums):
                # 1. add x
                if left.size == right.size:  # add to left
                    left.push(-right.pushpop(x))
                else:  # add to right
                    right.push(-left.pushpop(-x))
                if i < k-1:
                    continue
                # 2. get median & calc result
                median = -left.top()
                cost = median * left.size - (-left.sum) + right.sum - median * right.size
                ans[i - k + 1] = cost
                # 3. remove nums[i-k+1]
                out = nums[i - k + 1]
                if out <= median:
                    left.remove(-out)
                    if left.size < right.size:  # rebalance
                        left.push(-right.pop())
                else:
                    right.remove(out)
                    if left.size > right.size + 1:
                        right.push(-left.pop())
            return ans

        cost = medianSlidingWindow(nums, x)
        n = len(nums)
        f = [[0] * (n+1) for _ in range(k+1)]
        for i in range(1, k+1):
            f[i][i*x-1] = inf
            for j in range(i*x, n+1):
                f[i][j] = min(f[i][j-1], f[i-1][j-x] + cost[j - x])
        return f[k][n]  # 题目一定满足要求

class LazyHeap:
    """ 懒删除堆, 维护元素个数和元素和 """
    def __init__(self):
        self.heap = []
        self.remove_cnt = defaultdict(int)
        self.size = 0
        self.sum = 0

    def remove(self, x: int) -> None:
        self.remove_cnt[x] += 1
        self.size -= 1
        self.sum -= x

    def apply_remove(self) -> None:
        while self.heap and self.remove_cnt[self.heap[0]] > 0:
            x = heapq.heappop(self.heap)
            self.remove_cnt[x] -= 1
    
    def top(self) -> int:
        self.apply_remove()
        return self.heap[0] 
    
    def pop(self) -> int:
        self.apply_remove()
        x = heapq.heappop(self.heap)
        self.size -= 1
        self.sum -= x
        return x
    
    def push(self, x: int) -> None:
        if self.remove_cnt[x] > 0:
            self.remove_cnt[x] -= 1
        else:
            heapq.heappush(self.heap, x)
        self.size += 1
        self.sum += x

    def pushpop(self, x:int) -> int:
        self.apply_remove()
        if not self.heap or x <= self.heap[0]:
            return x
        self.sum += x - self.heap[0]
        return heapq.heapreplace(self.heap, x)  # heapq.heappushpop

sol = Solution()
result = [
    # sol.minCosts(cost = [5,3,4,1,3,2]),
    # sol.longestPalindrome(s = "abc", t = "cba"),
    # sol.longestPalindrome(s = "abcde", t = "ecdba"),
    sol.minOperations(nums = [5,-2,1,3,7,3,6,4,-1], x = 3, k = 2),
]
for r in result:
    print(r)
