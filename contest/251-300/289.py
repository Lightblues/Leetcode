from typing import List, Optional
import collections
import math
import bisect
import heapq
from functools import lru_cache
# import sys
# sys.setrecursionlimit(10000)

from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 6070. 计算字符串的数字和 """
    def digitSum(self, s: str, k: int) -> str:
        while len(s) > k:
            tmp = ""
            while s:
                firstK, s = s[:k], s[k:]
                tmp += str(sum(int(i) for i in firstK))
            s = tmp
        return s
    
    """ 6071. 完成所有任务需要的最少轮数 """
    def minimumRounds(self, tasks: List[int]) -> int:
        tasks = collections.Counter(tasks)
        result = 0
        for num in tasks.values():
            if num==1:
                return -1
            a,b = divmod(num, 3)
            result += a + (b>0)
        return result
    
    """ 6072. 转角路径的乘积中最多能有几个尾随零
给定一个矩阵, 一条「转角路径」最多出现一个转折, 求所有路径乘积的尾随零的最大数量.

思路: 1) 显然, 路径越长越好, 所以折角的两条边可以直接到矩阵的边上. 2) 为了计算乘积的「尾随零」, 注意到0的数量完全取决于 2/5 因子的数量;
3) 因此, 分别计算行和列级别的前缀和, 然后遍历所有可能的折角.
    """
    def maxTrailingZeros(self, grid: List[List[int]]) -> int:
        def getCount(num, d):
            # 计算 num 中有多少个因子 d
            c = 0
            while num % d == 0:
                c += 1
                num //= d
            return c
        
        m, n = len(grid), len(grid[0])
        # 记录 行和列 级别的前缀和
        c2row = [[0] * (n+1) for _ in range(m+1)]
        c2col = [[0] * (n+1) for _ in range(m+1)]
        c5row = [[0] * (n+1) for _ in range(m+1)]
        c5col = [[0] * (n+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                num = grid[i][j]
                c2, c5 = getCount(num, 2), getCount(num, 5)
                c2row[i+1][j+1] = c2row[i+1][j] + c2
                c5row[i+1][j+1] = c5row[i+1][j] + c5
                c2col[i+1][j+1] = c2col[i][j+1] + c2
                c5col[i+1][j+1] = c5col[i][j+1] + c5
        
        result = 0
        # 遍历行列组合
        for i in range(m):
            for j in range(n):
                c2, c5 = c2row[i+1][j+1]-c2row[i+1][j], c5row[i+1][j+1]-c5row[i+1][j]
                c2left, c5left = c2row[i+1][j], c5row[i+1][j]
                c2right, c5right = c2row[i+1][n]-c2row[i+1][j+1], c5row[i+1][n]-c5row[i+1][j+1]
                c2up, c5up = c2col[i][j+1], c5col[i][j+1]
                c2down, c5down = c2col[m][j+1]-c2col[i+1][j+1], c5col[m][j+1]-c5col[i+1][j+1]
                for c2r, c5r in [(c2left, c5left), (c2right, c5right)]:
                    for c2c, c5c in [(c2up, c5up), (c2down, c5down)]:
                        result = max(result, min(c2r+c2c+c2, c5r+c5c+c5))
        return result
    
    """ 6073. 相邻字符不同的最长路径
给一棵树上的节点都定义一个 label, 要求返回树上一条相邻节点的label不同的最长路径的长度。

思路: 正常 DFS 即可. 注意: 1) 最长路径可能在节点的子树中, 因此需要在遍历过程中更新全局变量; 2) 注意DFS返回: 「从该节点出发的子路径的最大长度」, 而全局维护的是「一条符合条件的路径的最大长度」, 注意区分.
    """
    def longestPath(self, parent: List[int], s: str) -> int:
        # 节点定义
        class Node:
            def __init__(self, val: int, label: str = "") -> None:
                self.val = val      # 就是 id, 没用
                self.label = label
                self.childs = []
        id2node = {}
        # 哨兵节点
        root = Node(-1)
        id2node[-1] = root
        
        # 构建树. 
        # 注意乱序的, 因此需要建立所有点之后再构造树
        for i, label in enumerate(s):
            node = Node(i, label)
            id2node[i] = node
        for i, p in enumerate(parent):
            id2node[p].childs.append(id2node[i])
        
        # 至少有一个节点
        result = 1
        def dfs(node: Node):
            # 返回: 经过节点 node 的最长路径长度
            # 注意在遍历孩子的时候, 遇到相同 label 的节点, 需要继续遍历, 但不加入 lenChilds
            if not node.childs:
                return 1
            
            lenChilds = []
            for child in node.childs:
                # 注意即使是相同 label, 也要继续向下遍历 —— 更新 result
                lenChild = dfs(child)
                if child.label != node.label:
                    lenChilds.append(lenChild)
            lens = sorted(lenChilds, reverse=True)
            lens.append(0) # 哨兵
            
            nonlocal result
            result = max(result, sum(lens[:2]) + 1)
            
            return max(lens) + 1
        
        dfs(root.childs[0])
        return result


sol = Solution()
result = [
    # sol.digitSum(s = "11111222223", k = 3),
    # sol.minimumRounds(tasks = [2,2,3,3,2,4,4,4,4,4]),
    
    sol.maxTrailingZeros(grid = [[23,17,15,3,20],[8,1,20,27,11],[9,4,6,2,21],[40,9,1,10,6],[22,7,4,5,3]])
    
    # sol.longestPath(parent = [-1,0,0,1,1,2], s = "abacbe"),
    # sol.longestPath(parent = [-1,0,0,0], s = "aabc"),
    # sol.longestPath([-1,0,1], "aab"),
    # sol.longestPath([-1,137,65,60,73,138,81,17,45,163,145,99,29,162,19,20,132,132,13,60,21,18,155,65,13,163,125,102,96,60,50,101,100,86,162,42,162,94,21,56,45,56,13,23,101,76,57,89,4,161,16,139,29,60,44,127,19,68,71,55,13,36,148,129,75,41,107,91,52,42,93,85,125,89,132,13,141,21,152,21,79,160,130,103,46,65,71,33,129,0,19,148,65,125,41,38,104,115,130,164,138,108,65,31,13,60,29,116,26,58,118,10,138,14,28,91,60,47,2,149,99,28,154,71,96,60,106,79,129,83,42,102,34,41,55,31,154,26,34,127,42,133,113,125,113,13,54,132,13,56,13,42,102,135,130,75,25,80,159,39,29,41,89,85,19], 
    #                 "ajunvefrdrpgxltugqqrwisyfwwtldxjgaxsbbkhvuqeoigqssefoyngykgtthpzvsxgxrqedntvsjcpdnupvqtroxmbpsdwoswxfarnixkvcimzgvrevxnxtkkovwxcjmtgqrrsqyshxbfxptuvqrytctujnzzydhpal")
]
for r in result:
    print(r)