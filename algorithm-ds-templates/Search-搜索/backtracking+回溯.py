from easonsi import utils
from easonsi.util.leetcode import *

""" 
https://oi-wiki.org/search/backtracking/
"""

class Solution:
    """ 0784. 字母大小写全排列 #medium
对于一个字符串中的所有英文字母, 组合其大小写可以有多种结果, 返回所有可能的结果. 限制: 字符串长度 n 12
思路1: 直接构造, 可以写成 #迭代 的形式.
    复杂度: `O(2^n n)`
思路2: 可以借助 #itertools 写成 #笛卡尔积 product 的形式, 简化.
[official](https://leetcode.cn/problems/letter-case-permutation/solution/zi-mu-da-xiao-xie-quan-pai-lie-by-leetcode/)
"""
    def letterCasePermutation(self, s: str) -> List[str]:
        result = [[]]
        for char in s:
            lenResult = len(result)
            # 数组直接倍增.
            if char.isalpha():
                for i in range(lenResult):
                    result.append(result[i][:])
                    result[i].append(char.lower())
                    result[lenResult+i].append(char.upper())
            else:
                for i in range(lenResult):
                    result[i].append(char)
        return list(map("".join, result))
    def letterCasePermutation(self, S):
        f = lambda x: (x.lower(), x.upper()) if x.isalpha() else x
        return map("".join, itertools.product(*map(f, S)))

    """ 0051. N 皇后 #hard #题型
给定棋盘大小, 返回所有N皇后问题的解. 限制: N <= 9
思路1: 遍历行, 每次判断可以放置的位置; 递归求解
    如何得到当前行可以放置的位置? 需要记录之前的 列, 主副对角线 三个信息.
    1.1: 用一个set来记录已有的信息 (注意主对角线方向上, x-y 的值相同)
    1.2: 还可以用bit进行记录, 通过移位操作完成状态转移.
    详见 [官答](https://leetcode.cn/problems/n-queens/solution/nhuang-hou-by-leetcode-solution/)
 """
    def solveNQueens(self, n: int) -> List[List[str]]:
        # 1.2: 还可以用bit进行记录, 通过移位操作完成状态转移.
        def generateBoard():
            board = list()
            for i in range(n):
                row[queens[i]] = "Q"
                board.append("".join(row))
                row[queens[i]] = "."
            return board

        def solve(row: int, columns: int, diagonals1: int, diagonals2: int):
            # 当前为row行; 列和两个对角线方向的记录为三个数字.
            if row == n:
                board = generateBoard()
                solutions.append(board)
            else:
                # 所有放置的位置. 注意最大位置不能超过n-1.
                availablePositions = ((1 << n) - 1) & (~(columns | diagonals1 | diagonals2))
                while availablePositions:
                    position = availablePositions & (-availablePositions)       # 取最低位的1.
                    availablePositions = availablePositions & (availablePositions - 1)  # 去掉最低位的1.
                    # column = bin(position - 1).count("1")
                    column = (position-1).bit_length()      # 3.10以上版本可以使用.bit_count()
                    queens[row] = column
                    # 递归. 约束转移
                    solve(row + 1, columns | position, (diagonals1 | position) << 1, (diagonals2 | position) >> 1)

        solutions = list()
        queens = [-1] * n
        row = ["."] * n
        solve(0, 0, 0, 0)
        return solutions

    def solveNQueens(self, n: int) -> List[List[str]]:
        # 1.1 自己的实现
        cols, diag1, diag2 = set(), set(), set()
        state = []
        ans = []
        def record():
            result = [''.join(['Q' if i==c else '.' for i in range(n)]) for c in state]
            ans.append(result)
        def dfs(idx: int):
            if idx == n:
                record(); return
            for i in range(n):
                if i in cols or idx+i in diag1 or idx-i in diag2: continue
                cols.add(i); diag1.add(idx+i); diag2.add(idx-i)
                state.append(i)
                dfs(idx+1)
                state.pop()
                cols.remove(i); diag1.remove(idx+i); diag2.remove(idx-i)
        dfs(0)
        return ans
    """ 0052. N皇后 II 同 0051 """
    def totalNQueens(self, n: int) -> int:
        cols, diag1, diag2 = set(), set(), set()
        state = []
        ans = 0
        def dfs(idx: int):
            nonlocal ans
            if idx == n:
                ans += 1; return
            for i in range(n):
                if i in cols or idx+i in diag1 or idx-i in diag2: continue
                cols.add(i); diag1.add(idx+i); diag2.add(idx-i)
                state.append(i)
                dfs(idx+1)
                state.pop()
                cols.remove(i); diag1.remove(idx+i); diag2.remove(idx-i)
        dfs(0)
        return ans
sol = Solution()
reslts = [
    # sol.letterCasePermutation("abc"),
    # sol.solveNQueens(4),
    # sol.totalNQueens(4),
]
for r in reslts:
    print(r)