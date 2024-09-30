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
https://leetcode.cn/contest/weekly-contest-415
T2 没有一下子想到 DP, 不太行
T4 有点复杂! 值得学习~ (字符串哈希)
Easonsi @2023 """
class Solution:
    """ 3289. 数字小镇中的捣蛋鬼 """
    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        s = set()
        ans = []
        for x in nums:
            if x in s: ans.append(x)
            else: s.add(x)
        return ans
    
    """ 3290. 最高乘法得分 从一个数组中找到有序的四个数字, 要求其和已有的四个数字乘积之和最大. 
限制: n 1e5; x +/- 1e5
思路1: #DP
    记 f(i, j) 表示从前 i 个数中选 j 个数的最大乘积
    则有 f(i,j) = max{
        f(i-1,j),
        f(i-1, j-1) + a[j]*b[i],
    }
    边界: f[i, -1] = 0
    """
    def maxScore(self, a: List[int], b: List[int]) -> int:
        @lru_cache(None)
        def f(i,j):
            if j < 0: return 0
            if i < 0: return -inf
            return max(
                f(i-1,j),
                f(i-1, j-1) + a[j]*b[i]
            )
        return f(len(b)-1, 3)
    
    """ 3291. 形成目标字符串需要的最少字符串数 I 可以用的素材是一些words的 **前缀**, 将这些字符串连接构成target, 问最少操作数. 
限制: n 100; sum{len(w)} 1e5; len(target / word) 5e3
思路1: 
    观察本题的要求: 因为是前缀字符串, 所以 "到达i必然可以到达i-1"! 
        同时, 对于每个位置idx而言, 它构成前缀是有限制的! 可以记 sz[i] 是能够匹配的最大长度
        -> 注意, 这样本题就变为 "0045. 跳跃游戏 II"
    如何判断是否满足前缀呢? 一种方法是用 #字符串哈希
from [ling](https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-ii/solutions/2917929/ac-zi-dong-ji-pythonjavacgo-by-endlessch-hcqk/)
另外一种高级的做法是 #AC自动机
    """
    def minValidStrings(self, words: List[str], target: str) -> int:
        import random
        n = len(target)

        # 多项式字符串哈希（方便计算子串哈希值）
        # 哈希函数 hash(s) = s[0] * BASE^(n-1) + s[1] * BASE^(n-2) + ... + s[n-2] * BASE + s[n-1]
        MOD = 1_070_777_777
        BASE = random.randint(8 * 10 ** 8, 9 * 10 ** 8)  # 随机 BASE，防止 hack
        pow_base = [1] + [0] * n  # pow_base[i] = BASE^i
        pre_hash = [0] * (n + 1)  # 前缀哈希值 pre_hash[i] = hash(s[:i])
        for i, b in enumerate(target):
            pow_base[i + 1] = pow_base[i] * BASE % MOD
            pre_hash[i + 1] = (pre_hash[i] * BASE + ord(b)) % MOD  # 秦九韶算法计算多项式哈希

        # 计算子串 target[l:r] 的哈希值，注意这是左闭右开区间 [l,r)
        # 计算方法类似前缀和
        def sub_hash(l: int, r: int) -> int:
            return (pre_hash[r] - pre_hash[l] * pow_base[r - l]) % MOD

        # 保存每个 words[i] 的每个前缀的哈希值，按照长度分组
        max_len = max(map(len, words))
        sets = [set() for _ in range(max_len)]
        for w in words:
            h = 0
            for j, b in enumerate(w):
                h = (h * BASE + ord(b)) % MOD
                sets[j].add(h)  # 注意 j 从 0 开始

        # -------------------------
        ans = 0
        curr_r = 0
        next_r = 0
        for i in range(n):
            check = lambda sz: sub_hash(i, i+sz+1) not in sets[sz]
            sz = bisect_left(range(min(n-i, max_len)), True, key=check)
            next_r = max(next_r, i + sz)
            if i == curr_r:
                if i == next_r: return -1
                ans += 1
                curr_r = next_r
        return ans

    
sol = Solution()
result = [
    # sol.maxScore(a = [3,2,5,6], b = [2,-6,4,-5,-3,2,-7]),
    sol.minValidStrings(words = ["abc","aaaaa","bcdef"], target = "aabcdabc"),
]
for r in result:
    print(r)
