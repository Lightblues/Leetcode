from typing import *

""" 
https://leetcode.cn/contest/weekly-contest-446
Easonsi @2025 """
class Solution:
    """  """
    def calculateScore(self, instructions: List[str], values: List[int]) -> int:
        n = len(instructions)
        score = 0
        visited = set()
        i = 0
        
        while i >= 0 and i < n:
            if i in visited:
                break
            visited.add(i)
            
            if instructions[i] == "add":
                score += values[i]
                i += 1
            else:  # "jump"
                i += values[i]
        
        return score

    def maximumPossibleSize(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        prev_max = 0  # 上一段的 max
        cur_max = 0   # 当前段的 max
        for i in range(n):
            cur_max = max(cur_max, nums[i])
            # 当前段的 max >= 上一段的 max，满足非递减，可以在此结束当前段
            if cur_max >= prev_max:
                ans += 1
                prev_max = cur_max
                cur_max = 0
        # 如果最后还剩余元素（cur_max > 0 说明最后一段还没结束），
        # 需要将其合并到前一段（不增加 ans）
        return ans


sol = Solution()
result = [
    sol.calculateScore(instructions = ["jump","add","add","jump","add","jump"], values = [2,1,3,1,-2,-3]),
    sol.maximumPossibleSize(nums = [4,2,5,3,5]),
    sol.maximumPossibleSize(nums = [1,2,3]),
    sol.maximumPossibleSize(nums = [1,1,1]),
]
for r in result:
    print(r)
