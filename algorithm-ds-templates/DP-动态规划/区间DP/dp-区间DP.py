from easonsi.util.leetcode import *
from functools import cache

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
https://www.bilibili.com/video/BV1Gs4y1E7EU/

0516. 最长回文子序列 https://leetcode.cn/problems/longest-palindromic-subsequence/solution/shi-pin-jiao-ni-yi-bu-bu-si-kao-dong-tai-kgkg/
1039. 多边形三角剖分的最低得分 https://leetcode.cn/problems/minimum-score-triangulation-of-polygon/solution/shi-pin-jiao-ni-yi-bu-bu-si-kao-dong-tai-aty6/

0375. 猜数字大小 II #题型 https://leetcode.cn/problems/guess-number-higher-or-lower-ii/
    注意两侧的子问题取max
1312. 让字符串成为回文串的最少插入次数 https://leetcode.cn/problems/minimum-insertion-steps-to-make-a-string-palindrome/
1547. 切棍子的最小成本 https://leetcode.cn/problems/minimum-cost-to-cut-a-stick/
1000. 合并石头的最低成本 https://leetcode.cn/problems/minimum-cost-to-merge-stones/

Easonsi @2023 """
class Solution:
    """ 0516. 最长回文子序列 #medium f[i,j] 表示在区间 [i,j] 中的最长回文子序列长度 
思路1: #DP
    `f[i][j]` 表示 s[i...j] 内的最长长度
    递推: 1) 若 s[i]==s[j], 则 `f[i][j] = f[i+1][j-1] + 2`; 2) 否则, `f[i][j] = max(f[i+1][j], f[i][j-1])`
    边界: `f[i][i] = 1`. 
    """
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        @cache
        def f(i,j):
            if i==j: return 1
            if i>j: return 0
            if s[i]==s[j]: return f(i+1,j-1)+2
            return max(f(i+1,j), f(i,j-1))
        return f(0,n-1)
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        f = [[0]*n for _ in range(n)]
        for i in range(n): f[i][i] = 1
        for d in range(1, n):
            for i in range(n-d):
                j = i+d
                if s[i]==s[j]: f[i][j] = f[i+1][j-1] + 2
                else: f[i][j] = max(f[i+1][j], f[i][j-1])
        return f[0][n-1]
    
    """ 1039. 多边形三角剖分的最低得分 #medium 但感觉 #hard 对于边n的凸多边形, 可以分割成n-2个三角形, 每个三角形的得分为三个顶点的乘积, 求最小得分
限制: n 100
思路1: #区间 DP 记 f[i,j] 表示 i...j 连续节点构成的凸多边形的最小得分
    可以枚举 (i,j) 边所对应的那个顶点 (范围在 i+1...j-1), 分割成 f[i,k] + f[k,j] + A[i]*A[k]*A[j]
    注意: 这一直接把「环形数组」的环边作为底边, 从而避免了环形数组的处理!! 
    边界: f[i,i+1] = 0
    复杂度: O(n^3)
图见 [灵神](https://leetcode.cn/problems/minimum-score-triangulation-of-polygon/solution/shi-pin-jiao-ni-yi-bu-bu-si-kao-dong-tai-aty6/)
    """
    def minScoreTriangulation(self, values: List[int]) -> int:
        @cache
        def f(i,j):
            if i+1==j: return 0
            return min(f(i,k)+f(k,j)+values[i]*values[k]*values[j] for k in range(i+1,j))
        return f(0,len(values)-1)

    """ 0375. 猜数字大小 II #medium #题型 在 [1,n] 范围内猜数字, 会告诉大/小, 猜i错误的代价是i, 问保证能猜对的策略代价. 
限制: n 200
思路1: f(i,j) 表示区间的最小代价
    递推: f(i,j) = min{ k + max(f(i,k-1), f(k+1,j)) }
        注意, 两边只有一种可能! 取max
    边界: i>=j: 0
    """
    def getMoneyAmount(self, n: int) -> int:
        @cache
        def f(i,j):
            if i>=j: return 0
            if j==i+1: return i
            return min( k + max(f(i,k-1),f(k+1,j)) for k in range(i+1,j))
        return f(1,n)

sol = Solution()
result = [
    # sol.minScoreTriangulation(values = [3,7,4,5]),

    sol.getMoneyAmount(10),
    sol.getMoneyAmount(1),
    sol.getMoneyAmount(2),
    sol.getMoneyAmount(4),

]
for r in result:
    print(r)
