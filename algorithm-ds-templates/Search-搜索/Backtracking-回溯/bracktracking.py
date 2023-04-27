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
    """ 0036. 有效的数独 #medium 只需要检查填入部分是否合法即可, 并不要求是否可解 """
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # isValid = True
        def isUnique(l):
            return len(set(l))==len(l)
        for line in board:
            if not isUnique([n for n in line if n!='.']):
                return False
        for i in range(9):
            col = [line[i] for line in board if line[i]!='.']
            if not isUnique(col):
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subBoard = [line[j:j+3] for line in board[i:i+3]]
                subBoard = [i for line in subBoard for i in line if i!= '.']
                if not isUnique(subBoard):
                    return False
        return True

    """ 0037. 解数独 #hard #题型 #回溯 
思路0: 自己写的不考虑优化的算法
    分离了一些函数逻辑
        get_potential_values(r, c)
        find_first_empty(r,c) 从这个位置找下一个空格
[官答](https://leetcode.cn/problems/sudoku-solver/solution/jie-shu-du-by-leetcode-solution/)
    """
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

    """ 0679. 24 点游戏 #hard #hardhard 给定四张牌, 问是否可以构成24点
思路1: #回溯 注意, 需要考虑数字的顺序!! 
    首先看复杂度: 从4张牌中选择两个考虑顺序 4*3, 四种操作, 把结果放回得到3张牌; 继续 3*2 *4; 2*2 *4; 考虑所有的情况, 共9216种可能!
    实现: 在回溯过程中生成新的数组!
    优化: 加法, 乘法是对称的, 可以剪枝!
    细节: 浮点数! 因此检查合法可以计算 abs(x-y)<EPSILON; 注意除法合法可以检查 abs(y)<EPSILON
    """
    def judgePoint24(self, cards: List[int]) -> bool:
        TARGET = 24
        EPSILON = 1e-6
        ADD, MULTIPLY, SUBTRACT, DIVIDE = 0, 1, 2, 3
        def solve(nums):
            if not nums: return False
            if len(nums)==1: return abs(nums[0]-TARGET) < EPSILON
            for i,x in enumerate(nums):
                for j,y in enumerate(nums):
                    if i==j: continue
                    newNums = [nums[k] for k in range(len(nums)) if k!=i and k!=j]
                    for idx in range(4):
                        # 剪枝: 加法, 乘法是对称的!
                        if idx<2 and i>j: continue
                        if idx==ADD: newNums.append(x+y)
                        elif idx==MULTIPLY: newNums.append(x*y)
                        elif idx==SUBTRACT: newNums.append(x-y)
                        else:
                            if abs(y)<EPSILON: continue
                            newNums.append(x/y)
                        if solve(newNums): return True
                        newNums.pop()   # note to pop the last element
            return False
        return solve(cards)
    
    

    
sol = Solution()
result = [
    sol.judgePoint24(cards = [4, 1, 8, 7]),
    sol.judgePoint24(cards = [1, 2, 1, 2]),
]
for r in result:
    print(r)
