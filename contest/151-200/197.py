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
https://leetcode.cn/contest/weekly-contest-197
T3是 Dijkstra WA了一次, 正好跟着官答总结一下; T4居然考虑最优化/梯度下降, 值得总结!

@2022 """
class Solution:
    """ 1512. 好数对的数目 """
    def numIdenticalPairs(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ans = 0
        for v in cnt.values():
            ans += math.comb(v, 2)
        return ans
    
    """ 1513. 仅含 1 的子串数 """
    def numSub(self, s: str) -> int:
        parts = s.split('0')
        parts = map(len, parts)
        ans = 0
        for p in parts:
            ans += p*(p+1)//2
        return ans
    
    """ 1514. 概率最大的路径 #medium #题型
等价于, 经典的「单源最短路径路径」, 在带权图上求 (s,e) 之间的最短距离.
思路1: #Dijkstra 算法
    回顾 Dijkstra算法的核心思想: 1) 将节点分成两类: 「未确定节点」和「已确定节点」; 2) (「松弛」过程) 每次从「未确定节点」中取一个与起点距离最短的点，将它归类为「已确定节点」，并用它「更新」从起点到其他所有「未确定节点」的距离。直到所有点都被归类为「已确定节点」。
    细节: 1) 如何找到「未确定节点」中最小距离点? 例如可以用最小堆实现. 2) 如何分离两类节点? 一种方式是用 `visited` 字典标记已确定节点; 另一种方式是, 用一个 `minDist` 记录当前的距离, 更新过程中只有当v的距离比minDist小时才更新, 入栈. 实验下来两种方式没有复杂度上的区别.
    [官答](https://leetcode.cn/problems/path-with-maximum-probability/solution/gai-lu-zui-da-de-lu-jing-by-leetcode-solution/)
"""
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        # 一种方式是用 `visited` 字典标记已确定节点
        g = [[] for _ in range(n)]
        for (u,v),p in zip(edges, succProb):
            g[u].append((v,p)); g[v].append((u,p))
        h = [(-1, start)]
        visited = set()     # 已确定的点
        while h:
            prob,u = heappop(h)
            if u==end: return -prob
            if u in visited: continue
            visited.add(u)  # 注意, visited 中的点的距离已确定为最小值.
            for v,p in g[u]:
                if v not in visited:
                    heappush(h, (prob*p, v))
        return 0
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        # 另一种方式是, 用一个 `minDist` 记录当前的距离, 更新过程中只有当v的距离比minDist小时才更新, 入栈
        g = [[] for _ in range(n)]
        for (u,v),p in zip(edges, succProb):
            g[u].append((v,p)); g[v].append((u,p))
        h = [(-1, start)]
        # maxProb 记录当前点最大概率. 可用于剪枝
        maxProb = [0] * n; maxProb[start] = 1
        while h:
            prob,u = heappop(h)
            if u==end: return -prob
            for v,p in g[u]:
                pp = -prob*p
                if pp <= maxProb[v]: continue
                maxProb[v] = pp
                heappush(h, (-pp, v))
        return 0
    """ 1515. 服务中心的最佳位置 #hard #题型 #最优化
给定一组点, 寻找一个点, 使其到这些点的距离只和最小. 限制: 数量 50, 范围 [0,100], 京都要求 1e-5
提示: 这个点就是 [几何中位数](https://en.wikipedia.org/wiki/Geometric_median) 注意没有解析解
思路0: 一种作弊的方法是直接调用 `scipy.optimize.minimize`
思路1: #梯度下降
    注意, 我们的目标是 `f(xc,yc) = sum{ dist((xc,yc), (xi,yi)) } = sum{ sqrt((xc-xi)^2 + (yc-yi)^2) }` 这里的距离为欧氏距离.
    该函数为凸函数, 因此可以用梯度下降法求解局部最小值即为全局解.
    求梯度, `df/dxc = sum{ (xc-xi)/sqrt((xc-xi)^2 + (yc-yi)^2) }`
    更新公式: `xc = xc - learning_rate * df/dxc`, 对于y同样.
    技巧: 本题中用了 **学习率衰减** 来加快收敛. 将初始学习率设置为1并设置衰减为1e-3. 实验发现 设置得太大会导致收敛过快, 可能精度不够, 例如 1e-2; 太小则收敛过慢, 可能会超时, 例如 1e-5.
思路2: #爬山 法 利用了是凸函数的性质
    由于我们的目标是搜索凸函数的极值, 不会出现崎岖的平面. 因此我们可以选择一定的步长分别尝试向四个坐标轴方向移动, 直到收敛.
    具体而言, 在每一步, 我们依次查询
    总结与梯度下降的区别: 1) GD由于更新方向是正确的, 每轮都发生学习率缩减; 而爬山法的方向是固定的四个备选项, 比较模糊, 何时更新step? 答案是如果每轮没有发生移动, 则缩减step (考虑与坐标轴45度角的, 较长的山脊, 若在移动过程中搜索step可能无法收敛到正确值); 2)GD的终止条件是位置变化小于eps, 而爬山的种植条件是step小于eps (当然其实也就是位置变化).
思路3: #三分查找 同样利用了凸函数性质
    核心: 假设当前搜索范围为 [L,R], 我们取三等分点 a,b, 若 `f(a) < f(b)`, 则最小值一定不会在 [b,R] 范围内. 具体证明见官答.
    这样, 每次缩减 1/3 的区间, 直到收敛.
    注意: 本题中是二维情况, 例如可以外层循环搜索x, 内层循环搜索y.
[官答](https://leetcode.cn/problems/best-position-for-a-service-centre/solution/fu-wu-zhong-xin-de-zui-jia-wei-zhi-by-leetcode-sol/)
"""
    def getMinDistSum(self, positions: List[List[int]]) -> float:
        # 思路1 梯度下降
        import random
        
        eps = 1e-7
        alpha = 1.0
        decay = 1e-3    # 学习率衰减（learning rate decay）
        # 设置得太大会导致收敛过快, 可能精度不够, 例如 1e-2; 太小则收敛过慢, 可能会超时, 例如 1e-5

        n = len(positions)
        # 调整批大小
        batchSize = n   # 这里设置为全批量

        # 初始化为重心
        x = sum(pos[0] for pos in positions) / n
        y = sum(pos[1] for pos in positions) / n
        
        # 计算服务中心 (xc, yc) 到客户的欧几里得距离之和
        getDist = lambda xc, yc: sum(((x - xc) ** 2 + (y - yc) ** 2) ** 0.5 for x, y in positions)
        
        while True:
            # 将数据随机打乱
            random.shuffle(positions)
            xPrev, yPrev = x, y

            for i in range(0, n, batchSize):
                j = min(i + batchSize, n)
                dx, dy = 0.0, 0.0

                # 计算导数，注意处理分母为零的情况
                for k in range(i, j):
                    pos = positions[k]
                    dx += (x - pos[0]) / (sqrt((x - pos[0]) * (x - pos[0]) + (y - pos[1]) * (y - pos[1])) + eps)
                    dy += (y - pos[1]) / (sqrt((x - pos[0]) * (x - pos[0]) + (y - pos[1]) * (y - pos[1])) + eps)
                
                x -= alpha * dx
                y -= alpha * dy

                # 每一轮迭代后，将学习率进行衰减
                alpha *= (1.0 - decay)
            
            # 判断是否结束迭代
            if ((x - xPrev) ** 2 + (y - yPrev) ** 2) ** 0.5 < eps:
                break

        return getDist(x, y)

    def getMinDistSum(self, positions: List[List[int]]) -> float:
        # 思路2: #爬山 法 利用了是凸函数的性质
        # 四个探索方向
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        eps = 1e-7
        # 步长和衰减
        step = 1.0
        decay = 0.5

        n = len(positions)
        x = sum(pos[0] for pos in positions) / n
        y = sum(pos[1] for pos in positions) / n
        
        # 计算服务中心 (xc, yc) 到客户的欧几里得距离之和
        getDist = lambda xc, yc: sum(((x - xc) ** 2 + (y - yc) ** 2) ** 0.5 for x, y in positions)
        
        while step > eps:
            # 记录是否进行了移动
            modified = False
            for dx, dy in dirs:
                xNext = x + step * dx
                yNext = y + step * dy
                if getDist(xNext, yNext) < getDist(x, y):
                    x, y = xNext, yNext
                    modified = True
                    break
            # 只有在未发生移动的情况下, 将步长进行衰减
            if not modified:
                step *= (1.0 - decay)

        return getDist(x, y)

    def getMinDistSum(self, positions: List[List[int]]) -> float:
        # 思路3: #三分查找 同样利用了凸函数性质
        eps = 1e-7

        # 计算服务中心 (xc, yc) 到客户的欧几里得距离之和
        getDist = lambda xc, yc: sum(((x - xc) ** 2 + (y - yc) ** 2) ** 0.5 for x, y in positions)

        # 固定 xc，使用三分法找出最优的 yc
        def checkOptimal(xc: float) -> float:
            yLeft, yRight = 0.0, 100.0
            while yRight - yLeft > eps:
                yFirst = (yLeft + yLeft + yRight) / 3
                ySecond = (yLeft + yRight + yRight) / 3
                if getDist(xc, yFirst) < getDist(xc, ySecond):
                    yRight = ySecond
                else:
                    yLeft = yFirst
            return getDist(xc, yLeft)
        
        xLeft, xRight = 0.0, 100.0
        while xRight - xLeft > eps:
            # 左 1/3 点
            xFirst = (xLeft + xLeft + xRight) / 3
            # 右 1/3 点
            xSecond = (xLeft + xRight + xRight) / 3
            if checkOptimal(xFirst) < checkOptimal(xSecond):
                xRight = xSecond
            else:
                xLeft = xFirst

        return checkOptimal(xLeft)

    def getMinDistSum(self, positions: List[List[int]]) -> float:
        # 思路0
        from scipy.optimize import minimize
        # result 包括 x,fun 等属性.
        return minimize(lambda t: sum([math.dist(p, t) for p in positions]), (0, 0))['fun']


sol = Solution()
result = [
    # sol.numSub(s = "0110111"),
    # sol.numSub(s = "000111"),
    sol.maxProbability(n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2),
    sol.maxProbability(n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], start = 0, end = 2),
    # sol.getMinDistSum(positions = [[0,1],[1,0],[1,2],[2,1]]),
]
for r in result:
    print(r)
