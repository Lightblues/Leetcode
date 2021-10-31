"""
给定一个二维网格和一个单词，找出该单词是否存在于网格中。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

board =
[
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]

给定 word = "ABCCED", 返回 true
给定 word = "SEE", 返回 true
给定 word = "ABCB", 返回 false

"""
from typing import List
"""
原本的想法是从每一个可能的字符出发搜索，但这样很难避免「无法使用重复单元」
"""
class Solution_try:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        # wordL = len(word)
        directs = [
            (1,0),
            (-1,0),
            (0,1),
            (0,-1)
        ]
        def findChar(r, c, ch):
            res = []
            for x,y in directs:
                if 0 <= r+x < m and 0 <= c+y < n and board[r+x][c+y]==ch:
                    res.append((r+x, c+y))
            return res
        potentials = []
        for r in range(m):
            for c in range(n):
                if board[r][c] == word[0]:
                    potentials.append((r,c))
        for ch in word[1:]:
            new = [findChar(r, c, ch) for r,c in potentials]
            potentials = [i for l in new for i in l]
            if not potentials:
                return False
        return True

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        wordL = len(word)
        directs = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]
        visited = [[False]*n for _ in range(m)]
        def check(i, j , k):
            for di, dj in directs:
                ni, nj = i+di, j+dj
                if 0<=ni<m and 0<=nj<n and not visited[ni][nj] and board[ni][nj]==word[k]:
                    if k==wordL-1:
                        return True
                    visited[ni][nj] = True
                    if check(ni, nj, k+1):
                        return True
                    visited[ni][nj] = False
            return False
        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0]:
                    # word 长度为 1
                    # 因此官答中是不进行判断 board[i][j] == word[0]，直接调用 check(i,j, 0) 的
                    if wordL==1:
                        return True
                    visited[i][j] = True
                    if check(i,j, 1):
                        return True
                    visited[i][j] = False
        return False


board = [
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]
# word = "ABCCED"
word = "ABCB"

# board = [["a"]]
# word = 'a'
print(Solution().exist(board, word))