"""
给定一个非负整数数组，你最初位于数组的第一个位置。
数组中的每个元素代表你在该位置可以跳跃的最大长度。
你的目标是使用最少的跳跃次数到达数组的最后一个位置。

输入: [2,3,1,1,4]
输出: 2
解释: 跳到最后一个位置的最小跳跃数是 2。
    从下标为 0 跳到下标为 1 的位置，跳 1 ，然后跳 3 步到达数组的最后一个位置。
"""

from typing import List
class Solution:
    def jump_try(self, nums: List[int]) -> int:
        # DFS，贪心
        n = len(nums)
        target = n-1
        steps = 0
        def dfs(i):
            nonlocal steps
            num = nums[i]
            if num >= target-i:
                return steps+1
            steps += 1
            for hop in range(num, 0, -1):
                res = dfs(i+hop)
                if res>0:
                    return res
            # 否则，说明检索失败
            steps -= 1
            return -1
        res = dfs(0)
        return res

    def jump(self, nums: List[int]) -> int:
        # 贪心
        n = len(nums)
        steps = 0
        curr = 0

        while curr < n-1:
            max_hop_two = 0
            nex = 0
            for hop in range(nums[curr], 0, -1):
                if hop + curr >= n-1:
                    return steps+1
                if nums[curr+hop] + hop + curr >= n-1:
                    return steps+2
                if nums[curr+hop] + hop > max_hop_two:
                    max_hop_two = nums[curr+hop] + hop
                    nex = hop
            curr = curr + nex
            steps += 1
        return steps


# nums = [2,3,1,1,4]
nums = [2,1]
print(Solution().jump(nums))



