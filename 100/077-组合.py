"""
给定两个整数 n 和 k，返回 1 ... n 中所有可能的 k 个数的组合。

输入: n = 4, k = 2
输出:
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]
"""
from typing import List

class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        now = []
        nums = list(range(1, n+1))
        def backtrack(i, k_):
            if k_ == 0:
                res.append(now.copy())
                return
            for j in range(i, n-k_+1):
                now.append(nums[j])
                backtrack(j+1, k_-1)
                now.pop()
        backtrack(0, k)
        return res
n = 4; k = 2
print(Solution().combine(n, k))




