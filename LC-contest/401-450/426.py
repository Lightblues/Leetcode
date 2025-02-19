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
https://leetcode.cn/contest/weekly-contest-426

两道树上的题目, 比较 easy
Easonsi @2024 """
class Solution:
    """ 3370. 仅含置位位的最小整数 #easy 将所有二进制位转为1即可 """
    def smallestNumber(self, n: int) -> int:
        s = bin(n)[2:]
        return int('1'*len(s), 2)

    """ 3371. 识别数组中的最大异常值 """
    def getLargestOutlier(self, nums: List[int]) -> int:
        c = Counter(nums)
        s = sum(nums)
        for a in sorted(c.keys(), reverse=True):
            if (s-a)%2!=0:
                continue
            target = (s-a)//2
            if target in c and (target!=a or c[target]>1):
                return a
        return -1

    """ 3372. 连接两棵树后最大目标节点数目 I #medium 有两棵树, 定义一个节点的 "目标节点" 为距离它 <=k 的节点. 对于树A上的所有节点, 问连接B的任意节点之后, 最多的目标节点数量
限制: n 1e3
思路1: 等价于, 在A上计算每个点距离k的节点数量; 在B上计算距离 k-1 的节点的最大数量是多少. 
    复杂度: 因为对于每个节点暴力搜索, 复杂度为 O(n^2 + m^2)
ling 优雅的代码 https://leetcode.cn/problems/maximize-the-number-of-target-nodes-after-connecting-trees-i/solutions/3006334/nao-jin-ji-zhuan-wan-bao-li-mei-ju-pytho-ua6k/
    """
    def maxTargetNodes(self, edges1: List[List[int]], edges2: List[List[int]], k: int) -> List[int]:
        n, m = len(edges1)+1, len(edges2)+1
        def build_tree(edges):
            g = defaultdict(list)
            for u,v in edges:
                g[u].append(v)
                g[v].append(u)
            return g
        g1 = build_tree(edges1)
        g2 = build_tree(edges2)
        
        def search(g, i, fa, k):
            if k<0: return 0
            if k==0: return 1
            ans = 1
            for j in g[i]:
                if j==fa: continue
                ans += search(g, j, i, k-1)
            return ans
        d = max(search(g2, i, -1, k-1) for i in range(m))
        return [search(g1, i, -1, k) + d for i in range(n)]
    
    """ 3373. 连接两棵树后最大目标节点数目 II #hard 对于上一题的目标节点, 定义为 "距离为偶数" 的节点 (自己的距离为0也算)
限制: n 1e5
思路1: #树形DP 可以计算每个点距离为偶数的节点数量
ling https://leetcode.cn/problems/maximize-the-number-of-target-nodes-after-connecting-trees-ii/solutions/3006331/an-qi-ou-fen-lei-pythonjavacgo-by-endles-dweg/
    """
    def maxTargetNodes(self, edges1: List[List[int]], edges2: List[List[int]]) -> List[int]:
        n, m = len(edges1)+1, len(edges2)+1
        def build_tree(edges):
            g = defaultdict(list)
            for u,v in edges:
                g[u].append(v)
                g[v].append(u)
            return g
        g1 = build_tree(edges1)
        g2 = build_tree(edges2)
        
        def color_tree(g):
            res = [-1] * len(g)
            def dfs(i, fa, c=0):
                res[i] = c
                for j in g[i]:
                    if j==fa: continue
                    dfs(j, i, c^1)
            dfs(0, -1, 0)
            return res
        c1 = color_tree(g1)
        c2 = color_tree(g2)
        delta = max(Counter(c2).values())
        cnt = [0] * 2
        for x in c1: 
            cnt[x] += 1
        return [cnt[x] + delta for x in c1]
    

sol = Solution()
result = [
    # sol.smallestNumber(10)
    # sol.getLargestOutlier(nums = [-2,-1,-3,-6,4])
    # sol.maxTargetNodes(edges1 = [[0,1],[0,2],[2,3],[2,4]], edges2 = [[0,1],[0,2],[0,3],[2,7],[1,4],[4,5],[4,6]], k = 2),
    # sol.maxTargetNodes([[0,1]], [[0,1]], 0),
    
    sol.maxTargetNodes(edges1 = [[0,1],[0,2],[2,3],[2,4]], edges2 = [[0,1],[0,2],[0,3],[2,7],[1,4],[4,5],[4,6]]),
]
for r in result:
    print(r)
