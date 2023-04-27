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
https://leetcode.cn/contest/weekly-contest-313

T3写得太不优雅了; T4感觉类似KMP? 尝试了用字符串哈希, 结果超时了...字符串也还需要加强一下!! 结果发现需要用到的居然是 #LCP 最长公共子串的 DP, 那时候居然没写出来, 有点失误.

@2022 """
class Solution:
    """ 2427. 公因子的数目 暴力 """
    def commonFactors(self, a: int, b: int) -> int:
        # from math import gcd
        # g = gcd(a,b)
        ans = 0
        for i in range(1, min(a,b)+1):
            if a%i==0 and b%i==0:
                ans += 1
        return ans
    
    """ 2428. 沙漏的最大总和 #暴力 """
    def maxSum(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        bars = [(0,0), (0,1), (0,2), (1,1), (2,0), (2,1), (2,2)]
        ans = 0
        for i in range(m-2):
            for j in range(n-2):
                a = sum(grid[i+dx][j+dy] for dx,dy in bars)
                ans = max(ans, a)
        return ans
    
    """ 2429. 最小 XOR #medium 给定两个数字 num1, num2. 要求找到一个「置位数」和num2相同的数字x, 使得x和num1的异或值最小. 
思路1: #模拟. 根据直接, 可知应该先通过异或匹配掉高位的1, 若有多出来的1, 则补充到低位.
    下面的代码写得太烦了.
"""
    def minimizeXor(self, num1: int, num2: int) -> int:
        def f(x):
            ret = []
            bit = 0
            while x:
                if x&1: ret.append(bit)
                x >>= 1; bit += 1
            return ret
        bits1, bits2 = f(num1), f(num2)
        if len(bits2) <= len(bits1):
            ret = bits1[- (len(bits2)):]
        else:
            ret = bits1[:]; bit = 0
            cnt = len(bits2) - len(bits1)
            while cnt:
                if bit not in bits1: ret.append(bit); cnt -= 1
                bit += 1
        return sum(1<<i for i in ret)
    
    
    """ 2430. 对字母串可执行的最大删除数 #hard #review 给定一个字符串, 每次可以删除 1) 首位的l个字符, 要求 s[:l]==s[l:2*l]; 2) 所有字符. 问给定一个字符串, 全部删除所需的最大步数. 限制: n 4000.
思路0: 尝试用 #字符串哈希. 结果 #TLE. 每一阶段的复杂度都应该是 O(n^2), 但常数太大了
    基本思路: 从后往前进行 #DP. 对于每个位置, 我们需要计算出它可以删除头部的几个字符? 
思路1: #DP 基本的递推关系是明确的: f[i] 表示 s[i:] 可以删除的最大步数. 
    对于每个位置, 枚举可能匹配的长度 j, 若有 `f[i...i+j-1] = f[i+j...i+2j-1]`, 则有 f[i] 可能有更大的答案 f[i+j]+1
    那么, 关键就是, 如何判断两个子串是否相等? 一种方式是采用 #LCP 最长公共前缀. 记 `lcp[i,j]` 表示 s[i:] 和 s[j:] 的最长公共前缀. 
        有递推: 当 s[i]=s[j] 时, `lcp[i,j] = lcp[i+1,j+1]+1`; 否则, lcp[i,j] = 0. 根据递推公式, 倒序即可.
思路2: 事实上, 直接用Python的切片速度比较快的 特性, 居然也可以 #暴力 过.
https://leetcode.cn/problems/maximum-deletions-on-a-string/
"""
    def deleteString(self, s: str) -> int:
        # 思路0: 尝试用 #字符串哈希. 结果 #TLE.
        n = len(s)
        # 
        base = 31
        mod = 10**9+9
        span2hash = {}
        for i in range(n):
            h = 0
            for j in range(i, n):
                h = (h*base + ord(s[j])-ord('a')) % mod
                span2hash[(i,j)] = h
        # 
        idx2pair = [[] for _ in range(n)]
        for i in range(n):
            for ll in range(1, n):
                if i+2*ll-1 >= n: break
                if span2hash[(i,i+ll-1)]==span2hash[(i+ll,i+2*ll-1)]:
                    idx2pair[i].append(ll)
        # 
        dp = [1] * (n+1)
        for i in range(n-1, -1, -1):
            for ll in idx2pair[i]:
                dp[i] = max(dp[i], 1+dp[i+ll])
        return dp[0]


    def deleteString(self, s: str) -> int:
        # 思路1: #DP
        n = len(s)
        if len(set(s)) == 1: return n  # 特判全部相同的情况
        lcp = [[0] * (n + 1) for _ in range(n + 1)]  # lcp[i][j] 表示 s[i:] 和 s[j:] 的最长公共前缀
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i, -1):
                if s[i] == s[j]:
                    lcp[i][j] = lcp[i + 1][j + 1] + 1
        f = [0] * n
        for i in range(n - 1, -1, -1):
            for j in range(1, (n - i) // 2 + 1):
                if lcp[i][i + j] >= j:  # 说明 s[i:i+j] == s[i+j:i+2*j]
                    f[i] = max(f[i], f[i + j])
            f[i] += 1
        return f[0]

    def deleteString(self, s: str) -> int:
        # 利用切片暴力做...居然也可以过...
        n = len(s)
        f = [1] * (n)
        for i in range(n-1, -1, -1):
            for j in range(i+1, n):
                if s[i:j]==s[j:2*j-i]: f[i] = max(f[i], f[j]+1)
        return f[0]




sol = Solution()
result = [
    # sol.commonFactors(a = 12, b = 6),
    # sol.commonFactors(25,30),
    # sol.maxSum(grid = [[1,2,3],[4,5,6],[7,8,9]]),
    # sol.maxSum(grid = [[6,2,1,3],[4,2,1,5],[9,2,8,7],[4,1,2,9]]),
    # sol.minimizeXor(3,5),
    # sol.minimizeXor(1,12),
    sol.deleteString("aaabaab"),
    sol.deleteString("abcabcdabc"),
    sol.deleteString("aaaaa"),
    
]
for r in result:
    print(r)
