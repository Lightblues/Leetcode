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
https://leetcode.cn/contest/weekly-contest-413
Easonsi @2023 
T3 反过来的考虑的 DP 有意思
T4 分析的过程值得学习; 关于DP的方法梦回算法课
"""
class Solution:
    """ 3274. 检查棋盘方格颜色是否相同 """
    def checkTwoChessboards(self, coordinate1: str, coordinate2: str) -> bool:
        def f(co):
            x,y = co
            return ord(x)-ord('a') + int(y)-1
        return f(coordinate1)%2 == f(coordinate2)%2
    
    """ 3275. 第 K 近障碍物查询 """
    def resultsArray(self, queries: List[List[int]], k: int) -> List[int]:
        h = []
        ans = []
        for x,y in queries:
            key = abs(x)+abs(y)
            if len(h) < k:
                heappush(h, -key)
            else:
                if key < -h[0]:
                    heappushpop(h, -key)
            ans.append(-h[0] if len(h) == k else -1)
        return ans
    
    """ 3276. 选择矩阵中单元格的最大得分 #hard 从矩阵每一行选一个数字, 要求数值互不相同, 求最大得分 (和)
限制: m,n 10; x 100
思路0: 尝试贪心, 失败了
    观察 case=[[8,7,6],[8,3,2]], 8 选择的应该是idx=1 -- 贪心的想法是, 每次选择首位最大的数字, 从行中选择最小的那个
    -- 但有问题, case = [[8,11,3],[17,7,3],[13,20,3],[3,17,20]]
思路1: #DP
    定义 f(i, j) 表示从数字 1...i 中选择, 并且所选的行号集合为j的最大分数. 则有
        f[i,j] = max{
            f[i-1, j]  # 没有选择数字 i
            f[i-1, j | idx] + i, # 表示选择了 idx \notin j 的数字 i
        }
    边界: f(0, j) = 0
    答案: f(mx, null)
[ling](https://leetcode.cn/problems/select-cells-in-grid-with-maximum-score/solutions/)
其中还介绍了 #费用流 的做法
    """
    def maxScore(self, grid: List[List[int]]) -> int:
        # WA!
        ans = 0
        grid = [sorted(row, reverse=True) for row in grid]
        while grid:
            mx = max(row[0] for row in grid)
            idxs = [i for i, row in enumerate(grid) if row[0] == mx]
            for i in idxs: 
                while grid[i] and grid[i][0] == mx:
                    grid[i].pop(0)
            ans += mx
            i = 0
            for j in range(1, len(idxs)):
                if grid[idxs[j]] < grid[idxs[i]]:
                    i = j
            grid.pop(idxs[i])
            grid = [row for row in grid if row]
        return ans
    def maxScore(self, grid: List[List[int]]) -> int:
        val2rows = defaultdict(list)
        for i,row in enumerate(grid):
            for x in set(row):
                val2rows[x].append(i)
        numberMap = sorted(val2rows.keys())
        @lru_cache(None)
        def f(i: int, j: int) -> int:
            if i < 0: return 0
            ans = f(i-1, j)  # 没有选择数字 i
            for r in val2rows[numberMap[i]]:
                if 1 << r & j: continue
                ans = max(ans, f(i-1, j | 1 << r) + numberMap[i])
            return ans
        return f(len(numberMap)-1, 0)
        
    
    """ 3277. 查询子数组最大异或值 #hard 对于一个数组, 每次 q=[l,r] 需要从 nums[l...r] 中找到子数组的得分最大
分数计算方式: 每次将 a[i] <- a[i] XOR a[i+1] 然后移除最后一个元素. 问最后剩下的数字
限制: n 2e3; q 1e5; x 2^32
思路1: 两次区间 #DP
    我们来看 f[i,j] = S{ nums[i..j] } 这个得分怎么计算? 
        结论: f[i,j] = f[i,j-1] XOR f[i+1,j]. 这个自己推导一下就懂了, 或者参见 [ling]
        边界: f[i,i] = nums[i]
        -> 可视化看一下公式的计算方向, 需要对于 i 从大到小遍历
    接下来, 对于 nums[l...r] 的子数组中的最大值, 如何计算?
        结论: g[l,r] = max{ f[i,j], g[i+1,j], g[i,j-1] }. 也即在整个区间之外, 可以分解为两个子问题
        边界: g[i,i] = nums[i] 
    复杂度: O(n^2 + q)
[ling](https://leetcode.cn/problems/maximum-xor-score-subarray-queries/)
    """
    def maximumSubarrayXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        f = [[0]*(n) for _ in range(n)]
        g = [[0]*(n) for _ in range(n)]
        for i in range(n-1, -1, -1):
            f[i][i] = nums[i]
            g[i][i] = nums[i]
            for j in range(i+1, n):
                f[i][j] = f[i][j-1] ^ f[i+1][j]
                g[i][j] = max(g[i][j-1], g[i+1][j], f[i][j])
        return [g[l][r] for l,r in queries]
    
sol = Solution()
result = [
    # sol.checkTwoChessboards(coordinate1 = "a1", coordinate2 = "c3"),
    # sol.resultsArray(queries = [[1,2],[3,4],[2,3],[-3,0]], k = 2),
    # sol.maxScore(grid = [[1,2,3],[4,3,2],[1,1,1]]),
    # sol.maxScore(grid = [[8,7,6],[8,3,2]]),
    # sol.maxScore([[12,12],[4,4],[12,12]]),
    # sol.maxScore([[8,11,3],[17,7,3],[13,20,3],[3,17,20]]),
    sol.maximumSubarrayXor(nums = [0,7,3,2,8,5,1], queries = [[0,3],[1,5],[2,4],[2,6],[5,6]]),
    
]
for r in result:
    print(r)
