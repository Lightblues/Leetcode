import collections
from typing import List
import copy

""" https://leetcode-cn.com/contest/biweekly-contest-66 """

class Solution66:
    """ 2085. 统计出现过一次的公共字符串 """
    def countWords(self, words1: List[str], words2: List[str]) -> int:
        c1 = collections.Counter(words1)
        c2 = collections.Counter(words2)
        words1 = [k for k,v in c1.items() if v==1]
        words2 = [k for k,v in c2.items() if v==1]
        return len(set(words1).intersection(set(words2)))

    """ 2086. 从房屋收集雨水需要的最少水桶数 #题型 #medium #贪心
给定一个字符串, 两种元素表示房屋和空地; 要求在每一栋房屋边上放一个水桶, 最少的数量 (无法安排则返回 -1).
第一次做的时候思路很乱: 尝试一次遍历解答, 用两个指针分别记录最近的一个水桶和最近的一个没有被覆盖的房屋. 但是判断比较复杂.
思路1: 重新做发现了更简单粗暴的思路 (没有必要追求一次遍历, 反正复杂度不要超即可). 也是 #贪心 的思路: 这里能够节省水桶的情况就是其两侧都有房屋. 
因此, 每遇到 `H.H` 的情况就放置一个水桶 (注意 `H.H.H` 这种情况, 要对于以覆盖的房屋进行标记). 这样, 剩余的没有被覆盖的房屋在其相邻的空地放一个水桶即可. 
思路2: 贪心 see [官方答案](https://leetcode-cn.com/problems/minimum-number-of-buckets-required-to-collect-rainwater-from-houses/solution/cong-fang-wu-shou-ji-yu-shui-xu-yao-de-z-w2vj/)
这里的想法更为简洁: 因为实际上, 我们放置冗余水桶的情况只可能为 `.H.H` 这样的特征错放在第一个位置上了. 因此, 贪心只需要 **优先将水桶放在右侧**.
只考虑遍历到房子的情况: 1) 两侧有了, 则不放; 2) 否则, 判断该点的房屋是否可被覆盖, 优先放右侧.
改进: 这里需要记录水桶的放置情况, 1) 可以通过修改数组 (将原本的字符串转为可变结构); 2) 进一步可知, 对于右侧放水桶的情况, 可以直接向前跳两个, 从而避免了修改字符串. 
"""
    def minimumBuckets2(self, street: str) -> int:
        """ [官方答案](https://leetcode-cn.com/problems/minimum-number-of-buckets-required-to-collect-rainwater-from-houses/solution/cong-fang-wu-shou-ji-yu-shui-xu-yao-de-z-w2vj/) """
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

    def minimumBuckets(self, street: str) -> int:
        """ 一个更为粗暴的思路: 先放置两侧都有房子的空地 (贪心). 然后补充其他没有覆盖的房子
        1: 没被覆盖的房子; 2: 水桶; 3: 已经被覆盖的房子
        """
        street = [1 if ch=="H" else 0 for ch in street]
        n = len(street)
        ans = 0
        for i in range(1,n-1):
            if street[i-1:i+2] == [1,0,1]:
                street[i-1:i+2] = [3,2,3]
                ans += 1
        for i in range(n):
            if street[i]==1:
                if i-1>=0 and street[i-1]==0:
                    street[i-1] = 2
                    street[i] = 3
                elif i+1<n and street[i+1]==0:
                    street[i+1] = 2
                    street[i] = 3
                else:
                    return -1
                ans += 1
        return ans

    """ 尝试: 复杂判断 """
    def minimumBuckets_0(self, street: str) -> int:
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

    """ 2088. 统计农场中肥沃金字塔的数目 #hard
给定一个gird, 每个格子 0/1 表示是否肥沃. 定义「肥沃金字塔」为 `.:.` 这种样子的 (高度 > 2). 要求统计所有肥沃金字塔 (还有倒三角也算) 的数目.
解法1: #DP, 参见 [here](https://leetcode-cn.com/problems/count-fertile-pyramids-in-a-land/solution/tong-ji-nong-chang-zhong-fei-wo-jin-zi-t-paok/)
关键在于如何判断一个格子是否是 (以及是多少个) 肥沃金字塔的顶点? 注意到, **一个高度为 h 的金字塔, 其顶点之下的三个元素也必然为高度为 h-1 的金字塔的顶点**. 例如这一观察, 可以得到递归方程.
这样, 一个最大高度为 h 的金字塔, 顶点元素作为金字塔顶点的所有可能为 h-1 个. 为了计算的方便, 定义 dp 矩阵的元素: 
若不合法 -1, 合法则为最大可能三角的 h-1. (也即单一个肥沃格子, 无法构成三角, 定义其元素为 0)
这样, 可以得到统一的递推公式: 当 i,j 位置合法的时候, `dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1]) + 1`. 
思路2: #前缀和 判断底边中心点可以构成几个金字塔
上一种 DP思路聚焦顶点, 我的直觉是看底边可以构成多少金字塔. 注意到, 一个金字塔, 其底边的每个元素之上肥沃土地的数量形如 `12321`. 因此可以从上往下累计每块土地之上的肥沃土地数量 (复杂度 mn).
然后, 对于每一行序列, 例如 `[3,3,3,3,1]`, 我们需要判断以这一行为底边的金字塔数量.
分析可知, 以每个元素为底边中心的金字塔数量为 [0,1,2,1,0]. 如何计算? 我们用左右两个数组来表示当前元素左右的情况.
例如, 这一例子中, left=[0,1,2,2,0], right=[2,2,2,1,0]. 综合这两个约束, 求和可知这一行共包含 4个金字塔.
如何更新这一约束? 以left为例, 初始化 lLimit=-1, 对于位置j的元素有递推公式 `lLimit = min(lLimit+1, v-1)`: 1) 金字塔是阶梯形的; 2) 当前高低为v点的元素为中心最多有 v-1 个金字塔.
"""
    def countPyramids_0(self, grid: List[List[int]]) -> int:
        """ https://leetcode-cn.com/problems/count-fertile-pyramids-in-a-land/solution/tong-ji-nong-chang-zhong-fei-wo-jin-zi-t-paok/ """
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
        # 倒三角
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

    """ 思路2: 判断底边中心点可以构成几个金字塔 """
    def countPyramids(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        def count(grid):
            # 统计每个格子上方的肥沃土地数量
            for i in range(1, m):
                for j in range(n):
                    if grid[i][j] == 0: continue
                    grid[i][j] += grid[i-1][j]
            # 
            """ 例如对于序列 [3,3,3,3,1], 以每个元素为底边中心的金字塔数量为 [0,1,2,1,0]. 我们用左右两个数组来约束计算.
            这一例子中, left=[0,1,2,2,0], right=[2,2,2,1,0].
            """
            ans = 0
            for i in range(1, m):
                line = grid[i]
                left, right = [0]*n, [0]*n
                lLimit = 0
                for j, v in enumerate(line):
                    lLimit = min(lLimit+1, j, v-1)
                    left[j] = lLimit
                # 这样的判断更合理
                rLimit = -1
                for j,v in enumerate(reversed(line)):
                    rLimit = min(rLimit+1, v-1)
                    right[n-j-1] = rLimit
                for l,r in zip(left, right):
                    ans += max(0, min(l,r))
            return ans
        return count(copy.deepcopy(grid)) + count(copy.deepcopy(grid[::-1]))

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

    sol.countPyramids(grid = [[0,1,1,0],[1,1,1,1]]),
]
for r in result:
    print(r)