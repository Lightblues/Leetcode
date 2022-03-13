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
https://leetcode-cn.com/contest/weekly-contest-284/
@20220313 """
class Solution:
    """ 6031. 找出数组中的所有 K 近邻下标 """
    def findKDistantIndices(self, nums: List[int], key: int, k: int) -> List[int]:
        iindexs = [i for i, n in enumerate(nums) if n == key]
        res = set()
        for i in iindexs:
            for j in range(-k, k+1):
                if i+j >= 0 and i+j < len(nums):
                    res.add(i+j)
        return sorted(list(res))

    """ 5203. 统计可以提取的工件
给定一个网格, 放了一组由 `artifacts[i] = [r1i, c1i, r2i, c2i]` 确定边界的「工件」, 以及 `dig[i] = [ri, ci]` 是会进行挖掘的点, 只有当工件占据的所有点都被挖掘时, 我们才能提取这个工件. 要求返回可以挖到的工件数量.

思路一: 数量比较少直接暴力: 在网格上用不同的数字标记工件, 最后统计还在网格上的不同数字即为没被挖开的数量.
 """
    def digArtifacts(self, n: int, artifacts: List[List[int]], dig: List[List[int]]) -> int:
        grid = [[0]*n for _ in range(n)]
        count = 1
        for i1,j1, i2,j2 in artifacts:
            for i in range(i1, i2+1):
                for j in range(j1, j2+1):
                    grid[i][j] = count
            count += 1
        for i,j in dig:
            grid[i][j] = 0
        c = set()
        for i in range(n):
            for j in range(n):
                if grid[i][j] != 0:
                    c.add(grid[i][j])
        return len(artifacts) - len(c)

    """ 5227. K 次操作后最大化顶端元素
给一个非空栈和可操作数量k, 要求返回执行这些操作后, 能够留在栈顶的最大值. (如果执行完 k 次操作以后，栈一定为空，请你返回 -1)
两种操作: 1. 弹出栈顶元素; 2. 压入弹出的某一个元素.

输入：nums = [2], k = 1
输出：-1
解释：
第 1 次操作中，我们唯一的选择是将栈顶元素弹出栈。
由于 1 次操作后无法得到一个非空的栈，所以我们返回 -1 。

先考虑边界: 什么情况下最后栈为空? `len(nums)==1 and k%2==1`
而在一般情况下, 对于k次操作, 我们可以在栈顶留下第 1,...,k-1 和 k+1 个元素 (从1开始). 需要对k和数组长度n的关系讨论.
另外, 需要确保 nums[:k-1] 操作中 k-1 非负, 添加到边界条件中.
     """
    def maximumTop(self, nums: List[int], k: int) -> int:
        # 边界条件
        if len(nums)==1 and k%2==1:
            return -1
        if k==0:
            return nums[0]
        
        n = len(nums)
        if k<n:
            tmp = nums[:k-1] + [nums[k]]
        elif k==n:
            tmp = nums[:k-1]
        else:
            tmp = nums
        return max(tmp)

    """ 6032. 得到要求路径的最小带权子图
给一张带权图, 给定三个点, 要求返回 **边权和最小** 的子图 (的边权和)，使得在这个子图中从 `src1` 和 `src2` 出发都可到达 `dest` 。如果这样的子图不存在，请返回 `-1` 。

输入：n = 6, edges = [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]], src1 = 0, src2 = 1, dest = 5
输出：9
解释：
上图为输入的图。
蓝色边为最优子图之一。
注意，子图 [[1,0,3],[0,5,6]] 也能得到最优解，但无法在满足所有限制的前提下，得到更优解。

输入：n = 3, edges = [[0,1,1],[2,1,1]], src1 = 0, src2 = 1, dest = 2
输出：-1
解释：
上图为输入的图。
可以看到，不存在从节点 1 到节点 2 的路径，所以不存在任何子图满足所有限制。


注意到, 双点出发求最短路径的情况, 可能出现共用一条路径的情况. (此时, 最小边权和为 `s1->u, s2->u, u->d` 三条路径之和, 而非 `s1->d, s2->d`). 需要判断这种情况出现的边界: 
简单判断, 假设两点的最短路径分别为 d1,d2, 则共用的路径长度不能超过 d1+d2. 
因此, 暴力来解, 可以先从 s1,s2 出发BFS, 然后(逆)从d出发进行长度约束为 d1+d2 的BFS.
为了判断所有可能的中间节点, 需要记录正反向BFS过程中所有经过的点的路径长.

思路一: BFS + 节点判断
首先, 从src1和src2出发, 返回距离d和在这一范围内的节点集合(及其路径长); 分别用 dist1, dist2 两个map记录两个范围内所有点的距离.
然后在逆图上进行长度 d1+d2 约束的BFS, 同样记录各个点的路径长 dist
遍历三个字典交集, 取最短距离 `dist[u]+dist1[u]+dist2[u]`.
 """
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        g = collections.defaultdict(list)
        rev_g = collections.defaultdict(list)
        for u,v,weight in edges:
            g[u].append((weight, v))
            rev_g[v].append((weight, u))
        
        def BFS(src):
            """ BFS. 从 src 到 dest 的最短路径
            返回: 距离d(没有的话返回-1); 以及在d范围内的所有点的距离map
             """
            dist = {src:0}
            q = [(0, src)]
            while q:
                d, u = heapq.heappop(q)
                if u == dest:
                    return d, dist
                for w, v in g[u]:
                    if v not in dist:
                        dist[v] = d+w
                        heapq.heappush(q, (dist[v], v))
                    else:
                        dist[v] = min(dist[v], d+w)
            return -1, dist
        def BFS2(src, dist_limit):
            """ 在逆图上, 搜索dist范围内的所有点的最短路径值 """
            dist = {src:0}
            q = [(0, src)]
            while q:
                d, u = heapq.heappop(q)
                for w, v in rev_g[u]:
                    if v not in dist:
                        if d+w < dist_limit:
                            dist[v] = d+w
                            heapq.heappush(q, (dist[v], v))
                    else:
                        dist[v] = min(dist[v], d+w)
            return dist

        d1, dist1 = BFS(src1)
        if d1==-1:
            return -1
        d2, dist2 = BFS(src2)
        if d2==-1:
            return -1
        # print(d1, d2)

        dist = BFS2(dest, d1+d2)
        # res = float('inf') # 实际上初始化为 inf 也可以, 因为dest必然在这三个字典中
        res = d1+d2
        for u,d in dist.items():
            if u in dist1 and u in dist2:
                res = min(res, d+dist1[u]+dist2[u])
        return res


sol = Solution()
result = [
    # sol.findKDistantIndices(nums = [3,4,9,1,3,9,5], key = 9, k = 1),

    # sol.digArtifacts(n = 2, artifacts = [[0,0,0,0],[0,1,1,1]], dig = [[0,0],[0,1],[1,1]]),
    # sol.digArtifacts(n = 2, artifacts = [[0,0,0,0],[0,1,1,1]], dig = [[0,0],[0,1]]),
    # sol.digArtifacts(5, [[3,1,4,1],[1,1,2,2],[1,0,2,0],[4,3,4,4],[0,3,1,4],[2,3,3,4]], [[0,0],[2,1],[2,0],[2,3],[4,3],[2,4],[4,1],[0,2],[4,0],[3,1],[1,2],[1,3],[3,2]]),

    # sol.maximumTop(nums = [5,2,2,4,0,6], k = 4),
    # sol.maximumTop([35,43,23,86,23,45,84,2,18,83,79,28,54,81,12,94,14,0,0,29,94,12,13,1,48,85,22,95,24,5,73,10,96,97,72,41,52,1,91,3,20,22,41,98,70,20,52,48,91,84,16,30,27,35,69,33,67,18,4,53,86,78,26,83,13,96,29,15,34,80,16,49],15),
    # sol.maximumTop([18], 3),

    sol.minimumWeight(n = 6, edges = [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]], src1 = 0, src2 = 1, dest = 5),
    sol.minimumWeight(8, [[4,7,24],[1,3,30],[4,0,31],[1,2,31],[1,5,18],[1,6,19],[4,6,25],[5,6,32],[0,6,50]], 4, 1, 6),
]
for r in result:
    print(r)