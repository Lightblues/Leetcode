"""
给定一个可包含重复数字的序列 nums ，按任意顺序 返回所有不重复的全排列。

输入：nums = [1,1,2]
输出：
[[1,1,2],
 [1,2,1],
 [2,1,1]]

---
和上一题的区别在于，这里可能出现重复数字。
为了避免重复，这里简单用了 set 进行删除。
自己实现的 dfs 中间遍历都用了 list/set 的复制，内存开销较大（但题目要求将所有 permutation 记录下来本身内存开销就很大）；
官方实现用了指针，此时需要👇注释掉的排序行，然后在挑选数字的时候，避免在同一位置放入相同的数字

"""
from typing import List
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        # nums.sort()
        results = []
        permutation = []

        def dfs():
            if not nums:
                results.append(permutation.copy())
                return
            # 避免重复
            for num in set(nums.copy()):
                permutation.append(num)
                nums.remove(num)
                dfs()  # 递归调用
                permutation.pop()
                nums.append(num)  # 再放回去

        dfs()
        return results
# nums = [1,1,2]
nums = [2,2,1,1]
print(Solution().permuteUnique(nums))