from typing import List
from collections import defaultdict, deque
import heapq
import random

class Solution:
    """ 128. 最长连续序列 """
    def longestConsecutive(self, nums: List[int]) -> int:
        nums = set(nums)
        currL, maxL = 0, 0
        for i in nums:
            if i-1 not in nums:
                currL = 1
                while i+1 in nums:
                    i += 1
                    currL += 1
                maxL = max(maxL, currL)
        return maxL


sol = Solution()
results = [
    sol.longestConsecutive([100,4,200,1,3,2]),
    # sol.findAllPeople(4, [[3,1,3],[1,2,2],[0,3,3]], 3),
    # sol.findAllPeople2(6, [[1,2,5],[2,3,8],[1,5,10]], 1),
    # sol.findAllPeople2(4, [[3,1,3],[1,2,2],[0,3,3]], 3),
    

]
for r in results:
    print(r)

