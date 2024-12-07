from easonsi.util.leetcode import *
from math import gcd

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
https://leetcode.cn/contest/weekly-contest-421
T3 DP 的推导需要一定技巧
T4 矩阵快速幂, 自己实现了嘿嘿
Easonsi @2024 """
class Solution:
    """ 3334. 数组的最大因子得分 #题型 #medium 对于一个数组, 分数为 GCD * LCM. 问最多移除一个元素得到的分数最大值. 
限制: n 100; x 30
如何避免暴力枚举? 
    前后缀分解! 
思路1: 尝试枚举所有的删除一个元素的情况

[ling](https://leetcode.cn/problems/find-the-maximum-factor-score-of-array/solutions/2967105/fei-bao-li-zuo-fa-qian-hou-zhui-fen-jie-27f8y/)
    """
    def maxScore(self, nums: List[int]) -> int:
        from math import gcd, lcm
        n = len(nums)
        post_gcd = [0] * (n + 1)        # gcd(0,x) = x
        post_lcm = [0] * (n) + [1]      # lcm(1,x) = x
        for i in range(n - 1, -1, -1):
            post_gcd[i] = gcd(post_gcd[i + 1], nums[i])
            post_lcm[i] = lcm(post_lcm[i + 1], nums[i])
        ans = post_gcd[0] * post_lcm[0] # 不删除
        pre_gcd = [0] * (n + 1)
        pre_lcm = [1] + [0] * (n)
        for i,x in enumerate(nums):
            # 先不考虑 x; 然后再更新前缀
            ans = max(ans, gcd(pre_gcd[i], post_gcd[i+1]) * lcm(pre_lcm[i], post_lcm[i+1]))
            pre_gcd[i+1] = gcd(pre_gcd[i], x)
            pre_lcm[i+1] = lcm(pre_lcm[i], x)
        return ans
    
    """ 3335. 字符串转换后的长度 I #medium 每次操作中, 将除了z之外的字符变为后一个, z变为ab, 问最后得到的字符串长度, 取模
限制: n 1e5; t 1e5
    """
    def lengthAfterTransformations(self, s: str, t: int) -> int:
        MOD = 10**9 + 7
        cnt = [0] * 26
        for c in s:
            cnt[ord(c) - ord('a')] += 1
        for _ in range(t):
            ncnt = [0] + cnt[:-1]
            ncnt[0] =cnt[25]
            ncnt[1] = (cnt[0] + cnt[25]) % MOD
            cnt = ncnt
        return sum(cnt) % MOD
    

    """ 3336. 最大公约数相等的子序列数量 #hard 要从nums找到两个子序列, 它们没有重复元素, 使得他们GCD相同. 问有多少种情况
限制: n 200; x 200 取模
思路1: #DP
    考虑 "从右往左" 选, 记 f(i,a,b) 表示到i位置, 后缀构成 gcd = a 和 b, 最终得到合法序列的数量. 
    转移方程: 考虑不选i; 或者分别放到a / b
        f(i,a,b) = f(i-1,a,b) + f(i-1, gcd(a, nums[i]), b) + f(i-1, a, gcd(b, nums[i]))
    答案: f(n-1, 0,0) - 1, 减1需要去掉空序列. 
    边界: f(-1, x,y) = (x!=y)
    """
    def subsequencePairCount(self, nums: List[int]) -> int:
        n = len(nums)
        MOD = 10**9 + 7
        @lru_cache(None)
        def f(i, a,b):
            if i<0: return int(a==b)
            return (f(i-1,a,b) + f(i-1, gcd(a, nums[i]), b) + f(i-1, a, gcd(b, nums[i]))) % MOD
        return (f(n-1, 0,0) - 1) % MOD

    """ 3337. 字符串转换后的长度 II #hard 同样问经过t次操作之后得到的字符串长度. 取模. 
每次操作, 将字符ch换成字母表后续的 nums[ord(ch)-ord('a')] 个字符, 例如若 nums[0]=3, 则将 a 换成 bcd. 
限制: n 1e5; t 1e9
思路1: 矩阵 #快速幂
见 [ling](https://leetcode.cn/problems/total-characters-in-string-after-transformations-ii/solutions/2967037/ju-zhen-kuai-su-mi-you-hua-dppythonjavac-cd2j/)
    """
    def lengthAfterTransformations(self, s: str, t: int, nums: List[int]) -> int:
        MOD = 10**9 + 7
        mat = [[0] * 26 for _ in range(26)]
        for i,x in enumerate(nums):
            for j in range(i+1, i+x+1):
                mat[i][j%26] += 1
        vec = [0] * 26
        for c in s:
            vec[ord(c) - ord('a')] += 1
        # 快速幂
        def matmul(a, b):
            res = [[0] * 26 for _ in range(26)]
            for i in range(26):
                for j in range(26):
                    for k in range(26):
                        res[i][j] += a[i][k] * b[k][j]
                        res[i][j] %= MOD
            return res
        def vecmul(m, v):
            # 注意这里维度: v[i] 变为m第i行所表示的若干字符
            res = [0] * 26
            for i in range(26):
                for j in range(26):
                    res[j] += m[i][j] * v[i]
                    res[j] %= MOD
            return res
        def qpow(x, n):
            if n==1: return x
            x2 = qpow(x, n//2)
            if n%2==0: return matmul(x2, x2)
            else: return matmul(x2, matmul(x2, x))
        res = vecmul(qpow(mat, t), vec)
        return sum(res) % MOD
    
sol = Solution()
result = [
    # sol.maxScore(nums = [2,4,8,16]),
    # sol.maxScore(nums = [1,2,3,4,5]),
    # sol.maxScore([2,29]),
    # sol.lengthAfterTransformations(s = "abcyy", t = 2),
    # sol.lengthAfterTransformations("azbk", 1),
    # sol.subsequencePairCount(nums = [1,2,3,4]),
    # sol.subsequencePairCount( nums = [1,1,1,1]),

    sol.lengthAfterTransformations(s = "abcyy", t = 2, nums = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]),
    sol.lengthAfterTransformations(s = "azbk", t = 1, nums = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]),
    sol.lengthAfterTransformations("k", 2, [2,2,1,3,1,1,2,3,3,2,1,2,2,1,1,3,1,2,2,1,3,3,3,2,2,1]),
]
for r in result:
    print(r)
