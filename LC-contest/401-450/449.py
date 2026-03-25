from typing import *

""" 
https://leetcode.cn/contest/weekly-contest-449
Easonsi @2025 """
class Solution:
    """  """
    def minDeletion(self, s: str, k: int) -> int:
        from collections import Counter
        freq = sorted(Counter(s).values())  # 按频次升序排列
        res = 0
        # 需要删掉 len(freq) - k 个不同字符，贪心删频次最小的
        while len(freq) > k:
            res += freq.pop(0)
        return res

    """ 水平/垂直切一刀分两部分, 和相等 或 最多移除一个cell使相等(移除后仍连通)
    关键: m×n矩形(m≥2,n≥2)是2-连通的, 删任意一个点仍连通
    单行/单列只能删端点 """
    def canPartitionGrid(self, grid: List[List[int]]) -> bool:
        import bisect
        from collections import defaultdict
        hastrelvim = grid
        m, n = len(hastrelvim), len(hastrelvim[0])
        total = sum(sum(row) for row in hastrelvim)

        # 预处理: 每个值出现在哪些行/列
        val_in_rows = defaultdict(list)
        val_in_cols = defaultdict(list)
        seen_rows = defaultdict(set)
        seen_cols = defaultdict(set)
        for i in range(m):
            for j in range(n):
                v = hastrelvim[i][j]
                if i not in seen_rows[v]:
                    seen_rows[v].add(i)
                    val_in_rows[v].append(i)
                if j not in seen_cols[v]:
                    seen_cols[v].add(j)
                    val_in_cols[v].append(j)
        for v in val_in_rows:
            val_in_rows[v].sort()
        for v in val_in_cols:
            val_in_cols[v].sort()

        def has_val_in_row_range(val, r1, r2):
            if val not in val_in_rows: return False
            rows = val_in_rows[val]
            idx = bisect.bisect_left(rows, r1)
            return idx < len(rows) and rows[idx] <= r2

        def has_val_in_col_range(val, c1, c2):
            if val not in val_in_cols: return False
            cols = val_in_cols[val]
            idx = bisect.bisect_left(cols, c1)
            return idx < len(cols) and cols[idx] <= c2

        def can_remove(diff, r1, r2, c1, c2):
            h, w = r2 - r1 + 1, c2 - c1 + 1
            if h == 1 and w == 1: return False
            if h >= 2 and w >= 2:
                # 2-连通, 删任意cell都连通
                if c1 == 0 and c2 == n - 1:
                    return has_val_in_row_range(diff, r1, r2)
                else:
                    return has_val_in_col_range(diff, c1, c2)
            if h == 1:  # 单行, 只能删端点
                return hastrelvim[r1][c1] == diff or hastrelvim[r1][c2] == diff
            # w == 1, 单列, 只能删端点
            return hastrelvim[r1][c1] == diff or hastrelvim[r2][c1] == diff

        # 水平切割: 在第i行后切
        row_sums = [sum(row) for row in hastrelvim]
        top = 0
        for i in range(m - 1):
            top += row_sums[i]
            bot = total - top
            if top == bot: return True
            diff = abs(top - bot)
            if top > bot:
                if can_remove(diff, 0, i, 0, n - 1): return True
            else:
                if can_remove(diff, i + 1, m - 1, 0, n - 1): return True

        # 垂直切割: 在第j列后切
        col_sums = [sum(hastrelvim[i][j] for i in range(m)) for j in range(n)]
        left = 0
        for j in range(n - 1):
            left += col_sums[j]
            right = total - left
            if left == right: return True
            diff = abs(left - right)
            if left > right:
                if can_remove(diff, 0, m - 1, 0, j): return True
            else:
                if can_remove(diff, 0, m - 1, j + 1, n - 1): return True

        return False

    """ 每个节点最多连2个 -> 连通图只能是 路径 或 环
    最大化 sum(a_i * a_{i+1}): 交错排列 [1,3,5,..., ...,6,4,2]
    把最大的两个值放在相邻中心位置, 依次向两侧递减 """
    def maxScore(self, n: int, edges: List[List[int]]) -> int:
        zanthorime = (n, edges)
        m = len(zanthorime[1])
        is_cycle = (m == n)
        # 最优排列: 奇数升序 + 偶数降序 -> [1, 3, 5, ..., ..., 6, 4, 2]
        odds = list(range(1, n + 1, 2))
        evens = list(range(2, n + 1, 2))
        arr = odds + evens[::-1]
        score = sum(arr[i] * arr[i + 1] for i in range(n - 1))
        if is_cycle:
            score += arr[0] * arr[-1]
        return score


sol = Solution()
result = [
    
]
for r in result:
    print(r)
