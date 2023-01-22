from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-236
@2022 """
class Solution:
    """ 1822. 数组元素积的符号 """
    def arraySign(self, nums: List[int]) -> int:
        sign = 1
        for num in nums:
            if num==0:
                return 0
            elif num<0:
                sign *= -1
        return sign
    
    """ 1823. 找出游戏的获胜者 #medium #题型 #约瑟夫环
n个玩家围成一圈, 从1开始编号; 在剩余人数超过一人的情况下, 顺时针数第k个人出局. 问最后剩余的人是谁.
限制: 进阶要求 O(n) 的算法
思路1: 暴力模拟, 每次找到出局的人, 环的长度-1. 因此需要pop数组的中间元素, 复杂度 O(nk)
思路2: #推导 #公式. 实际上该问题正是 #约瑟夫环 [wiki](https://zh.wikipedia.org/wiki/%E7%BA%A6%E7%91%9F%E5%A4%AB%E6%96%AF%E9%97%AE%E9%A2%98)
    方便起见, 下面编号按照从0开始.
    记 `f(n, k)` 表示「长为n的环, 从0开始顺时针, 每次第k个人出局」这样的设置下, 最后剩余的人的编号.
    分类: 1) 若n=1, 则 `f(n, k) = 0`; 2) 否则, 本轮出局的人为 `x' = (k-1)%n`, 然后, 记 `x = f(n-1, k)` 表示子问题最后剩余的人. 它们之间的关系有: 由于本轮出局 x', 则子问题中编号为0的在本轮中的编号为 `x'+1`, 因此原问题最终的胜利者编号为 `f(x,n) = (x'+1 + f(n-1, k)) %n = (f(x-1,n)+k) % n`.
    当然, 得到上述推导公式之后, #递归 形式可以展开为 #迭代.
[官答](https://leetcode.cn/problems/find-the-winner-of-the-circular-game/solution/zhao-chu-you-xi-de-huo-sheng-zhe-by-leet-w2jd/)
"""
    def findTheWinner(self, n: int, k: int) -> int:
        # 思路1
        circle = [i for i in range(1, n+1)]
        idx = 0
        while len(circle)>1:
            idx = (idx + k-1) % len(circle)
            circle.pop(idx)
        return circle[0]
    
    def findTheWinner(self, n: int, k: int) -> int:
        # 思路2
        def f(n):
            if n==1: return 0
            return (k + f(n-1)) % n
        return f(n)+1
    def findTheWinner(self, n: int, k: int) -> int:
        # 展开递归为迭代
        f = 0
        for i in range(2, n+1):    # 出局 n-1 人
            f = (f+k) % i
        return f+1
    
    
    """ 1824. 最少侧跳次数 #medium #化简
有三条跑道, 上面各有一些石头. 要从起点跑到终点, 仅能进行侧跳 (在相同的距离处, 从跑道i跳到跑道j). 要求最少侧跳次数.
限制: 每个距离最多有一个石子; 距离 5e5
思路1: #DP
    记 `f[d][i]` 表示到达距离d处的跑道i的最少侧跳次数. 
    则有递推: 若i有障碍物, 则无法到达记为inf; 否则, `f[d+1][i] = min(f[d][i], f[d][j]*{f[d+1][j]!=j} + 1}` 这里的第二项表示从j跑道跳过来, 要求j报道的d+1处没有石子.
    化简: 注意到, 对于相同距离无障碍的跑道, **f[d] 之间的差距最大为1**. 将DP数组压缩为1维的情况下, 先将有障碍的位置置为inf, 然后记数组最小值为mn, 则对于非障碍位置有 `f[d+1][i] = min(f[d][i], mx+1)`
思路2: 转为图上求最短路径, 叫做 #0-1BFS
    将路上的位置 (dist,i) 作为节点, 根据向前走/侧跳进行连边, 代价分别为 0/1. 
    这样, 可以采用 #Dijkstra 算法求最短路径. 但复杂度超过了 O(n)
    如何进行「图上的BFS」? 这样复杂度可以是 O(n)
        对于树上的BFS (边权均为1), 可以采用 #队列 的方式进行BFS.
        那么在图上, 
            若边权均为1, 也可以正常利用 dis 来防止重复访问, 进行BFS. 
            若边权为0/1, 则需要利用 #双端队列 的方式进行BFS. 具体见下: 
    0-1BFS
        注意, 我们需要保证当前访问的节点的距离是最小的, 因此需要用到 #双端队列.
            维护的队列有一个性质, 队列中节点的距离是递增的, 并且同时只会出现 d,d+1 距离的节点
        从距离为d的x节点出发, 对于一条 x->y 的路径: 
            若边权为1, 并且 dis[y]>d+1, 则更新y的距离, 加入队尾.
            若边权为0, 并且 dis[y]>d, 则更新y的距离; 为了保证队列的递增, 需要加入队头!
    说明: 如果边权不止 0和1，把双端队列换成最小堆，就得到了 Dijkstra 算法。
    见 [灵神](https://leetcode.cn/problems/minimum-sideway-jumps/solution/cong-0-dao-1-de-0-1-bfspythonjavacgo-by-1m8z4/)
    关联: 「2290. 到达角落需要移除障碍物的最小数目」「1368. 使网格图至少有一条有效路径的最小代价」
"""
    def minSideJumps(self, obstacles: List[int]) -> int:
        f  = [1, 0, 1]
        for o in obstacles:
            # 若该位置有障碍物, 先置为 inf
            if o!=0:
                f[o-1] = inf
            # 利用上面的化简公式更新
            mn = min(f)
            for i in range(3):
                if i==o-1: continue
                else: f[i] = min(f[i], mn+1)
        return min(f)
    def minSideJumps(self, obstacles: List[int]) -> int:
        n = len(obstacles)
        dis = [[n] * 3 for _ in range(n)]
        dis[0][1] = 0
        q = deque([(0, 1)])  # 起点
        while True:
            i, j = q.popleft()
            d = dis[i][j]
            if i == n - 1: return d  # 到达终点
            if obstacles[i + 1] != j + 1 and d < dis[i + 1][j]:  # 向右
                dis[i + 1][j] = d
                q.appendleft((i + 1, j))  # 加到队首
            for k in (j + 1) % 3, (j + 2) % 3:  # 枚举另外两条跑道（向上/向下）
                if obstacles[i] != k + 1 and d + 1 < dis[i][k]:
                    dis[i][k] = d + 1
                    q.append((i, k))  # 加到队尾


""" 1825. 求出 MK 平均值 #hard #题型
"""

    
sol = Solution()
result = [
    sol.findTheWinner(n = 5, k = 2),
    sol.findTheWinner(n = 6, k = 5),
    # sol.minSideJumps(obstacles = [0,2,1,0,3,0]),
    # sol.minSideJumps(obstacles = [0,1,1,3,3,0]),
    # sol.minSideJumps([0,1,2,3,0]),

]
for r in result:
    print(r)
