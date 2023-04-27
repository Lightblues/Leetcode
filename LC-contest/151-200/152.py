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
https://leetcode.cn/contest/weekly-contest-152
T3 没看清题意是「重排」. T4 也是阅读理解有问题... 整体的质量很高~

@2022 """
class Solution:
    """ 1175. 质数排列 """
    def numPrimeArrangements(self, n: int) -> int:
        def getPrimes(n):
            ps = [2]
            for x in range(3, n+1, 2):
                for p in ps:
                    if x % p == 0:
                        break
                else:
                    ps.append(x)
            return ps
        primes = getPrimes(n)
        p = len(primes)
        mod = 10**9 + 7
        return math.factorial(p) * math.factorial(n-p) % mod
    
    """ 1176. 健身计划评估 #easy """
    
    """ 1177. 构建回文串检测 #medium #题型 对于字符串, 需要返回 q个检查, 每次检查 (l,r) 范围的子串元素在 **修改k个字符的限制下** 能否 **通过重排** 构成回文串 限制: n, q 1e5
思路1: 利用 #位运算 记录每个字符的奇偶性. 
    对于可 #重排 的情况是否 #回文? 判断字符数量的 #奇偶性 即可!
    提示: 利用 #二进制 #压缩表示. 
    可以利用 #前缀和 快速得到区间元素的奇偶性. 
    具体而言, 假设一组数字中, 出现奇数的个数有 x个, 则当 x//2 <= k 时是可以的. 例如 abc 只需要修改一次. 
"""
    def canMakePaliQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        mask = 0
        acc = [0]
        for x in s:
            mask ^= 1 << (ord(x) - ord('a'))
            acc.append(mask)
        ans = []
        for l,r,k in queries:
            m = acc[r+1] ^ acc[l]
            ans.append(m.bit_count()//2 <= k)
        return ans
    

    
sol = Solution()
result = [
    # sol.numPrimeArrangements(100),
    sol.canMakePaliQueries(s = "abcda", queries = [[3,3,0],[1,2,0],[0,3,1],[0,3,2],[0,4,1]]),
]
for r in result:
    print(r)
