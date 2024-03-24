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
https://leetcode-cn.com/contest/biweekly-contest-120
https://leetcode.cn/circle/discuss/07yq9c/

T1/3 有点意思, 整体比较简单. 
Easonsi @2023 """
class Solution:
    """ 2972. 统计移除递增子数组的数目 II #hard 对于一个数组, 移除其子数组之后若是递增的 (最后变成空的也算), 则称被移除的非空子数组为 移除递增 子数组. 问其数量
思路1: 分别枚举左右边界, #双指针
    """
    def incremovableSubarrayCount(self, nums: List[int]) -> int:
        n = len(nums)
        left = 0
        while left+1 < n and nums[left+1] > nums[left]:
            left += 1
        if left == n-1:
            return (n+1) * n //2
        right = n-1
        while right-1 >= 0 and nums[right-1] < nums[right]:
            right -= 1
        ans = 1 + n - right
        r = right
        for i in range(left+1):
            x = nums[i]
            while r < n and nums[r] <= x:
                r += 1
            ans += n - r + 1
        return ans
    
    """ 2971. 找到最大周长的多边形 """
    def largestPerimeter(self, nums: List[int]) -> int:
        nums.sort()
        acc = list(accumulate(nums, initial=0))
        for i in range(len(nums)-1, 1, -1):
            if nums[i] < acc[i]:
                return nums[i] + acc[i]
        return -1
    
    """ 2973. 树中每个节点放置的金币数目 #hard 一棵树的每个节点都对应了一个cost, 对于每个节点, 1) 子树中节点数量少于3则放置一个金币; 2) 否则放置节点中3个分数乘积最大的数值, 若为负数则放置0
    """
    def placedCoins(self, edges: List[List[int]], cost: List[int]) -> List[int]:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        ans = [0] * n
        def dfs(u, pa=-1):
            """ 递归, 返回最大和最小的三个cost """
            mx = []
            mn = []
            for v in g[u]:
                if v == pa: continue
                mxi, mni = dfs(v, u)
                mx += mxi
                mn += mni
            if cost[u] > 0: mx.append(cost[u])
            else: mn.append(cost[u])
            if len(mx) + len(mn) < 3:
                ans[u] = 1
                return mx, mn
            else:
                mx.sort(reverse=True)
                mn.sort()
                t = 0
                if len(mx) > 2:
                    t = max(t, reduce(mul, mx[:3]))
                if len(mn) >= 2 and len(mx) >= 1:
                    t = max(t, mn[0]*mn[1] * mx[0])
                ans[u] = t
                return mx[:3], mn[:3]
        dfs(0)
        return ans
    
sol = Solution()
result = [
    # sol.incremovableSubarrayCount(nums = [1,2,3,4]),
    # sol.incremovableSubarrayCount([6,5,7,8]),
    # sol.incremovableSubarrayCount([8,7,6,6]),
    # sol.incremovableSubarrayCount([9,9]),

    # sol.largestPerimeter(nums = [5,5,5]),
    # sol.largestPerimeter([5,5,50]),
    # sol.largestPerimeter(nums = [1,12,1,2,5,50,3]),

    sol.placedCoins(edges = [[0,1],[0,2],[0,3],[0,4],[0,5]], cost = [1,2,3,4,5,6]),
    sol.placedCoins(edges = [[0,1],[0,2],[1,3],[1,4],[1,5],[2,6],[2,7],[2,8]], cost = [1,4,2,3,5,7,8,-4,2]),
    sol.placedCoins(edges = [[0,1],[0,2]], cost = [1,2,-2]),
]
for r in result:
    print(r)
