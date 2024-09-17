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
https://leetcode.cn/contest/weekly-contest-410
T4: TODO: 


Easonsi @2023 """
class Solution:
    """ 3248. 矩阵中的蛇 """
    def finalPositionOfSnake(self, n: int, commands: List[str]) -> int:
        x,y = 0,0
        for c in commands:
            if c=="RIGHT": x+=1
            elif c=="LEFT": x-=1
            elif c=="UP": y-=1
            else: y+=1
        return n*y+x
            
    """ 3249. 统计好节点的数目 """
    def countGoodNodes(self, edges: List[List[int]]) -> int:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        
        ans = 0
        def dfs(u, fa) -> int:
            nonlocal ans
            chlid_num_counts = []
            for v in g[u]:
                if v==fa: continue
                chlid_num_counts.append(dfs(v,u))
            if len(chlid_num_counts)==0 or len(set(chlid_num_counts))==1:
                ans += 1
            return sum(chlid_num_counts+[1])
        dfs(0,-1)
        return ans
    
    """ 3250. 单调数组对的数目 I 
    3251. 单调数组对的数目 II #hard 
https://leetcode.cn/problems/find-the-count-of-monotonic-pairs-ii/solutions/2876190/qian-zhui-he-you-hua-dppythonjavacgo-by-3biek/
"""

sol = Solution()
result = [
    sol.countGoodNodes(edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]),
]
for r in result:
    print(r)
