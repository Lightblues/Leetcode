from typing import *
from functools import lru_cache

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-142

T2 的DFS需要 "恢复现场", 需要注意!
T4 没有事先进行复杂度分析, 思路错误.
Easonsi @2025 """
class Solution:
    """ 3330. 找到初始输入字符串 I  """
    def possibleStringCount(self, word: str) -> int:
        ans = 1
        pre = ''
        for c in word:
            if c == pre: ans += 1
            pre = c
        return ans

    """ 3331. 修改后子树的大小 #medium 一棵树上, 每个节点有一个字母. 现在同时进行一次操作: 对于节点x, 找到其最近的祖先节点满足 s[x]==s[y], 然后将x的父亲设置为y. 问经过操作后的各节点的子树大小
限制: n 1e5
思路1: 先 #DFS 找到所有所有节点的父节点 -- 得到重构之后的树
    NOTE: 在DFS过程中, 需要 "恢复现场"!
[ling](https://leetcode.cn/problems/find-subtree-sizes-after-changes/solutions/2966800/liang-ci-dfszi-ding-xiang-xia-zi-di-xian-k4zj/)
    """
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        n = len(parent)
        g = [[] for _ in range(n)]
        for i,p in enumerate(parent):
            if p == -1: continue
            g[p].append(i)
        # build the new tree
        ng = [[] for _ in range(n)]
        def f(u: int, p: int, h: dict[int,int]):
            if s[u] in h:
                ng[h[s[u]]].append(u)
            else:
                if p != -1:  # avoid root!
                    ng[p].append(u)
            old = h.get(s[u], None)
            h[s[u]] = u
            for v in g[u]:
                f(v, u, h)
            if old is not None: h[s[u]] = old  # 恢复现场!
            else: h.pop(s[u])
        f(0, -1, {})
        # BFS the size of each subtree
        ans = [0] * n
        def f(u: int) -> int:
            c = 1
            for v in ng[u]:
                c += f(v)
            ans[u] = c
            return c
        f(0)
        return ans

    """3332. 旅客可以得到的最多点数 #medium 在n个城市旅游k天, 每天可以做两种决策: 1) 呆在改城市, 获得 stayScore[i][curr]; 2) 移动到另一城市, 获得  travelScore[curr][dest], 其中i为第i天. 求最大得分. 可以从任意出发
限制: n,k 200
思路1: 经典 #DP
    记 f[i,j] 表示第i天在j城市的最大得分, 则可通过所有的 n 个决策从后往前推. 
    复杂度: O(n^2k)
    """
    def maxScore(self, n: int, k: int, stayScore: List[List[int]], travelScore: List[List[int]]) -> int:
        @lru_cache(None)
        def f(i: int, j: int) -> int:
            if i==k: return 0
            return max(f(i+1,j)+stayScore[i][j], max(f(i+1,v)+travelScore[j][v] for v in range(n)))
        return max(f(0,j) for j in range(n))


    """3333. 找到初始输入字符串 II #hard 键盘输入, 可能重复的情况下, 已知最终输出, 以及意图的输入至少为k. 求所有可能, 取模.
限制: n 5e5; k 2e3
思路1: 模拟 #TLE
    首先构造非重复字符串 & 每个字符的重复次数. 然后枚举 f(i,j) 表示第i个字符可以构成多少长j的字符串
    e.g. 对于 aaabbb; 非重复为 ab, dup=[3,3]
    则对于 i==0, 可以构成 [1,1,1]. 长度范围 [1,3]
    对于 i==1, 可以构成 [0,1,2,3,2,1], 长度范围 [2,6] -- 观察其变化, 是一个滑动窗口!
    复杂度: 然而, 这样的复杂是 O(nk), 会超!
思路2: #DP + #前缀和
    问题转化: 等价于任意长度方案数 - 长度 < k 的方案数
    前者直接乘法即可. 对于后者, 记非重复字符出现频次数组为 freq, 则有转移:
    f[i,j] = sum{f[i-1, j-j'], 其中 1 <= j' <= freq[i]}, 其中 f[i,j] 表示用前i种字符构成长j的方案.
    这样复杂度为 O(k^3), 会超时!
    注意到转移方程是对前一个状态组的线性求和, 因此可以引入前缀和优化!
[official](https://leetcode.cn/problems/find-the-original-typed-string-ii/solutions/3706277/zhao-dao-chu-shi-shu-ru-zi-fu-chuan-ii-b-ldyv/)
    """
    def possibleStringCount(self, word: str, k: int) -> int:
        # TLE方案!
        MOD = 10**9 + 7
        word2 = []; dup = []
        pre, cnt = "", 0
        for c in word + " ":
            if c == pre:
                cnt += 1
            else:
                if pre:
                    word2.append(pre)
                    dup.append(cnt)
                pre, cnt = c, 1
        # 
        mn, mx = 1, dup[0]; pre = [1] * mx
        for c in dup[1:]:
            mn, mx = mn+1, mx+c
            new = []
            acc = 0
            for j in range(mx-mn+1):
                if j < len(pre): acc += pre[j]
                if j-c >= 0: acc -= pre[j-c]
                new.append(acc % MOD)
            pre = new
        idx = max(0, k-mn)
        return sum(pre[idx:]) % MOD


sol = Solution()
result = [
    # sol.possibleStringCount(word = "abbcccc"),

    sol.findSubtreeSizes(parent = [-1,0,0,1,1,1], s = "abaabc"),
    sol.findSubtreeSizes(parent = [-1,0,4,0,1], s = "abbba"),
    
    # sol.maxScore(n = 3, k = 2, stayScore = [[3,4,2],[2,1,2]], travelScore = [[0,2,1],[2,0,4],[3,2,0]]),

    sol.possibleStringCount(word = "aabbccdd", k = 7),
]
for r in result:
    print(r)
