"""
给定一个非负整数数组 nums ，你最初位于数组的 第一个下标 。
数组中的每个元素代表你在该位置可以跳跃的最大长度。
判断你是否能够到达最后一个下标。


输入：nums = [2,3,1,1,4]
输出：true
解释：可以先跳 1 步，从下标 0 到达下标 1, 然后再从下标 1 跳 3 步到达最后一个下标。

输入：nums = [3,2,1,0,4]
输出：false
解释：无论怎样，总会到达下标为 3 的位置。但该下标的最大跳跃长度是 0 ， 所以永远不可能到达最后一个下标。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/jump-game
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


from typing import List
class Solution:
    def canJump0(self, nums: List[int]) -> int:
        # DFS，贪心。还是超时了！！
        n = len(nums)
        target = n-1
        def dfs(i):
            num = nums[i]
            if num >= target-i:
                return True
            for hop in range(num, 0, -1):
                res = dfs(i+hop)
                if res:
                    return res
                # 否则，说明检索失败
            return False
        res = dfs(0)
        return res

    def canJump(self, nums):
        n = len(nums)
        curr = 0

        while curr < n - 1:
            max_hop_two = 0
            nex = 0
            if nums[curr] == 0:
                return False
            for hop in range(nums[curr], 0, -1):
                if hop + curr >= n - 1:
                    return True
                if nums[curr + hop] + hop > max_hop_two:
                    max_hop_two = nums[curr + hop] + hop
                    nex = hop
            curr = curr + nex
        return True     # 还可能 [0]

    def canJump2(self, nums: List[int]) -> bool:
        n, rightmost = len(nums), 0
        for i in range(n):
            if i <= rightmost:
                rightmost = max(rightmost, i + nums[i])
                if rightmost >= n - 1:
                    return True
        return False



# nums = [2,3,1,1,4]
nums = [3,2,1,0,4]
# nums = [2,0,6,9,8,4,5,0,8,9,1,2,9,6,8,8,0,6,3,1,2,2,1,2,6,5,3,1,2,2,6,4,2,4,3,0,0,0,3,8,2,4,0,1,2,0,1,4,6,5,8,0,7,9,3,4,6,6,5,8,9,3,4,3,7,0,4,9,0,9,8,4,3,0,7,7,1,9,1,9,4,9,0,1,9,5,7,7,1,5,8,2,8,2,6,8,2,2,7,5,1,7,9,6]
print(Solution().canJump(nums))