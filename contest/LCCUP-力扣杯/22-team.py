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
https://leetcode.cn/circle/discuss/FjxrUR/
灵神视频: https://www.bilibili.com/video/BV1rT411P7NA/

@2022 """


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ LCP 66. 最小展台数量 """
    def minNumBooths(self, demand: List[str]) -> int:
        cnt = Counter()
        for d in demand:
            for k,v in Counter(d).items():
                cnt[k] = max(cnt[k], v)
        return sum(cnt.values())

    """ LCP 67. 装饰树 在二叉树的每一个节点间插入一个值为 -1 的节点 """
    def expandBinaryTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(root: TreeNode):
            if root.left is not None:
                l = dfs(root.left)
                root.left = TreeNode(-1, l, None)
            if root.right is not None:
                r = dfs(root.right)
                root.right = TreeNode(-1, None, r)
            return root
        return dfs(root)


    """ 3. 美观的花束 """
    def beautifulBouquet(self, flowers: List[int], cnt: int) -> int:
        mod = 10**9 + 7
        n = len(flowers)
        cnter = Counter()
        r = 0
        ans = 0
        for l in range(n):
            while r<n and cnter[flowers[r]]<cnt:
                cnter[flowers[r]] += 1
                r += 1
            ans = (ans + r-l) % mod
            cnter[flowers[l]] -= 1
        return ans
    
    """ LCP 69. Hello LeetCode! #hardhard 需要从一组单词中取出 `helloleetcode` 这些字符. 在一个长n的单词中, 取出第i个字符的代价是 (i)*(n-i-1), 也即左右剩余字符长度乘积.
问取出这些字符的最小代价是多少? 限制: 单词数 n 24; 单词长度 m 8. 
思路1: #状压 #DP
    提示: 最后的选取结果是13个字符, 选取情况可以用二进制进行表示.
    考虑DP, 记 `f[i,mask]` 表示 **从第i个单词开始取, 当前选择的字符集合为 mask, 所需的最小代价**.
        转移: 考虑从 words[i] 中可选的 sub, 将其与现在的mask进行 merge. 取最小cost.
    具体而言, 
        如何表示状态? 下面灵神的表示是, 对于每一个需要的字符, 用 `(pos, limit, m)` 来定义, 分别表示当前字符在整个掩码中的位置, 所需的最大个数, 最后的m表示 位掩码.
        如何得到每个单词中可能取到的字符集合? 由于单词长度较短, 可以进行 暴力 #预处理.
    复杂度? 略, 不太好判断.
    具体见下代码, [灵神](https://leetcode.cn/problems/rMeRt2/solution/z-by-endlesscheng-6ver/)
本题的状态表示可以有更多的形式, 比如更简单的 [here](https://leetcode.cn/problems/rMeRt2/solution/daydayuppp-zhuang-ya-ji-yi-hua-sou-suo-b-0i7j/)
"""
    def Leetcode(self, words: List[str]) -> int:
        # 状态表示: dcthoolleee 分别表示每个字符出现的位置. 对于这些字符, 我们的目标分别需要取出 1,1,1,1,2,3,4 个数字
        # 因此, 我们需要最终的状态是 0b11111011100==2012
        
        # (字母在二进制上的起始位置, 这个字母能选择的上限, 位掩码)
        # 这样设计的作用? pos, limit, m = RULES[c]; 这样我们可以通过 `(mask >> pos) & m` 来快速得到一个mask中字符c现在的状态, 通过与 limit的比较判断是否还可以选择该字符.
        RULES = {
            'e': (0, 4, 7),
            'l': (3, 3, 3),
            'o': (5, 2, 3),
            'h': (7, 1, 1),
            't': (8, 1, 1),
            'c': (9, 1, 1),
            'd': (10, 1, 1),
        }
        FULL = 2012  # 0b11111011100，每个字母都选到了对应的上限
        # 合并两种选择字母的方案. 
        def merge(cur: int, add: int) -> int:
            for pos, limit, m in RULES.values():
                c1 = (cur >> pos) & m
                c2 = (add >> pos) & m
                if c1 + c2 > limit: return -1 # 判断是否可行
                cur += c2 << pos
            return cur

        # 预处理每个单词的每种选择字母的方案所消耗的代币的最小值
        costs = []
        for word in words:
            cost = {}
            def dfs(s: str, mask: int, tot: int) -> None:
                if mask not in cost or tot < cost[mask]:
                    cost[mask] = tot
                # 实际上是暴力枚举, 但因为m比较小, 所以可行
                for i, c in enumerate(s):  # 枚举选择字母的位置
                    if c not in RULES: continue
                    pos, limit, m = RULES[c]
                    if (mask >> pos) & m < limit:  # 可以选字母 c
                        dfs(s[:i] + s[i + 1:], mask + (1 << pos), tot + i * (len(s) - 1 - i))
            dfs(word, 0, 0)
            costs.append(cost)

        # @cache
        @lru_cache(None)
        # f(i, mask) 表示从第i个单词开始, 选择字母的方案为mask的最小代币消耗
        def dfs(i: int, mask: int) -> int:
            if i == len(words):
                return 0 if mask == FULL else inf  # inf 表示不合法，没有选完要求的字母
            res = inf
            for add, tot in costs[i].items():
                if tot >= res: continue  # 剪枝
                m = merge(mask, add)
                if m >= 0:
                    res = min(res, tot + dfs(i + 1, m))
            return res
        ans = dfs(0, 0)
        return ans if ans < inf else -1

    """ LCP 70. 沙地治理 #hardhard https://leetcode.cn/problems/XxZZjK/
有一组三角形grid. 在上面种植沙柳树, 传播的规则是, 三角形两边有树的话, 就可以被传播. 求最少需要种植多少棵树, 才能让所有的三角形都被传播. 限制: n 1000
"""


    """ LCP 71. 集水器 #hardhard https://leetcode.cn/problems/kskhHQ/
在一个grid中, 有一些 主/副对角线 形式的隔板. 初始状态下浸在水中, 然后往上提出容器, 问最后能够容纳多少水. 限制: grid 长宽 N 50
思路1: 核心是「从下到上」来考虑每个位置是否可能有水.
    具体而言, 将每个格子划分成 上下左右四块. 然后在遍历的过程中连接子格子.
    如何判断格子是否可能有水?
        在「从下往上」考虑的过程中, 我们考虑当前行的格子是否和边界联通! 若不连通, 则「可能」有水.
        为什么是可能? 因为如果是密闭的, 那么也不会有水.
    总结: 为何是从下往上来考虑? 在联通子格的过程中, 判断是否和边界发生了联通.
    以下代码见 [here](https://leetcode.cn/problems/kskhHQ/solution/by-minori-94tx/)
    [灵神视频](https://www.bilibili.com/video/BV1rT411P7NA/) 中的代码会更简洁一点.
"""
    def reservoir(self, shape: List[str]) -> int:
        class DisjointSet:
            # 只用路径压缩的并查集
            def __init__(self, n):
                self.fa = [i for i in range(n + 1)]
            def add(self, u, v):
                u = self.father(u)
                v = self.father(v)
                if u == v:
                    return False
                self.fa[u] = v
                return True
            def query(self, u, v):
                return self.father(u) == self.father(v)
            def father(self, u):
                if self.fa[u] == u:
                    return u
                self.fa[u] = self.father(self.fa[u])
                return self.fa[u]
        
        def g(i, j, d):
            # 从二维坐标（以及分割的四个等腰直角三角形）对应到建的无向图编号
            return i * n * 4 + j * 4 + d
        m = len(shape)
        n = len(shape[0])
        total = m * n * 4 # 总结点数
        left = set() # 与左边界相邻的结点
        right = set() # 与右边界相邻的结点
        down = set() # 与下边界相邻的结点
        up = set() # 与上边界相邻的结点
        graph = [[] for i in range(total)] # 无向图，邻接表表示
        # 步骤I：构建无向图
        for i in range(m):
            for j in range(n):
                # 0, 1, 2, 3 直角三角形划分为逆时针方向，逐次与方格的左、下、右、上相邻
                if j > 0:
                    graph[g(i, j, 0)].append(g(i, j - 1, 2))
                else:
                    left.add(g(i, j, 0))
                if j < n - 1:
                    graph[g(i, j, 2)].append(g(i, j + 1, 0))
                else:
                    right.add(g(i, j, 2))
                if i > 0:
                    graph[g(i, j, 3)].append(g(i - 1, j, 1))
                else:
                    up.add(g(i, j, 3))
                if i < m - 1:
                    graph[g(i, j, 1)].append(g(i + 1, j, 3))
                else:
                    down.add(g(i, j, 1))
                if shape[i][j] != 'r':
                    graph[g(i, j, 0)].append(g(i, j, 1))
                    graph[g(i, j, 1)].append(g(i, j, 0))
                    graph[g(i, j, 2)].append(g(i, j, 3))
                    graph[g(i, j, 3)].append(g(i, j, 2))
                if shape[i][j] != 'l':
                    graph[g(i, j, 0)].append(g(i, j, 3))
                    graph[g(i, j, 3)].append(g(i, j, 0))
                    graph[g(i, j, 1)].append(g(i, j, 2))
                    graph[g(i, j, 2)].append(g(i, j, 1))
        # 步骤II：判断初始有水的位置. 
        # 也即: 用water记录所有与「虚结点」连接的结点
        djs = DisjointSet(total)
        water = set()
        for u in range(total):
            for v in graph[u]:
                djs.add(u, v)
            if u in up or u in down or u in left or u in right:
                djs.add(u, total) # 虚结点编号为total，对应边界外部
        for u in range(total):
            if djs.query(u, total):
                water.add(u)
        # 步骤III：逐高度层处理，判断与外界的连通性. 
        # 这里重新通过图来建立并查集联通关系
        ans = 0
        djs = DisjointSet(total)
        for i in range(m - 1, -1, -1): # 从下到上处理
            for j in range(n):
                for d in range(4):
                    u = g(i, j, d)
                    for v in graph[u]:
                        if v != g(i - 1, j, 1):
                            djs.add(u, v)
                    if u in left or u in right or u in down:
                        djs.add(u, total)
            for j in range(n):
                for d in range(4):
                    u = g(i, j, d)
                    if not djs.query(u, total) and u in water: # 初始有水 and 没流出去 => 最终有水
                        ans += 1
        return ans // 2 # 每个方格蓄水量为2，每个方格的1/4的蓄水量是0.5，因此最终需要除以2

sol = Solution()
result = [
    # sol.minNumBooths(demand = ["acd","bed","accd"]),
    # sol.minNumBooths(demand = ["abc","ab","ac","b"]),
    # sol.beautifulBouquet(flowers = [1,2,3,2], cnt = 1),
    # sol.beautifulBouquet(flowers = [5,3,3,3], cnt = 2),
    # sol.beautifulBouquet([1,10,1,10,1,10],2),
    # sol.Leetcode(words = ["hold","engineer","cost","level"]),
    # sol.Leetcode(words = ["hello","leetcode"]),
    sol.reservoir(shape = ["....rl","l.lr.r",".l..r.","..lr.."]),
    sol.reservoir([".rlrlrlrl","ll..rl..r",".llrrllrr","..lr..lr."]),
    sol.reservoir(shape = ["rlrr","llrl","llr."]),
    sol.reservoir(["...rl...","..r..l..",".r.rl.l.","r.r..l.l","l.l..rl.",".l.lr.r.","..l..r..","...lr..."])
]
for r in result:
    print(r)
