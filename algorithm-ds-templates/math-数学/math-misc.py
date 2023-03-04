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
Easonsi @2023 """
class Solution:
    """ 0041. 缺失的第一个正数 #hard 一个正数数组, 要求在 O(n) 范围内, 常数空间内找到缺失的最小正数.
分析: 
    若利用 #哈希表, 则空间是 O(n) 
    若枚举 1...n 检查, 时间是 O(n^2) 
    「真正」满足时间复杂度为 O(N) 且空间复杂度为 O(1) 的算法是不存在的
思路1: 修改数组来记录状态! #标记
    我们如何利用原始数组来额外记录一些信息? 答案的范围是 [1,n] 而我们正好有长为n的数组
    我们考虑修改原始数组! 先去除所有负数; 再遍历一遍, 若出现范围内的x, 则将 arr[x-1] 取负数, 标记出现过这个数字!
思路2: #置换 来「还原」有序数组
    对于在 [1,n] 范围内的数字x, 我们尝试将其放到应该在的x-1位置上; 
        对这个被换出现的数字, 若其仍在范围内, 继续! 
        注意死循环! x=arr[x-1], 需要手动终止
    然后, 遍历一遍即可找到
[官答](https://leetcode.cn/problems/first-missing-positive/solution/que-shi-de-di-yi-ge-zheng-shu-by-leetcode-solution/)
"""
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            if nums[i]<=0: 
                nums[i] = n+1
        for i in range(n):
            x = abs(nums[i])        # 注意之前标记过可能为 -
            if 0<x<=n:
                nums[x-1] = -abs(nums[x-1])
        for i in range(n):
            if nums[i]>0:
                return i+1
        # 注意别漏了
        return n+1
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            while 0<nums[i]<=n and nums[nums[i]-1]!=nums[i]:
                # 注意死循环! x=arr[x-1], 需要手动终止
                x = nums[i]
                nums[i], nums[x-1] = nums[x-1], nums[i] # 交换! 这是最省事的方法
        for i in range(n):
            if nums[i]!=i+1:
                return i+1
        return n+1
    
    
    

    
sol = Solution()
result = [
    # sol.firstMissingPositive(nums = [3,4,-1,1]),
    sol.firstMissingPositive([3,4,-1,1]),
]
for r in result:
    print(r)
