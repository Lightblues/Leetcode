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
https://leetcode.cn/contest/weekly-contest-403

T4 的变量debug了好久orz 大模拟/枚举 很久没写了, 有点意思
Easonsi @2023 """
class Solution:
    """ 3194. 最小元素和最大元素的最小平均值 """
    def minimumAverage(self, nums: List[int]) -> float:
        nums.sort()
        i,j = 0,len(nums)-1
        mn = inf
        while i<j:
            mn = min(mn, (nums[i]+nums[j])/2)
            i += 1
            j -= 1
        return mn
    
    """ 3195. 包含所有 1 的最小矩形面积 I """
    def minimumArea(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        l,r = n-1,0
        t,b = m-1,0
        for i,row in enumerate(grid):
            for j,x in enumerate(row):
                if x==1:
                    l = min(l,j)
                    r = max(r,j)
                    t = min(t,i)
                    b = max(b,i)
        return (r-l+1)*(b-t+1)
    
    """ 3196. 最大化子数组的总成本 """
    def maximumTotalCost(self, nums: List[int]) -> int:
        n = len(nums)
        l,r = nums[0], nums[0]
        for i in range(1,n):
            x = nums[i]
            l, r = max(l,r)+x, l-x
        return max(l,r)
    
    """ 3197. 包含所有 1 的最小矩形面积 II # hard 用3个非空矩阵来覆盖区间内所有的值为1的格子, 要求最小面积
限制: n,m 30 这题居然有8分! 
思路1: #暴力 #枚举
    直接分割成三个部分, 下面的 f1,f2 分别解决两个矩阵的问题. 
见 [ling](https://leetcode.cn/problems/find-the-minimum-area-to-cover-all-ones-ii/solutions/2819357/mei-ju-pythonjavacgo-by-endlesscheng-uu5p/)
"""
    def minimumSum(self, grid: List[List[int]]) -> int:
        @lru_cache(None)
        def f1(b,t,l,r):
            ll,rr = r,l
            tt,bb = b,t
            for i in range(b,t+1):
                for j in range(l,r+1):
                    if grid[i][j] == 1:
                        rr = max(rr,j)
                        ll = min(ll,j)
                        tt = max(tt,i)
                        bb = min(bb,i)
            res = (rr-ll+1)*(tt-bb+1)
            return max(res, 1)
        @lru_cache(None)
        def f2(b,t,l,r):
            ans = inf
            if r > l:
                for i in range(l,r):
                    ans = min(ans, f1(b,t,l,i)+f1(b,t,i+1,r))
            if t > b:
                for i in range(b,t):
                    ans = min(ans, f1(b,i,l,r)+f1(i+1,t,l,r))
            return ans
        m,n = len(grid), len(grid[0])
        ans = inf
        if n > 1:
            for i in range(0, n-1):
                ans = min(ans, f1(0,m-1,0,i)+f2(0,m-1,i+1,n-1))
                ans = min(ans, f1(0,m-1,i+1,n-1)+f2(0,m-1,0,i))
        if m > 1:
            for i in range(0, m-1):
                ans = min(ans, f1(0,i,0,n-1)+f2(i+1,m-1,0,n-1))
                ans = min(ans, f1(i+1,m-1,0,n-1)+f2(0,i,0,n-1))
        return ans


sol = Solution()
result = [
    # sol.minimumAverage(nums = [7,8,3,4,15,13,4,1]),
    # sol.minimumArea(grid = [[0,1,0],[1,0,1]]),
    # sol.maximumTotalCost(nums = [1,-2,3,4]),
    # sol.maximumTotalCost(nums = [1,-1,1,-1]),
    sol.minimumSum( grid = [[1,0,1],[1,1,1]]),
    sol.minimumSum( grid = [[1,0,1,0],[0,1,0,1]]),
    sol.minimumSum([[0,1],[1,1]]),
]
for r in result:
    print(r)
