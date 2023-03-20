from easonsi import utils
from easonsi.util.leetcode import *

""" 回溯
https://oi-wiki.org/search/backtracking/
[灵神](https://www.bilibili.com/video/BV1mG4y1A7Gu/)
wiki [Backtracking](https://en.wikipedia.org/wiki/Backtracking)

== 子集型
枚举每个位置的可能情况
0017. 电话号码的字母组合 #medium 给定一个数字按键 (映射), 对于一串按下的数字, 问它可能对应的字符串有哪些?
0078. 子集 #medium #题型 给定一组不含重复元素的整数数组 nums, 返回该数组所有可能的子集 (幂集). 注意避免重复. 限制: n<=10 
    1.1 输入的视角（选或不选） dfs(i) 中考虑第i个元素是否加入答案
    1.2 答案的视角（选哪个数） dfs(i) 中固定 [0...i-1] 中所选, 枚举下一个是 i,i+1...
0131. 分割回文串 #medium 将一个字符串分割成一些回文串, 返回所有的可能.
0784. 字母大小写全排列 #medium 对于一个字符串中的所有英文字母, 组合其大小写可以有多种结果, 返回所有可能的结果. 限制: 字符串长度 n 12

"""

class Solution:
    """ 0017. 电话号码的字母组合 #medium 给定一个数字按键 (映射), 对于一串按下的数字, 问它可能对应的字符串有哪些? 限制: n<=4
思路1: #回溯
    注意, 区别于一般的递归问题, 这里的递归深度 (for的数量) 是不确定的, 需要用 回溯; 确定边界条件
    复杂度: O(n 4^n). 每次转移最多生成4个节点; 递归过程生成答案的复杂度为 O(n)
"""
    def letterCombinations(self, digits: str) -> List[str]:
        MAPPING = ("", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz")
        
        n = len(digits)
        # 边界
        if n == 0: return []
        ans = []
        path = [''] * n     # 记录当前路径
        def dfs(i: int) -> None:
            """ 递归/回溯函数. 重点包含 1] 终止条件; 2] 递归搜索, 也即调用 dfs(i) 自己 """
            if i == n:
                # 回溯终止条件! 将答案记录下来
                ans.append(''.join(path))
                return
            # 递归往下进行搜索
            for c in MAPPING[int(digits[i])]:
                path[i] = c     # 记录当前的路径
                dfs(i + 1)
                # 一般回溯还需要「恢复现场」, 不过这题中没有必要写
                # path[i] = ''
        # 开始进行搜索/递归
        dfs(0)
        return ans

    """ 0078. 子集 #medium #题型 给定一组不含重复元素的整数数组 nums, 返回该数组所有可能的子集 (幂集). 注意避免重复. 限制: n<=10 
思路1: 回溯. 复杂度 O(n 2^n)
    1.1 输入的视角（选或不选） dfs(i) 中考虑第i个元素是否加入答案
    1.2 答案的视角（选哪个数） dfs(i) 中固定 [0...i-1] 中所选, 枚举下一个是 i,i+1...
"""
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # 1.1 输入的视角（选或不选） dfs(i) 中考虑第i个元素是否加入答案
        ans = []
        path = []
        n = len(nums)
        def dfs(i: int) -> None:
            if i == n:
                ans.append(path.copy())  # 固定答案
                return
            # 不选 nums[i]
            dfs(i + 1)
            # 选 nums[i]
            path.append(nums[i])
            dfs(i + 1)
            path.pop()  # 恢复现场
        dfs(0)
        return ans
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # 1.2 答案的视角（选哪个数） dfs(i) 中固定 [0...i-1] 中所选, 枚举下一个是 i,i+1...
        ans = []
        path = []
        n = len(nums)
        def dfs(i: int) -> None:
            ans.append(path.copy())  # 固定答案
            if i == n:
                return
            for j in range(i, n):  # 枚举选择的数字
                path.append(nums[j])
                dfs(j + 1)
                path.pop()  # 恢复现场
        dfs(0)
        return ans


    """ 0131. 分割回文串 #medium 将一个字符串分割成一些回文串, 返回所有的可能. 限制: n<=16
思路1: 回溯. 复杂度 O(n 2^n). 状态数 O(2^n), 检查回文、生成答案都是 O(n)
    1.1 输入的视角（选或不选）
    1.2 答案的视角（枚举子串结束位置）
"""
    def partition(self, s: str) -> List[List[str]]:
        # 1.1 输入的视角（选或不选）
        n = len(s)
        ans = []
        path = []
        def dfs(i,start):
            # 当前片段为 [start...i]
            if i==n:
                ans.append(path[:]); return
            # 将当前片段继续延伸
            if i<n-1:
                dfs(i+1,start)
            # 尝试将当前片段放入
            t = s[start:i+1]
            if t==t[::-1]:
                path.append(t)
                dfs(i+1,i+1)
                path.pop()
        dfs(0,0)
        return ans
    def partition(self, s: str) -> List[List[str]]:
        # 1.2 答案的视角（枚举子串结束位置）
        n = len(s)
        ans = []
        path = []
        def dfs(i):
            if i==n:
                ans.append(path[:]); return
            for j in range(i,n):
                t = s[i:j+1]
                if t==t[::-1]:
                    path.append(t)
                    dfs(j+1)
                    path.pop()
        dfs(0)
        return ans
    
    
    """ 0784. 字母大小写全排列 #medium 对于一个字符串中的所有英文字母, 组合其大小写可以有多种结果, 返回所有可能的结果. 限制: 字符串长度 n 12
思路1: 回溯. 复杂度 O(2^n n). 代码同上
思路2: 直接构造, 可以写成 #迭代 的形式.
    复杂度: `O(2^n n)`
思路3: 可以借助 #itertools 写成 #笛卡尔积 product 的形式, 简化.
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
    def letterCasePermutation(self, S):
        # 思路1: 回溯. 复杂度 O(2^n n)
        letters = list(S)
        n = len(letters)
        ans = []
        def dfs(i):
            if i==n: ans.append("".join(letters)); return
            if letters[i].isalpha():
                letters[i] = letters[i].lower()
                dfs(i+1)
                letters[i] = letters[i].upper()
                dfs(i+1)
            else:
                dfs(i+1)
        dfs(0)
        return ans

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
    
    # sol.partition(s = "aab"),
    sol.letterCasePermutation("a1b2"),
]
for r in reslts:
    print(r)