"""
n 皇后问题 研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。
给你一个整数 n ，返回所有不同的 n 皇后问题 的解决方案。
每一种解法包含一个不同的 n 皇后问题 的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。


输入：n = 4
输出：[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
解释：如上图所示，4 皇后问题存在两个不同的解法。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/n-queens
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        board = [[False]*n for _ in range(n)]
        results = []

        def is_valid(r, c):
            if any(board[r]):
                return False
            if any([board[i][c] for i in range(n)]):
                return False
            # if any([board[r+i][c+i] for i in range(-min(r,c), n-max(r,c)) if 0<=r+i<n and 0<=c+i<n]):
            if any([board[r + i][c + i] for i in range(-min(r, c), n - max(r, c))]):
                return False
            if any([board[r+i][c-i] for i in range(max(-r, c-n+1), min(c, n-1-r)+1)]):
                return False
            return True
        # print(is_valid(2,3))

        def record():
            result = [''.join(['Q' if i else '.' for i in row]) for row in board]
            results.append(result)

        def dfs(row):
            option_cols = []
            for c in range(n):
                if is_valid(row, c):
                    option_cols.append(c)
            # if not option_cols:
            #     # 搜索失败
            #     return False
            if row == n-1:
                for c in option_cols:
                    board[row][c] = True
                    record()
                    board[row][c] = False   # 清除
                return
            else:
                for c in option_cols:
                    board[row][c] = True
                    dfs(row+1)
                    board[row][c] = False
        dfs(0)
        return results


print(Solution().solveNQueens(4))