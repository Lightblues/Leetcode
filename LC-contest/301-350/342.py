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
https://leetcode.cn/contest/weekly-contest-342


Easonsi @2023 """
class Solution:
    """ 6387. 计算列车到站时间 """
    
    """ 6391. 倍数求和 求 [1,n] 范围内能被 3,5,7 整除的所有整数之和 
    限制: n 1e3"""
    def sumOfMultiples(self, n: int) -> int:
        ans = 0
        for i in range(1,n+1):
            if i%3==0 or i%5==0 or i%7==0: ans += i
        return ans
    
    """ 6390. 滑动子数组的美丽值 对于长度为k的滑窗, 求其中第 x 小的数
限制: n 1e5; vals [-50,50]
思路1: 考虑到数据的范围, 转化为 [0,100] 之间, 分桶计数
    """
    def getSubarrayBeauty(self, nums: List[int], k: int, x: int) -> List[int]:
        cnt = [0] * 101
        for xx in nums[:k]: cnt[xx+50] += 1
        def get_x(cnt, x):
            for i in range(101):
                x -= cnt[i]
                if x<=0: return i-50 if i-50<0 else 0
        ans = [get_x(cnt, x)]
        for i in range(k, len(nums)):
            cnt[nums[i-k]+50] -= 1
            cnt[nums[i]+50] += 1
            ans.append(get_x(cnt, x))
        return ans

    """ 6392. 使数组所有元素变成 1 的最少操作次数 #medium
对于数组, 一次操作可以将相邻两个数字求最大公约数, 替换掉其中某个数字. 问最小操作多少次. 
限制: n 50; val 1e5
思路1: #规律
    注意, 如果有1的话, 答案就是 n - nums.count(1)
    如果连续的l个数字可以使得 gcd==1, 得到一个1之后剩余下根据这个1来继续
    """

    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        if 1 in nums: return n - nums.count(1)
        for mnL in range(2, n+1):
            for l in range(0, n-mnL+1):
                if math.gcd(*nums[l:l+mnL]) == 1: 
                    return n + mnL-2
        return -1

sol = Solution()
result = [
    sol.getSubarrayBeauty(nums = [-3,1,2,-3,0,-3], k = 2, x = 1),
    sol.getSubarrayBeauty(nums = [1,-1,-3,-2,3], k = 3, x = 2),
    # sol.minOperations(nums = [2,6,3,4]),
    # sol.minOperations(nums = [2,10,6,14]),


]
for r in result:
    print(r)
