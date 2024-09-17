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
https://leetcode.cn/contest/weekly-contest-405
https://leetcode.cn/circle/discuss/jFqfNu/
T4 有争议的字符串题目, 竞赛玩家

Easonsi @2023 """
class Solution:
    """ 3210. 找出加密后的字符串 """
    def getEncryptedString(self, s: str, k: int) -> str:
        k %= len(s)
        return s[k:]+s[:k]
    
    """ 3211. 生成不含相邻零的二进制字符串 """
    def validStrings(self, n: int) -> List[str]:
        if n==1: return ["0","1"]
        def check(i):
            return "00" not in bin(i)[2:]
        res = [f"{bin(i)[2:]}" for i in range((1<<(n-2)), 1<<n) if check(i)]
        res = ["0" + i if len(i)<n else i for i in res]
        return res
    
    """ 3212. 统计 X 和 Y 频数相等的子矩阵数量 """
    def numberOfSubmatrices(self, grid: List[List[str]]) -> int:
        m,n = len(grid), len(grid[0])
        accX, accY = [0]*n, [0]*n
        ans = 0
        for row in grid:
            ax,ay = 0,0
            for i,x in enumerate(row):
                if x=='X': 
                    ax += 1
                elif x=='Y': 
                    ay += 1
                accX[i] += ax   # NOTE: this is necessary
                accY[i] += ay
                if accX[i] == accY[i] and accX[i] > 0: ans += 1
        return ans
    
    """ 3213. 最小代价构造字符串 #hard 有一组字符串, 分别有不同的代价. 问将它们拼成 target的最小代价 (每个字符串可以用多次)
限制: n 5e4; sum(len) 5e4; 
思路0: 利用 #字典树, 然后用 DP #TLE
    显然, 对于 s[i+1...j] 存在, 我们可以用 DFS 递推完成 f[j] = f[i] + cost
    但是会超时! 例如 target = 'aaaa...a', words = ['a', 'aa...a']
        这样, 字典树就是一个链. 对于每个位置i, 都需要尝试遍历这个链 -- 复杂度 O(n^2)
思路1: #字符串哈希
    关键是复杂度的计算! 
    由于 sum(len) <= L, 于是最多有 sqrt(L) 个长度不同的字符串
    对于每个位置, 尝试看不同长度的字符串中是否有该长度所需的字符串 -- 复杂度 O(n sqrt(L))
思路2: #后缀树 #AC自动机
[ling](https://leetcode.cn/problems/construct-string-with-minimum-cost/solutions/2833949/hou-zhui-shu-zu-by-endlesscheng-32h9/)
    """
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        pass
    
sol = Solution()
result = [
    # sol.validStrings(3),
    sol.numberOfSubmatrices( grid = [["X","Y","."],["Y",".","."]]),
]
for r in result:
    print(r)
