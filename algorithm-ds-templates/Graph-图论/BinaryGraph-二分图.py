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

class BinaryGraph:
    def __init__(self, n, m) -> None:
        self.g = [[] for _ in range(n)]     # 仅记录单向边.
        self.n = n  # 左右两组点的数量.
        self.m = m
        self.pa = [-1] * n
        self.pb = [-1] * m
        self.dfn = 0        # 时间戳记
        self.vis = [0] * n  # 访问时间戳
    
    def add(self, u,v):
        self.g[u].append(v)
    
    def dfs(self, v):
        # 最大匹配
        self.vis[v] = self.dfn
        for u in self.g[v]:
            if self.pb[u] == -1 or (self.vis[self.pb[u]] != self.dfn and self.dfs(self.pb[u])):
                self.pa[v] = u
                self.pb[u] = v
                return True
        return False

    def solve(self):
        res = 0
        while True:
            # 不断地尝试增广.
            self.dfn += 1
            cnt = 0
            for i in range(self.n):
                if self.pa[i] == -1 and self.dfs(i):
                    cnt += 1
            if cnt==0: break
            res += cnt
        return res

""" 
https://leetcode.cn/contest/weekly-contest-312
https://leetcode-cn.com/contest/biweekly-contest-81
@2022 """
class Solution:
    """ LCP 04. 覆盖 #hard #hardhard 给定一个grid, 有些部分是坏的, 问能够不重叠地防止多少个 1*2 的骨牌 (可横放). 限制: 长宽 n 8.
提示: 将grid按照相邻的规则标记为 x,y, 则放置的骨牌一定占据 1个x, 1个y. 注意到, **可以将本问题转化为二分图最大匹配**.
思路1: 为了求最大匹配, 可以用 #匈牙利 算法.
    基本思路: 1) 初始时，最大匹配集合为空; 2) 我们先找到一组匹配边，加入匹配集合; 3) 找到一条增广路径，我们将其中的所有匹配边变为未匹配边，将所有的未匹配边变为匹配边; 4) 循环步骤 33，直到图中不存在增广路径。算法结束
    所谓「增广路径」: 匹配/未匹配边交替, 并且以未匹配边开始和结束的路径.
    复杂度: 匈牙利算法的复杂度为 O(EV), 本题中节点, 边都是 mn, 因此总体 `O(m^2n^2)`.
[here](https://leetcode.cn/problems/broken-board-dominoes/solution/suan-fa-xiao-ai-cong-ling-dao-yi-jiao-hu-8b4k/)
"""
    def domino(self, n: int, m: int, broken: List[List[int]]) -> int:
        bg = BinaryGraph(n*m, n*m)
        
        graph = [[0]*m for _ in range(n)]
        for i,j in broken: graph[i][j] = 1
        
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        # (i, j) -> 四边扩展
        for i in range(n):
            for j in range(m):
                if graph[i][j]: continue
                for dx,dy in directions:
                    x,y = i+dx, j+dy
                    if 0<=x<n and 0<=y<m and not graph[x][y]:
                        if (i+j)%2==0:
                            bg.add(i*m+j, x*m+y)
        return bg.solve()
    
    
    
    

    
sol = Solution()
result = [
    sol.domino(n = 2, m = 3, broken = [[1, 0], [1, 1]]),
    sol.domino(n = 3, m = 3, broken = []),
]
for r in result:
    print(r)
