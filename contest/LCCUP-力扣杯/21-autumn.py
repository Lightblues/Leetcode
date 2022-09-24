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
[力扣杯竞赛真题集](https://leetcode.cn/study-plan/lccup)
https://leetcode.cn/study-plan/lccup/?progress=s2x5c97



@2022 """
class Solution:
    """ LCP 39. 无人机方阵 #easy
将一组数量为n的数字, 变换为另一组长度也为n的数字, 可以随意调换顺序, 问最小需要修改多少次数字的值?
思路1: 利用 Counter 计数. 然后计算差值
    1.1 将s和t分别统计到两个哈希表. 结果是什么? 注意不应该取 (cnt_s - cnt_t) 的 abs, 而应该取正数部分! (考虑对称)
    1.2 也可以将s和t中的数字统计在一个哈希表中, 分别取 +和-. 这样答案自然就是正数/负数 之和.
 """
    def minimumSwitchingTimes(self, source: List[List[int]], target: List[List[int]]) -> int:
        cnts = Counter(itertools.chain(*source))
        # cnts = reduce(add, [Counter(s) for s in source])
        cntt = reduce(add, [Counter(s) for s in target])
        ans = 0
        for k,v in cnts.items():
            # 注意, 这里统计的不能是 abs 和!
            # 考虑 [1,2,2] -> [1,1,2] 的情况, 取一个方向的正值即可.
            ans += max(v - cntt[k], 0)
        return ans
    
    """ LCP 40. 心算挑战 #easy
要求从一组数字中选出cnt个, 要求这些数字之和为偶数. 若取不到则返回0. 限制: cnt, n 1e5
思路1: 排序+前缀和+遍历
    对于奇偶数分组, 排序.
    因为要求和为偶数, 奇数组必须选择偶数个, 遍历所有的可能, 取最大值. 为了快速得到区间和, 使用 #前缀和.
 """
    def maxmiumScore(self, cards: List[int], cnt: int) -> int:
        odds, evens = [], []
        for c in cards:
            if c & 1: odds.append(c)
            else: evens.append(c)
        odds.sort(reverse=True); evens.sort(reverse=True)
        oddcum = list(accumulate(odds, initial=0))
        evencum = list(accumulate(evens, initial=0))
        ans = 0
        for i in range(0, cnt+1, 2):
            if i > len(odds) or cnt-i > len(evens): continue
            ans = max(ans, oddcum[i] + evencum[cnt-i])
        return ans
    
    
    """ LCP 41. 黑白翻转棋 #medium 给定一个黑白棋盘, 问在任意位置下黑棋, 最多能翻转多少个白棋? 限制: 长宽 8


"""
    def flipChess(self, chessboard: List[str]) -> int:
        m,n = len(chessboard), len(chessboard[0])
        
    
    """ LCP 01. 猜数字 #easy """
    
    """ LCP 02. 分式化简 #easy #题型 给定一组系数, 每个元素按照 a0 + 1 / { a1 + 1 / { a2 + 1 / { ... } } } 的形式展开. 求最终的最简分式. 限制: n 10
思路1: 从后往前便利, 假设当前的分数为 m/n, 则去倒数再加上x之后变为 (n+mx)/m
"""
    def fraction(self, cont: List[int]) -> List[int]:
        m,n = cont[-1],1
        for x in cont[-2::-1]:
            m, n = x*m + n, m
        g = math.gcd(m, n)
        return [m//g, n//g]
    
    """ LCP 03. 机器人大冒险 #medium 机器人原本在 (0,0), 给定一系列指令例如 `URR` (只能向上向右), 机器人将循环这一组指令. 还有一些障碍物. 问机器人能否顺利到达终点 (x,y).
限制: 指令长度 n 1000. x,y 1e9. 障碍物数量 o 1e3.
思路1: 只需要检查指令的第一条路径即可, 对于重复的部分, 用一个 `meet(p, pos)` 函数进行碰撞检测.
    细节: 1) 机器人的路径要经过终点; 2) 对于在终点之外的障碍物, 需要进行过滤.
    复杂度: O(n*o).
"""
    def robot(self, command: str, obstacles: List[List[int]], x: int, y: int) -> bool:
        oneRoop = (command.count('R'), command.count('U'))  # 循环一次的位移.
        pos = [0,0]
        canReach = False
        def meet(p, pos):
            # 判断 x 经过若干 roop 后能否到达 pos
            dx,dy = pos[0]-p[0], pos[1]-p[1]
            if dx%oneRoop[0] or dy%oneRoop[1]: return False
            return dx//oneRoop[0]==dy//oneRoop[1] and dx//oneRoop[0]>=0
        def check(p):
            nonlocal canReach
            if meet(p, (x,y)): canReach = True
            for obs in obstacles:
                if meet(p, obs): return False
            return True
        def filterObs(p): return p[0]<=x and p[1]<=y
        obstacles = list(filter(filterObs, obstacles))
        for c in command:
            collapse = not check(pos)
            if collapse: return False
            if c=='U': pos[1]+= 1
            else: pos[0]+=1
        return canReach
    
    """ LCP 04. 覆盖 #hard 给定一个grid, 有些部分是坏的, 问能够不重叠地防止多少个 1*2 的骨牌 (可横放). 限制: 长宽 n 8.
提示: 将grid按照相邻的规则标记为 x,y, 则放置的骨牌一定占据 1个x, 1个y. 注意到, **可以将本问题转化为二分图最大匹配**.
"""
    def domino(self, n: int, m: int, broken: List[List[int]]) -> int:
        pass

    """ LCP 05. 发 LeetCoin #hard 一个树形结构, 表示公司层级关系. 设置三种操作: 1) 给某一节点发币; 2) 给某一节点及其所有子节点发币; 3) 查询某一节点所定义的子树中发币总数. 返回每次查询的结果.
限制: 节点数 N 操作数 Q 5e4; 每次发币数量 5e3. 对于结果取模.
"""
    def bonus(self, n: int, leadership: List[List[int]], operations: List[List[int]]) -> List[int]:
        pass
        ceil
    
    """ LCP 06. 拿硬币 """
    
    """ LCP 07. 传递信息 #easy 在一张有向图上, 从A到B的长为 k的路径数. 限制: n 10; k 5  """
    def numWays(self, n: int, relation: List[List[int]], k: int) -> int:
        g = [[] for _ in range(n)]
        for u,v in relation:
            g[u].append(v)
        ans = 0
        def dfs(u, k):
            nonlocal ans
            if k==0: ans+= u==n-1; return
            for child in g[u]:
                dfs(child, k-1)
        dfs(0, k)
        return ans
    
    """ LCP 08. 剧情触发时间 #medium #题型 游戏有三个属性. 开始状态都为 0. increse 数组表示每天新增的属性, 例如 [[1,2,1]]; requirements 数组表示一些剧情的触发条件. 问每个剧情触发的最早时间. 
限制: len(increse) 1e4; len(requirements) 1e5; 每天的属性增加 10; requirements 元素 1e5.
思路1: 分开考虑三个属性, 对于每个属性其每天的值是递增的, 对于每个属性进行 #二分 查找.
细节: 注意下面 `cmp_to_key` 函数的使用 (配合 `bisect_left`).
"""
    def getTriggerTime(self, increase: List[List[int]], requirements: List[List[int]]) -> List[int]:
        # 采用 cmp_to_key 转为类进行比较, 速度较慢.
        from functools import cmp_to_key
        n = len(increase)
        dp = [[0,0,0] for _ in range(n+1)]
        for i in range(n):
            dp[i+1][0] = dp[i][0] + increase[i][0]
            dp[i+1][1] = dp[i][1] + increase[i][1]
            dp[i+1][2] = dp[i][2] + increase[i][2]
        
        # 关于 cmp 函数, 参见 https://www.zhihu.com/question/266307824
        def cmp(x:list, y: list):
            # 这里的函数形式由 cmp_to_key 和 bisect.bisect_left 所共同决定. 
            # 二分搜索的调用为 bisect_left(dp, key(r), key=key), 这里是对 dp 进行二分搜索 (采用key进行变换). bisect_left 的更新逻辑是, 当 `key(a[mid]) < x` 时更新 lo. 因此, 这里需要确保 all(x>=y) 的时候才返回 1.
            # return -1 if all(x[i]<=y[i] for i in range(3)) else 1
            return 1 if all(x[i]>=y[i] for i in range(3)) else -1
        key = cmp_to_key(cmp)
        ans = []
        for r in requirements:
            i = bisect.bisect_left(dp, key(r), key=key)
            ans.append(i if i<=n else -1)
        return ans
    def getTriggerTime(self, increase: List[List[int]], requirements: List[List[int]]) -> List[int]:
        # 手动实现, 思路居然更简单些.
        n = len(increase)
        dp = [[0], [0], [0]]
        for i in range(len(increase)):
            dp[0].append(dp[0][-1]+increase[i][0])
            dp[1].append(dp[1][-1]+increase[i][1])
            dp[2].append(dp[2][-1]+increase[i][2])
        ans = []
        for r in requirements:
            idx = max(bisect.bisect_left(dp[i], r[i]) for i in range(3))
            ans.append(idx if idx<=n else -1)
        return ans
    
    
    """ LCP 09. 最小跳跃次数 #hard 有一排n个弹簧, 位置i的弹簧可以跳到左侧任意位置或者 i+jump[i] 处. 问要将小球从位置0弹出 (idx>=n) 所需的最少次数. 限制: n1e6; jump[i] 1e4.

"""
    def minJump(self, jump: List[int]) -> int:
        
sol = Solution()
result = [
    # sol.minimumSwitchingTimes(source = [[1,2,3],[3,4,5]], target = [[1,3,5],[2,3,4]]),
    # sol.maxmiumScore(cards = [1,2,8,9], cnt = 3),
    # sol.fraction(cont = [3, 2, 0, 2]),
    # sol.robot(command = "URR", obstacles = [], x = 3, y = 2),
    # sol.robot(command = "URR", obstacles = [[2, 2]], x = 3, y = 2),
    # sol.robot(command = "URR", obstacles = [[4, 2]], x = 3, y = 2)
    # sol.numWays(n = 5, relation = [[0,2],[2,1],[3,4],[2,3],[1,4],[2,0],[0,4]], k = 3),
    sol.getTriggerTime(increase = [[2,8,4],[2,5,0],[10,9,8]], requirements = [[2,11,3],[15,10,7],[9,17,12],[8,1,14]]),
]
for r in result:
    print(r)
