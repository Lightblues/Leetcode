from typing import *
import math

""" 
https://leetcode.cn/contest/weekly-contest-436

T2 调和级数枚举
T3 整除类型的 DP 非常值得学习!
T4 二分 + 贪心 也非常精彩

Easonsi @2025 """
class Solution:
    """ 3446. 按对角线进行矩阵排序 #medium 对于上三角, 按照对角线方向排序; 对于下三角逆序.
参考: [ling](https://leetcode.cn/problems/sort-matrix-by-diagonals/solutions/3068709/mo-ban-mei-ju-dui-jiao-xian-pythonjavacg-pjxp/)
 """
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        n = len(grid)
        # upper triangle
        for j in range(1,n):  # 包括主对角线
            line = []
            for i in range(n-j):
                line.append(grid[i][j+i])
            line.sort()
            for i in range(n-j):
                grid[i][j+i] = line[i]
        # lower triangle
        for i in range(n):
            line = []
            for j in range(n-i):
                line.append(grid[i+j][j])
            line.sort(reverse=True)
            for j in range(n-i):
                grid[i+j][j] = line[j]
        return grid
    
    """ 3447. 将元素分配给有约束条件的组 #medium 给定一组数字, 对于每个数字x, 找到elements里面最早出现的x的因子.
限制: n 1e5; K 1e5
思路1: #预处理 + #调和级数 枚举
    假设groups里面的数字最大为 mx, 考虑直接从左到右枚举elements
        用 target[j] 表示其第j个元素可以被整除的最左侧因子.
        枚举 x = elements[i], 我们直接将 y = x, 2x, ... 位置的target更新为 i.
    避免重复标记? 初始化 target=-1, 遇到 target[x] != -1 则跳过. (前面已经枚举或者其因子已经被枚举)
    复杂度: 核心是调和级数枚举, 复杂度为 O(n log mx), 其中n为elements的长度
     """
    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:
        mx = max(groups)
        target = [-1]*(mx+1)
        for i,x in enumerate(elements):
            if x>mx or target[x]>=0: continue
            for y in range(x, mx+1, x):
                if target[y] == -1:
                    target[y] = i
        return [target[x] for x in groups]
    
    """ 3448. 统计可以被最后一个数位整除的子字符串数目 #hard 给定一个数字字符串, 问其子串中, 结尾不为0, 且其可以被最后一位整除的子串数量.
限制: n 1e5; 可以有前导0
思路1: #数学 #DP
    推导: 假设s的第i为数字为 s[i], 某一位置开始到i位置的子串数字为 v[i], 根据 v[i] =  v[i-1]*10 + s[i] 可以得到, 约束为:
        (v[i-1]*10 + s[i]) mod s[i] = 0
    - 注意到, 数值v不重要! 重要的关于除数的余数 rem
        (rem[i-1]*10 + s[i]) mod s[i] = 0
    - 启发采用 #DP 来统计, #刷表法
        记 f[i+1][m][rem] 表示以 s[i] 结尾的, 关于m余数为rem的子串数量
        转移方程: 对于 s[i] 和除数 m, 有:
            f[i+1][m][(rem*10+s[i]) mod m] += f[i][m][rem], #刷表法
        初始值: f[i+1][m][s[i] mod m] = 1, 也即单独的 s[i]
        - 在前向过程中, 可以去掉第一个维度, #滚动数组 优化
    复杂度: O(n D^2)
    [ling](https://leetcode.cn/problems/count-substrings-divisible-by-last-digit/solutions/3068623/gong-shi-tui-dao-dong-tai-gui-hua-python-iw4a/)
 """
    def countSubstrings(self, s: str) -> int:
        ans = 0
        f = [[0]*9 for _ in range(10)]
        for d in map(int, s):
            nf = [[0]*9 for _ in range(10)]  # 新的DP表, 事实上可以是一维的 (更新 f[m])
            for m in range(1, 10):  # 枚举除数, 注意 !=0
                nf[m][d%m] = 1
                for rem in range(m):  # 枚举余数
                    nf[m][(rem*10+d)%m] += f[m][rem]
            f = nf
            ans += f[d][0]
        return ans
    
    """ 3449. 最大化游戏分数的最小值 #hard 每个位置有分数 points[i], 你开始在 -1 位置, 共m次操作机会, 每次可以选择坐标+1/-1, 并将 scores[i] += points[i].
要求经过m次操作后, 最大化 min(scores). 限制: n 5e4; m 1e9
思路1: #二分 + #贪心
    注意到, 对于任意的移动操作, 可以将它们分解为 "最多回退一步" 的动作序列. 
    因此, 可以在 O(n) 的时间内进行一次check操作.
        check 操作: 对于目标值 t, 需要 s = ceil(t / point[i]) 次到达该点.
            (i==0) 从 -1 到0, 然后经过 1 位置 s-1 次, 最后回到 0; 共 2s-1 次操作
            (i>0) 的时候, s 需要先减去此前的步骤
    外层, 二分答案即可
    复杂度: O(n log mx)
    [ling](https://leetcode.cn/problems/maximize-the-minimum-game-score/solutions/3068672/er-fen-da-an-cong-zuo-dao-you-tan-xin-py-3bhl/)
 """
    def maxScore(self, points: List[int], m: int) -> int:
        def check(t:int) -> bool:
            if t==0: return True
            n = len(points)
            rem = m
            pre = 0
            for i,x in enumerate(points):
                s = math.ceil(t/x) - pre
                if s<=0:
                    if i == n-1: return True  # 到达终点! 不需要那一步了!
                    pre = 0
                    rem -= 1
                else:
                    pre = s-1
                    rem -= 2*s-1
                if rem<0: return False
            return True
        l = 0
        r = min(points) * (m+1)//2  # 最小值最多经过 (m+1)//2 次
        ans = 0
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                l = mid+1
            else:
                r = mid-1
        return ans



sol = Solution()
result = [
    # sol.sortMatrix(grid = [[1,7,3],[9,8,2],[4,5,6]]),
    # sol.assignElements(groups = [8,4,3,2,4], elements = [4,2]),
    # sol.countSubstrings(s = "12936"),
    # sol.countSubstrings(s = "5701283"),
    sol.maxScore(points = [2,4], m = 3),
    sol.maxScore(points = [1,2,3], m = 5),
]
for r in result:
    print(r)
