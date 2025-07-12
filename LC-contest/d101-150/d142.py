from typing import *
from functools import lru_cache

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-142

Easonsi @2025 """
class Solution:
    def possibleStringCount(self, word: str) -> int:
        ans = 1
        pre = ''
        for c in word:
            if c == pre: ans += 1
            pre = c
        return ans

    """  """
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        n = len(parent)
        g = [[] for _ in range(n)]
        for i,p in enumerate(parent):
            if p == -1: continue
            g[p].append(i)
        ng = [[] for _ in range(n)]
        def f(u: int, p: int, h: dict[int,int]):
            if s[u] in h:
                ng[h[s[u]]].append(u)
            else:
                if p != -1:  # avoid root!
                    ng[p].append(u)
            isnew = s[u] not in h
            if isnew: h[s[u]] = u
            for v in g[u]:
                f(v, u, h)
            if isnew: del h[s[u]]
        f(0, -1, {})
        ans = [0] * n
        def f(u: int) -> int:
            c = 1
            for v in ng[u]:
                c += f(v)
            ans[u] = c
            return c
        f(0)
        return ans

    """ 在n个城市旅游k天, 每天可以做两种决策: 1) 呆在改城市, 获得 stayScore[i][curr]; 2) 移动到另一城市, 获得  travelScore[curr][dest], 其中i为第i天. 求最大得分. 可以从任意出发
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


    """ 键盘输入, 可能重复的情况下, 已知最终输出, 以及意图的输入至少场k. 求所有可能, 取模.
限制: n 5e5; k 2e3
    """
    def possibleStringCount(self, word: str, k: int) -> int:
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
        pre = []; mn = mx = 0
        for i,c in enumerate(dup):
            mn, mx = mn+1, mn+c
            new = []
            acc = 0
            for j in range(mx-mn+1):
                if j < len(pre): acc += pre[j]
                if j-c >= 0: acc -= pre[j-c]
                new.append(acc)
            pre = new
        return pre[k]


sol = Solution()
result = [
    # sol.possibleStringCount(word = "abbcccc"),

    # sol.findSubtreeSizes(parent = [-1,0,0,1,1,1], s = "abaabc"),
    # sol.findSubtreeSizes(parent = [-1,0,4,0,1], s = "abbba"),
    
    sol.maxScore(n = 3, k = 2, stayScore = [[3,4,2],[2,1,2]], travelScore = [[0,2,1],[2,0,4],[3,2,0]]),
]
for r in result:
    print(r)
