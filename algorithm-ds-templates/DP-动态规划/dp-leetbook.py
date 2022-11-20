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
[动态规划精讲（一）](https://leetcode.cn/leetbook/detail/dynamic-programming-1-plus/)

题目列表
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
打家劫舍系列
    打家劫舍
    打家劫舍 II
    删除与获得点数
    3n 块披萨
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

    """ 0354. 俄罗斯套娃信封问题 #hard #题型 需要 (w,h) 同时满足严格小关系才可以套娃, 问最多层数. 限制: n 1e5
思路1: 对于 (w,-h) 进行排序, 然后在得到 h 序列上求 LIS 即可
    原因: 对于相同的w, 逆序排序使得不会出现相同w的问题. 
"""
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        return self.lengthOfLIS([x[1] for x in envelopes])


    """ 0053. 最大子数组和 #题型 最大子序和
DP: f[i] = max(f[i-1], 0) + nums[i], 表示以i结尾的子数组最大.
细节: 注意子数组需要是非空的
"""
    def maxSubArray(self, nums: List[int]) -> int:
        ans = nums[0]
        s = nums[0]
        for x in nums[1:]:
            s = max(s+x, x)
            ans = max(ans, s)
        return ans
    """ 0152. 乘积最大子组数 #medium #题型 注意可能有负数和零!
启发: 不需要考虑数字的符号, 只用两个变量来记录可能得到的 mx, mn 即可. 
"""
    def maxProduct(self, nums: List[int]) -> int:
        ans = nums[0]
        mx = mn = nums[0]
        for x in nums[1:]:
            mx, mn = max(x, x*mx, x*mn), min(x, x*mx, x*mn)
            ans = max(ans, mx)
        return ans
    """ 0918. 环形子数组的最大和 #medium #题型
思路1: 分两部分考虑, 子数组是中间的连续部分, 或者两头(等价求最小连续子数组). 
    细节: 注意数组全负的情况
[官答](https://leetcode.cn/problems/maximum-sum-circular-subarray/solution/huan-xing-zi-shu-zu-de-zui-da-he-by-leetcode/) 给出了多种思路. 
"""
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        MX = mx = nums[0]
        MN = mn = nums[0]
        for x in nums[1:]:
            mx = max(mx+x, x)
            MX = max(MX, mx)
            mn = min(mn+x, x)
            MN = min(MN, mn)
        # 注意边界! 当nums全负的时候, sum(nums)-MN=0 不合法!
        return max(MX, sum(nums)-MN) if MX>0 else MX
    """ 面试题 17.24. 最大子矩阵 #hard #题型 #review 找到和最大的子矩阵 限制: n 200
DP: f[i,j,x] 表示以 (i,j) 为右下角的底边长x的最大和. 
    递推: `f[i,j,x] = max{ f[i-1,j,x], 0 } + sum(matrix[i][j-x+1:j+1])` 复杂度 O(n^3)
    细节: 这题要返回子矩阵坐标, 需要记录高度信息
https://leetcode.cn/problems/max-submatrix-lcci/
关联: 0363. 矩形区域不超过 K 的最大数值和 #hard. 下面给出来的思路简单得多!
"""
    def getMaxMatrix(self, matrix: List[List[int]]) -> List[int]:
        ans = (0,0,0,0)     # 当前最大值的两个点坐标
        mx = matrix[0][0]   # 当前最大值
        m,n = len(matrix), len(matrix[0])
        # 初始化不能用 0!
        #  DP记录 (最大和, 矩阵高度-1)
        f = [[(-inf,0)]*(i+1) for i in range(n)]
        for i,row in enumerate(matrix):
            nf = [[(-inf,0)]*(i+1) for i in range(n)]
            for j in range(n):
                acc = 0
                for x in range(j+1):    # 注意这里一共 j+1 个底边长度
                    acc += row[j-x]
                    if f[j][x][0] > 0:
                        nf[j][x] = (f[j][x][0]+acc, f[j][x][1]+1)
                    else:
                        nf[j][x] = (acc, 0)
                    if nf[j][x][0] > mx:
                        mx = nf[j][x][0]
                        ans = (i-nf[j][x][1], j-x, i, j)
            f = nf
        return ans
    """ 0363. 矩形区域不超过 K 的最大数值和 #hard #题型 找到子矩阵中, 不超过k的最大子矩阵和 限制: n 100
子问题: 一维情况下, 如何求不超过k的子数组和? 
    对于前缀数组, 要求 acc[r+1]-acc[l] <= k. 
    也即, 对于当前的前缀 s=acc[r+1], 需要找到最小的比 >=s-k 的acc. 因此可以对所有的前缀排序之后 bisect_left, 用到 #有序数组
如何解决原问题? 枚举矩阵上下边界 up, down, 然后就可以看成一维的情况.
复杂度: 枚举上下边界 O(m^2), 对于长n的一维数组计算的复杂度 O(nlogn), 因此 O(m^2 nlogn)
[官答](https://leetcode.cn/problems/max-sum-of-rectangle-no-larger-than-k/solution/ju-xing-qu-yu-bu-chao-guo-k-de-zui-da-sh-70q2/)
关联: 面试题 17.24. 最大子矩阵
"""
    def maxSumSubmatrix(self, matrix: List[List[int]], k: int) -> int:
        from sortedcontainers import SortedList
        m,n = len(matrix), len(matrix[0])
        ans = -inf
        for up in range(m):
            tot = [0] * n
            for down in range(up, m):
                for j in range(n): tot[j] += matrix[down][j]
                acc = 0
                accs = SortedList([0])
                for x in tot:
                    acc += x
                    idx = accs.bisect_left(acc-k)
                    if idx < len(accs): ans = max(ans, acc-accs[idx])
                    accs.add(acc)
        return ans
    
    
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
    # sol.lengthOfLIS(nums = [10,9,2,5,3,7,101,18]),
    # sol.findNumberOfLIS([1,3,5,4,7]),
    # sol.findNumberOfLIS([1,2,4,3,5,4,7,2]),
    # sol.maxEnvelopes(envelopes = [[5,4],[6,4],[6,7],[2,3]])
    
    # sol.maxSubArray(nums = [-2,1,-3,4,-1,2,1,-5,4]),
    # sol.maxProduct(nums = [2,3,-2,4]),
    # sol.maxSubarraySumCircular(nums = [5,-3,5]),
    # sol.maxSubarraySumCircular([-3,-2,-3]),
    # sol.getMaxMatrix(matrix = [[1,0,1],[0,-2,3]]),
    # sol.getMaxMatrix([[9,-8,1,3,-2],[-3,7,6,-2,4],[6,-4,-4,8,-7]]),
    # sol.maxSumSubmatrix(matrix = [[1,0,1],[0,-2,3]], k = 2),
    
    # sol.rob([2,7,9,3,1]),
    # sol.rob(nums = [2,3,2]),
    # sol.deleteAndEarn(nums = [2,2,3,3,3,4]),
    sol.maxSizeSlices(slices = [8,9,8,6,1,1]),
]
for r in result:
    print(r)
