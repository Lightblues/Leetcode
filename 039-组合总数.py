"""
给定一个无重复元素的数组 candidates和一个目标数 target ，找出 candidates 中所有可以使数字和为 target的组合。
candidates 中的数字可以无限制重复被选取。

输入：candidates = [2,3,6,7], target = 7,
所求解集为：
[
  [7],
  [2,2,3]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/combination-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
from typing import List
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        combination = {}
        results = []

        def record():
            results.append([k for k, v in combination.items() for _ in range(v)])

        def backtrace(i, remains):
            if i == -1:
                return
            num = candidates[i]
            quiotient, _ = divmod(remains, num)

            for q in range(quiotient, -1, -1):
                new_remains = remains - q*num
                combination[num] = q
                if new_remains == 0:
                    record()
                else:
                    backtrace(i-1, new_remains)

        backtrace(len(candidates)-1, target)
        return results

candidates = [2,3,6,7]; target = 7
print(Solution().combinationSum(candidates, target))