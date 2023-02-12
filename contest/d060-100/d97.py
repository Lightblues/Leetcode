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
https://leetcode-cn.com/contest/biweekly-contest-97
https://leetcode.cn/circle/discuss/F06Kf0/
灵神: https://www.bilibili.com/video/BV1rM4y1X7z9

T4思维题, 灵神的轮廓线解法和统计路径数的解法都超级奇妙!
Easonsi @2023 """
class Solution:
    """ 6303. 分割数组中数字的数位 """
    def separateDigits(self, nums: List[int]) -> List[int]:
        ans = []
        for num in nums:
            ans += [int(c) for c in str(num)]
        return ans

    """ 6304. 从一个范围内选择最多整数 I """
    def maxCount(self, banned: List[int], n: int, maxSum: int) -> int:
        banned = set(banned)
        cnt = 0; acc = 0
        for i in range(1,n+1):
            if i not in banned and acc+i<=maxSum:
                cnt += 1
                acc += i
        return cnt
        
    """ 6331. 两个线段获得的最多奖品 #medium 一些奖品分布在一些整数点上 (一个点可以有多个). 现在可以用两根长K的线段, 拿到两个线段上的奖品. 问最多能拿到几个? 
思路1: #滑动窗口 维护一个长度为实际长度K的窗口, 还要记录此前窗口 (与当前窗口不重叠) 的最大值! 
    代码 #细节: 需要用一个 deque 来记录此前的score列表
    复杂度: O(n)
    灵神: 关联「两数之和」. 枚举第二条线段 (右端点), 判断和第一条线段的组合!
"""
    def maximizeWin(self, prizePositions: List[int], k: int) -> int:
        # 自己的实现, 乱七八糟...
        n = len(prizePositions)
        ans = 0
        preMx = 0
        scores = deque()    # (pos, score)
        l = 0
        for r in range(n):
            while l<=r and prizePositions[r]-prizePositions[l]>k:
                l += 1
            score = r-l+1
            scores.append((prizePositions[r],score))
            while scores and scores[0][0]<prizePositions[r]-k: 
                _, s = scores.popleft()
                preMx = max(preMx, s)
            # if r>k: preMx = max(preMx, scores[r-k-1])
            ans = max(ans, preMx+score)
        return ans
    def maximizeWin(self, prizePositions: List[int], k: int) -> int:
        # from 灵神, 优雅!
        pre = [0] * (len(prizePositions) + 1)
        ans = left = 0
        for right, p in enumerate(prizePositions):
            while p - prizePositions[left] > k:
                left += 1
            ans = max(ans, right - left + 1 + pre[left])
            pre[right + 1] = max(pre[right], right - left + 1)
        return ans


    """ 6305. 二进制矩阵中翻转最多一次使路径不连通 #medium 但挺 #hard 要在一个0/1矩阵上从左上走到右下, 只能走1的位置, 只能向下向右走, 在最多翻转1个格子的情况下, 能否使得无法走通? 
限制: m,n 1e3
思路0: #WA 原本以为等价于, 一个连通的0区域, 将左上角右下角分离开; 也即有一条贯穿左右两边的 0路径. 
    但实际上, [[1,0], [0,1]] 形状的也可以走通, 也即0不一定要连起来!
Orz 看错题目了, 限制了行动的方向只能是向下向右
思路1: #计数 分别统计从左上, 右下做到 (i,j) 的路径数量
    若两者乘积 = 总的路径数量, 则说明该点是必经点!
    关联 「0063. 不同路径 II」
    见 [Ts](https://leetcode.cn/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/solution/ji-shu-by-tsreaper-m01b/)
思路2 :转换成求 #轮廓 是否相交
    将所有可能的路径「涂色」, 则形成了一块「区域」 —— 可以由上下两条「轮廓线」描述.
    则答案等价于: 上下轮廓线存在交集! 
        重点: 如何求「下轮廓」? 可以 #DFS
    简化: 再考虑一下, 假如我们将下轮廓线上的点全部堵住, 那么没有「存在交集」, 等价于无法再找到一条路径! 
        因此, 只需要两次DFS即可!
    见 [灵神](https://leetcode.cn/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/solution/zhuan-huan-cheng-qiu-lun-kuo-shi-fou-xia-io8x/)
"""
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        # 思路1: #计数 分别统计从左上, 右下做到 (i,j) 的路径数量
        mod = 10**9+7   # 路径数可能很大
        m,n = len(grid), len(grid[0])
        f = [[0]*(n+1) for _ in range(m+1)]
        f[0][1] = 1
        for i in range(1,m+1):
            for j in range(1,n+1):
                if grid[i-1][j-1]==0: continue
                f[i][j] = (f[i-1][j] + f[i][j-1]) % mod
        g = [[0]*(n+2) for _ in range(m+2)]     # 注意这里的边界!!
        g[-1][-2] = 1
        for i in range(m,0,-1):
            for j in range(n,0,-1):
                if grid[i-1][j-1]==0: continue
                g[i][j] = (g[i+1][j] + g[i][j+1]) % mod
        # 
        if f[m][n]==0: return True  # 原本就无法走通
        for i in range(1,m+1):
            for j in range(1,n+1):
                if (i==1 and j==1) or (i==m and j==n): continue # 不能翻转左上角和右下角
                # 经过(i,j)的路径数量 是否等于总的路径数量! 
                cnt_ij = f[i][j] * g[i][j] % mod
                if cnt_ij == f[m][n]: return True
        return False
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        # from 灵神
        m,n = len(grid), len(grid[0])
        def dfs(x,y):
            if x==m-1 and y==n-1: return True
            grid[x][y] = 0  # 直接修改! 
            return x < m - 1 and grid[x + 1][y] and dfs(x + 1, y) or \
                   y < n - 1 and grid[x][y + 1] and dfs(x, y + 1)
            # 优先往下走, 再往右走
            if x<m-1 and grid[x+1][y]:
                if dfs(x+1,y): return True
            if y<n-1 and grid[x][y+1]:
                if dfs(x,y+1): return True
            return False
        # 要么第一次就无法走到 (第一个检查); 要么翻转下轮廓之后无法走到
        return not dfs(0,0) or not dfs(0,0)

    """ 0063. 不同路径 II #medium 机器人从左上走到右下, 0/1 表示是否有障碍物. 问方案数量
思路1: 基本 #DP
    可以压缩到一维, 见 [官答](https://leetcode.cn/problems/unique-paths-ii/solution/bu-tong-lu-jing-ii-by-leetcode-solution-2/)
"""
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m,n = len(obstacleGrid),len(obstacleGrid[0])
        dp = [[0]*(n+1) for _ in range(m+1)]
        dp[0][1] = 1
        for i in range(1,m+1):
            for j in range(1,n+1):
                if obstacleGrid[i-1][j-1]==1: continue
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        return dp[m][n]
    
sol = Solution()
result = [
    # sol.separateDigits(nums = [13,25,83,77]),
    # sol.maxCount(banned = [1,6,5], n = 5, maxSum = 6),
    # sol.maxCount(banned = [1,2,3,4,5,6,7], n = 8, maxSum = 1),
    # sol.maxCount(banned = [11], n = 7, maxSum = 50),
    # sol.maximizeWin(prizePositions = [0,1,1,2,2,3,3,4,5], k = 1),
    # sol.maximizeWin(prizePositions = [1,2,3,4], k = 0),
    sol.isPossibleToCutPath(grid = [[1,1,1],[1,0,0],[1,1,1]]),
    sol.isPossibleToCutPath(grid = [[1,1,1],[1,0,1],[1,1,1]]),
    sol.isPossibleToCutPath([[1,1,1,0,0],[1,0,1,0,0],[1,1,1,1,1],[0,0,1,1,1],[0,0,1,1,1]]),
    
    # sol.uniquePathsWithObstacles(obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]),
]
for r in result:
    print(r)
