


from typing import List
class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        def get_potential_values(r, c):
            potentials = set("123456789")
            row = board[r]
            potentials = potentials - set(row)
            col = [board[i][c] for i in range(9)]
            potentials = potentials - set(col)
            sub_r = r//3*3
            sub_c = c//3*3
            sub_board = [board[i][j] for i in range(sub_r, sub_r+3) for j in range(sub_c, sub_c+3)]
            potentials -= set(sub_board)
            return potentials
        # print(get_potential_values(0,3))

        def find_first_empty(r,c):
            # 从 (r,c) 坐标开始找到第一个非空点
            for col in range(c, 9):
                if board[r][col] == '.':
                    return r, col
            for row in range(r+1, 9):
                for col in range(9):
                    if board[row][col] == ".":
                        return row, col
            return -1, -1

        def backtrack(c, r):
            newr, newc = find_first_empty(c, r)
            if newc == newr == -1:
                # 没有待填空格，说明已成功
                return True
            potentials = get_potential_values(newr, newc)
            if not potentials:
                # 没有符合要求的了数可填入，需要将 (c,r) 处的尝试删去 ---（1）
                return False
            for potential in potentials:
                board[newr][newc] = potential
                res = backtrack(newr, newc)
                # 接收（1）处传来的尝试结果，若尝试失败则清除尝试填入的数字
                if not res:
                    board[newr][newc] = '.'
                else:
                    return res  # 若成功则直接回传

        backtrack(0, 0)

board = [
["5","3",".",".","7",".",".",".","."],
["6",".",".","1","9","5",".",".","."],
[".","9","8",".",".",".",".","6","."],
["8",".",".",".","6",".",".",".","3"],
["4",".",".","8",".","3",".",".","1"],
["7",".",".",".","2",".",".",".","6"],
[".","6",".",".",".",".","2","8","."],
[".",".",".","4","1","9",".",".","5"],
[".",".",".",".","8",".",".","7","9"]
]
Solution().solveSudoku(board)
print(board)
