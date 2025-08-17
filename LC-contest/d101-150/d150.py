from typing import *

""" 
https://leetcode.cn/contest/biweekly-contest-150
Easonsi @2025 """
class Solution:
    """ 3452. 好数字之和 """
    def sumOfGoodNumbers(self, nums: List[int], k: int) -> int:
        acc = 0
        for i,x in enumerate(nums):
            if i-k>=0 and x<=nums[i-k]: continue
            if i+k<len(nums) and x<=nums[i+k]: continue
            acc += x
        return acc

    """ 3453. 分割正方形 I #medium 给定一组二维坐标里的正方形, 问最小的平行x轴的线, 使得直线上下分割得到的面结之和相等.
限制: n 5e4; 总面积 1e12. 答案精确到 1e-5
    """
    def separateSquares(self, squares: List[List[int]]) -> float:
        total_s, mn, mx = 0, 0, 0
        for x,y,l in squares:
            total_s += l*l
            mn = min(mn, y)
            mx = max(mx, y+l)
        # 
        def check(yline):
            s = 0
            for x,y,l in squares:
                if y+l <= yline: s += l*l

sol = Solution()
result = [
    
]
for r in result:
    print(r)