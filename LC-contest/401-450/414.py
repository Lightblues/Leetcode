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
https://leetcode.cn/contest/weekly-contest-414
T2 居然被卡了, 太久没做二分
T4 混合和国际象棋还有博弈论, 自己做出来的成就感也太高了! 
Easonsi @2023 """
class Solution:
    """ 3280. 将日期转换为二进制表示 """
    def convertDateToBinary(self, date: str) -> str:
        parts = date.split('-')
        return '-'.join(str(bin(int(i)))[2:] for i in parts)
    
    """ 3281. 范围内整数的最大得分 从n个长d的区间中各选一个数字, 求这些数字间距的最大值. 
限制: n 1e5
思路0: 尝试 贪心, 发现错了!
思路1: #二分
    """
    def maxPossibleScore(self, start: List[int], d: int) -> int:
        n = len(start)
        start.sort()
        s, e = start[0], start[-1] + d
        mx = (e - s) // (n-1)
        def check(x):
            pre = s
            for i in range(1, n):
                l = start[i]
                if l >= pre + x: pre = l
                elif l + d >= pre + x: pre += x
                else: return False
            return True
        ans = 0
        l, r = 0, mx
        while l <= r:
            mid = (l + r) >> 1
            if check(mid):
                ans = mid
                l = mid + 1
            else:
                r = mid - 1
        return ans
    
    """ 3282. 到达数组末尾的最大得分 #medium 从位置0跳到n-1, 每次从i到j的得分为 (j-i)*nums[i], 问最大得分总和
限制: n 1e5
思路1: 因为每一段宽度都作为因子, 因此每次跳到更高位!
    """
    def findMaximumScore(self, nums: List[int]) -> int:
        ans = 0
        mx = 0
        for x in nums:
            ans += mx
            mx = max(mx, x)
        return ans
    
    """ 3283. 吃掉所有兵需要的最多移动次数 #hard 在 50x50 的棋盘上有一个马和一些兵 (最多 15). 
在一个回合中, 玩家选择一个兵, 让马用最少步骤到那边吃掉, (中间经过的话不会被吃). A 的目标是最大化总步骤; B 相反. 问最优情况下的总步骤. 
思路1: 综合题
    首先, 马从 (0,0) 走到 (i, j) 的最小步数是可以通过 #DFS 找到的. 
    从而, 对于最多15个兵, 可以构建 (n+1)x(n+1) 的距离矩阵. 
        没啥用的结论: 每个AB 的决策构成了一个长 (n+1) 的路径. 
    记 A 当前在 i, 剩余的兵状态 s, 则有 #DP
        f(i,s) = max{ d(i,j) + g(j, s \ j) } for i in s
    同理
        g(i, s) = min{ d(i,j) + f(j, s \ j) } for j in s
    边界: g(i,0) = f(i,0) = 0
    ans: f(0, 2^n - 1)
思路2: 除了计算两两之间的距离, 另外可以计算所有 "马到棋盘上所有位置的最短距离", 这样就避免了 calc_dist 的实现! 
[ling](https://leetcode.cn/problems/maximum-number-of-moves-to-kill-all-pawns/solutions/2909069/pai-lie-xing-zhuang-ya-dpxiang-lin-xiang-q49q/)
    """
    def maxMoves(self, kx: int, ky: int, positions: List[List[int]]) -> int:
        # 计算 d(i,j), i,j in [-1, 49]
        dist = defaultdict(int)
        dist[(0,0)] = 0
        q = [(0,0)]
        dirs = ((1,2), (2,1), (-1,-2), (-2,-1), (1,-2), (2,-1), (-1,2), (-2,1))
        while q:
            nq = []
            for x,y in q:
                for dx,dy in dirs:
                    nx,ny = x+dx,y+dy
                    #  有些步骤需要走到边界外才能吃到! --> 其实只有下面那个 (0,0) - (1,1) 的情况! 
                    if not (-1<=nx<=49 and -1<=ny<=49): continue
                    if (nx, ny) in dist: continue
                    dist[(nx,ny)] = dist[(x,y)] + 1
                    nq.append((nx,ny))
            q = nq
        # 计算 马+兵 之间的距离矩阵, 第0个为马
        n = len(positions)
        corners = [(0,0), (0,49), (49,0), (49,49)]
        def calc_dist(i, j):
            dx,dy = abs(i[0] - j[0]), abs(i[1] - j[1])
            # 注意这种特殊情况! 
            if dx==dy==1:
                if i in corners or j in corners: return 4  # 注意输入的 i,j 需要是 tuple
            return dist[dx, dy]
        d = [[0]*(n+1) for _ in range(n+1)]
        positions = [(kx,ky)] + [tuple(pos) for pos in positions]       # 将马放在第0个
        for i,pos_i in enumerate(positions):
            for j,pos_j in enumerate(positions):
                d[i][j] = calc_dist(pos_i, pos_j)
        # DP
        @lru_cache(None)
        def f(i, s):
            if s==0: return 0
            ans = 0
            for j in range(n+1):
                if s & (1<<j): 
                    ans = max(ans, d[i][j] + g(j, s^(1<<j)))
            return ans
        @lru_cache(None)
        def g(i, s):
            if s==0: return 0
            ans = inf
            for j in range(n+1):
                if s & (1<<j): 
                    ans = min(ans, d[i][j] + f(j, s^(1<<j)))
            return ans
        return f(0, (1<<(n+1))-1-1)
    
sol = Solution()
result = [
    # sol.convertDateToBinary(date = "2080-02-29"),
    # sol.maxPossibleScore(start = [6,0,3], d = 2),
    # sol.maxPossibleScore(start = [2,6,13,13], d = 5),
    # sol.maxPossibleScore([100,1000000000,0], 1009), 
    # sol.findMaximumScore(nums = [1,3,1,5]),
    sol.maxMoves(kx = 1, ky = 1, positions = [[0,0]]),
    sol.maxMoves(kx = 0, ky = 2, positions = [[1,1],[2,2],[3,3]]),
    sol.maxMoves(kx = 0, ky = 0, positions = [[1,2],[2,4]]),
    sol.maxMoves(0, 0, [[6,9],[2,8],[0,10]]),
]
for r in result:
    print(r)
