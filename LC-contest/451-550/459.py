from typing import *
from collections import defaultdict
from math import comb, inf

"""
https://leetcode.cn/contest/weekly-contest-459
1. 判断整除性. 简单模拟
2. 统计梯形的数目 I "维护左, 枚举右"
3. 位计数深度为 K 的整数数目 II - 套着位运算壳的数组元素更新+区间查询问题 -- 树状数组!
    TODO: 回顾 数组元素 写法
4. 统计梯形的数目 II -- 考虑对于平面坐标的理解, 本质上考了计算
    通过斜率 k 来区分平行边, 通过截距 b 来避免共线
    还需要减去重复计数 -- 平行四边形数量

Easonsi @2026 """

class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] += val
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def pre(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.tree[i]
            i &= i - 1
        return res

    # 计算区间和 a[l] + ... + a[r]
    # 1 <= l <= r <= n
    # 时间复杂度 O(log n)
    def query(self, l: int, r: int) -> int:
        return self.pre(r) - self.pre(l - 1)


class Solution:
    """ 3622. 判断整除性 """
    def checkDivisibility(self, n: int) -> bool:
        s,p = 0,1
        x = n
        while x:
            x, r = divmod(x, 10)
            s += r
            p *= r
        return n % (s+p) == 0

    """ 3623. 统计梯形的数目 I #4 """
    def countTrapezoids(self, points: List[List[int]]) -> int:
        MOD = 10**9+7
        y_group = defaultdict(int)
        for _,y in points:
            y_group[y] += 1
        ans = acc = 0
        for c in y_group.values():
            ans = (ans + comb(c,2)*acc) % MOD
            acc = (acc + comb(c, 2)) % MOD
        return ans % MOD

    """ 3624. 位计数深度为 K 的整数数目 II #6
对于一个整数, 定义 popcount-depth（位计数深度）为经过 "pi+1 = popcount(pi)" 最少操作次数后变为 1 的操作数. 其中 popcount(x) 计算二进制中 1 的数量
对于一个数组, 定义 1. op 1: 统计 [l,r] 范围内 popcount-depth=k 的数量; 2. op 2: 将 nums[idx]=val
限制: n 1e5; val 1e15; 查询 0<=k<=5
思路 1: 6 个树状数组
    对于一个查询, "统计 [l,r] 区间内符合条件的数量"; 还需要对于元素做更新 -> 树状数组!
    考虑本题中 k 的范围, 可以对于每个条件 (共 6 个) 各自维护一颗树状数组, 对应更新即可
    NOTE: 树状数组中只有 "update" 操作; 既然我们使用 0/1+区间和的方式统计符合条件数量; 因此需要用 update(i,-1) 来撤销
    复杂度: O(nK + (n+q)logn), 其中 K=6
https://leetcode.cn/problems/number-of-integers-with-popcount-depth-equal-to-k-ii/solutions/3728547/6-ge-shu-zhuang-shu-zu-pythonjavacgo-by-klqxt/
    """
    def popcountDepth(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        # 不写记忆化，直接迭代
        def pop_depth(x: int) -> int:
            res = 0
            while x > 1:
                res += 1
                x = x.bit_count()
            return res

        n = len(nums)
        f = [FenwickTree(n) for _ in range(6)]  # 6 个树状数组

        def update(i: int, delta: int) -> None:
            d = pop_depth(nums[i])
            f[d].update(i + 1, delta)

        for i in range(n):
            update(i, 1)  # 添加

        ans = []
        for q in queries:
            if q[0] == 1:
                ans.append(f[q[3]].query(q[1] + 1, q[2] + 1))
            else:
                i = q[1]
                update(i, -1)  # 撤销旧的
                nums[i] = q[2]
                update(i, 1)  # 添加新的
        return ans

    """ 3625. 统计梯形的数目 II #6
统计所有点构成梯形的数量, 梯形要求两条边平行即可.
限制: n 500; val [-1000,1000]
思路 1: 统计直线 + 去掉重复统计的平行四边形
    枚举所有的边 (n^2), 可以计算它们的斜率 K 来区分! 为了避免共线, 进一步通过截距 b 来分组.
    上面的统计重复计算了平行四边形, 需要去除! 采用类似的双重分组逻辑:
        - 考虑平行四边形的特点: 两条对角线的中点重合!
        - 因此, 可以再用一个哈希表来统计中点!
        - 同样要避免共线问题 -- 二重通过斜率来区分
    NOTE: 浮点数作为 key 有问题吗? 考虑接近 1 但不相同的两个分数 a/(a+1), (a-1)/a, 差值小于 IEEE 754 的最小精度的时候才会错! 本题范围不会
    复杂度: O(n^2)
    优化: 复杂度在于嵌套的哈希表 -- 而在随机数据下, 斜率相同的点是很少的! 
        因此, 可以用代价更小的数组来先维护内部数据 -> 在枚举的时候在去选择性创建 Counter -- 仅当该组数量 >1 的时候!
    思考: 换成正方形? 矩形? 菱形? 等腰梯形? 直角梯形?
https://leetcode.cn/problems/count-number-of-trapezoids-ii/solutions/3728529/tong-ji-zhi-xian-qu-diao-zhong-fu-tong-j-a3f9/
    """
    def countTrapezoids(self, points: List[List[int]]) -> int:
        cnt = defaultdict(lambda: defaultdict(int))  # 斜率 -> 截距 -> 个数
        cnt2 = defaultdict(lambda: defaultdict(int))  # 中点 -> 斜率 -> 个数
        for i, (x,y) in enumerate(points):
            for x2,y2 in points[:i]:
                k = (y2-y)/(x2-x) if x2!=x else inf
                # NOTE: 再通过 k 来计算 b, 居然会因为误差传递而 error!
                # b = y-k*x if k!=inf else x  # 在斜率都 inf 的时候, 通过 x 作为来区分
                b = (x2*y-x*y2) / (x2-x) if x2!=x else x
                cnt[k][b] += 1
                cnt2[(x+x2,y+y2)][k] += 1  # 技巧: 虽然是中点, 但可以通过统一 *2 避免浮点数!
        ans = 0
        for m in cnt.values():
            s = 0
            for c in m.values():
                ans += s * c
                s += c
        for m in cnt2.values():
            s = 0
            for c in m.values():
                ans -= s*c
                s += c
        return ans


sol = Solution()
result = [
    # sol.checkDivisibility(n = 23),
    sol.countTrapezoids(points = [[1,0],[2,0],[3,0],[2,2],[3,2]]),
    sol.countTrapezoids([[-99,-79],[30,-60],[-70,-60],[61,50]]),

    sol.countTrapezoids(points = [[-3,2],[3,0],[2,3],[3,2],[2,-3]]),
    sol.countTrapezoids([[-32,12],[-32,-94],[-32,-15],[-30,88]]),
]
for r in result:
    print(r)