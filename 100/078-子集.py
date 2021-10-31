"""
给你一个整数数组 nums ，数组中的元素 互不相同 。返回该数组所有可能的子集（幂集）。
解集 不能 包含重复的子集。你可以按 任意顺序 返回解集。

1 <= nums.length <= 10


输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
"""
from typing import List
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        now = []
        n = len(nums)
        def backtrack(index):
            if index==n:
                res.append(now.copy())
                return
            backtrack(index+1)
            now.append(nums[index])
            backtrack(index+1)
            now.pop()       # 注意，最后还要 pop 出来，因为 DFS 之后还要回溯
        backtrack(0)
        return res
nums = [1,2,3]
print(Solution().subsets(nums))


