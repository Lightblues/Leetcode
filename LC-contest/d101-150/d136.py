# from easonsi.util.leetcode import *
from collections import Counter
from typing import *

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
https://leetcode.cn/contest/biweekly-contest-136
T3 的数学建模需要灵光, 一开始开错题目了...
T4 #树上DP 的思路需要理清! 
Easonsi @2025 """
class Solution:
    """ 3238. 求出胜利玩家的数目 """
    def winningPlayerCount(self, n: int, pick: List[List[int]]) -> int:
        cnts = [Counter() for _ in range(n)]
        for i,j in pick:
            cnts[i][j] += 1
        return sum(1 for i,c in enumerate(cnts) if c and c.most_common(1)[0][1] > i)
    
    """ 3239. 最少翻转次数使二进制矩阵回文 I #medium 对于一个二进制矩阵, 问最少翻转多少个, 使得所有行 / 所有列都是回文的 """
    def minFlips(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        a = b = 0
        for i in range(m):
            for j in range(n//2):
                if grid[i][j] != grid[i][n-1-j]:
                    a += 1
        for j in range(n):
            for i in range(m//2):
                if grid[i][j] != grid[m-1-i][j]:
                    b += 1
        return min(a,b)
    
    """ 3240. 最少翻转次数使二进制矩阵回文 II #medium 对于一个二进制矩阵, 问最少翻转多少个, 可以使得 (1) 所有行/列都回文, (2) 并且1的数量为4的倍数
限制: mn 2e5
思路1: #分类
    显然, 对于naive情况, 4个对称格子数字都相同, 天然满足条件2; 
    这样, 只需要行/列为奇数时候的中间行/列
        若m/n有一个为奇数, 则中间行数字的个数为偶数! 考虑其对应位置 (0,1),(1,1),(0,0) 的个数. 记作 x,y,z 个
            注意, 经过x次翻转之后, (0,1)对可以满足情况1, 并且产生0/2/...2x个 1
            因此, 对于 y%2==1, 也即多了两个1的情况, 通过对(0,1)的操作可以弥补!
            总结: 仅当 y%2==1 and x==0 的时候, 需要翻转 2次; 否则需要翻转 x 次
        若m/n均为奇数, 则最中间的一定要变为0; 其他情况同上

下面看错题目了, 理解成情况1同上一题
    显然, 我们可以枚举数对 (0,1), (0,0),(1,1), (1),(0) 出现的次数, 显然只有第一种是需要修复的. 
    假设原本1的数量%4为 c1, 上述情况次数分别出现 x, d0,d1, s0,s1 次. 分类讨论: 
        c1==0: 若x%2==0, 则需要x次
            若x%2==1, 
    """
    def minFlips(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        ans = 0
        for i in range(m//2):
            for j in range(n//2):
                cnt = sum((grid[i][j], grid[i][n-1-j], grid[m-1-i][j], grid[m-1-i][n-1-j]))
                if cnt==2: ans += 2
                elif cnt==1 or cnt==3: ans += 1
        x=y=z = 0
        def update(a,b):
            nonlocal x,y,z
            if a>b: a,b = b,a
            if a==0 and b==1: x += 1
            elif a==1 and b==1: y += 1
            else: z += 1
        if m%2==1:
            for j in range(n//2):
                update(grid[m//2][j], grid[m//2][n-1-j])
        if n%2==1:
            for i in range(m//2):
                update(grid[i][n//2], grid[m-1-i][n//2])
        if x==0 and y%2==1: ans += 2
        else: ans += x
        if m%2==1 and n%2==1 and grid[m//2][n//2]==1: ans += 1
        return ans
    
    """ 3241. 标记所有节点需要的时间 #hard 对于一棵树的节点 0~n-1, 问在t=0时标记任意节点, 到所有节点都被标记的时间. 标记规则
- 对于节点 i %2 == 1, 若 t-1 时刻一个邻居被标记, 在 t时刻标记
- 对于节点 i %2 == 0, 若 t-2 时刻一个邻居被标记, 在 t时刻标记
限制: n 1e5
思路1: #树上DP
    参考示例3, edges = [[2,4],[0,1],[2,3],[0,2]]. 整体思路是两次遍历! 
        一方面, 对于root=0, 计算其到所有leaf的路径长度max;
        另一方面, 对于中间节点, 其他分支路径经过root的max信息再下传到特定分支v, -- 传递全图信息!
    注意点: 一条边的权重取决于其入节点的奇偶性! 
参见 [ling](https://leetcode.cn/problems/time-taken-to-mark-all-nodes/solutions/2868276/di-er-lei-huan-gen-dppythonjavacgo-by-en-411w/)
    核心优化在于, 第一次dfs的过程中维护了每个节点的三个信息: 
        子树 x 的最大深度 max_d，次大深度 max_d2，以及最大深度要往儿子 my 走
 """
    def timeTaken(self, edges: List[List[int]]) -> List[int]:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # 
        down_dist_map = [{} for _ in range(n)]
        def f1(u, parent) -> int:
            # calc distance from u
            for v in g[u]:
                if v==parent: continue
                down_dist_map[u][v] = f1(v, u) + (1 if v%2 else 2)
            return max(down_dist_map[u].values()) if down_dist_map[u] else 0
        f1(0, -1)
        # 
        ans = [None] * n
        def f2(u, pre) -> int:
            # pre: max distance from other_leaf -> parent -> u
            if not down_dist_map[u]:
                ans[u] = pre
            elif len(down_dist_map[u]) == 1:
                v, d = list(down_dist_map[u].items())[0]
                ans[u] = max(d, pre)
                new_pre = pre + (1 if u%2 else 2)
                f2(v, new_pre)
            else:
                mx_two = sorted(down_dist_map[u].values(), reverse=True)
                ans[u] = max(pre, mx_two[0])        # 要么是从root(其他leaf)过来的, 要么是往下到leaf
                for v, d in down_dist_map[u].items():
                    d_mx = max(pre, mx_two[0] if d!=mx_two[0] else mx_two[1])  # 从v经过u到任意leaf的最长距离
                    new_pre = d_mx + (1 if u%2 else 2)
                    f2(v, new_pre)
        f2(0, 0)
        return ans

sol = Solution()
result = [
    # sol.winningPlayerCount(n = 4, pick = [[0,0],[1,0],[1,0],[2,1],[2,1],[2,0]]),
    # sol.minFlips(grid = [[1,0,0],[0,0,0],[0,0,1]]),
    
    sol.minFlips(grid = [[1,0,0],[0,1,0],[0,0,1]]),
    sol.minFlips(grid = [[0,1],[0,1],[0,0]]),
    sol.minFlips(grid = [[1],[1]]),

    # sol.timeTaken(edges = [[0,1],[0,2]]),
    # sol.timeTaken([[0,1]]),
    # sol.timeTaken([[2,4],[0,1],[2,3],[0,2]])
]
for r in result:
    print(r)
