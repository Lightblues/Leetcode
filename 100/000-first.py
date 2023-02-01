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

Easonsi @2023 """
class Solution:
    """  """
    # 054 螺旋数组
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return list()

        rows, columns = len(matrix), len(matrix[0])
        order = list()
        left, right, top, bottom = 0, columns - 1, 0, rows - 1
        
        while left <= right and top <= bottom:
            # 每次循环一圈
            for column in range(left, right + 1):
                order.append(matrix[top][column])
            for row in range(top + 1, bottom + 1):
                order.append(matrix[row][right])
            # 只剩下一行/一列 的情况下, 下面是不需要的
            if left < right and top < bottom:
                for column in range(right - 1, left, -1):
                    order.append(matrix[bottom][column])
                for row in range(bottom, top, -1):
                    order.append(matrix[row][left])
            left, right, top, bottom = left + 1, right - 1, top + 1, bottom - 1
        return order
    
    """ 037 解数独 """
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
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
