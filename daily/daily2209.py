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

@2022 """
class Solution:
    """ 0785. 判断二分图 #medium 给定一张图, 判断是否二分. 限制: 节点数 n 100.
思路1: 由于仅仅要判断是否二分, 可以随便从那个节点开始DFS, 对于相邻节点涂上另一种颜色即可.
    """
    def isBipartite(self, graph: List[List[int]]) -> bool:
        # 1. 颜色标记法
        # 2. 深度优先搜索
        n = len(graph)
        color = [0] * n
        def dfs(node, c):
            color[node] = c
            for next in graph[node]:
                if color[next] == c:
                    return False
                if color[next] == 0 and not dfs(next, -c):
                    return False
            return True
        for i in range(n):
            if color[i] == 0:
                if not dfs(i, 1):
                    return False
        return True
    
    
    
    
    
    

    
sol = Solution()
result = [
    sol.isBipartite(graph = [[1,2,3],[0,2],[0,1,3],[0,2]]),
    sol.isBipartite(graph = [[1,3],[0,2],[1,3],[0,2]]),
]
for r in result:
    print(r)
