from typing import *
from functools import cache
import math
import itertools
import operator
import bisect
import heapq

"""
https://leetcode.cn/contest/weekly-contest-456
1. 关于字符串哈希的题目
    注意字符串 hash 的复杂度; 
    另外字典树的实现也值得借鉴!
2. 对于一个数组, 计算去除任意位置元素后的影响
    "维护前二大 LCP" 的思路 & 代码技巧
    这类问题 "前后缀分解" 的思路!
3. 最小化最大值问题 
    1. 划分型DP 属于 "约束划分个数" 的题型
    2. 这类问题另一类想法: 二分! -- 不过还需要建图求解
    3. 更完全地建模为图上搜索问题 -- Dijkstra
4. 最大化生成树边权问题, 核心是对于 生成树 的理解 -- 通过并查集来检查!
Easonsi @2026 """


class Solution:
    """ 3597. 分割字符串 给定一个字符串进行分段. 规则是记录所有已出现的段, 思路出现一个新段 
限制: n 1e5
思路 1: #哈希集合
    复杂度: NOTE 字符串 #hash 的复杂度为 O(L)! -- 计算 hash 的操作
        因此, 考虑构成段的最大长度, 可知在所有字符都相同的情况下最大为 1,2,... -> 因此最大长度为 log n
        考虑遍历操作, 整体复杂度 O(n logn)
思路 2: #字典树 #trie
    复杂度: O(n) -- 这里是用 hash 来实现的; 如果是列表来存储 (而非字典) 复杂度为 O(n|Σ|)
https://leetcode.cn/problems/partition-string/solutions/3710991/an-ti-yi-mo-ni-ha-xi-ji-he-pythonjavacgo-p761/
    """
    def partitionString(self, s: str) -> List[str]:
        st = set()
        ans = []
        l = 0
        for i,ch in enumerate(s):
            if s[l:i+1] not in st:  # NOTE: 这里可以通过维护一个递增的字符串来避免字符串切分!
                ans.append(s[l:i+1])
                st.add(s[l:i+1])
                l = i+1
        return ans

    def partitionString(self, s: str) -> List[str]:
        curr = root = {}
        ans = []
        l = 0
        for i, c in enumerate(s):
            if c not in curr:
                curr[c] = {}
                ans.append(s[l:i+1])
                curr = root
                l = i+1
            else: curr = curr[c]
        return ans

    """ 3598. 相邻字符串之间的最长公共前缀 #medium
对于一个字符串数字, 计算移除每一个i 位置 word 后, "相邻字符串的最长前缀的最大值"
限制: n 1e5; L 1e4
思路 1: 维护前三大 LCP
    对于原数组, 可以计算所有相邻位置的 #LCP. 对于一次移除操作, 减少两个 lcp, 新增一个 -- 考虑这些变化即可!
        在代码实现上, 只需要位置 mx1,mx2,mx3, i1,i2 即可! 其中 i1/i2 标记最大/次大出现的位置, 在 for 循环中可以简化判断!
        - 若移除元素 i 影响了 mx1,mx2, 答案为 max(mx3, l); -- 其中 l 为新增那个 lcp
        - 若只影响 mx1, 答案为 max(mx2, l);
        - 否则, 答案为 max(mx1, l);
    复杂度: O(L), 其中 L 为所有 word 长度之和
    ling 提供了优雅得多的代码!
思路 2: 维护前二大 LCP
    对于上面继续优化! 考虑 "同时影响 mx1,mx2" 的情况, 只可能出现在 i1,i2 相邻的时候!
    有定理: 此时 l >= mx2. 因此直接返回 l 即可!
        直接考虑 (A, B, C), 假设 lcp 分别为 mx1, mx2, 可知 lcp(A,C)>=mx2
思路 3: #前后缀分解
    对于位置 i, 问题等价于: max{ max(0..i-1), lcp(i-1,i+1), max(i+1...n-1) }
    计算 "前后缀" 最大值, 可以直接 #递推 计算
    复杂度: O(L)
https://leetcode.cn/problems/longest-common-prefix-between-adjacent-strings-after-removals/solutions/3710963/qian-hou-zhui-fen-jie-pythonjavacgo-by-e-8sn2/
    """
    def longestCommonPrefix(self, words: List[str]) -> List[int]:
        if len(words) <= 2: return [0] * len(words)  # NOTE: 注意边界!
        def check(s: str, t: str) -> int:
            for i, (a,b) in enumerate(zip(s,t)):
                if a!=b: return i
            return min(len(s), len(t))
        n = len(words)
        dist = [check(words[i], words[i+1]) for i in range(n-1)]
        dist_max = sorted(dist, reverse=True)[:3]
        ans = []
        for i in range(n):
            dist_max_ = dist_max[:]
            if i-1>=0 and dist[i-1] in dist_max_: dist_max_.remove(dist[i-1])
            if i<n-1 and dist[i] in dist_max_: dist_max_.remove(dist[i])
            if i-1>=0 and i+1<n: dist_max_.append(check(words[i-1], words[i+1]))
            ans.append(max(dist_max_))
        return ans

    def longestCommonPrefix(self, words: List[str]) -> List[int]:
        # 思路 3: #前后缀分解
        @cache
        def lcp(s: str, t: str) -> int:
            cnt = 0
            for a,b in zip(s,t):
                if a==b: cnt += 1
                else: break
            return cnt

        n = len(words)
        if n == 1: return [0]
        suf_max = [0] * n  # words[i:] 的后缀最大值
        for i in range(n-2, -1, -1):
            suf_max[i] = max(suf_max[i+1], lcp(words[i], words[i+1]))
        ans = [0] * n
        ans[0] = suf_max[1]  # 第一个对应位置为 1
        pre_max = 0
        for i in range(1,n-1):  # 注意边界!
            ans[i] = max(pre_max, lcp(words[i-1],words[i+1]), suf_max[i+1])
            pre_max = max(pre_max, lcp(words[i-1], words[i]))
        ans[-1] = pre_max  # 只计算到了 n-2!
        return ans

    """ 3599. 划分数组得到最小 XOR
要求将数组划分为 k 段, 要求 min{ max(XOR(seg)) }
限制: n,k 250
思路 1: #划分型DP 属于 "约束划分个数" 的题型
    记 f(i,j) 为对于前缀 i 拆分成j 段的最小值, 则有 f(i,j) = min{ max(f(k-1,j-1), xor(k..i)) }
    复杂度: O(k(n-k)^2) 平方项是 n-1,...,n-k+1 枚举构成! 
    优化: 下面 NOTE 里面的两点, 参见 ling
思路 2: 二分 (但二分里面还是得写 DP, 没必要)
    考虑二分: 则问题变为, 在上界 upper 限制, 对于所有的 (i,j), 若 xor(i+1...j) <= upper 则连边, 问是否有从 0 -> n 的路径, 恰好 k 步
    定义 dfs (i) 为 从 i 到 0 的所有可能的步数集合, 例如若从 5 到 0 可以走 1/3/4 步, 则 dfs(5) = {1,3,4}
    边界: dfs(0) = {0}
    入口: dfs(n) -> 答案就是判断其中是否包含 k
    #技巧: 为计算区域 xor, 有 xor(i+1...j) = pre_xor(i) ^ pre_xor(j)
    复杂度: O(n^3/w logU), 其中 U 为搜索范围; n^2 为搜索的复杂度; O(n/w) 是处理位长 n 的二进制集合表示的复杂度!
思路 3: 采用 #Dijkstra
    考虑从 (n,k) -> (0,0) "最短路" -- 其中最短的定义不是求和而是 max 操作
    建图方式同上，边权为子数组异或和
    复杂度: O(M logM), 其中边数 M = n^2k
https://leetcode.cn/problems/partition-array-to-minimize-xor/solutions/3710966/hua-fen-xing-dp-de-tong-yong-tao-lu-pyth-lmcm/
    """
    def minXor(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # 初始化 j=1
        f = []; xor_ = 0
        for x in nums:  # NOTE: 可以合并到下面 for 中
            xor_ ^= x
            f.append(xor_)
        for j in range(2,k+1):
            nf = [-1] * n  # NOTE: 可以倒序原地更新, 不用开新数组
            for i in range(j-1,n):
                mn = math.inf
                xor_ = 0
                for k in range(i, j-2, -1):
                    xor_ ^= nums[k]
                    mn = min(mn, max(f[k-1], xor_))
                nf[i] = mn
            f = nf
        return f[-1]

    def minXor(self, nums: List[int], k: int) -> int:
        s = list(itertools.accumulate(nums, operator.xor, initial=0))  # 前缀异或和; accumulate 包括前缀 0

        def check(upper: int) -> bool:
            @cache
            def dfs(i: int) -> int:
                if i==0: return 1
                res = 0
                for j in range(i):
                    if s[i] ^ s[j] <=upper:
                        res |= dfs(j) << 1  # 位运算复杂度: O(n/w)
                return res
            return dfs(len(nums)) >> k & 1 > 0

        mx = (1 << max(nums).bit_length()) - 1  # 二分最大: 看最大数字有多少位!
        # NOTE: 位运算优先级!
        return bisect.bisect_left(range(mx), True, key=check) # NOTE: bisect 用法

    def minXor(self, nums: List[int], k: int) -> int:
        max = lambda a, b: b if b > a else a
        s = list(itertools.accumulate(nums, operator.xor, initial=0))  # 前缀异或和; accumulate 包括前缀 0
        n = len(nums)

        dist = [[math.inf] * (k+1) for _ in range(n+1)]
        h = [(0, n, k)]
        while h:
            d, i, k_ = heapq.heappop(h)
            if d > dist[i][k_]: continue  # 已有更优的达到 (i,k_) 的方案
            if k_==0:  # 走完了 k 步
                if i==0: return d
                continue
            for j in range(i):
                nd = max(s[i] ^ s[j], d)
                if nd < dist[j][k_-1]:
                    dist[j][k_-1] = nd
                    heapq.heappush(h, (nd, j, k_-1))
        # NOTE: 题目保证了一定有答案 (k<=n)

    """ 3600. 升级后最大生成树稳定性
给定一组边 (u,v,s,must), s 是初始的强度; must=1 表示必须出现在生成树中, 且不能升级; =0 表示可升级一次 s*=2
给定最多k 次升级, 求 max{生成树稳定性}, "稳定性" 为生成树的最小边权
限制: n 1e5
思路 1: 二分答案 + 并查集
    处理边界情况: 若本身不联通, 或者 must 构成了环, 返回 -1, 否则一定有值
    确保有解的情况下, 采用 #二分
        对于每个 low 做 check:
            首先, 处理所有 must=1 (若 s<low 直接不可行) 和 s>=lower 的边 -- 利用并查集合并
            然后, 依次遍历所有剩余边, 若 2s>=low, 说明可以连接两个 component, 加入! 验证在 k 范围内是否可以做到
                NOTE: 只需要遍历即可! 生成树特性!
    复杂度: O((n+mlogn) logU) 其中m 为边数; logU 是二分复杂度.
思路 2: 可以用 #Kruskal 算法 来求 #最大生成树
    """
    def maxStability(self, n: int, edges: List[List[int]], k: int) -> int:
        pass

sol = Solution()
result = [
    # sol.partitionString(s = "abbccccd"),
    # sol.partitionString("aaaa"),
    # sol.longestCommonPrefix(["jump","run","run","jump","run"]),
    sol.minXor(nums = [1,2,3], k = 2),
    sol.minXor(nums = [2,3,3,2], k = 3),
]
for r in result:
    print(r)