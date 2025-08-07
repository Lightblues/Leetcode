from typing import *
from functools import lru_cache
from collections import defaultdict

""" 
https://leetcode.cn/contest/biweekly-contest-146
Easonsi @2025 """
class Solution:
    """ 3392. 统计符合条件长度为 3 的子数组数目 """
    def countSubarrays(self, nums: List[int]) -> int:
        ans = 0
        for i in range(1, len(nums)-1):
            if (nums[i-1]+nums[i+1])*2 == nums[i]: ans += 1
        return ans
    
    """ 3393. 统计异或值为给定值的路径数目 #medium 在网格中从 (0,0) 到 (m-1,n-1) 的路径, 满足经过的所有数字的 xor == k
限制: m,n 300; k, val 15. 对结果取模
思路1: #DP 
    记 f(i,j,v) 表示到达 (i,j) 且经过的数字的 xor == v 的路径数; 
    状态转移: 只允许往右/往下走
    """
    def countPathsWithXorValue(self, grid: List[List[int]], k: int) -> int:
        MOD = 10**9 + 7
        m, n = len(grid), len(grid[0])
        @lru_cache(None)
        def f(i:int, j:int, v:int) -> int:
            if i==0==j: return int(grid[0][0]==v)
            target = v ^ grid[i][j]
            ans = 0
            if i>0: ans += f(i-1,j,target)
            if j>0: ans += f(i,j-1,target)
            return ans % MOD
        return f(m-1,n-1,k)

    """ 3394. 判断网格图能否被切割成块 #medium 给定二维坐标下的一组矩形, 问能否找到都 水平/垂直 的两条线, 这两条线不经过任何矩形, 且对它们分成3组
限制: 网格范围 n 1e9; 矩形数量 m 1e5
思路1: #差分
    显然, 可以分别考虑 x/y 轴. 每部分通过 #差分 来统计是否有至少两个非重叠区域
    - 如何处理上一个区间右端点和下一个区间左端点重合的情况? e.g. (0,2),(2,3) 因为判断非重叠的方式是 acc==0
        可以讲右端点 -0.5 加空隙
思路2: #排序 即可. 
    ref: 0056. 合并区间
    本题中, 就是合并重叠区间, 从 x/y 轴分别计算合并之后的区间数量是否 >= 3
    [ling](https://leetcode.cn/problems/check-if-grid-can-be-cut-into-sections/solutions/3026888/he-bing-qu-jian-pythonjavacgo-by-endless-dn1g/)
    """
    def checkValidCuts(self, n: int, rectangles: List[List[int]]) -> bool:
        xs, ys = defaultdict(int), defaultdict(int)
        for x1,y1, x2,y2 in rectangles:
            xs[x1] += 1
            xs[x2-.5] -= 1
            ys[y1] += 1
            ys[y2-.5] -= 1
        acc = 0; p = 0
        for x,v in sorted(xs.items()):
            acc += v
            if acc == 0: p += 1
            if p>2: return True  # 注意最右侧必然回归到 0
        acc = 0; p = 0
        for y,v in sorted(ys.items()):
            acc += v
            if acc == 0: p += 1
            if p>2: return True
        return False
    
    """ 3395. 唯一中间众数子序列 I #hard 统计所有的长5的子序列, 要求其存在唯一众数, 并且 seq[2] 是众数  
限制: n 100; 取模
思路1: #枚举
    从n个数中选择5个的可能性有 C(n,5); 考虑其中不合法的
    """
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        


sol = Solution()
result = [
    # sol.countPathsWithXorValue(grid = [[2, 1, 5], [7, 10, 0], [12, 6, 4]], k = 11),
    sol.checkValidCuts(n = 5, rectangles = [[1,0,5,2],[0,2,2,4],[3,2,5,3],[0,4,4,5]]),
    sol.checkValidCuts(n = 4, rectangles = [[0,0,1,1],[2,0,3,4],[0,2,2,3],[3,0,4,3]]),
    sol.checkValidCuts(n = 4, rectangles = [[0,2,2,4],[1,0,3,2],[2,2,3,4],[3,0,4,2],[3,2,4,4]]),
]
for r in result:
    print(r)
