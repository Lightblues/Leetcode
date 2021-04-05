"""
给定一个 没有重复 数字的序列，返回其所有可能的全排列。

输入: [1,2,3]
输出:
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/permutations
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        results = []
        permutation = []
        def dfs():
            if not nums:
                results.append(permutation.copy())
                return
            for num in nums.copy():
                permutation.append(num)
                nums.remove(num)
                dfs()   # 递归调用
                permutation.pop()
                nums.append(num)    # 再放回去
        dfs()
        return results

nums = [1,2,3]
print(Solution().permute(nums))