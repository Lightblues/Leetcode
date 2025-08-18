from typing import *
from functools import reduce
import math

""" 
https://leetcode.cn/contest/weekly-contest-431

Easonsi @2025 """
class Solution:
    """ 3411. 最长乘积等价子数组
#滑动窗口 可以把复杂度压缩到 O(n logU), 其中U为数字范围
[ling](https://leetcode.cn/problems/maximum-subarray-with-equal-products/solutions/3039079/mei-ju-ti-qian-tui-chu-xun-huan-pythonja-a21k/)
    """
    def maxLength(self, nums: List[int]) -> int:
        def check(i,j):
            prod = reduce(lambda x,y: x*y, nums[i:j+1])
            gcd = reduce(lambda x,y: math.gcd(x,y), nums[i:j+1])
            lcm = reduce(lambda x,y: math.lcm(x,y), nums[i:j+1])
            return prod == gcd * lcm
        n = len(nums)
        ans = 0
        for i in range(n):
            for j in range(i,n):
                if j-i+1 <= ans: continue
                if check(i,j):
                    ans = max(ans, j-i+1)
        return ans
    
    """ 3412. 计算字符串的镜像分数 """
    def calculateScore(self, s: str) -> int:
        st = [[] for _ in range(26)]
        ans = 0
        for i,ch in enumerate(s):
            idx = 25 - (ord(ch) - ord('a'))
            if st[idx]:
                ans += i - st[idx].pop()
            else:
                st[25-idx].append(i)
        return ans

    """ 3413. 收集连续 K 个袋子可以获得的最多硬币数量 """
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        coins.sort(key=lambda x: x[0])
        n = len(coins)
        ans = 0
        # 
        ridx = rlimit = 0; acc = 0
        for i, (l,r,v) in enumerate(coins):
            if i > 0:
                acc -= coins[i-1][2] * min((coins[i-1][1] - coins[i-1][0]), k)
            while ridx < n and coins[ridx][0] <= l+k:
                acc += v * (min(r, l+k) - max(l, rlimit) + 1)
                if l+k < r:
                    rlimit = l+k
                    break
                ridx += 1
                rlimit = r+1  # 
            ans = max(ans, acc)
        # 
        lidx = llimit = n-1; acc = 0
        for i in range(n-1, -1, -1):
            l,r,v = coins[i]
            if i < n-1:
                acc -= coins[i+1][2] * min((coins[i+1][1] - coins[i+1][0]), k)
            while lidx >= 0 and coins[lidx][0] >= r-k:
                acc += v * (min(r, llimit) - max(l, l-k) + 1)
                if r-k > l:
                    llimit = r-k
                    break
                lidx -= 1
                llimit = l-1
            ans = max(ans, acc)
        return ans



    
sol = Solution()
result = [
    # sol.maxLength(nums = [1,2,1,2,1,1,1]),
    # sol.calculateScore(s = "aczzx"),
    sol.maximumCoins(coins = [[8,10,1],[1,3,2],[5,6,4]], k = 4),
]
for r in result:
    print(r)
