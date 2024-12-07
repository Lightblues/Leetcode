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
https://leetcode.cn/contest/weekly-contest-408
https://leetcode.cn/circle/discuss/GNUiDD/
T2 就需要用到质数表!
T3 建立索引的思路非常赞 #题型
T4 非常有意思的题目! 分析思路非常赞, 也涉及到几何里面的很多边界判断 star

Easonsi @2023 """

N = 4 * 10**4       # N*2 > 1e9
is_prime = [True] * (N+1)
is_prime[0] = is_prime[1] = False
for i in range(2, N+1):
    if not is_prime[i]: continue
    for j in range(i*2, N+1, i):
        is_prime[j] = False

class Solution:
    """ 3232. 判断是否可以赢得数字游戏 """
    def canAliceWin(self, nums: List[int]) -> bool:
        s = sum(nums)
        aa = sum(i for i in nums if i<10)
        return aa*2 != s
    
    """ 3233. 统计不是特殊数字的数字数量 #medium 定义: 一个正数正好只有两个 "真因数", 也即除了自身之外只有 1,x 两个因数, 叫作特殊数字. 问 [l,r] 范围内的数量
限制: n 1e9
注意到, 这里的特殊数字的要求 -- 它必然是 prime**2
    """
    def nonSpecialCount(self, l: int, r: int) -> int:
        cnt = 0
        _l = max(2, ceil(sqrt(l)))
        for i in range(_l, floor(sqrt(r))+1):
            if not is_prime[i]: continue
            if i**2 > r: break
            cnt += 1
        return (r-l+1) - cnt
    
    """ 3234. 统计 1 显著的字符串的数量 #medium #题型 统计一个 01 字符串满足要求的子串数量, 要求 #1 >= #0^2 
限制: n 4e4
思路1: 索引0出现的位置!
    假设子串中0的个数是 n0, 由于 n0^2 <= n1 <= n, 于是 n0 < sqrt(n)
    我们枚举左端点! 然后枚举0出现的位置
        所有0出现的地方记作index数组 index
        假设现在的位置是i, 对于其后面的的 [index[k], index[k+1]) 范围内, 0的个数是 c0 = k
            1 的个数为 c1 = index[k] - i + delta, 这里的 delta指的是从 index[k] 往后的1的个数
            需要满足 delta >= k^2 - (index[k]-i)
    复杂度 O(n sqrt(n))
[ling](https://leetcode.cn/problems/count-the-number-of-substrings-with-dominant-ones/solutions/2860198/mei-ju-zi-chuan-zhong-de-0-de-ge-shu-pyt-c654/)
    """
    def numberOfSubstrings(self, s: str) -> int:
        n = len(s)
        index0 = []
        total0 = 0
        for i,ch in enumerate(s):
            if ch=='0': 
                index0.append(i)
                total0 += 1
        index0.append(n)     # dummy
        total1 = n - total0
        # 
        ans = 0
        first_0 = 0 # the idx in `index0` of the first 0 after i
        for i,ch in enumerate(s):
            if ch == '1':                       # add the first part, i.e., c0 = 0
                ans += index0[first_0] - i
            for k in range(first_0, len(index0)-1):
                c0 = k - first_0 + 1           # number of 0
                if c0 ** 2 > total1: break
                c1_first_part = (index0[k] - i + 1) - c0
                ava = index0[k+1] - index0[k] - 1           # 可用的1的数量
                needed = max(c0**2 - c1_first_part, 0)
                if ava >= needed:
                    ans += ava - needed + 1                 # +1 对应的是那个0
            if ch == '0': 
                first_0 += 1
        return ans
    
    """ 3235. 判断矩形的两个角落是否可达 #hard #hardhard 需要从矩阵左下角走到右上角, 不接触边界和一些障碍的圆 (包括内部和边界)! 
限制: x/y 1e9; #circles 1e3. 此外所有的点都在第一象限 (x,y >= 0), 方便一些讨论
思路1: 并查集 或者 DFS
    反过来想: 什么情况下无法到达? 上/左侧边 和 下/右侧边 任意一组之间被连起来了! 发生了阻断! 
    简单起见, 先考虑圆心在在矩形内部的情况. 
        我们可以将这些圆看作一系列的节点, 相接或者相切的话就连起来; 另外, 四条边也分别看作特殊节点! 
        判断条件, 上/左侧边 和 下/右侧边 是否相连! 在具体的实现上, 可以用 #并查集 或者 #DFS 来实现! 
    然而, 还需要考虑圆心在外侧的情况! 
        例如, 对于数据 3,3,[[2,4,1],[4,4,1],[4,2,1]], 这里的三个圆心将上边和右边连起来了, 但是不影响矩形内的连接情况! 
        也可以只有两个圆, 它们都不包含边界点 (3,3), 同时在矩形外侧发生了相接关系! 
    另外, 有两个特殊点: 矩形的左上角和右下角, 如果有圆包含了其中一个点, 必然不可达! -- 这让我们排除了很多判断! 
    上面思路理清楚之后, 需要实现几个函数:
        condition_1: 是否与矩形上边界/左边界相交相切. 注意到所有的点都在第一象限, 可以分成 
            1) 在 x<X 的情况下和上边(线段)相交 (注意 x>X 的情况不用考虑, 已经被排除!); 
            2) 在 y<Y 的情况下与左边(线段)相交; 
            3) 在 y>Y 的情况下包括左上角
        condition_2: 是否与矩形下边界/右边界相交相切. 同理
        is_connected: 两个圆相交, 并且相交的部分发生在矩阵内! 
            因为已经保证了两个圆不包含左下角/右上角, 任取一个相交部分的点来做验证即可!
            不妨选择圆心连线和相交点连线的交点 A, 显然是 (x1, y1) + r1/(r1+r2) * (x2-x1, y2-y1)
            显然, A也在第一象限, 需要满足 A[0] <= X, A[1] <= Y 即可!
[ling](https://leetcode.cn/problems/check-if-the-rectangle-corner-is-reachable/solutions/2860214/deng-jie-zhuan-huan-bing-cha-ji-pythonja-yf9y/)
    """
    def canReachCorner(self, X: int, Y: int, circles: List[List[int]]) -> bool:
        # 判断点 (x,y) 是否在圆 (ox,oy,r) 内
        def in_circle(ox: int, oy: int, r: int, x: int, y: int) -> bool:
            return (ox - x) * (ox - x) + (oy - y) * (oy - y) <= r * r

        vis = [False] * len(circles)
        def dfs(i: int) -> bool:
            x1, y1, r1 = circles[i]
            # 圆 i 是否与矩形右边界/下边界相交相切
            if y1 <= Y and abs(x1 - X) <= r1 or \
               x1 <= X and y1 <= r1 or \
               x1 > X and in_circle(x1, y1, r1, X, 0):
                return True
            vis[i] = True
            for j, (x2, y2, r2) in enumerate(circles):
                # 在两圆相交相切的前提下，点 A 是否严格在矩形内
                if not vis[j] and \
                   (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) <= (r1 + r2) * (r1 + r2) and \
                   x1 * r2 + x2 * r1 < (r1 + r2) * X and \
                   y1 * r2 + y2 * r1 < (r1 + r2) * Y and \
                   dfs(j):
                    return True
            return False

        for i, (x, y, r) in enumerate(circles):
            # 圆 i 包含矩形左下角 or
            # 圆 i 包含矩形右上角 or
            # 圆 i 与矩形上边界/左边界相交相切
            if in_circle(x, y, r, 0, 0) or \
               in_circle(x, y, r, X, Y) or \
               not vis[i] and (x <= X and abs(y - Y) <= r or
                               y <= Y and x <= r or
                               y > Y and in_circle(x, y, r, 0, Y)) and dfs(i):
                return False
        return True



sol = Solution()
result = [
    # sol.canAliceWin([4,3,4,9,21]),
    # sol.canAliceWin([1,2,3,4,10]),
    # sol.nonSpecialCount(l = 4, r = 16),
    # sol.nonSpecialCount( l = 5, r = 7),
    # sol.numberOfSubstrings(s = "00011"),
    # sol.numberOfSubstrings(s = "101101"),
    sol.canReachCorner(3,3,[[2,4,1],[4,4,1],[4,2,1]]),
]
for r in result:
    print(r)
