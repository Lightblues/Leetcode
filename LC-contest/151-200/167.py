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
https://leetcode.cn/contest/weekly-contest-167

@2022 """
class Solution:
    """ 1290. 二进制链表转整数 """
    
    """ 1291. 顺次数 """
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        s = '123456789'
        r = []
        for i in range(9):
            for j in range(9-i):
                n = int(s[j:j+i+1])
                if low<=n<=high:
                    r.append(n)
        return r
    
    """ 1292. 元素和小于等于阈值的正方形的最大边长 #medium #题型 给定一个grid, 要从中找到最大的正方形, 使得其元素之和不大于阈值 threshold 限制: m,n 300. 
思路1: 二维 #前缀和
    在得到前缀和之后, 如何找到最大满足条件的 k?
    1.1 最为基本的思路是直接从大到小枚举, 复杂度 O(MN * min{M,N}).
    1.2 采用 #二分 进行查找. 复杂度 O(MN * log(min(M,N)))
    1.3 实际上, 可以从另外的角度进行优化. (舍弃二分思想)
        考虑三重循环: 枚举ij左上角的位置, 再枚举边长k. 哪些可以舍弃?
        枚举过程中, 1) 当k不满足的时候, 终止; 2) 前面已经找到边长k的正方形了, 接下来可以直接从k进行枚举. 这样, 枚举的复杂度是 O(min(m,n) + mn). 比二分更优! 
"""
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        m,n = len(mat),len(mat[0])
        acc = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                acc[i+1][j+1] = acc[i+1][j]+acc[i][j+1]-acc[i][j]+mat[i][j]
        for k in range(min(m,n),0,-1):
            for i in range(m-k+1):
                for j in range(n-k+1):
                    if acc[i+k][j+k]-acc[i+k][j]-acc[i][j+k]+acc[i][j]<=threshold:
                        return k
        return 0
    
    """ 1293. 网格中的最短路径 #hard 给定一个 m,n 的网格从左上到右下, 0/1表示是否有障碍物. 问最多消除k个障碍物的前提下, 最短路径. 限制: m,n 40; 
思路0: 用一个函数 `f(x,y, d, r)` 记录到达 x,y 位置的距离, 和剩余的可移除障碍数量. 记忆化搜索? 
    剪枝: 若 nd>d, 只有当 nr>r 的时候才需要继续搜索. 
    但实际想起来, 不太好实现.
思路1: 直接 #BFS. 但这里的状态需要记录 (x,y,r). 由于BFS的特点, 这样就不需要担心距离的先后问题了 (上面的重复搜索判断).
    如何避免重复搜索? 这里对于某位置, 可能有一条更长的, 但是消耗更少的路径. 
        因此, 可以用一个字典 idx2maxRemain 记录到达某位置所剩余的最大可移除障碍数量. 当重复搜索到该点时, 若能有更多的剩余则继续搜索. 
见 [官答](https://leetcode.cn/problems/shortest-path-in-a-grid-with-obstacles-elimination/solution/wang-ge-zhong-de-zui-duan-lu-jing-by-leetcode-solu/)
"""
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        m,n = len(grid),len(grid[0])
        idx2maxRemain = defaultdict(lambda: -1)
        d = 0
        ans = inf
        q = [(0,0,k)]
        while q:
            nq = []
            for x,y,r in q:
                if x==m-1 and y==n-1: 
                    # return d
                    ans = min(ans, d)
                    continue
                for dx,dy in dirs:
                    nx,ny = x+dx,y+dy
                    if nx<0 or nx>=m or ny<0 or ny>=n: continue
                    if grid[nx][ny]==1:
                        if r<=0: continue
                        if idx2maxRemain[(nx,ny)]<r-1:
                            nq.append((nx,ny,r-1))
                            idx2maxRemain[(nx,ny)] = r-1
                    else: 
                        if idx2maxRemain[(nx,ny)]<r:
                            nq.append((nx,ny,r))
                            idx2maxRemain[(nx,ny)] = r
            q = nq
            d += 1
        return -1 if ans==inf else ans
    
sol = Solution()
result = [
    sol.shortestPath(grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1),
    sol.shortestPath(grid = [[0,1,1],[1,1,1],[1,0,0]], k = 1),
    sol.shortestPath([[0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,0],[0,1,0,0,0,0,0,0,0,0],[0,1,0,1,1,1,1,1,1,1],[0,1,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,0],[0,1,0,0,0,0,0,0,0,0],[0,1,0,1,1,1,1,1,1,1],[0,1,0,1,1,1,1,0,0,0],[0,1,0,0,0,0,0,0,1,0],[0,1,1,1,1,1,1,0,1,0],[0,0,0,0,0,0,0,0,1,0]], 1)
    # sol.maxSideLength(mat = [[1,1,3,2,4,3,2],[1,1,3,2,4,3,2],[1,1,3,2,4,3,2]], threshold = 4),
    # sol.maxSideLength(mat = [[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]], threshold = 1),
]
for r in result:
    print(r)
