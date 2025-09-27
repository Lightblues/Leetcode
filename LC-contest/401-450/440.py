from typing import *
import heapq

""" 
https://leetcode.cn/contest/weekly-contest-440
Easonsi @2025 """
class Solution:
    """ 3477. 水果成篮 II """
    def numOfUnplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        ans = 0
        for f in fruits:
            for i,b in enumerate(baskets):
                if b >= f:
                    baskets[i] = -1
                    break
            else:
                ans += 1
        return ans
    
    """ 3478. 选出和最大的 K 个元素 #medium  """
    def findMaxSum(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        nums = [(a,b) for a,b in zip(nums1, nums2)]
        nums.sort(key=lambda x: x[0])
        ans = []; acc = 0; h = []
        pre = -1; buffer = []
        for a,b in nums:
            if a == pre:
                buffer.append(b)
                ans.append(acc)
            else:
                for x in buffer:
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
