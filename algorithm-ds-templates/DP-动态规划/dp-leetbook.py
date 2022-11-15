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

LIS: Longest increasing subsequence (最长递增子序列) 
    最长上升子序列
    最长递增子序列的个数
    俄罗斯套娃信封问题 —— LIS
最大子数组和
    最大子序和
    乘积最大子数组
    环形子数组的最大和 —— 环形数组的处理
    最大子矩阵 —— 思路类似一维的最大子数组和
    矩形区域不超过 K 的最大数值和 —— 在上一题基础上加了一个 K
@2022 """
class Solution:
    """ 0300. 最长上升子序列 """
    def lengthOfLIS(self, nums: List[int]) -> int:
        # 基本DP, 复杂度 O(n^2)
        n = len(nums)
        dp = [1] * n
        for i in range(n):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
    def lengthOfLIS(self, nums: List[int]) -> int:
        # 复杂度 O(n logn)
        f = []   # 长度为 i的上升子序列的最小结尾
        for i,x in enumerate(nums):
            idx = bisect_left(f, x)
            if idx==len(f): f.append(x)
            else: f[idx] = x
        return bisect_left(f, inf)
    
    """ 0673. 最长递增子序列的个数 #题型 #hard
思路1: 基本DP, 复杂度 O(n^2)
    对于每一个位置 nums[i], 我们记录以该元素结尾的最长长度和数量 (length, cnt). 
    递推: 对于当前元素j, 枚举所有满足 i<j, nums[i]<nums[j] 的位置, 更新DP值. 
思路2: 拓展 0300. 为此, 我们需要记录更多的信息, 参见官答. 
[官答](https://leetcode.cn/problems/number-of-longest-increasing-subsequence/solution/zui-chang-di-zeng-zi-xu-lie-de-ge-shu-by-w12f/)
"""
    def findNumberOfLIS(self, nums: List[int]) -> int:
        # O(n^2)
        n = len(nums)
        length = [0] * n
        cnt = [1] * n
        for j,x in enumerate(nums):
            for i in range(j):
                if nums[i]<x:
                    if length[i] >= length[j]:
                        length[j] = length[i] + 1
                        cnt[j] = cnt[i]
                    elif length[i] == length[j]-1:
                        cnt[j] += cnt[i]
        mxlen = max(length)
        return sum(c for l,c in zip(length, cnt) if l==mxlen)

    """ 俄罗斯套娃信封问题 需要 (w,h) 同时满足严格小关系才可以套娃, 问最多层数. 
思路1: 对于 (w,-h) 进行排序, 然后在得到 h 序列上求 LIS 即可
    原因: 对于相同的w, 逆序排序使得不会出现相同w的问题. 
"""
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        return self.lengthOfLIS([x[1] for x in envelopes])


    """ 最大子序和 """
    def maxSubArray(self, nums: List[int]) -> int:
        ans = nums[0]
        s = 0
        for x in nums:
            s += x
            ans = max(ans , s)
            s = max(s, 0)
        return ans

sol = Solution()
result = [
    # sol.lengthOfLIS(nums = [10,9,2,5,3,7,101,18]),
    # sol.findNumberOfLIS([1,3,5,4,7]),
    # sol.findNumberOfLIS([1,2,4,3,5,4,7,2]),
    # sol.maxEnvelopes(envelopes = [[5,4],[6,4],[6,7],[2,3]])
    
    sol.maxSubArray(nums = [-2,1,-3,4,-1,2,1,-5,4]),
]
for r in result:
    print(r)
