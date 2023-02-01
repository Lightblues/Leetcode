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
    """ 0198. 打家劫舍 #medium 要求闯入的房屋不能连续.
DP1: 记 `f[i]` 表示前i个房屋的最优解, 有递推: `f[i] = max{ f[i-2]+nums[i], f[i-1] }`. 注意只用一个值即可记录!
DP2: 记 `f[i]` 表示前i个房屋并且偷第i个的最优, 有递推 `f[i] = max{f[...i-2]} + nums[i]`, 前者可以用一个累计最大值来记录. 代码见下
"""
    def rob(self, nums: List[int]) -> int:
        if not nums: return 0
        if len(nums) == 1: return nums[0]
        f = [0] * len(nums)
        f[0], f[1] = nums[0], max(nums[0], nums[1])
        for i in range(2, len(nums)):
            f[i] = max(f[i-2]+nums[i], f[i-1])
        return f[-1]
    """ 0213. 打家劫舍 II #medium 要求闯入的房屋不能连续. 但是首尾相连.
这里的robLine就是上面说的DP2
思路: 考虑两种情况 max(robLine(nums[1:]), robLine(nums[:-1]))
[官答](https://leetcode.cn/problems/house-robber-ii/solution/da-jia-jie-she-ii-by-leetcode-solution-bwja/)
"""
    def rob_2(self, nums: List[int]) -> int:
        def robLine(nums):
            f = [0] * len(nums)
            f[0] = nums[0]
            mx = 0
            for i in range(1, len(nums)):
                f[i] = nums[i] + mx
                mx = max(mx, f[i-1])
            return max(mx, f[-1])
        return max(robLine(nums[1:]), robLine(nums[:-1])) if len(nums) > 1 else nums[0]
    """ 0740. 删除与获得点数 #medium 从数组中取数字x, 则会删除所有的 x-1,x+1, 数字可以重复, 问最大能取多少? 限制: n 2e4; 数字范围 [1,1e4]
思路1: 注意这里的数字范围比较小, 因此可以直接用一个arr记录每个数字可以取得的分数, 相邻元素不能同时取, 转化为 「0198. 打家劫舍」
"""
    def deleteAndEarn(self, nums: List[int]) -> int:
        mx = max(nums)
        arr = [0] * (mx+1)
        for x in nums:
            arr[x] += x
        return self.rob(arr)
    """ 1388. 3n 块披萨 #hard #题型 有环形的数组, 每次你选择一块之后, AB分别取顺/逆时针相邻的那一块, 问最大能取多少? 限制: len(arr) 500
转换: 问题等价于, 在3n个数字中取n个不相邻的数字, 使得和最大!
    可以用 #归纳法 证明, 见 [官答](https://leetcode.cn/problems/pizza-with-3n-slices/solution/3n-kuai-pi-sa-by-leetcode-solution/)
DP1: 不考虑环形. 记 `f[i,j]` 表示前i个中取j个最优解. 递推 `f[i,j] = max{ f[i-1,j], f[i-2,j-1]+arr[i] }` 
"""
    def maxSizeSlices(self, slices: List[int]) -> int:
        n = len(slices)//3
        def robLine(arr):
            f = [[0]*(n+1) for _ in range(len(arr)+1)]
            f[1][1] = arr[0]
            for i in range(2, len(arr)+1):
                for j in range(1, n+1):
                    f[i][j] = max(f[i-1][j], f[i-2][j-1]+arr[i-1])
            return f[-1][-1]
        return max(robLine(slices[1:]), robLine(slices[:-1]))
    
    


    
sol = Solution()
result = [
    # sol.rob([2,7,9,3,1]),
    # sol.rob(nums = [2,3,2]),
    # sol.deleteAndEarn(nums = [2,2,3,3,3,4]),
    sol.maxSizeSlices(slices = [8,9,8,6,1,1]),
]
for r in result:
    print(r)
