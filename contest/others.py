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


    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        t1 = len(text1)
        t2 = len(text2)
        memo = [[-1] * t2] * t1
        def dp(s1, i, s2, j):
            #这里到底是t1还是t1-1呢？边界条件搞不懂
            # 要看这里的返回条件. 为什么返回? 其实就是走到边界了! (数组越界). 所以这里是 t1
            if i == t1 or j == t2:
                return 0
            else:
                if memo[i][j] != -1:    return memo[i][j]
                else:
                    if s1[i] == s2[j]:
                        memo[i][j] = 1 + dp(s1, i+1, s2, j+1)
                    else:
                        memo[i][j] = max(dp(s1, i+1, s2, j), dp(s1, i, s2, j+1))
                        return memo[i][j]
        res = dp(text1, 0, text2, 0)
        return res
    #报了超时的错误。。不懂是为什么
    #自下而上和自上而下怎么理解

sol = Solution()
results = [
    sol.longestConsecutive([100,4,200,1,3,2]),
    # sol.findAllPeople(4, [[3,1,3],[1,2,2],[0,3,3]], 3),
    # sol.findAllPeople2(6, [[1,2,5],[2,3,8],[1,5,10]], 1),
    # sol.findAllPeople2(4, [[3,1,3],[1,2,2],[0,3,3]], 3),
    

]
for r in results:
    print(r)

