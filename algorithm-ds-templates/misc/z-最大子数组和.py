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
0053. 最大子数组和

环形上的最大子数组和-力扣 0918
最大子数组乘积-力扣 0152
最大子矩阵和-面试题17.24
带大小限制的最大子矩阵和-力扣 0363
增删改后的最大子数组和-力扣1191、力扣1186
子数组和的绝对值的最大值-力扣1749
可以修改正负号时的子数组和的绝对值的最大值-LCP65

潮汐 [最大子数组和的三种解法](https://chengzhaoxi.xyz/8501.html)

带长度限制的最大子数组和 [潮汐](https://chengzhaoxi.xyz/f1d4b382.html)
思路1: 就是 前缀和+

Easonsi @2023 """
class Solution:
    """ 0053. 最大子数组和 #题型
思路1: #DP f[i] = max(f[i-1], 0) + nums[i], 表示以i结尾的子数组最大.
    细节: 注意子数组需要是非空的
思路2: #前缀和 + #单调队列
    求出acc之后, 对于每个j, 枚举匹配的i, 使得acc[j]-acc[i]最大
    直接记录最小的acc即可, 或者说是单调队列
思路3: #分治
潮汐 [最大子数组和的三种解法](https://chengzhaoxi.xyz/8501.html)
    """
    def maxSubArray(self, nums: List[int]) -> int:
        # 思路1: #DP f[i] = max(f[i-1], 0) + nums[i]
        ans = nums[0]
        s = nums[0]
        for x in nums[1:]:
            s = max(s+x, x)
            ans = max(ans, s)
        return ans
    
    def maxSubArray(self, nums: List[int]) -> int:
        # 
        acc = list(accumulate(nums))
        mnAcc = 0
        ans = nums[0]
        for i,x in enumerate(nums):
            ans = max(ans, acc[i]-mnAcc)
            mnAcc = min(mnAcc, acc[i])
        return ans
    
    
    

    
sol = Solution()
result = [
    sol.maxSubArray(nums = [-2,1,-3,4,-1,2,1,-5,4]),
]
for r in result:
    print(r)
