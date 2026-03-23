from typing import *

""" 
https://leetcode.cn/contest/weekly-contest-447
Easonsi @2025 """
class Solution:
    def countCoveredBuildings(self, n: int, buildings: List[List[int]]) -> int:
        # 对每一行/每一列, 记录该行/列上建筑坐标的最小值和最大值
        # 一个建筑 (x, y) 被覆盖 ⟺
        #   同一列(x相同)存在 y' < y 和 y'' > y  (上下方向)
        #   同一行(y相同)存在 x' < x 和 x'' > x  (左右方向)
        # 等价于: x 严格在该列 x 范围内部, y 严格在该行 y 范围内部
        row_min = {}  # row -> (min_x, max_x)  同一行 y 相同, 记录 x 的范围
        col_min = {}  # col -> (min_y, max_y)  同一列 x 相同, 记录 y 的范围
        for x, y in buildings:
            if y not in row_min:
                row_min[y] = (x, x)
            else:
                row_min[y] = (min(row_min[y][0], x), max(row_min[y][1], x))
            if x not in col_min:
                col_min[x] = (y, y)
            else:
                col_min[x] = (min(col_min[x][0], y), max(col_min[x][1], y))
        ans = 0
        for x, y in buildings:
            # 左右: 同行(y相同)中, x 严格在 (min_x, max_x) 内部
            # 上下: 同列(x相同)中, y 严格在 (min_y, max_y) 内部
            rmin, rmax = row_min[y]
            cmin, cmax = col_min[x]
            if rmin < x < rmax and cmin < y < cmax:
                ans += 1
        return ans


    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[bool]:
        # nums 已按非递减排序, 相邻元素差 <= maxDiff 则连通
        # 扫描一遍, 给每个节点分配连通分量编号
        comp = [0] * n
        for i in range(1, n):
            if nums[i] - nums[i - 1] > maxDiff:
                comp[i] = comp[i - 1] + 1
            else:
                comp[i] = comp[i - 1]
        return [comp[u] == comp[v] for u, v in queries]

# 测试用例
sol = Solution()
result = [
]
for r in result:
    print(r)
