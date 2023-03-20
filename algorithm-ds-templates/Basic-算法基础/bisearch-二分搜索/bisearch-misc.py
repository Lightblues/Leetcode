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
1552. 两球之间的磁力 #medium #二分 一数轴上有n个位置, 求放m个球, 要求任意相邻球之间的最小距离最大化
2439. 最小化数组中的最大值 #medium [可以贪心直接数学求解]
2513. 最小化两个数组中的最大值 #medium 要求从尽可能小的自然数中, 放在两个数组中, 分别要求有 uniqueCnt1/2 个不同的数字, 其中的每个数字不能被 divisor1/2 整除
2517. 礼盒的最大甜蜜度 #medium
2528. 最大化城市的最小供电站数目 #hard 给定一个数组表示每个城市供电站数量, 给定r表示每个发电站可以覆盖的范围为 [i-r,i+r]; 在新增最多k个的限制下, 要求最大化 min{每个城市可接受到的发电站数量}.


Easonsi @2023 """
class Solution:
    """ 0074. 搜索二维矩阵 #medium 矩阵按照一行一行具有递增性质, 在其中进行搜索
思路1: 就是在 MN 的有序数组上进行 #二分
"""
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        def listIndex2matrixIndes(i):
            quotient, remainder = divmod(i, n)
            return quotient, remainder
        left, right = 0, m*n-1
        while left <= right:
            mid = (left+right)//2
            i,j = listIndex2matrixIndes(mid)
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] < target:
                left = mid+1
            else:
                right = mid-1
        return False
    
    
    """ 1552. 两球之间的磁力 #medium #二分 一数轴上有n个位置, 求放m个球, 要求任意相邻球之间的最小距离最大化 (也即「平均放置」).
限制: m,n 1e5, 位置限制 p 1e9.
思路1: #二分
    提示: 如何检查间距x是否可以达到? 注意, 可以贪心放置: 尽量将占据的位置放在左侧. 证明: 若有另一种放置方案, 其不会优于这种.
    因此, 可以在O(n)的时间内检查; 搜索范围为p, 因此复杂度为 O(n logp)
"""
    def maxDistance(self, position: List[int], m: int) -> int:
        def check(x) -> bool:
            pre = -inf
            acc = 0
            for p in position:
                if p-pre >= x:
                    acc += 1; pre = p
                    if acc>=m: return True
            return False
        position.sort()
        l,r = 1,(position[-1]-position[0])//(m-1) + 1
        ans = 1
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                l = mid+1
            else:
                r = mid-1
        return ans
    
    """ 2517. 礼盒的最大甜蜜度 #medium #题型 需要从一组价格为 price 的糖果中选k个打包, 定义其「甜蜜度」 是礼盒中任意两种糖果 价格 绝对差的最小值, 要求获得最大「甜蜜度」. 限制: n 1e5. 价格 1e9
思路1: #二分 
    子问题「能否选取一组k个糖果使得甜蜜度至少为 x」可以通过贪心求解 复杂度 O(n). 二分的范围 [0, (mx-mn)/(k-1)]
参见 [灵神](https://leetcode.cn/problems/maximum-tastiness-of-candy-basket/solution/er-fen-da-an-by-endlesscheng-r418/)
关联: 「1552. 两球之间的磁力」
"""
    def maximumTastiness(self, price: List[int], k: int) -> int:
        price.sort()
        def check(x):
            # 检查可否取k个糖果, 使得他们的「甜蜜度」至少为x
            # 显然可以贪心, 取最小的, 然后遍历...
            pre=price[0]
            acc = 1
            for a in price[1:]:
                if a-pre>=x:
                    acc += 1
                    pre = a
                    if acc>=k: return True
            return False
        # 二分搜索最大的解
        l=0; r=ceil((price[-1]-price[0])/(k-1))
        ans=0
        while l<=r:
            mid = (l+r)//2
            if check(mid): 
                ans = mid
                l = mid+1
            else: r = mid-1
        return ans
    
    """ 2513. 最小化两个数组中的最大值 #medium 要求从尽可能小的自然数中, 放在两个数组中, 分别要求有 uniqueCnt1/2 个不同的数字, 其中的每个数字不能被 divisor1/2 整除
限制: divisor1/2 1e5; 元素数量 1e9
思路1: #二分 
    如何检查前x个自然是是否可以满足条件? 一开始纠结如何对每个数字进行分配, 后来想到, 问题等价于: 总体数量满足; 两个分组的数量都满足即可. 
    二分的范围? 下界是 uniqueCnt1+uniqueCnt2, 上界不好确定, 直接取了 10*(uniqueCnt1+uniqueCnt2)
见 [灵神](https://leetcode.cn/problems/minimize-the-maximum-of-two-arrays/solution/er-fen-da-an-by-endlesscheng-y8fp/)
"""
    def minimizeSet(self, divisor1: int, divisor2: int, uniqueCnt1: int, uniqueCnt2: int) -> int:
        # 两个除数的共同因子
        divisor12 = math.lcm(divisor1, divisor2)
        def check(x):
            # 检查: 总体数量满足; 两个分组的数量都满足
            if x - x//divisor12 < uniqueCnt1+uniqueCnt2: return False
            if x - x//divisor1 < uniqueCnt1: return False
            if x - x//divisor2 < uniqueCnt2: return False
            return True
        l,r = uniqueCnt1+uniqueCnt2, 10*(uniqueCnt1+uniqueCnt2)
        ans = inf
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = min(ans, mid)
                r = mid-1
            else:
                l = mid+1
        return ans
    
    """ 2528. 最大化城市的最小供电站数目 #hard 给定一个数组表示每个城市供电站数量, 给定r表示每个发电站可以覆盖的范围为 [i-r,i+r]; 在新增最多k个的限制下, 要求最大化 min{每个城市可接受到的发电站数量}.
限制: n 1e5; r<n, k 1e9
思路1: #二分 + #贪心
    观察k的数量, 可以尝试二分.
    如何判断能够构造满足min值至少为x? 可以用贪心
    具体而言, #滑动窗口 考查每个城市所被覆盖的范围, 若没有被满足, 则在最右边贪心补上所需的发电站.
        细节: 注意由于在滑动过程中需要新增/修改发电站数量, 在被移除滑窗的时候也需要被删掉, 因此需要用格外的数组来进行记录!!
[灵神](https://leetcode.cn/problems/maximize-the-minimum-powered-city/solution/er-fen-da-an-qian-zhui-he-chai-fen-shu-z-jnyv/)
    """
    def maxPower(self, stations: List[int], r: int, k: int) -> int:
        n = len(stations)
        def f(x):
            # 判断在k的约束下能否满足条件x, 贪心解决
            # 注意由于在滑动过程中需要新增/修改发电站数量, 在被移除滑窗的时候也需要被删掉, 因此需要用格外的数组来进行记录!!
            s = stations[:]
            remain = k
            acc = sum(s[:r])
            for i in range(n):
                if i+r<n:
                    acc += s[i+r]
                if i-r-1>=0:
                    acc -= s[i-r-1]
                if acc<x:
                    needed = x-acc
                    if needed>remain:
                        return False
                    remain -= needed
                    s[min(i+r, n-1)] += needed
                    acc += needed
            return True
        # 注意这里的搜索范围! right 不能用max!
        left,right = min(stations), sum(stations)+k
        ans = left
        while left<=right:
            mid = (left+right)//2
            if f(mid):
                ans = mid
                left = mid+1
            else: right = mid-1
        return ans

    """ 6325. 修车的最少时间 #hard 能力为r的工人完成x个工作需要 r*x^2 时间, 给定一组工人和要完成的数量x, 问最少时间. 限制: 1<=ranks[i]<=10^5, 1<=cars<=10^6
思路1: #二分 给定一个时间, 可以在 O(n) 时间检查是否可行, 二分答案
    注意范围! 这里的最大应该在 1e6^2 * 100 数量级
[灵神](https://leetcode.cn/problems/minimum-time-to-repair-cars/solution/er-fen-da-an-pythonjavacgo-by-endlessche-keqf/) 的优雅写法
     """
    def repairCars(self, ranks: List[int], cars: int) -> int:
        # 我一般喜欢写一个check函数, 返回是否可以满足条件
        cnt = Counter(ranks)
        def check(x):
            cc = 0
            for r,c in cnt.items():
                cc += floor((x/r)**0.5) * c
            return cc>=cars
        # 下面是我的二分模版
        l,r = 0, 10**14 # 搜索的边界, [l,r] 闭区间
        ans = inf       # 记录答案
        while l<=r: # 因为是闭区间, 所以 <=
            mid = (l+r)//2
            if check(mid):
                # 判断成功, 更新答案
                ans = mid
                r = mid-1
            else:
                l = mid+1
        return ans
    
    def repairCars(self, ranks: List[int], cars: int) -> int:
        # from 灵神, 直接调用了Python的bisect包
        s = lambda t: sum(floor(sqrt(t // r)) for r in ranks)
        return bisect_left(range(min(ranks) * cars * cars), cars, key=s)
    def repairCars(self, ranks: List[int], cars: int) -> int:
        # 分组优化
        cnt = Counter(ranks)
        s = lambda t: sum(floor(sqrt(t // r)) * c for r, c in cnt.items())
        return bisect_left(range(min(cnt) * cars * cars), cars, key=s)


sol = Solution()
result = [
    
]
for r in result:
    print(r)
