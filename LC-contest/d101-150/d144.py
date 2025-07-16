from typing import *
from functools import lru_cache
from heapq import heappop, heappush

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-144
T3 用栈的思维, 一时间没反应过来;
T4 数学直觉, 比较简单
Easonsi @2025 """
class Solution:
    """ 3360. 移除石头游戏 """
    def canAliceWin(self, n: int) -> bool:
        t = 10
        for i in range(10):
            if n >= t:
                n -= t
                t -= 1
            else:
                return i % 2 == 1
    """ 3361. 两个字符串的切换距离 
[ling](https://leetcode.cn/problems/shift-distance-between-two-strings/solutions/2998657/qian-zhui-he-on-zuo-fa-pythonjavacgo-by-b4hfx/)
用前缀和求解更为简单
    """
    def shiftDistance(self, s: str, t: str, nextCost: List[int], previousCost: List[int]) -> int:
        @lru_cache(None)
        def f(i:int, j:int) -> int:
            if i==j: return 0
            # return min(
            #     f((i+1)%26, j) + nextCost[i],
            #     f((i-1)%26, j) + previousCost[i]
            # )
            if j < i: 
                j1 = j+26
                j2 = j
            else: 
                j1 = j
                j2 = j-26
            return min(
                sum(nextCost[k%26] for k in range(i,j1)),
                sum(previousCost[k%26] for k in range(i,j2,-1))
            )
        return sum(f(ord(x)-ord('a'), ord(y)-ord('a')) for x,y in zip(s,t))

    """ 3362. 零数组变换 III #medium 对于每个 query[l,r], 都能将 nums[l..r] 中的每个元至多 -1 (或不操作).
问至多删除多少个query, 还能使得 nums 变为全0数组
限制: n 1e5; q 1e5
思路1: #贪心
    前置: 3355. 零数组变换 I -- 用 #差分 来统计区间
    本题中, 从左往右考虑每个位置i, 用贪心的思想, "从左端点 <=i 的query中先用右端点最大的那个"!
    如何实现? 
        - 用堆来维护右端点
        - 在遍历i的时候, 动态增加堆的元素! -- 需要先按照左端点sort一下!
[ling](https://leetcode.cn/problems/zero-array-transformation-iii/solutions/2998650/tan-xin-zui-da-dui-chai-fen-shu-zu-pytho-35o6/)
     """
    def maxRemoval(self, nums: List[int], queries: List[List[int]]) -> int:
        queries.sort(key=lambda x: x[0])
        diff = [0] * (len(nums) + 1)
        acc = 0
        h = []; idx = 0
        for i,x in enumerate(nums):
            acc += diff[i]
            target = x - acc
            # add into heap
            while idx<len(queries) and queries[idx][0] <= i:
                heappush(h, -queries[idx][1])
                idx += 1
            # try handle target
            while target>0 and h and -h[0]>=i:  # 注意避免空堆!
                r = -heappop(h)
                acc += 1
                diff[r+1] -= 1
                target -= 1
            if target>0: return -1
        return len(h)

    """ 3363. 最多可收集的水果数目 #hard 在一个 n*n 的网格中, 每个单元有分数, (0,0) 沿对角线到 (n-1,n-1); (0,n-1) 每次i+1, j选择 -1/0/+1; (n-1,0) 每次j+1, i选择 -1/0/+1.
可知, 3人都经过 n-1 到达 (n-1,n-1). 收集的分数不能重叠. 问最大分数和.
限制: n 1000
思路1: #数学 直觉 #DP
    分析可知, 第一个人肯定走对角线. 其他两人是对称的. 仅分析左下角的人: 
        肯定不会触碰/穿越对角线
        肯定无法到达副对角线以上部分
        其余情况, 直接DP即可
    另外, 需要注意不要重复计算单元格分数. 参见代码
    复杂度: O(n^2)
[ling](https://leetcode.cn/problems/find-the-maximum-number-of-fruits-collected/solutions/2998667/nao-jin-ji-zhuan-wan-wang-ge-tu-dppython-gjcm/)
 """
    def maxCollectedFruits(self, fruits: List[List[int]]) -> int:
        n = len(fruits)
        # person 1
        ans = sum(fruits[i][i] for i in range(n))
        # person 2
        @lru_cache(None)
        def f(i:int,j:int) -> int:
            if not (0<=i<n and 0<=j<n): return 0
            if (not i==j==n-1) and i<=j: return 0
            if i+j<n-1: return 0
            return max(f(i-1,j-1), f(i,j-1), f(i+1,j-1)) + fruits[i][j]
        ans += f(n-1,n-1)
        # person 3
        @lru_cache(None)
        def g(i:int,j:int) -> int:
            if not (0<=i<n and 0<=j<n): return 0
            if (not i==j==n-1) and i>=j: return 0
            if i+j<n-1: return 0
            return max(g(i-1,j-1), g(i-1,j), g(i-1,j+1)) + fruits[i][j]
        ans += g(n-1,n-1)
        return ans - 2*fruits[n-1][n-1]  # 重复计算了右下角


sol = Solution()
result = [
    # sol.canAliceWin(n = 12),
    # sol.canAliceWin(2),
    # sol.shiftDistance(s = "abab", t = "baba", nextCost = [100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], previousCost = [1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    # sol.shiftDistance(s = "leet", t = "code", nextCost = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], previousCost = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]),
    sol.maxRemoval(nums = [2,0,2], queries = [[0,2],[0,2],[1,1]]),
    # sol.maxCollectedFruits(fruits = [[1,2,3,4],[5,6,8,7],[9,10,11,12],[13,14,15,16]]),
    # sol.maxCollectedFruits(fruits = [[1,1],[1,1]]),
]
for r in result:
    print(r)
