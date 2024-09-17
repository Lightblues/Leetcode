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
https://leetcode.cn/contest/weekly-contest-409
https://leetcode.cn/circle/discuss/iy9mXc/ 比较数学+细节的一场比赛
T2 T3 最短距离的题目非常好玩!
T4 也有着实际的价值, 不过很 #hardhard

Easonsi @2023 """
class Solution:
    """ 3243. 新增道路查询后的最短距离 I #medium  原本有编号 0->1->n-1 的一条链. 在q次操作中, 每次对于 (i,j) 新增一条边, 问每次操作之后 0到n-1 的距离. 
限制: n 5e2; q 5e2
思路1: #DP 的思想, 没写出来. 类似 [ling] 的思路2
    记 f[x] 表示从0到位置x的最小步数
    对于每一条新加入的边 (i,j), 影响的是 j,j+1...n-1
        什么时候更新? f[i]+1 < f[j]
        要向右更新到什么位置? 注意到对于 j<k<target, 在更新target的时候不应该考虑只考虑 j (target-j), 可能j的更新影响了k, 进一步可以减少到target的代价!
            因此, 对于每个位置, 记录所有到这个位置的跳边的起点! (维护一个列表)
    复杂度? O(q * (q+l))
思路2: 每次修改图之后进行 #BFS, 计算一下复杂度和上面一样的! 
[ling](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-i/solutions/2869215/liang-chong-fang-fa-bfs-dppythonjavacgo-mgunf/)
    """
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        ans = []
        f = list(range(n))
        froms = [[] for _ in range(n)]  # 记录每个位置的跳边
        for i,j in queries:
            froms[j].append(i)
            for k in range(j, n):
                f[k] = min(
                    f[k], f[k-1]+1, # 向后传递
                    *[f[l] + 1 for l in froms[k]] # 再利用记录下来的跳边!
                )
            ans.append(f[-1])
        return ans
            
    
    """ 3244. 新增道路查询后的最短距离 II #hard 原本有编号 0->1->n-1 的一条链. 在q次操作中, 每次对于 (i,j) 新增一条边, 问每次操作之后 0到n-1 的距离. 
另外, 任意两个查询都不满足 queries[i][0] < queries[j][0] < queries[i][1] < queries[j][1]
限制: n 1e5; q 1e5
思路0: 记录一系列的 "短接" 的边, 统计所有短接的长度 (省下的路程)
    难点在于, 对于一系列的区间, 怎么在有限复杂度内进行合并呢? -- 考虑一开始 [1,3], [4,6], ... 这种连边, 然后 [1,6] 从左边合并过去, 这种边界情况
思路1: #并查集
    想到了并查集, 但没有具体的思路. 看到ling一句话就悟了 -- 把所有节点看成独立的点, 连边就是将这些节点合并起来了!
    每一轮路径就是并查集的大小! 
    复杂度: O(q + n)
思路2: 记录每个位置的跳边froms!
    一开始的时候, 位置 i 的 from 只包含了 i-1
    同上一题不一样, 因为增加了新的条件, 可以直接将包含关系的区间丢掉! 
    假设一开始 2->3->4->5, 当新增连边 (2,5) 的时候, 可以根据 from[5]=4 把节点4丢掉, 并进一步把 from[4] = 3 丢掉! 
    -- 这里用set的写法清楚一点, 参见ling的回复里面! 
[ling](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-ii/solutions/2868558/qu-jian-bing-cha-ji-pythonjavacgo-by-end-a9k7/)
    """
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        ans = []
        froms = {i:i-1 for i in range(1,n)}
        for i,j in queries:
            if j in froms and froms[j] > i: # 说明会进行合并! 
                ii = froms[j]
                while ii > i: # 注意到这里 ii in froms 这种判断是没必要的! 
                    ii = froms.pop(ii)
                froms[j] = i
            ans.append(len(froms))
        return ans
    
    """ 3245. 交替组 III #hard 有一个0/1 的环, 包括两种操作: 一个是修改某一位置的颜色, 另一个是统计环上长度为 k的交替序列 (0101..) 的数量.
限制: n 1e5; q 1e5
思路1: 先统计不同的 "交替区间", 然后计数
    
[ling](https://leetcode.cn/problems/alternating-groups-iii/solutions/2869147/cong-yi-dao-nan-yi-bu-bu-tui-dao-pythonj-jho9/)
    """
    
    
""" 3242. 设计相邻元素求和服务 """
class NeighborSum:
    def __init__(self, grid: List[List[int]]):
        self.adjSum = {}
        self.diaSum = {}
        n = len(grid)
        for i,row in enumerate(grid):
            for j,x in enumerate(row):
                if i>0: self.adjSum[x] += grid[i-1][j]
                if i<n-1: self.adjSum[x] += grid[i+1][j]
                if j>0: self.adjSum[x] += grid[i][j-1]
                if j<n-1: self.adjSum[x] += grid[i][j+1]
                if i>0 and j>0: self.diaSum[x] += grid[i-1][j-1]
                if i>0 and j<n-1: self.diaSum[x] += grid[i-1][j+1]
                if i<n-1 and j>0: self.diaSum[x] += grid[i+1][j-1]
                if i<n-1 and j<n-1: self.diaSum[x] += grid[i+1][j+1]

    def adjacentSum(self, value: int) -> int:
        return self.adjSum.get(value, 0)

    def diagonalSum(self, value: int) -> int:
        return self.diaSum.get(value, 0)


# Your NeighborSum object will be instantiated and called as such:
# obj = NeighborSum(grid)
# param_1 = obj.adjacentSum(value)
# param_2 = obj.diagonalSum(value)
    
sol = Solution()
result = [
    # sol.shortestDistanceAfterQueries(n = 5, queries = [[2,4],[0,2],[0,4]]),
    # sol.shortestDistanceAfterQueries(14, [[4,7],[2,5],[1,4],[10,12],[9,11],[8,12]]),
    
    sol.shortestDistanceAfterQueries(n = 5, queries = [[2, 4], [0, 2], [0, 4]]),
]
for r in result:
    print(r)
