from easonsi.util.leetcode import *
import numpy as np

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
https://leetcode.cn/contest/weekly-contest-333
灵神: https://www.bilibili.com/video/BV1jM411J7y7/
Easonsi @2023 """
class Solution:
    """ 6362. 合并两个二维数组 - 求和法 #easy 有两组排序好的 (id, val) 数组, 合并; 若有相同的id, 将val相加
思路1: 用字典存储, 然后排序输出 #暴力
思路2: #归并排序 #模版
    复杂度 O(n)
[灵神](https://leetcode.cn/problems/merge-two-2d-arrays-by-summing-values/solution/xian-xing-zuo-fa-gui-bing-pai-xu-o1-e-wa-iy7u/)
"""
    def mergeArrays(self, nums1: List[List[int]], nums2: List[List[int]]) -> List[List[int]]:
        m = defaultdict(int)
        for i,x in nums1: m[i]+= x
        for i,y in nums2: m[i]+= y
        return sorted(m.items())
    def mergeArrays(self, a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
        # 思路2: #归并排序 #模版
        ans = []
        i, n = 0, len(a)
        j, m = 0, len(b)
        while True:
            if i == n:
                ans.extend(b[j:])
                return ans
            if j == m:
                ans.extend(a[i:])
                return ans
            if a[i][0] < b[j][0]:
                ans.append(a[i])
                i += 1
            elif a[i][0] > b[j][0]:
                ans.append(b[j])
                j += 1
            else:
                a[i][1] += b[j][1]
                ans.append(a[i])
                i += 1
                j += 1

    
    """ 6365. 将整数减少到零需要的最少操作数 #easy 但实际 #hard #题型 对于一个数字, 每次可以 +/- 任意2的幂, 问最少多少操作后得到0? 
思路1: #记忆化 搜索
    注意到, 高位的1会被低位的修改影响!! 但是低位的1只能自己发生修改
    所以, 搜索的过程中仅考虑如何消去 lowbit? 可以加上/减去它自己!
思路2: #贪心 注意到, 若有低位的连续多个1, 则好的办法是, 「先加上再减掉进位」!
思路2.2: #位运算 优化
    注意到, 对于 00011...1000 的连续1结构, 3x ^ x 可以得到两个1位
        对于 0001000 的结构 3x ^ x 可以得到一个1位
        [感觉还需要证明在 11011 这种情况下也是成立的]
    因此, 答案就是 (3x ^ x).bit_count()
[灵神](https://leetcode.cn/problems/minimum-operations-to-reduce-an-integer-to-0/solution/ji-yi-hua-sou-suo-by-endlesscheng-cm6l/)
思路0: 比赛时候缝缝补补出来的
    考虑 1, 11...1, 11011, 1010101 这些情况
"""
    def minOperations(self, n: int) -> int:
        # 比赛时候缝缝补补出来的
        # 考虑 1, 11...1, 11011, 1010101 这些情况
        s = bin(n)[2:]
        ans = 0
        for x in re.split('00+', s.strip('0')):
            if len(x)==1: ans += 1
            else: ans += min(
                x.count('0')+2, x.count('1')
            )
        return ans

    def minOperations(self, n: int) -> int:
        # 思路1: #记忆化 搜索
        @lru_cache(None)
        def dfs(x):
            if x&(x-1) == 0:    # 2的幂
                return 1
            lb = x&-x       # 修改最低位1
            return 1 + min(dfs(x-lb), dfs(x+lb))
        return dfs(n)

    def minOperations(self, n: int) -> int:
        # 思路2: #贪心 注意到, 若有低位的连续多个1, 则好的办法是, 「先加上再减掉进位」!
        ans = 1
        while n & (n - 1):  # 不是 2 的幂次
            lb = n & -n
            if n & (lb << 1): n += lb  # 多个连续 1
            else: n -= lb  # 单个 1
            ans += 1
        return ans

    def minOperations(self, n: int) -> int:
        # 思路2.2: #位运算 优化
        return (3 * n ^ n).bit_count()


    """ 6364. 无平方子集计数 实际上 #hard 考虑数组的所有子集中, 各个元素的乘积不包含平方因子, 这样的子集的数量 限制: n 1e3; 元素大小 [1,30]
预处理: 
    把「无平方因子数的数字」记作 NSQ.
    我们把 [2,30]  范围内的数字, 根据质因子分解得到其表示 (二进制)
思路1: 转换成 0-1 背包方案数
    我们可以把这些数字看成一些物品; 题目就变成「选一些不相交的质数集合，它们的并集恰好为集合 j 的方案数」
    这是 0-1 背包求方案数的模型 #模板 见 [01背包]
    复杂度: O(n * 2^m) 其中 m 为数字范围内质数的个数 (这里是 10)
思路2: #子集状压 DP #子集枚举 [dp]
    相较于01背包将所有数字看成不同的物品, 这里实际上有很多重复的数字! 
    先用 cnt 记录每一个数字出现的次数, 然后采用 子集状压 DP
    记 `f[i][j]` 表示前 i 个数字中, 选出若干个数字, 使得它们的并集恰好为 j 的方案数
        对于新的数字 mask, 对于其他与mask不相较的数字 other, 我们可以更新 f[i][other|mask] += f[i-1][other] * cnt[mask]
    复杂度: O(n + 30*2^m) 快了很多!
    技巧: 除了暴力枚举所有可能的other, 还可以利用 #枚举子集 来完成枚举
[灵神](https://leetcode.cn/problems/count-the-number-of-square-free-subsets/solution/liang-chong-xie-fa-01bei-bao-zi-ji-zhuan-3ooi/)
"""
    def squareFreeSubsets(self, nums: List[int]) -> int:
        # 思路1: 转换成 0-1 背包方案数
        # 将数字表示成质数因子的形式
        PRIMES = 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
        NSQ_TO_MASK = [0] * 31  # NSQ_TO_MASK[i] 为 i 对应的质数集合（用二进制表示）
        for i in range(2, 31):
            for j, p in enumerate(PRIMES):
                if i % p == 0:
                    if i % (p * p) == 0:  # 有平方因子
                        NSQ_TO_MASK[i] = -1
                        break
                    NSQ_TO_MASK[i] |= 1 << j  # 把 j 加到集合中
        # 0-1 背包求方案数
        MOD = 10 ** 9 + 7
        M = 1 << len(PRIMES)
        f = [0] * M  # f[j] 表示恰好组成集合 j 的方案数
        f[0] = 1  # 空集的方案数为 1
        for x in nums:
            mask = NSQ_TO_MASK[x]
            # 注意, 这里数字1的 mask=0, 不需要特殊考虑
            if mask >= 0:  # x 是 NSQ
                # for j in range(mask, M):
                for j in range(M - 1, mask - 1, -1):        # 直接写 range(mask,M) 也行, 因为不会冲突的
                    if (j | mask) == j:  # mask 是 j 的子集
                        f[j] = (f[j] + f[j ^ mask]) % MOD  # 不选 mask + 选 mask
        return (sum(f) - 1) % MOD  # -1 去掉空集




    """ 6363. 找出对应 LCP 矩阵的字符串 #hard #LCP 给定一个 `n x n` 的LCP矩阵, 要求 #构造 出字典序最小的字符串 限制: n 1e3
定义LCP: LCP[i][j] 表示字符串 S[i:] 和 S[j:] 的最长公共前缀的长度
正向: LCP矩阵的计算方式. lcp[i][j]=lcp[i+1][j+1]+1 若 s[i]==s[j] 否则 lcp[i][j]=0
思路1: 先尝试 #构造 出字符串, 然后 #验证 是否满足矩阵要求
    对于矩阵中==1的位置 (i,j), 它们一定是相同字符. 
    为了得到字典序最小的字符串, 可以优先填入较小的字符 (abc...)
    因此: 依次尝试填入当前剩余最小的字符 (将与它像等字符的位置也填上), 就得到了 (可能合法) 的候选字符
    最后, 按照LCP的DP方式进行验证
"""
    def findTheString(self, lcp: List[List[int]]) -> str:
        # print(np.array(lcp))
        n = len(lcp)
        s = [''] * n
        idx = 0
        for ch in string.ascii_lowercase:
            while idx < n and s[idx]: idx += 1  # 已经填好了
            if idx==n: break    # 构造完毕
            s[idx] = ch
            for j in range(idx, n):
                if lcp[idx][j]: s[j] = ch
        if '' in s: return ""
        # 验证
        for i in range(n-1,-1,-1):
            for j in range(n-1,-1,-1):  # 如果是对称的, 直接从 i...0 即可
                actual = 0
                if s[i]==s[j]:
                    if i==n-1 or j==n-1: actual=1
                    else: actual = lcp[i+1][j+1]+1
                if actual != lcp[i][j]: return ""
        return ''.join(s)
    
sol = Solution()
result = [
    # sol.mergeArrays(nums1 = [[1,2],[2,3],[4,5]], nums2 = [[1,4],[3,2],[4,1]]),
    # sol.mergeArrays(nums1 = [[2,4],[3,6],[5,5]], nums2 = [[1,3],[4,3]]),
    # sol.minOperations(39),
    # sol.minOperations(54),
    # sol.minOperations(38),
    # sol.minOperations(82),  # 3
    # sol.minOperations(701), # 5
    sol.minOperations(27),
    
    # sol.findTheString(lcp = [[4,0,2,0],[0,3,0,1],[2,0,2,0],[0,1,0,1]]),
    # sol.findTheString(lcp = [[4,3,2,1],[3,3,2,1],[2,2,2,1],[1,1,1,1]]),
    # sol.findTheString(lcp = [[4,3,2,1],[3,3,2,1],[2,2,2,1],[1,1,1,3]]),
    
]
for r in result:
    print(r)
