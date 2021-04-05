"""
返回 n 皇后解决方案的数量
"""

class Solution:
    """
    采用三个集合，来记录每一列/斜线位置是否已有皇后。这样可以将 is_valid 判断减小复杂度到 O(1)
    注意，因为只需要输出综述，就不需要「棋盘」的概念了
    """
    def totalNQueens(self, n: int) -> int:
        columns = set()
        diagonal1 = set()
        diagonal2 = set()
        def dfs(row):
            # 说明 n 行全部填充成功
            if row == n:
                return 1
            else:
                count = 0
                for col in range(n):
                    if col in columns or row-col in diagonal1 or row+col in diagonal2:
                        continue
                    columns.add(col)
                    diagonal1.add(row-col)
                    diagonal2.add(row+col)
                    count += dfs(row+1)
                    columns.remove(col)
                    diagonal1.remove(row-col)
                    diagonal2.remove(row+col)
                return count
        return dfs(0)


    def totalNQueens2(self, n: int) -> int:
        def solve(row, columnes, diagonal1, diagonal2):
            if row == n:
                return 1
            else:
                count = 0
                availavle_positions = ((1<<n)-1) & (~(columnes | diagonal1 | diagonal2))
                while availavle_positions:
                    position = availavle_positions & (-availavle_positions)
                    availavle_positions = availavle_positions & (availavle_positions-1)
                    count += solve(row+1, columnes|position, (diagonal1|position)<<1, (diagonal2|position)>>1)
                return count
        return solve(0, 0, 0, 0)

print(Solution().totalNQueens(4))
print(Solution().totalNQueens2(4))
