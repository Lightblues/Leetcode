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
https://leetcode.cn/contest/weekly-contest-391
https://leetcode.cn/circle/discuss/fGVzcv/
T4 的曼哈顿距离有意思!!

Easonsi @2023 """
class Solution:
    """ 3099. 哈沙德数 """
    def sumOfTheDigitsOfHarshadNumber(self, x: int) -> int:
        a = 0; b = x
        while b:
            b,xx = divmod(b, 10)
            a += xx
        if x % a: return -1
        else: return a
    
    """ 3100. 换水问题 II """
    def maxBottlesDrunk(self, numBottles: int, numExchange: int) -> int:
        ans = numBottles
        while numBottles >= numExchange:
            numBottles -= numExchange - 1
            ans += 1
            numExchange += 1
        return ans
    
    """ 3101. 交替子数组计数 """
    def countAlternatingSubarrays(self, nums: List[int]) -> int:
        ans = 0
        l = 0
        nums.append(nums[-1])   # dummy
        for r,x in enumerate(nums):
            if r>0 and x==nums[r-1]:
                ll = r-l
                ans += ll*(ll+1)//2
                l = r
        return ans
    
    """ 3102. 最小化曼哈顿距离 #hard 有一组点, 可以移除一个点, 要求其他的点之间的 manhattan 距离的最大值最小! 
限制: n 1e5
思路1: 直觉
    直觉来看, manhattan 距离最大值一定和边界相关! (或者说, 四个角的位置)
    因此, 对于四个角维护最大/次大值即可! 然后枚举尝试删除
    NOTE: 注意到不是坐标轴的最大/次大! 
更为严谨的说, 可以将「曼哈顿距离与切比雪夫距离的相互转化」!
    也即,  (x,y) 的坐标变为 (x + y, x - y) 之后, 曼哈顿距离就变成了切比雪夫距离!!! (旋转, 扩大一倍)
    见 [oi-wiki](https://oi-wiki.org/geometry/distance/)

[ling](https://leetcode.cn/problems/minimize-manhattan-distances/solutions/2716755/tu-jie-man-ha-dun-ju-chi-heng-deng-shi-b-op84/)
相似题目
1330. 翻转子数组得到最大的数组值
1131. 绝对值表达式的最大值
    """
    def minimumDistance(self, points: List[List[int]]) -> int:
        # def plot_points(points):
        #     import matplotlib.pyplot as plt
        #     for p in points:
        #         plt.scatter(p[0], p[1])
        #     plt.show()
        # plot_points(points)

        points = [tuple(p) for p in points]
        cnt = Counter(points)
        candidates = []
        candidates_cnt = Counter()
        lambdas = (
            # lambda x: (x[0], x[1]),       # NOTE: 这样会有问题! 如下面最后一个 case
            # lambda x: (x[0], -x[1]),
            # lambda x: (x[1], x[0]),
            # lambda x: (x[1], -x[0]),
            lambda x: x[0] + x[1],
            lambda x: x[0] - x[1],
        )
        for f in lambdas:
            points.sort(key=f)
            for p in points[:2] + points[-2:]:
                if candidates_cnt[p] < cnt[p]:
                    candidates.append(p)
                    candidates_cnt[p] += 1
        m = len(candidates)
        def dist(p1, p2):
            return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
        ans = float('inf')
        for idx in range(m):
            dist_max = 0
            for i in range(m):
                if i==idx: continue
                for j in range(i+1, m):
                    if j==idx: continue
                    dist_max = max(dist_max, dist(candidates[i], candidates[j]))
            ans = min(ans, dist_max)
        return ans




sol = Solution()
result = [
    # sol.sumOfTheDigitsOfHarshadNumber(18),
    # sol.sumOfTheDigitsOfHarshadNumber(23),
    # sol.maxBottlesDrunk(10, 3),
    # sol.countAlternatingSubarrays( [1,0,1,0]),
    # sol.countAlternatingSubarrays( [0,1,1,1]),
    sol.minimumDistance(points = [[3,10],[5,15],[10,2],[4,4]]),
    sol.minimumDistance(points = [[1,1],[1,1],[1,1]]),
    sol.minimumDistance([[7,7],[9,3],[8,1],[8,8],[8,9],[5,1],[3,2],[6,9],[3,6]]),
]
for r in result:
    print(r)
