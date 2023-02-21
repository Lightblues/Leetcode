from easonsi.util.leetcode import *


""" 
5289. 公平分发饼干 #medium
1655. 分配重复整数
1178. 猜字谜 #hard
6364. 无平方子集计数 实际上 #hard
"""

class Solution:
    """ 6364. 无平方子集计数 实际上 #hard 考虑数组的所有子集中, 各个元素的乘积不包含平方因子, 这样的子集的数量 限制: n 1e3; 元素大小 [1,30]
预处理: 
    把「无平方因子数的数字」记作 NSQ.
    我们把 [2,30]  范围内的数字, 根据质因子分解得到其表示 (二进制)
思路1: 转换成 0-1 背包方案数
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
        # 思路2: #子集状压 DP
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
        MOD = 10 ** 9 + 7
        cnt = Counter(nums)
        M = 1 << len(PRIMES)
        f = [0] * M  # f[j] 表示恰好组成集合 j 的方案数
        f[0] = 1  # 空集的方案数为 1
        
        """ 注意到, 这里的顺序不太重要, 我们顺序的考虑前 i个数字可以构成的组合! """
        for x, c in cnt.items():
            mask = NSQ_TO_MASK[x]
            if mask > 0:  # x 是 NSQ
                # 枚举与mask没有交集的其余集合other; 更新 f[i][other|mask] += f[i-1][other] * c
                # 空间优化: 倒序枚举 other
                # 方法1: 直接枚举 other
                # for other in range(M-1,-1,-1):
                #     if (other&mask) == 0:
                #         f[other|mask] = (f[other|mask] + f[other] * c) % MOD  # 不选 mask + 选 mask
                
                # 方法2: 枚举补集的子集!!
                other = (M - 1) ^ mask  # mask 的补集
                j = other
                # 如何枚举包括空集? 可以用 while True 配合下面的 break 语法!
                while True:  # 枚举 other 的子集 j
                    f[j | mask] = (f[j | mask] + f[j] * c) % MOD  # 不选 mask + 选 mask
                    j = (j - 1) & other
                    if j == other: break # 注意这里的边界条件! 会枚举到0 (空集)
        return (sum(f) * pow(2, cnt[1], MOD) - 1) % MOD  # -1 去掉空集

    """ 1178. 猜字谜 #hard 一个word可以作为puzzle所匹配的条件是, word中所有字符都在puzzle中出现过, 并且包含其第一个字符. 现在给定一组 words 和 puzzles, 对于每个puzzle判断其可以作为多少word的谜面. 
限制: words数量 n 1e5; 每个词的长度 4...50; puzzle数量 m 1e4, 每个词的长度都是7 都是7个不同的字符. 
提示, 可以用二进制表示puzzle中所包含的7个字符, 再加上首位字符即可表示该谜面. (mask, firstCh)
思路1: 二进制 #状态压缩 的基础上, 进行 #子集枚举
    用什么来存储word的信息? 重要的只有其中所包含的字符, 直接二进制表示, 用一个cnt = {mask: freq} 存储即可.
    如何得到每个puzzle可能匹配的word? 其首字母一定到, 其他的六个字母 #子集枚举 即可. 
    复杂度分析: 对于所有的puzzle, 需要进行 2^6 级别的子集枚举. 
说明: 如何进行子集枚举? 1) 一种方式是对于 0~2^6 选出子集; 2) 也可以先得到6个字符的mask, 然后用 subset = (subset - 1) & mask 的方式筛选. 
见 [官答](https://leetcode.cn/problems/number-of-valid-words-for-each-puzzle/solution/cai-zi-mi-by-leetcode-solution-345u/)
"""
    def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:
        # 记录所有的谜面 (word) 信息: 计数
        cnt = Counter()
        for word in words:
            mask = 0
            for ch in word:
                mask |= 1 << (ord(ch) - ord('a'))
            cnt[mask] += 1
        # 得到所有的 6个字符的组合 (子集)
        combs = []
        for m in range(2**6):
            i = 0
            idxs = []
            while m:
                if m & 1: idxs.append(i)
                m>>=1; i+=1
            combs.append(idxs)
        # 对于每个puzzle, 进行子集枚举
        ans = []
        for puzzle in puzzles:
            acc = 0
            # 注意这里的 mask, chars 计算方式!
            mask = 1 << (ord(puzzle[0]) - ord('a'))
            chars = [1<<(ord(c)-ord('a')) for c in puzzle[1:]]
            for comb in combs:
                m = reduce(operator.or_, [mask] + [chars[i] for i in comb])
                acc += cnt[m]
            ans.append(acc)
        return ans

    """ 5289. 公平分发饼干 #medium 同 1723. 完成所有工作的最短时间
有一组饼干数组 cookies, 要分给k个孩子, 定义分配的不公平程度为所分配数的最大值. 要求所有分配方式中, 不公平程度最小化.
约束: 数组长度 n<=8; 分配数 k<=m
思路1: 暴力 #dfs + #剪枝
思路2: #状态压缩 #DP #子集遍历 [dp-subset]
    我们定义 `f[i][mask]` 表示分配完前i个孩子, 当前分配的饼干集合为mask, 时的最小不公平程度.
    我们遍历分配给第i个孩子的集合sub, 这样有 `f[i][mask] = min{ max{ f[i-1][mask\sub], sum[sub] } }` 这里的sub是mask的所有子集, sum[sub] 表示sub集合中的元素之和.
    因此, 需要两层遍历, 第一层遍历i, 第二层遍历mask (还要遍历mask的所有子集). 注意到, 若我们对于mask从大到小遍历, 则可以省略dp的第一个维度.
    遍历子集采用经典的 `sub = (sub - 1) & mask` 方式.
    复杂度: 对于mask从1遍历到 1<<n, 每次遍历mask所有的子集, 其复杂度为 `O(3^n)` (恰好是排列公式). 因此总复杂度为 O(k * 3^n).
    from [灵神](https://leetcode.cn/problems/fair-distribution-of-cookies/solution/by-endlesscheng-80ao/)
"""
    def minimumTimeRequired(self, jobs: List[int], k: int) -> int:
        """ 思路2: [灵神](https://leetcode.cn/problems/fair-distribution-of-cookies/solution/by-endlesscheng-80ao/) """
        n = len(jobs)
        # 预计算每一个mask所代表的工作集合之和
        sub2cost = [0] * (1<<n)
        for mask in range(1<<n):
            cost = 0
            for i,c in enumerate(jobs):
                if mask>>i & 1:
                    cost += c
            sub2cost[mask] = cost
        # f[i][mask] 表示给前i工人分配工作, 所有已分配的工作为为mask时的最短时间.
        # f = [[0] * (2<<n) for _ in range(k)]
        last = sub2cost[:]
        for i in range(1, k):
            new = [inf] * (1<<n)
            for mask in range(1, 1<<n):
                sub = mask
                while sub:
                    new[mask] = min(new[mask], max(last[mask^sub], sub2cost[sub]))
                    sub = (sub - 1) & mask
            last = new
        return last[-1]

sol = Solution()
result = [
    # sol.findNumOfValidWords(words = ["aaaa","asas","able","ability","actt","actor","access"], puzzles = ["aboveyz","abrodyz","abslute","absoryz","actresz","gaswxyz"]),

]
for r in result:
    print(r)