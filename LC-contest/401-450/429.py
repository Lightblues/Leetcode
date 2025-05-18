from math import ceil
from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-429
Easonsi @2024 """
class Solution:
    """ 3396. 使数组元素互不相同所需的最少操作次数 """
    def minimumOperations(self, nums: List[int]) -> int:
        n = len(nums)
        s = set()
        for i in range(n-1,-1,-1):
            if nums[i] in s:
                return ceil((i+1)/3)
            s.add(nums[i])
        return 0
    
    """ 3397. 执行操作后不同元素的最大数量 #medium 可以对于每个元素增加 [-k,k] 范围内的整数, 问最终数组中不同元素的最大数量 """
    def maxDistinctElements(self, nums: List[int], k: int) -> int:
        nums.sort()
        mx = -inf; cnt = 0
        for x in nums:
            if x-k > mx:  # 贪心, 每次选尽可能小的数字
                mx = x-k
                cnt += 1
            elif x+k > mx:
                mx += 1
                cnt += 1
        return cnt

    """ 3398. 字符相同的最短子字符串 I """
    
    

    
sol = Solution()
result = [
    # sol.minimumOperations(nums = [1,2,3,4,2,3,3,5,7]),
    sol.maxDistinctElements(nums = [4,4,4,4], k = 1),
]
for r in result:
    print(r)
