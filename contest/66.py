import collections
from typing import List

class Solution66:
    """ 2085. 统计出现过一次的公共字符串 """
    def countWords(self, words1: List[str], words2: List[str]) -> int:
        c1 = collections.Counter(words1)
        c2 = collections.Counter(words2)
        words1 = [k for k,v in c1.items() if v==1]
        words2 = [k for k,v in c2.items() if v==1]
        return len(set(words1).intersection(set(words2)))

    """ 2086. 从房屋收集雨水需要的最少水桶数 """
    """ 解法一 贪心 see https://leetcode-cn.com/problems/minimum-number-of-buckets-required-to-collect-rainwater-from-houses/solution/cong-fang-wu-shou-ji-yu-shui-xu-yao-de-z-w2vj/ 
    只考虑遍历到房子的情况
    - 两侧有了, 则不放
    - 否则, 优先放右侧 
    可以通过直接修改 grid 来记录水桶的位置. 官答中提出, 对于右侧放水桶的情况, 可以直接向前跳两个, 从而避免了修改字符串. """
    def minimumBuckets2(self, street: str) -> int:
        street = list(street)
        count = 0
        for i in range(len(street)):
            if street[i] == 'H':
                if i-1>=0 and street[i-1] == 'B':
                    continue
                if i+1<=len(street) and street[i+1] == '.':
                    street[i+1] = 'B'
                    count += 1
                elif i-1>=0 and street[i-1] == '.':
                    street[i-1] = 'B'
                    count += 1
                else:
                    return -1
        return count

    """ 尝试: 复杂判断 """
    def minimumBuckets(self, street: str) -> int:
        count = 0
        lastH = lastB = -2
        # lastH 记录最近一个没有覆盖的房子; lastB 记录最近一个桶的位置
        for i in range(len(street)):
            if street[i] == 'H':
                if lastH == i-1:
                    if i-2>=0 and street[i-2] == '.':
                        count += 1
                        lastB = i-2
                        lastH = i
                    else:
                        return -1
                else:
                    if lastB != i-1:
                        lastH = i
            else:       # .
                if lastH == i-1:
                    count += 1
                    lastH = -2
                    lastB = i
        # 最后一个位置
        if lastH != -2:
            if len(street) == 1:
                return -1
            if street[-2] == 'H':
                return -1
            else:
                if lastB == len(street)-2:
                    return count
                else:
                    return count+1
        return count

    """ 2087. 网格图中机器人回家的最小代价 """
    def minCost(self, startPos: List[int], homePos: List[int], rowCosts: List[int], colCosts: List[int]) -> int:
        sx, sy = startPos
        hx, hy = homePos
        if sx < hx:
            rows = list(range(sx+1, hx+1))
        else:
            rows = list(range(hx, sx))
        if sy < hy:
            cols = list(range(sy+1, hy+1))
        else:
            cols = list(range(hy, sy))
        print(rows, cols)
        return sum([rowCosts[r] for r in rows]) + sum([colCosts[c] for c in cols])

    """ 2088. 统计农场中肥沃金字塔的数目 
    统计 grid 中的所有三角/倒三角
    解法: DP, 参见 https://leetcode-cn.com/problems/count-fertile-pyramids-in-a-land/solution/tong-ji-nong-chang-zhong-fei-wo-jin-zi-t-paok/ 
    定义 dp 矩阵的元素: 若不合法 -1, 合法则为最大可能三角的 h-1, 也即单一个合法格子, 无法构成三角, 定义其元素为 0
    递推公式: 当 i,j 位置合法的时候, 正三角 `dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1]) + 1` 可知之前定义的 -1 配合这里的更新公式是合理的. """
    def countPyramids(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dp = [[0]*n for _ in range(m)]
        result = 0
        for i in range(m-1, -1, -1):
            for j in range(n):
                if grid[i][j] == 0:
                    dp[i][j] = -1
                elif i==m-1 or j==0 or j==n-1:
                    dp[i][j] = 0
                else:
                    dp[i][j] = min(dp[i+1][j-1], dp[i+1][j], dp[i+1][j+1]) + 1
                    result += dp[i][j]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    dp[i][j] = -1
                elif i==0 or j==0 or j==n-1:
                    dp[i][j] = 0
                else:
                    dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1]) + 1
                    result += dp[i][j]
        return result


sol = Solution66()
result = [
    # 66
    # sol.countWords(words1 = ["leetcode","is","amazing","as","is"], words2 = ["amazing","leetcode","is"]),

    # sol.minCost(startPos = [1, 0], homePos = [2, 3], rowCosts = [5, 4, 3], colCosts = [8, 2, 6, 7]),
    # sol.minCost(startPos = [0, 0], homePos = [0, 0], rowCosts = [5], colCosts = [26]),
    
    # sol.minimumBuckets("H..H"),
    # sol.minimumBuckets(".HHH."),
    # sol.minimumBuckets(".......HH"),
    # sol.minimumBuckets2(".HH.H.H.H.."),

    # sol.countPyramids(grid = [[0,1,1,0],[1,1,1,1]]),
]
for r in result:
    print(r)