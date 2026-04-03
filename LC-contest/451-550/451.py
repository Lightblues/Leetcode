from typing import *

"""
https://leetcode.cn/contest/weekly-contest-451
Easonsi @2025 """


class Solution:
    """
    有两根木材长度 n, m，三辆卡车每辆最多装一根长度 <= k 的木材。
    可以切割木材，切割长度为 x 的木材成 len1, len2 的代价为 len1 * len2。
    返回最小总代价。

    分析:
    - 3辆卡车 + 2根木材 → 最多只需要切一刀（1根变2段，共3段用3辆卡车）
    - 若 n <= k 且 m <= k，不需要切割，代价 = 0
    - 若只有一根超过 k，必须切那根
    - 切 x 成两段（其中一段 <= k），最优方案：
        令 len2 = k，len1 = x - k，代价 = (x - k) * k
        （因为 len1 * len2 = len1 * (x - len1) 在端点处最小）
    - 若两根都超过 k：无法用3辆卡车只切一刀装完（不可能，题目保证有解）
    """
    def minCuttingCost(self, n: int, m: int, k: int) -> int:
        if n <= k and m <= k:
            return 0
        elif n > k and m <= k:
            return (n - k) * k
        elif m > k and n <= k:
            return (m - k) * k
        else:
            # both > k: need to cut both, pick the cheaper one
            # but with 3 trucks we can only have 3 pieces total
            # cut the shorter one: keep 1 piece of the other (it must be <= k, contradiction)
            # actually impossible per constraints, but handle gracefully
            return min((n - k) * k, (m - k) * k)

    def resultingString(self, s: str) -> str:



sol = Solution()
result = [
    sol.minCuttingCost(5, 3, 3),   # n>k, m<=k → (5-3)*3=6
    sol.minCuttingCost(3, 5, 3),   # n<=k, m>k → (5-3)*3=6
    sol.minCuttingCost(2, 2, 3),   # both<=k   → 0
    sol.minCuttingCost(4, 4, 3),   # both>k    → (4-3)*3=3
]
for r in result:
    print(r)
