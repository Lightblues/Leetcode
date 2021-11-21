"""
给你一个整数数组 nums ，其中可能包含重复元素，请你返回该数组所有可能的子集（幂集）。

解集 不能 包含重复的子集。返回的解集中，子集可以按 任意顺序 排列。

输入：nums = [1,2,2]
输出：[[],[1],[1,2],[1,2,2],[2],[2,2]]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/subsets-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

重复的过滤策略：
首先，排序!
然后基于 78 题的两种思路：1. 枚举；2. 回溯

过滤的条件：对于排好序的，i位置和i-1位置元素相同，且i-1没有选入，则可以pass（因为之前因此选过了i-1了）
"""

from typing import List
class Solution:
    # 1 枚举
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums = sorted(nums)
        _len = len(nums)
        res = []
        for mask in range(2**_len):
            now = []
            flag = True
            for _index in range(_len):
                index = 2**_index
                if mask & index:
                    if _index>0 and nums[_index-1]==nums[_index] and not mask&(2**(_index-1)):      # 过滤
                        flag = False
                        break
                    now.append(nums[_index])
            if flag:
                res.append(now)
        return(res)
    # 2 回溯
    def subsetsWithDup2(self, nums):
        """这里使用一个数组 now 维护目前选入的元素，注意到 pop！
        """
        nums.sort()
        _len = len(nums)
        res = []
        now = []
        def backtrack(index, flag):        # flag 标志之前的元素是否选了
            if index==_len:
                res.append(now.copy())      # copy()
                return
            # 以下分 1. 没选index位置；2. 选了index位置 进行backtrack
            backtrack(index+1, flag=False)
            now.append(nums[index])
            if index>0 and nums[index-1]==nums[index] and flag==False:      # 过滤
                now.pop()       # 注意这里也要pop
                return
            backtrack(index+1, flag=True)
            now.pop()
        backtrack(0, False)
        return res



print(Solution().subsetsWithDup([1,2,2]))