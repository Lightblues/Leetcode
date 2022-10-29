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
https://leetcode.cn/contest/weekly-contest-165

T1 T2 都还挺有意思的. T3 一开始想复杂了, 但到答案的DP才恍然大悟: 考虑的简单些! T4的DP不难想到, 但居然被边界问题搞了好久...

@2022 """
class Solution:
    """ 1275. 找出井字棋的获胜者 #模拟 """
    def tictactoe(self, moves: List[List[int]]) -> str:
        def check(board):
            for i in range(3):
                if board[i][0]!=0 and board[i][0]==board[i][1]==board[i][2]:
                    return board[i][0]
                if board[0][i]!=0 and board[0][i]==board[1][i]==board[2][i]:
                    return board[0][i]
            if board[0][0]!=0 and board[0][0]==board[1][1]==board[2][2]:
                return board[0][0]
            if board[0][2]!=0 and board[0][2]==board[1][1]==board[2][0]:
                return board[0][2]
            return 0
        board = [[0]*3 for _ in range(3)]
        for i, (x, y) in enumerate(moves):
            role = i%2+1
            board[x][y] = role
            if check(board) != 0: return 'A' if role==1 else 'B'
        return "Draw" if len(moves)==9 else "Pending"
    
    """ 1276. 不浪费原料的汉堡制作方案 """
    def numOfBurgers(self, tomatoSlices: int, cheeseSlices: int) -> List[int]:
        x = (tomatoSlices-2*cheeseSlices)/2
        if int(x)!=x: return []
        x = int(x)
        y = cheeseSlices-x
        if x<0 or y<0: return []
        return [x,y]
    
    """ 1277. 统计全为 1 的正方形子矩阵 #medium #题型 给定一个01矩阵, 统计其中全为1的正方形子矩阵的个数. 限制: n 300
思路0: 计算好 前缀数组, 然后枚举每个点作为左上角, 枚举边长. 时间复杂度 O(n^3)
思路0.2: 尝试 #DP, 但考虑的是每一行的变化情况. (也是找 r,c 点作为左上角的最大正方形边长)
    预计算 pre[r][c] 表示在第r行的第 c个位置向后的连续1的个数. 
    然后对于每一列, 向下找 pre[0,1...][c] 看能够匹配构成的最大正方形. 
    但比较复杂, 估计复杂度是 O(n^2)
思路1: 有一种更为简便的 #DP 方案. 
    记 `f[i,j]` 表示该点作为左下角的最大正方形边长. 根据正方形的性质, 我们知道若该点的正方形长k, 则 f[i-1,j], f[i-1,j+1], f[i,j+1] 所构成的正方形至少为 k-1. 
    因此, 递推公式: 若 grid[i,j]=1, 则有 `f[i,j] = min(f[i-1,j], f[i-1,j+1], f[i,j+1]) + 1`
[官答](https://leetcode.cn/problems/count-square-submatrices-with-all-ones/solution/tong-ji-quan-wei-1-de-zheng-fang-xing-zi-ju-zhen-2/)
"""
    def countSquares(self, matrix: List[List[int]]) -> int:
        m,n = len(matrix), len(matrix[0])
        # 原地修改. 
        for i in range(1, m):
            for j in range(n-2, -1, -1):
                if matrix[i][j]==1:
                    matrix[i][j] = min(matrix[i-1][j], matrix[i-1][j+1], matrix[i][j+1]) + 1
        return sum(map(sum, matrix))
    
    
    """ 1278. 分割回文串 III #hard 给定一个字符串, 要求分割成k个回文串. 你可以修改字符串的每个字符, 问最少修改多少个字符 限制: n 100
思路1: #DP 被下面的边界问题折磨了半天 orz. 
    记 `f[i,k]` 表示将前i个字符分割成k个回文串的最少修改次数. 则有递推 `f[i,k] = min{ f[ii,k-1] + cost(ii+1,i) }` 其中 `cost(ii+1,i)` 表示将 `s[ii+1:i]` 变成回文串的最少修改次数
    这样, DP的复杂度是 `O(n^2 k)`
    如何求 cost? 用 `g[i,j]` 表示将 `s[i:j]` 变成回文串的最少修改次数. 则有递推 `g[i,j] = g[i+1,j-1] if s[i]==s[j] else g[i+,j-1]+1`
        这里的复杂度是 `O(n^2)`
    [官答](https://leetcode.cn/problems/palindrome-partitioning-iii/solution/fen-ge-hui-wen-chuan-iii-by-leetcode-solution/)
"""
    def palindromePartition(self, s: str, k: int) -> int:
        n = len(s)
        g = [[0]*n for _ in range(n)]
        for i in range(n-1,-1,-1):
            for j in range(i+1,n):
                g[i][j] = g[i+1][j-1] if s[i]==s[j] else g[i+1][j-1]+1
        f = [[0]*(k+1) for _ in range(n)]
        for i in range(n):
            f[i][1] = g[0][i]
            # 一共 i+1 个字符. 若分割成 i+1 个肯定代价为0.
            for kk in range(2, min(k+1, i+1)):
                # 注意这里的范围! 我们需要分割成 kk-1 个部分, 枚举所有的分割点. 因此kk应该从 kk-2 开始. 同时 [[ii,i]] 应该非空. 
                # 实际上, 写成for循环应该更清楚一点~
                f[i][kk] = min(f[ii][kk-1]+g[ii+1][i] for ii in range(kk-2, i))
        return f[n-1][k]
    
sol = Solution()
result = [
    # sol.tictactoe(moves = [[0,0],[2,0],[1,1],[2,1],[2,2]]),
    # sol.tictactoe(moves = [[0,0],[1,1],[2,0],[1,0],[1,2],[2,1],[0,1],[0,2],[2,2]]),
    sol.countSquares(matrix = [[0,1,1,1],[1,1,1,1],[0,1,1,1]]),
    # sol.palindromePartition(s = "abc", k = 2),
    # sol.palindromePartition(s = "aabbc", k = 3),
    # sol.palindromePartition(s = "leetcode", k = 8),
    # sol.palindromePartition("ihhyviwv", 7),
]
for r in result:
    print(r)
