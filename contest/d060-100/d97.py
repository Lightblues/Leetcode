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
"""
    def maximizeWin(self, prizePositions: List[int], k: int) -> int:
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
    

    """ 6305. 二进制矩阵中翻转最多一次使路径不连通 #medium 但挺 #hard 要在一个0/1矩阵上从左上走到右下, 只能走1的位置, 只能向下向右走, 在最多翻转1个格子的情况下, 能否使得无法走通? 
限制: m,n 1e3
思路0: #WA 原本以为等价于, 一个连通的0区域, 将左上角右下角分离开; 也即有一条贯穿左右两边的 0路径. 
    但实际上, [[1,0], [0,1]] 形状的也可以走通, 也即0不一定要连起来!
Orz 看错题目了, 限制了行动的方向只能是向下向右
思路1: #计数 分别统计从左上, 右下做到 (i,j) 的路径数量
    若两者乘积 = 总的路径数量, 则说明该点是必经点!
    关联 「0063. 不同路径 II」
    见 [Ts](https://leetcode.cn/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/solution/ji-shu-by-tsreaper-m01b/)
    
"""
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        # WA!!! 0不一定要连起来!
        m,n = len(grid), len(grid[0])
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        def test(i,j):
            return i==0 or j==n-1
        h = []
        for i in range(1,m):
            c = 1 if grid[i][0]==1 else 0
            heappush(h, (c,i,0))
        for j in range(1,n-1):
            c = 1 if grid[m-1][j]==1 else 0
            heappush(h, (c,m-1,j))
        visited = set()
        for c,x,y in h:
            visited.add((c,x,y))
        while h:
            c, x,y = heappop(h)
            if test(x,y): 
                return True
            for dx,dy in directions:
                nx,ny = x+dx, y+dy
                if not (0<=nx<m and 0<=ny<n): continue
                nc = c + (1 if grid[nx][ny]==1 else 0)
                if nc>1: continue
                if (nc,nx,ny) in visited: continue
                if (nx==0 and ny==0) or (nx==m-1 and ny==n-1): continue
                heappush(h, (nc,nx,ny))
                visited.add((nc,nx,ny))
        return False

    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
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
