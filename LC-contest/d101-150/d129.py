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
https://leetcode.cn/contest/biweekly-contest-129
T4 的 DP 不难, 但自己愣是没想到, 思路退化orz
Easonsi @2023 """
class Solution:
    """ 3127. 构造相同颜色的正方形 """
    def canMakeSquare(self, grid: List[List[str]]) -> bool:
        for i in range(2):
            for j in range(2):
                cnt = Counter(grid[i][j:j+2]) + Counter(grid[i+1][j:j+2])
                if max(cnt.values()) >= 3: return True
        return False
    
    """ 3128. 直角三角形 """
    def numberOfRightTriangles(self, grid: List[List[int]]) -> int:
        ans = 0
        m,n = len(grid), len(grid[0])
        col_sum = [sum(grid[i][j] for i in range(m)) for j in range(n)]
        row_sum = [sum(row) for row in grid]
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x == 1:
                    ans += (col_sum[j] - 1) * (row_sum[i] - 1)
        return ans
    
    """ 3129. 找出所有稳定的二进制数组 I #medium 计算"稳定"二进制数组的数量. 要求: 1) 规定了0/1的数量; 2) 要求所有长度超过limit的子数组都同时有0和1
    限制: n 200
3130. 找出所有稳定的二进制数组 II #hard 增加范围到 n 1e3
思路1: #DP
    考虑 f(i,j,b) 表示前 i+j 包括 i/j 个0/1. 且最后一位为b 的合法数量. 
    转移: 若b==0, 考虑前一位可能是 0/1, 有 f(i-1,j,0) + f(i-1,j,1). 
        还要考虑非法的情况! 也即前limit位都是0! 等价于 f(i-limit-1,j,1), 也即恰好前limit为都是0, 再前一位是1
[ling](https://leetcode.cn/problems/find-all-possible-stable-binary-arrays-ii/solutions/2758868/dong-tai-gui-hua-cong-ji-yi-hua-sou-suo-37jdi/)
"""
    def numberOfStableArrays(self, zero: int, one: int, limit: int) -> int:
        MOD = 10**9 + 7
        @lru_cache(None)
        def f(i,j,b):
            if i<0 or j<0: return 0
            # 前 i+j 包括 i/j 个0/1. 且最后一位为b
            if i==0: return int(b==1 and j<=limit)
            if j==0: return int(b==0 and i<=limit)
            if b==0:
                return (f(i-1,j,0) + f(i-1,j,1) - f(i-limit-1,j,1)) % MOD
            else:
                return (f(i,j-1,0) + f(i,j-1,1) - f(i,j-limit-1,0)) % MOD
        ans = (f(zero,one,0) + f(zero,one,1)) % MOD
        f.cache_clear()
        return ans
    
sol = Solution()
result = [
    # sol.canMakeSquare(grid = [["B","W","B"],["B","W","W"],["B","W","B"]]),
    # sol.numberOfRightTriangles(grid = [[1,0,1],[1,0,0],[1,0,0]]),
    sol.numberOfStableArrays(zero = 3, one = 3, limit = 2),
]
for r in result:
    print(r)
