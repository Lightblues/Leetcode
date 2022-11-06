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
https://leetcode.cn/contest/weekly-contest-157


@2022 """
class Solution:
    """ 1217. 玩筹码 """
    
    """ 1218. 最长定差子序列 """
    
    """ 1219. 黄金矿工 medium 找到矩阵中非零路径中累积和最大的, 限制: mn 15; 
对于每一个非零的点, 尝试进行 DFS 即可, 注意避免重复访问. 
    Copilot 牛! 下面的DFS直接帮写好了
    复杂度: 见 [官答](https://leetcode.cn/problems/path-with-maximum-gold/solution/huang-jin-kuang-gong-by-leetcode-solutio-f9gg/)
 """
    def getMaximumGold(self, grid: List[List[int]]) -> int:
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        m,n = len(grid), len(grid[0])
        def isValid(x,y):
            return 0<=x<m and 0<=y<n
        visited = [[False]*n for _ in range(m)]
        result = 0
        def dfs(x,y, cumsum):
            if not isValid(x,y):
                return
            if visited[x][y] or grid[x][y] == 0:
                return
            visited[x][y] = True
            nonlocal result
            result = max(result, cumsum+grid[x][y])
            for dx,dy in directions:
                dfs(x+dx, y+dy, cumsum+grid[x][y])
            visited[x][y] = False
        for i in range(m):
            for j in range(n):
                dfs(i,j,0)
        return result
    
    """ 1220. 统计元音字母序列的数目 #hard 基本的计数DP """
    def countVowelPermutation(self, n: int) -> int:
        mod = 10**9+7
        f = [1] * 5
        for _ in range(n-1):
            nf = [0] * 5
            nf[0] = (f[1]+f[2]+f[4]) % mod
            nf[1] = (f[0]+f[2]) % mod
            nf[2] = (f[1] + f[3])%mod
            nf[3] = f[2]
            nf[4] = (f[2] + f[3]) %mod
            f = nf
        return sum(f) % mod
    
    

    
sol = Solution()
result = [
    # sol.getMaximumGold(grid = [[0,6,0],[5,8,7],[0,9,0]]),
    
]
for r in result:
    print(r)
