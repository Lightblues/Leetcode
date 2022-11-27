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
https://leetcode-cn.com/contest/biweekly-contest-92
T1 因为边界WA了一次; T4写得好冗长...

@2022 """
class Solution:
    """ 6249. 分割圆的最少切割次数 注意边界: 当n==1时答案应该是0 """
    def numberOfCuts(self, n: int) -> int:
        if n==1: return 0
        return n//2 if n%2==0 else n
    
    """ 6277. 行和列中一和零的差值 #暴力 模拟 """
    def onesMinusZeros(self, grid: List[List[int]]) -> List[List[int]]:
        onesRow = [sum(i==1 for i in row) for row in grid]
        zerosRow = [sum(i==0 for i in row) for row in grid]
        onesCol = [sum(i==1 for i in col) for col in zip(*grid)]
        zerosCol = [sum(i==0 for i in col) for col in zip(*grid)]
        m,n = len(grid), len(grid[0])
        res = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                res[i][j] = onesCol[j]+onesRow[i] - zerosCol[j]-zerosRow[i]
        return res
    
    """ 6250. 商店的最少代价 0/1 表示该时刻是否有人来, 定义代价为关门前空闲的时段数+关门后来人的时段数, 要求一个最佳的「关门时间」
计算 #前缀数组, 简单遍历即可
"""
    def bestClosingTime(self, customers: str) -> int:
        custs = [ch=='Y' for ch in customers]
        acc = list(accumulate(custs, initial=0))
        n = len(customers); n_customers = acc[-1]
        ans = 0; minCost = n
        for i in range(n+1):
            cost = (i-acc[i]) + (n_customers-acc[i])
            if cost < minCost:
                minCost = cost
                ans = i
        return ans
    
    """ 6251. 统计回文子序列数目 #hard 统计由数字组成的字符串中, 长度为5的 #回文 子序列的数量. 限制: n 1e4
思路0: 枚举所有的中间数字, 统计左右符合对称的长尾2的数字川数量. 复杂度 O(d^2 n), 其中d为字符数量
    细节: 注意 left, right 两个计数器的更新
"""
    def countPalindromes(self, s: str) -> int:
        mod = 10**9+7
        n = len(s)
        s = [int(i) for i in s]
        # 对称的数字 (可构成回文)
        mmap = {}
        for i in range(10):
            for j in range(10):
                mmap[10*i+j] = 10*j+i
        
        # 计算前缀. acc[i+1][d] 记录 s[:i+1] 中数字 d 的数量
        cnt = [0]*10
        acc = [cnt[:]]
        for d in s:
            cnt[d] += 1
            acc.append(cnt[:])
        
        # 枚举
        left = Counter(); right = Counter()
        for i in range(n-2,-1,-1):
            c = s[i]
            for d in range(10):
                right[c*10+d] += cnt[d] - acc[i+1][d]
        ans = 0
        for i in range(n):
            c = s[i]
            for d in range(10):
                if i<n-1:
                    right[c*10+d] -= cnt[d] - acc[i+1][d]
                if i>1:
                    left[d*10+s[i-1]] += acc[i-1][d]
            for k,v in mmap.items():
                ans = (ans + left[k]*right[v]) % mod
        return ans
        
sol = Solution()
result = [
    # sol.numberOfCuts(5),
    # sol.numberOfCuts(6),
    # sol.onesMinusZeros(grid = [[0,1,1],[1,0,1],[0,0,1]]),
    # sol.onesMinusZeros(grid = [[1,1,1],[1,1,1]]),
    # sol.bestClosingTime(customers = "YYNY"),
    # sol.bestClosingTime("NNNN"),
    # sol.bestClosingTime("YYYY"),
    sol.countPalindromes("103301"),
    sol.countPalindromes("0000000"),
    sol.countPalindromes("9999900000"),
    sol.countPalindromes('0'*10000)
]
for r in result:
    print(r)
