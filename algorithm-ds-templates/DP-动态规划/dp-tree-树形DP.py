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
https://oi-wiki.org/dp/tree/


最大价值和与最小价值和的差值
    [灵神](https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/solution/by-endlesscheng-5l70/)
1245. 树的直径 #medium 
2246. 相邻字符不同的最长路径 #hard 树上的每个节点赋予一个字符, 要求最长路径, 满足相邻两点的字符都不同. 

Easonsi @2023 """
class Solution:
    """  """
    
    
    """ 6294. 最大价值和与最小价值和的差值 #hard #题型 #树 对于一个节点上有val的树, 定义任意一个以root作为根的「开销」为, 以root作为起点的路径中, 价值和 最大的一条路径与最小的一条路径的差值
限制: n 1e5
问题等价于, 对于一棵树, 求路径最大和, 这条路径不能是两端都是Leaf
思路1: #树形DP. 
    任选一个节点作为根 #DFS, 注意在此过程中考虑子路径的组合
    (参见 示例 1 图片)
    在DFS过程中, 我们还要判断以u的孩子节点作为根得到的最大值. 它需要组合子路径. 
        例如, u下面的一条路径值为mx1, 另一条路径去掉leaf的值为m2, 则组合出来的「开销」为 mx1+m2+val, 其中val为u的价值. 这个开销对应的是路径二的叶子节点作为根节点
        因此, 递归返回 `(以u为根的最大路径, 去掉叶子的最大路径)`
    见 [灵神](https://leetcode.cn/problems/difference-between-maximum-and-minimum-price-sum/solution/by-endlesscheng-5l70/)
关联: 「1245. 树的直径」
"""
    def maxOutput(self, n: int, edges: List[List[int]], price: List[int]) -> int:
        root = 0    # 任意选取一个作为树根
        # build
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # DFS
        ans = 0
        def dfs(u,fa):
            # 返回: (以u为根的最大路径, 去掉叶子的最大路径)
            # 自己写的, 判断条件太复杂了
            nonlocal ans
            val = price[u]
            mx1,mx2 = 0,0
            childs = [v for v in g[u] if v!=fa]
            # 特判: 叶子节点
            if len(childs)==0:
                return val, 0
            for v in childs:
                m1,m2 = dfs(v,u)
                ans = max(ans, m1)
                if len(childs)>1:
                    ans = max(ans, mx1+val+m2, mx2+val+m1)
                mx1 = max(mx1, m1)
                mx2 = max(mx2, m2)
                # ans = max(ans, mx2+val)
            return mx1+val, mx2+val
        def dfs(u,fa):
            # from 灵神, 简化了判断逻辑!!
            nonlocal ans
            val = price[u]
            # 注意, 初始化一端
            mx1=val; mx2=0
            for v in g[u]:
                if v==fa: continue
                m1,m2 = dfs(v,u)
                # 当只有一个孩子的情况下, mx1=val, 不会产生问题. 
                ans = max(ans, mx1+m2, mx2+m1)
                mx1 = max(mx1, m1+val)
                mx2 = max(mx2, m2+val)
            return mx1, mx2
        dfs(root,-1)
        return ans
    
    
    """ 1245. 树的直径 #medium """
    def treeDiameter(self, edges: List[List[int]]) -> int:
        # 边界
        if len(edges)==0: return 0
        # 建树
        n = len(edges)+1
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v); g[v].append(u)
        # 
        dim = 0
        def dfs(u,fa):
            nonlocal dim
            lens = []
            for v in g[u]:
                if v==fa: continue
                l = dfs(v,u)
                lens.append(l)
                lens.sort(reverse=True)
                dim = max(dim, sum(lens[:2])+1)
            return lens[0]+1 if lens else 1
        dfs(0,-1)
        return dim-1    # 定义dim为路径上边数
    
    """ 2246. 相邻字符不同的最长路径 #hard 树上的每个节点赋予一个字符, 要求最长路径, 满足相邻两点的字符都不同. 
    #树形DP
    """
    def longestPath(self, parent: List[int], s: str) -> int:
        n = len(parent)
        g = [[] for _ in range(n)]
        for c,p in enumerate(parent):
            if p==-1: continue
            g[p].append(c); g[c].append(p)
        # 
        ans = 1
        def dfs(u,fa):
            nonlocal ans
            lens = []
            for v in g[u]:
                if v==fa: continue
                m = dfs(v,u)
                if s[v]!=s[u]:
                    lens.append(m)
            lens.sort(reverse=True)
            ans = max(ans, sum(lens[:2])+1)
            return lens[0]+1 if lens else 1
        dfs(0,-1)
        return ans


    
    
    

    
sol = Solution()
result = [
    # sol.maxOutput(n = 3, edges = [[0,1],[1,2]], price = [1,1,1]),
    # sol.maxOutput(n = 6, edges = [[0,1],[1,2],[1,3],[3,4],[3,5]], price = [9,8,7,6,10,5]),
    
    # sol.treeDiameter(edges = [[0,1],[1,2],[2,3],[1,4],[4,5]]),
    # sol.longestPath(parent = [-1,0,0,1,1,2], s = "abacbe"),
]
for r in result:
    print(r)
