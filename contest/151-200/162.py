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
https://leetcode.cn/contest/weekly-contest-162

T1简单的思维; T2因为没有考虑边界WA了一次. T3并查集还是比较清楚的, 但还是有些繁琐. T4居然是直接暴力DFS...
@2022 """
class Solution:
    """ 1252. 奇数值单元格的数目 #对于一个 m,n 矩阵, 进行 x次操作, 每次对于 (x,y) 的行和列元素都加上1. 问最后累计的数字为奇数的元素数量. 限制: m,n 50, x 100
进阶: 要求复杂度 O(m+n+x).
思路1: 利用行列分别计数被操作的数量; 如何统计每个单元格的奇偶性? 直接统计 cntOddRow * cntEvenCol + cntEvenRow * cntOddCol 即可.
"""
    def oddCells(self, m: int, n: int, indices: List[List[int]]) -> int:
        rows = [0] * m
        cols = [0] * n
        for x,y in indices:
            rows[x] += 1
            cols[y] += 1
        cntOddRow = sum(x%2 for x in rows)
        # cntEven = m - cntOdd
        cntOddCol = sum(x%2 for x in cols)
        return cntOddRow * (n - cntOddCol) + (m - cntOddRow) * cntOddCol
    
    """ 1253. 重构 2 行二进制矩阵 #medium 模拟题, 可以自由构造
https://leetcode.cn/problems/reconstruct-a-2-row-binary-matrix/submissions/ """
    def reconstructMatrix(self, upper: int, lower: int, colsum: List[int]) -> List[List[int]]:
        if upper+lower != sum(colsum): return []
        # 注意这里的边界! 若colsum中出现的2的个数比行和还要大, 不可能!
        if min(upper, lower) < colsum.count(2): return []
        m = len(colsum)
        ans = [[0] * m, [0] * m]
        oneIdxs = []
        for i,v in enumerate(colsum):
            if v==1: oneIdxs.append(i)
            elif v==2: ans[0][i] = ans[1][i] = 1
        onesUpper = upper - sum(ans[0])
        for i in oneIdxs[:onesUpper]: ans[0][i] = 1
        for i in oneIdxs[onesUpper:]: ans[1][i] = 1
        return ans
    
    """ 1254. 统计封闭岛屿的数目 #medium #题型 0/1 表示陆地和水, 统计grid中 四面全部由1包围的岛屿数量. 限制: m,n 100
思路1: 先通过 #并查集 将所有相邻的陆地连起来, 对于每个联通分量检查是否有边界点, 若有则不是封闭岛屿.
    如何定义「边界」? 可以定义一个节点 0「超级节点」, 用于连接所有边界点
        这样, 对于边界上的点都连接到节点 0 (并查集用更小的节点作为父亲)
https://leetcode.cn/problems/number-of-closed-islands/
"""
    def closedIsland(self, grid: List[List[int]]) -> int:
        m,n = len(grid),len(grid[0])
        def xy2idx(x,y): return x*n+y + 1
        # 节点 0 是「超级节点」, 用于连接所有边界点
        fa = [i for i in range(m*n+1)]
        def find(x):
            if fa[x] != x: fa[x] = find(fa[x])
            return fa[x]
        def merge(x,y):
            fx,fy = find(x),find(y)
            # 始终将id小的作为father
            if fx>fy: fx,fy = fy,fx
            fa[fy] = fx
        for i in range(m):
            for j in range(n):
                if grid[i][j]==1: continue
                # 边缘的, 合并到超级节点 0
                if i==0 or i==m-1 or j==0 or j==n-1: merge(0,xy2idx(i,j))
                # 只需要向上向左合并即可
                if i>0 and grid[i-1][j]==0: merge(xy2idx(i,j), xy2idx(i-1,j))
                if j>0 and grid[i][j-1]==0: merge(xy2idx(i,j), xy2idx(i,j-1))
        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j]==1: continue
                idx = xy2idx(i,j)
                if fa[idx]==idx: ans += 1
        return ans
    
    """ 1255. 得分最高的单词集合 #hard 字母表中的每个字符都有一个分数. 现在给定一组字符(重复) 和一组单词, 问如何选择单词, 使得总分最高? 限制: 单词数 14; 每个单词长度 15; 字符数 100; 每个字符的分数 10.
思路1: 暴力 DFS, 检查每个mask所表示的单词组合是否合法, 计算分数. 
https://leetcode.cn/problems/maximum-score-words-formed-by-letters/
"""
    def maxScoreWords(self, words: List[str], letters: List[str], score: List[int]) -> int:
        n = len(words)
        remainLetters = [0] * 26
        for l in letters: remainLetters[ord(l)-ord('a')] += 1
        def p(word):
            cost = [0] * 26
            s = 0
            for w in word: 
                i = ord(w)-ord('a')
                cost[i] += 1
                s += score[i]
            return cost, s
        costs, scores = [], []
        for w in words: cost, s = p(w); costs.append(cost); scores.append(s)
        ans = 0
        def f(i, score):
            nonlocal ans
            if i==n: ans = max(ans, score); return
            if all(r>=c for r,c in zip(remainLetters, costs[i])):
                for j in range(26): remainLetters[j] -= costs[i][j]
                f(i+1, score+scores[i])
                for j in range(26): remainLetters[j] += costs[i][j]
            f(i+1, score)
        f(0,0)
        return ans
    
sol = Solution()
result = [
    # sol.oddCells(m = 2, n = 3, indices = [[0,1],[1,1]]),
    # sol.reconstructMatrix(upper = 2, lower = 1, colsum = [1,1,1]),
    # sol.closedIsland(grid = [[0,0,1,0,0],[0,1,0,1,0],[0,1,1,1,0]]),
    # sol.closedIsland(grid = [[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]),
    sol.maxScoreWords(words = ["dog","cat","dad","good"], letters = ["a","a","c","d","d","d","g","o","o"], score = [1,0,9,5,0,0,3,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0]), 
]
for r in result:
    print(r)
