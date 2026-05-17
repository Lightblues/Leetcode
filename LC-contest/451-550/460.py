from typing import *
from collections import defaultdict
from itertools import count

"""
https://leetcode.cn/contest/weekly-contest-460
1. 中位数之和的最大值, 基本贪心
2. 插入一个字母的最大子序列数, 通过状态机 DP 来计算前序子序列数量; 通过前后缀分解考虑插入的影响! 非常巧妙的 DP
3. 通过质数传送到达终点的最少跳跃次数
    很简单的题设, 但是思路值得深挖
    复杂度分析; 避免重复访问一个 group
    计算 MX 以下所有数字质因子的 "埃氏筛" 方法
4. 划分数组得到最大异或运算和与运算之和  #hard
    问题转为, 将数组划分为两组, 最大化 max{ XOR(A) + XOR(C) }
    等价于  "从 S' 中选择一些数 A'，计算这些数的最大异或和", 其中 S' 是将所有出现次数奇数的比特位置 0 所构成的新集合
    -- 这是 #线性基 的标准应用 -- "异或运算本质是 w 维线性空间中的模 2 加法"
    #remark: 从线性空间的角度理解 XOR, 非常精彩!
Easonsi @2026 """


class Solution:
    """ 3627. 中位数之和的最大值 #4
思路 1: 贪心, 返回 -2,-4,-6... 共 n//3 个元素
    """
    def maximumMedianSum(self, nums: List[int]) -> int:
        nums.sort()
        # ans = 0
        # for i in range(1, len(nums)//3 +1):
        #     ans += nums[-2*i]
        # return ans

        # 简洁写法!
        return sum(nums[len(nums)//3::2])

    """ 3628. 插入一个字母的最大子序列数 #5 
最多插入一个字母, 构成 LCT 子序列的最大数量
限制: n 1e5
思路 1: 状态机 DP + 前后缀分解
    - 可以通过 DP 来计算原本的 LCT 的数量 -- 问题转为新增一个字母的影响: 分类考虑:
        - 新增 L, 显然放到最左边最优, 新增 s 中 CT 数量
        - 新增 T, 最优放到最右边, 新增 LC 数量
        - 新增 C, 枚举所有位置, 新增前缀 C * 后缀 T 的数量
    三者取 max
https://leetcode.cn/problems/maximum-number-of-subsequences-after-one-inserting/solutions/3734800/fu-yong-115-ti-dai-ma-qian-hou-zhui-fen-gtkqz/
    """
    def numOfSubsequences(self, s: str) -> int:
        t = s.count("T")
        l = c = lc = ct = lct = 0
        lt = 0  # max of pre_c * post_t
        for i,ch in enumerate(s):
            if ch=="L":
                l += 1
            elif ch=="C":
                c += 1
                lc += l
                ct += t
            elif ch=="T":
                lct += lc
                t -= 1
            lt = max(lt, l*t)
        return lct + max(lc, ct, lt)

    """ 3629. 通过质数传送到达终点的最少跳跃次数 #5
需要从 0 -> n-1. 每一步可以: 1. 位置 +/-1; 2. 若 i 元素为质数, 可以跳到任意其倍数位置
限制: n 1e5; val 1e6
思路 1: 预处理 + 正向 BFS
    整体上就是 BFS 的思路 (下面用了双列表实现 BFS)
    - 对于位置 i, 可访问的 idx 集合为 { i-1,i+1 } + prime_ava(i), 其中 prime_ava 是若 nums[i] 为质数时候的可跳转范围
    如何求 prime_ava? 
        考虑到数据范围, 可以计算在 MX 范围内所有数字的质因子! -- 思路同埃氏筛
        则, 先遍历一遍 nums, 统计每个质因子可访问的下标范围!
    复杂度: 不考虑预处理! 
        复杂度取决于 BFS 的循环次数 (边数), 在本题中, 就是 "下标列表的总长度"
        在质因子数的限制下, 我们可以构造 logU 个质因子; 其他的 n-logU 为包含所有这些质因子的数; 则下标列表总长度 O(n logU)
        因此, 整体复杂度 O(n logU)
https://leetcode.cn/problems/minimum-jumps-to-reach-end-via-prime-teleportation/solutions/3734792/bfspythonjavacgo-by-endlesscheng-bu60/
    """
    def minJumps(self, nums: List[int]) -> int:
        # NOTE: 提交的时候, 预处理必须写到函数外面!
        # 预处理每个数的质因子列表，思路同埃氏筛
        MX = 1_000_001
        prime_factors = [[] for _ in range(MX)]
        for i in range(2, MX):
            if not prime_factors[i]: # 是质数
                for j in range(i, MX, i):
                    prime_factors[j].append(i)
        # 
        n = len(nums)
        groups = defaultdict(list)  # 每个(质数)可跳转的位置
        for i,x in enumerate(nums):
            for p in prime_factors[x]:
                groups[p].append(i)
        # BFS
        vis = [False] * n
        q = [0]; vis[0] = True
        for ans in count(0):  # NOTE: itertools.count 生成无限递增的
            nq = []
            for i in q:
                if i==n-1: return ans  # 达到条件
                idx = groups[nums[i]]
                idx.append(i+1)
                if i>0: idx.append(i-1)
                for j in idx:
                    if not vis[j]:
                        vis[j] = True
                        nq.append(j)
                idx.clear()  # NOTE: 对于一个 group, 仅遍历一次! 
            q = nq

    """ 3630. 划分数组得到最大异或运算和与运算之和 #7
将一个数组恰好划分成3 个子序列 A,B,C (可以为空), 要求最大化 XOR(A) + AND(B) + XOR(C)
限制: n 19
思路 1: 式子变形 + 线性基 + 最优性剪枝
    枚举所有子集 B, 假设剩余集合为 S, 则子问题变为, 最大化 XOR(A) + XOR(C), 其中 AC 划分 S
    枚举数字的每个比特位
        - 若在 S 中出现奇数次, 则无论如何划分, 都是 A,C 中包括奇数+偶数个该位 -> 贡献为 1
            考虑整体, 这些 "非特殊比特位" 的贡献为 XOR(S)
        - 若出现偶数次, 在 AC 中的划分要么都是 0, 要么都是 1. (*它们总是相等!) -- 将这些比特位叫做 特殊比特位
            将 S 中所有数字的 "非特殊比特位" 置为 0, 变成 S'
            考虑整体, 这些 "特殊比特位" 的贡献为 XOR(A') + XOR(C') = 2 * XOR(A')
        因此, 答案为 XOR(A) + XOR(C) = XOR(S) + 2 * XOR(A')
        -- 等价于, 最大化 XOR(A')
    对于问题 "从 S' 中选择一些数 A'，计算这些数的最大异或和。", 这是 #线性基 的标准应用
        为什么? 直接下 XorBasis 即可!
        "异或运算本质是 w 维线性空间中的模 2 加法，一个二进制数可以视作一个 w 维的向量，本题 w≤30。线性基（线性异或基）计算的是这个线性空间中的由 S' 张成的一组基，S' 中的每个二进制数（视作向量）都可以被这组基表出。
    复杂度: O(2^n n logU)
    参见: https://oi-wiki.org/math/linear-algebra/basis/
https://leetcode.cn/problems/partition-array-for-maximum-xor-and-and/solutions/3734850/shi-zi-bian-xing-xian-xing-ji-pythonjava-3e80/
 """
    def maximizeXorAndXor(self, nums: List[int]) -> int:
        n = len(nums)
        sz = max(nums).bit_length()

        # 预处理所有子集的 AND 和 XOR（刷表法）
        u = 1 << n
        sub_and = [0] * u
        sub_xor = [0] * u
        sub_and[0] = -1  # NOTE: 全1
        for i, x in enumerate(nums):
            high_bit = 1 << i
            for mask in range(high_bit):
                sub_and[high_bit | mask] = sub_and[mask] & x
                sub_xor[high_bit | mask] = sub_xor[mask] ^ x
        sub_and[0] = 0

        def max_xor2(sub: int) -> int:
            b = XorBasis(sz)
            xor = sub_xor[sub]
            for i, x in enumerate(nums):
                if sub >> i & 1:
                    # 只考虑有偶数个 1 的比特位（xor 在这些比特位上是 0）
                    b.insert(x & ~xor)
            return xor + b.max_xor() * 2

        return max(sub_and[i] + max_xor2((u - 1) ^ i) for i in range(u))

# 线性基模板
class XorBasis:
    def __init__(self, n: int):
        self.b = [0] * n

    def insert(self, x: int) -> None:
        b = self.b
        while x:
            i = x.bit_length() - 1  # x 的最高位
            if b[i] == 0:  # x 和之前的基是线性无关的
                b[i] = x  # 新增一个基，最高位为 i
                return
            x ^= b[i]  # 保证参与 max_xor 的基的最高位是互不相同的，方便我们贪心
        # 正常循环结束，此时 x=0，说明一开始的 x 可以被已有基表出，不是一个线性无关基

    def max_xor(self) -> int:
        b = self.b
        res = 0
        # 从高到低贪心：越高的位，越必须是 1
        # 由于每个位的基至多一个，所以每个位只需考虑异或一个基，若能变大，则异或之
        for i in range(len(b) - 1, -1, -1):
            if res ^ b[i] > res:
                res ^= b[i]
        return res





sol = Solution()
result = [
    # sol.numOfSubsequences(s = "LMCT"),
    # sol.numOfSubsequences(s = "LCCT"),
    # sol.minJumps(nums = [1,2,4,6]),
    sol.minJumps([2,1446,921,133,1487,507,1662,861,548,101,1187,760,997,1099,1171,624,986,825,701,1303,547,131,703,1033,1797,1498,386,1283,1471,1389,1361,1008,785,646,1118,991,400,207,1704,788,1320,1712,571]),
]
for r in result:
    print(r)