from typing import *

""" 
https://leetcode.cn/contest/weekly-contest-448
Easonsi @2025 """
class Solution:
    def maxProduct(self, n: int) -> int:
        digits = sorted((int(c) for c in str(n)), reverse=True)
        return digits[0] * digits[1]
    
    def specialGrid(self, n: int) -> List[List[int]]:
        if n == 0:
            return [[0]]
        size = 1 << n  # 2^n
        half = size // 2
        sub = self.specialGrid(n - 1)
        quarter = half * half  # number of cells per quadrant
        # Order: top-right(0), bottom-right(1), bottom-left(2), top-left(3)
        grid = [[0] * size for _ in range(size)]
        for i in range(half):
            for j in range(half):
                grid[i][j + half]     = sub[i][j]                  # top-right: offset 0
                grid[i + half][j + half] = sub[i][j] + quarter      # bottom-right: offset 1
                grid[i + half][j]     = sub[i][j] + 2 * quarter    # bottom-left: offset 2
                grid[i][j]            = sub[i][j] + 3 * quarter    # top-left: offset 3
        return grid

    def minTravelTime(self, l: int, n: int, k: int, position: List[int], time: List[int]) -> int:
        denavopelu = (l, n, k, position, time)
        # When markers are deleted, their times cascade RIGHT.
        # For consecutive kept markers ..., a, b, c, ...:
        #   rate at b = sum(time[a+1..b])  (accumulated from deletions between a and b)
        #   cost of segment [b, c] = rate_at_b * (pos[c] - pos[b])
        # Special case: rate at marker 0 = time[0] (nothing cascades from the left)
        #   i.e., rate at k_0=0 = time[0], cost of [0, k_1] = time[0] * (pos[k_1] - pos[0])
        # Times cascading into the last marker (n-1) are unused (no segment after it).
        
        from functools import lru_cache
        P = position
        # prefix sum: S[i] = time[0] + time[1] + ... + time[i]
        S = [0] * n
        S[0] = time[0]
        for i in range(1, n):
            S[i] = S[i-1] + time[i]
        
        @lru_cache(maxsize=None)
        def dp(prev, cur, rem):
            """min cost from segment starting at cur to the end.
            prev = previous kept marker index (-1 means virtual, so rate at cur=0 is time[0]).
            cur = current kept marker index.
            rem = remaining deletions to perform among markers cur+1..n-2.
            """
            # rate at cur
            if prev == -1:
                rate = time[0]  # cur must be 0
            else:
                rate = S[cur] - S[prev]  # sum(time[prev+1..cur])
            
            if cur == n - 1:
                return 0 if rem == 0 else float('inf')
            
            best = float('inf')
            for nxt in range(cur + 1, n):
                deletions = nxt - cur - 1
                if deletions > rem:
                    break
                # If nxt < n-1, it's a kept interior marker
                # If nxt == n-1, it's the last marker
                seg_cost = rate * (P[nxt] - P[cur])
                rest = dp(cur, nxt, rem - deletions)
                if rest < float('inf'):
                    best = min(best, seg_cost + rest)
            return best
        
        return dp(-1, 0, k)

    
sol = Solution()
result = [
    sol.minTravelTime(10, 4, 1, [0,3,8,10], [5,8,3,6]),  # expected 62
]
for r in result:
    print(r)
