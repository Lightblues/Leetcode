from typing import *
from heapq import heappop, heappush
# from easonsi.util.leetcode import *

# def testClass(inputs):
#     # 用于测试 LeetCode 的类输入
#     s_res = [None] # 第一个初始化类, 一般没有返回
#     methods, args = [eval(l) for l in inputs.split('\n')]
#     class_name = eval(methods[0])(*args[0])
#     for method_name, arg in list(zip(methods, args))[1:]:
#         r = (getattr(class_name, method_name)(*arg))
#         s_res.append(r)
#     return s_res

""" 
https://leetcode.cn/contest/biweekly-contest-139
T3 前后缀分解, 细节相当多, 值得反思
T4 俄罗斯套娃信封问题 的变体, 需要思维量

Easonsi @2025 """
class Solution:
    """ 3285. 找到稳定山的下标 """
    def stableMountains(self, height: List[int], threshold: int) -> List[int]:
        ans = []
        for i in range(1, len(height)):
            if height[i-1] > threshold:
                ans.append(i)
        return ans
    
    """ 3286. 穿越网格图的安全路径 #medium 
经典 #Dijkstra 的题目, 
但这里边权是 0/1, 因此可以用  0-1 BFS!
    """
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        m,n = len(grid), len(grid[0])
        vis = [(0,0)]
        frontier = [(grid[0][0], 0,0)]
        while frontier:
            d,i,j = heappop(frontier)
            for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                if i==m-1 and j==n-1:  # reach the target!
                    return True
                x,y = i+di, j+dj
                if x<0 or x>=m or y<0 or y>=n: continue
                if (x,y) in vis: continue
                v = d + grid[x][y]
                if v >= health: continue
                vis.append((x,y))
                heappush(frontier, (v, x, y))
        return False
    
    """ 3287. 求出数组中最大序列值 #hard 长度为2k的子序列, 得分为前一半OR和后一半OR 之后, 两个数字XOR的结果. 求最大得分
限制: n 400; x 2^7
思路1: #前后缀分解 #题型
    问题分解: 对于长n的序列在一个固定位置划分为左右两部分, 然后统计两侧分别可以构成的所有长k的子序列的OR的所有可能!
    如何统计 "长k的子序列的OR的所有可能"? #DP 记 f[i,j,k] 表示在 0...i 元素中选j个, OR值为k是否可能 #0-1背包
        转移: 
            不选第 i 个元素: f[i,j,k] = f[i-1,j,k]
            选第 i 个元素: 若 f[i-1,j-1,k] = True, 则 f[i,j,k|nums[i]] = True ( #刷表法 )
        初始: f[0,0,0] = True
        优化: 中间的维度可以cache删除!
        复杂度: O(nkU), 这里U是OR的可能范围 2^7
    复杂度: O(nkU + nU^2) 后面的是枚举分割点和合并 XOR结果
"""
    def maxValue(self, nums: List[int], k: int) -> int:
        from itertools import product
        n = len(nums)
        
        prefix = [None] * n  # 保存前i个元素中长k的子序列的OR的所有可能
        f = [set() for _ in range(k+1)]  # 枚举到现在位置, 长j的子序列的OR的所有可能
        f[0].add(0)
        for i,v in enumerate(nums):
            for j in range(k-1, -1, -1):  # 注意从后往前更新!
                f[j+1].update(x | v for x in f[j])
            prefix[i] = f[k].copy()
        
        suffix = [None] * n
        f = [set() for _ in range(k+1)]
        f[0].add(0)
        for i in range(n-1, -1, -1):
            v = nums[i]
            for j in range(k-1, -1, -1):
                f[j+1].update(x | v for x in f[j])
            suffix[i] = f[k].copy()
        
        ans = 0
        for i in range(k-1, n-k):  # 枚举分割点, 左侧极限为 0...k-1; 右侧极限为 n-k...n-1; 因此左分割点范围为 k-1...n-k-1
            ans = max(
                ans, 
                max(a ^ b for a,b in product(prefix[i], suffix[i+1]))
            )
        return ans
    
    """ 3288. 最长上升路径的长度 #hard 给定一组二维坐标点, 和其中一个点, 求一个最长的序列, 包含该点, 同时每个元素 x/y 严格递增
限制: n 1e5
思路1: #排序 + #LIS 最长递增子序列
    注意到, 若没有包含某一点的要求, 就是 [0354. 俄罗斯套娃信封问题] -- 对于x坐标排序!
    如何使得所选子序列严格递增? 在对x排序的基础上增加-y, 也即 (x,-y) 排序
    如何使得必然包含点 k=(kx,ky)? 我们可以仅仅保留 (x<kx and y<ky) or (x>kx and y>ky) 的点!
    如何计算 LIS? 可以 #DP + #二分, 用 g[l] 表示长度为 l 的子序列的最小结尾元素, 复杂度 O(n logn)
from [ling](https://leetcode.cn/problems/length-of-the-longest-increasing-path/solutions/2917590/pai-xu-lispythonjavacgo-by-endlesscheng-803g/)
"""
    def maxPathLength(self, coordinates: List[List[int]], k: int) -> int:
        from bisect import bisect_left
        kx,ky = coordinates[k]
        coordinates = [(x,y) for x,y in coordinates if (x<kx and y<ky) or (x>kx and y>ky)]
        coordinates.sort(key=lambda x: (x[0], -x[1]))
        
        # LIS: dp + binary search
        g = []
        for x,y in coordinates:
            j = bisect_left(g, y)
            if j == len(g): g.append(y)
            else: g[j] = y
        return len(g) + 1  # add k
    
sol = Solution()
result = [
    # sol.findSafeWalk(grid = [[1,1,1],[1,0,1],[1,1,1]], health = 5),
    # sol.findSafeWalk(grid = [[0,1,1,0,0,0],[1,0,1,0,0,0],[0,1,1,1,0,1],[0,0,1,0,1,0]], health = 3),
    
    sol.maxValue(nums = [4,2,5,6,7], k = 2),
    
    # sol.maxPathLength(coordinates = [[3,1],[2,2],[4,1],[0,0],[5,3]], k = 1),
]
for r in result:
    print(r)
