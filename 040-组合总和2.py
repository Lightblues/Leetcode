"""
和上一题的区别是 candidates 中的数字可能重复，但只能用一次了

输入: candidates = [10,1,2,7,6,1,5], target = 8,
所求解集为:
[
  [1, 7],
  [1, 2, 5],
  [2, 6],
  [1, 1, 6]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/combination-sum-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        # candidates.sort()
        # results = []
        # combination = []

        # 试图记录上一个加入的元素来避免，重复，但也会出现问题，例如 [6,1,1]=8 这样的就找不到了
        # def dfs(i, remainder, pre=None):
        #     if i<0:
        #         return
        #     num = candidates[i]
        #     if num<=remainder:
        #         new_remainder = remainder-num
        #         combination.append(num)
        #         if new_remainder==0:
        #             if num != pre:
        #                 results.append(combination.copy())  # 注意这里一定要用 copy
        #         else:
        #             dfs(i-1, new_remainder, pre=num)
        #         combination.pop()
        #     dfs(i-1, remainder, pre=num)
        #
        # dfs(len(candidates)-1, target)
        # return results

        from collections import Counter
        sorted_nums = sorted(Counter(candidates).items())
        # 记录了(num, count)元组

        combination = {}
        results = []

        def record():
            results.append([k for k, v in combination.items() for _ in range(v)])

        def backtrace(i, remains):
            if i == -1:
                return
            num, count = sorted_nums[i]
            quiotient, _ = divmod(remains, num)

            for q in range(min(quiotient, count), -1, -1):
                new_remains = remains - q * num
                combination[num] = q
                if new_remains == 0:
                    record()
                else:
                    backtrace(i - 1, new_remains)

        backtrace(len(sorted_nums) - 1, target)
        return results



candidates = [10,1,2,7,6,1,5]; target = 8
print(Solution().combinationSum2(candidates, target))