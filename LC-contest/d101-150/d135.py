from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/biweekly-contest-135
T3, T4 是都 #题型
T3 需要一步非常精妙的思路转换! 
T4 的DP分析非常精彩! 参见下面的数学题解. -- 真的, DP就是对于问题的"建模"
Easonsi @2025 """
class Solution:
    """ 3222. 求出硬币游戏的赢家 """
    def winningPlayer(self, x: int, y: int) -> str:
        v = min(x, y//4)
        return "Alice" if v%2 else "Bob"
    
    """ 3223. 操作后字符串的最短长度 """
    def minimumLength(self, s: str) -> int:
        cnt = Counter(s)
        ans = 0
        for v in cnt.values():
            if v<=2: ans += v
            else: ans += 2 if (v%2==0) else 1
        return ans
    
    """ 3224. 使差值相等的最少数组改动次数 #medium 对于一个长度为偶数数组, 所有元素都在 [0,K] 范围内, 问最少修改几个位置 (只能修改到 [0,K] 范围内), 使得 (i, n-1-i) 对应位置元素差值都相等
限制: n 1e5; K 1e5
思路1: 枚举X
    先考虑 "什么情况下, 数对 (p, q) 需要改 2 次, 使得差值为 X?" 其中 p<=q
        需要满足 1) q < X; 2) (k-p) < X
        可以总结为 max(q, k-p) < X
    -- 也即两个数字都靠中间的情况! 需要修改 0/1 次的case条件比较好判断.
        * 另外, 注意其他两种情况下, 上面的不等式都不成立!
    我们用两个数组 cnt1, cnt2 分别记录 q-p, max(q, k-p) 的次数
    然后枚举目标差值 X, 则需要修改的次数为
        n/2 - cnt1[X] + sum(cnt2[i] for i in range(X))
        对于最后一部分, 可以for循环来优化掉
    复杂度: O(n+k)
思路2: #查分数组 来统计修改到差值X所需的次数
    另一个角度, 考虑对一个数对 (p,q) 将其差值修改为X所需的操作数? 0/1/2 
    记 x=p-q, y=max(q, k-p), 则有:
        [0,x-1] 范围内 -> 1
        x -> 0
        [x+1,y] -> 1
        [y+1,K] -> 2
    我们可以用差分数组来记录这些区间更新操作! 
ling: https://leetcode.cn/problems/minimum-array-changes-to-make-differences-equal/solutions/2851502/mei-ju-x-fen-lei-tao-lun-pythonjavacgo-b-puh2/
    """
    def minChanges(self, nums: List[int], k: int) -> int:
        n = len(nums)
        cnt1 = [0] * (k+1)
        cnt2 = [0] * (k+1)
        for i in range(n//2):
            p, q = nums[i], nums[n-1-i]
            if p>q: p, q = q, p
            cnt1[q-p] += 1
            cnt2[max(q, k-p)] += 1
        ans = n
        s = 0
        for c1, c2 in zip(cnt1, cnt2):
            ans = min(ans, n//2 - c1 + s)
            s += c2
        return ans

    """ 3225. 网格图操作后的最大分数 #hard 给定一个正方形, 每个格子有一定分数, 对于每一列可以指定往下涂黑到某一行 (格子). 最终的分数为 sum{白色&左右至少有一个黑色}, 求最大分数
限制: n 100
思路1: #DP
    记 f(j,i) 表示第j列涂到第i行, 前缀的 j+1 列的分数和! 
        注意到, 现在不会有三列为空, 我们只需要考虑转移 j-1, j-2, j-3. 
        以下记 s(j, i1,i2) 为j列 [i1...i2] 的分数和
    (1.1) j-1 列涂到 i' 且 i' < i, 
        此时减少 s(j, 0, i'), 增加 s(j+1, 0, i)
        对于 j-1 列呢? 注意到 j-2列一定不能 >i' -- 否则可以去除 j-1 列, 得到更优解! (也即, 黑色的区域一定是倒着的一组 "山峰", 而不会是凹的)
        -- 因此, 我们事实上需要增加一个DP的维度, f(j,i,k=0/1) 表示j列比前一列低还是高
        总之, 有转移 f(j,i,1) = f(j-1,i'<=i,1) - s(j, 0, i') + s(j+1, 0, i) + s(j-1, i'+1, i)
    (1.2) j-1 列涂到 i' 且 i' > i, 此时减少 s(j, 0, i), 增加 s(j+1, 0, i)
        f(j,i,0) = f(j-1,i'>i,0<=t<=1) - s(j, 0, i) + s(j+1, 0, i)
        -- 注意, 在这种情况下, 我们不需要关心j-1和j-2列的关系!
    (2.1) j-2 列涂到 i' 且 i' < i, 增加j-1列多的部分和j+1列
        f(j,i,1) = f(j-2,i'<=i,0<=t<=1) + s(j-1, i'+1, i) + s(j+1, 0, i)
    (2.2) j-2 列涂到 i' 且 i' > i, 增加j+1列多的部分
        f(j,i,0) = f(j-2,i'>i,0<=t<=1) + s(j+1, 0, i)
    (3) j-3 列涂到 i', 增加两侧的
        f(j,i,1) = f(j-3,i',0<=t<=1) + s(j-1, 0, i) + s(j+1, 0, i)
    (4) 这是第一个操作的列
        f(j,i,1) = s(j-1, 0, i) + s(j+1, 0, i)
    答案: 所有情况取max, max(f(j,i,0/1))
    复杂度: O(n^3)
TsPaper: https://leetcode.cn/problems/maximum-score-from-grid-operations/
ling: https://leetcode.cn/problems/maximum-score-from-grid-operations/solutions/2852362/tu-jie-dp-ji-qi-you-hua-by-endlesscheng-pco6/
    """
    def maximumScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # presum (reverse i&j, index start from 1)
        sm = [[0]*(n+1) for _ in range(n+2)] # j列前后两个哨兵! , acc从1开始
        for j in range(1, n+1):
            for i in range(1, n+1):
                sm[j][i] = sm[j][i-1] + grid[i-1][j-1]
        def s(j, i1, i2):
            return sm[j][i2] - sm[j][i1-1]
        # dp
        f = [[[-inf]*2 for _ in range(n+1)] for _ in range(n+1)]
        for j in range(1, n+1):
            for i in range(1, n+1):
                # (4)
                f[j][i][1] = s(j-1, 1, i) + s(j+1, 1, i) # NOTE: index start from 1!
                # (1)
                if j>1:
                    for ii in range(1, i+1):
                        f[j][i][1] = max(f[j][i][1], f[j-1][ii][1] - s(j, 1, ii) + s(j+1, 1, i) + s(j-1, ii+1, i))
                    for ii in range(i+1, n+1):
                        # f[j][i][0] = max(f[j][i][0], f[j-1][ii][0] - s(j, 1, i) + s(j+1, 1, i))
                        f[j][i][0] = max(f[j][i][0], max(f[j-1][ii]) - s(j, 1, i) + s(j+1, 1, i))
                # (2)
                if j>2:
                    for ii in range(1, i+1):
                        f[j][i][1] = max(f[j][i][1], max(f[j-2][ii]) + s(j-1, ii+1, i) + s(j+1, 1, i))
                    for ii in range(i+1, n+1):
                        f[j][i][0] = max(f[j][i][0], max(f[j-2][ii]) + s(j+1, 1, i))
                # (3)
                if j>3:
                    for ii in range(1,n+1):
                        f[j][i][1] = max(f[j][i][1], max(f[j-3][ii]) + s(j-1, 1, i) + s(j+1, 1, i))
        return max(max(max(t) for t in row) for row in f)
    """ 上面引入函数居然会TLE? 去掉后可以通过 """
    def maximumScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # presum (reverse i&j, index start from 1)
        sm = [[0]*(n+1) for _ in range(n+2)] # j列前后两个哨兵!
        for j in range(1, n+1):
            for i in range(1, n+1):
                sm[j][i] = sm[j][i-1] + grid[i-1][j-1] # reverse!
        def fmax(i,j): return j if j>i else i
        # dp
        ans = 0
        f = [[[-inf]*2 for _ in range(n+1)] for _ in range(n+1)]
        for j in range(1, n+1):
            for i in range(1, n+1):
                # (4)
                f[j][i][1] = sm[j-1][i] + sm[j+1][i] # NOTE: index start from 1!
                # (1)
                if j>1:
                    for ii in range(1, i+1):
                        f[j][i][1] = fmax(f[j][i][1], f[j-1][ii][1] - sm[j][ii] + sm[j+1][i] + sm[j-1][i] - sm[j-1][ii])
                    for ii in range(i+1, n+1):
                        f[j][i][0] = fmax(f[j][i][0], fmax(f[j-1][ii][0], f[j-1][ii][1]) - sm[j][i] + sm[j+1][i])
                # (2)
                if j>2:
                    for ii in range(1, i+1):
                        f[j][i][1] = fmax(f[j][i][1], fmax(f[j-2][ii][0], f[j-2][ii][1]) + sm[j-1][i] - sm[j-1][ii] + sm[j+1][i])
                    for ii in range(i+1, n+1):
                        f[j][i][0] = fmax(f[j][i][0], fmax(f[j-2][ii][0], f[j-2][ii][1]) + sm[j+1][i])
                # (3)
                if j>3:
                    for ii in range(1,n+1):
                        f[j][i][1] = fmax(f[j][i][1], fmax(f[j-3][ii][0], f[j-3][ii][1]) + sm[j-1][i] + sm[j+1][i])
                ans = fmax(ans, fmax(f[j][i][0], f[j][i][1]))
        return ans


sol = Solution()
result = [
    # sol.minimumLength(s = "abaacbcbb"),
    # sol.minChanges(nums = [1,0,1,2,4,3], k = 4),
    sol.maximumScore(grid = [[0,0,0,0,0],[0,0,3,0,0],[0,1,0,0,0],[5,0,0,3,0],[0,0,0,0,2]]),
    sol.maximumScore(grid = [[10,9,0,0,15],[7,1,0,8,0],[5,20,0,11,0],[0,0,0,1,2],[8,12,1,10,3]]),
]
for r in result:
    print(r)
