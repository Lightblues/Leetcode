from itertools import pairwise
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
https://leetcode.cn/contest/weekly-contest-316
[灵神](https://www.bilibili.com/video/BV1ne4y1e7nu/)

T1 WA了一次, 完全失误. T3T4 两道hard. T3转换成了求凸函数最小值, 然后三分解决. T4是模模糊糊的贪心, 但写起来很快. 
然后看灵神的视频, 各种优化真的强! 

@2022 """
class Solution:
    """ 6214. 判断两个事件是否存在冲突 #easy 给定两个 hh:mm 表示的闭区间, 问两个区间是否存在交叉
灵神指出可以直接根据字符串大小比较. 
"""
    def haveConflict(self, event1: List[str], event2: List[str]) -> bool:
        return not (event1[0]>event2[1] or event2[0]>event1[1])
        def s2time(s):
            h,m = map(int, s.split(':'))
            return 60*h+m
        s1, s2 = s2time(event1[0]), s2time(event2[0])
        e1, e2 = s2time(event1[1]), s2time(event2[1])
        if s2>e1 or s1>e2: return False
        return True

    """ 6224. 最大公因数等于 K 的子数组数目 #medium 对于一个字符串, 统计其中子数组的数量, 满足其 gcd=k 限制: n 1e3
思路1: #暴力 枚举左端点, 匹配右端点
    直接双重循环即可. 通过 #前缀 来优化. 利用到了gcd递减的特性.
    复杂度: O(n^2 log(U)), 其中U是数字的max, 是计算gcd的复杂度. 
思路2: 利用 #GCD 的性质进行优化  #原地去重
    我们依次从 0,1,2,... 位置 **向前** 计算累计的gcd, 这样就可以利用到之前的信息
    如何对于信息进行压缩? 可能会有很多重复的数字, 我们用 (gcd, span) 来表示span内相同的元素. 
        由于gcd每次递减至少减少一半, 因此最多有 log(U) 个不同的gcd.
    递推: 对于当前新加入的首位元素x, 依次和上一轮的压缩记录 record 再取gcd. 
    复杂度: O(n log^2(U)), 这样对于 1e5 范围的数据也可以过了!
具体见 [灵神](https://leetcode.cn/problems/number-of-subarrays-with-gcd-equal-to-k/solution/by-endlesscheng-1f1r/)
更多利用到 #原地去重 的问题, 见 2411. 按位或最大的最小子数组长度 [灵神](https://leetcode.cn/problems/smallest-subarrays-with-maximum-bitwise-or/solution/by-endlesscheng-zai1/)
"""
    def subarrayGCD(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            # 通过 #前缀 来优化. 
            g = nums[i]
            for j in range(i, n):
                g = math.gcd(g, nums[j])
                if g==k: ans += 1
                elif g<k: break # 剪枝
        return ans
    def subarrayGCD(self, nums: List[int], k: int) -> int:
        # 思路2: 利用 #GCD 的性质进行优化  #原地去重
        ans = 0
        record = []  # 存储 [GCD，相同 GCD 区间的右端点]
        i0 = -1     # 来记录上一个不合法的位置, 类似哨兵? 
        for i, x in enumerate(nums):
            if x % k:  # 保证后续求的 GCD 都是 k 的倍数
                record = []
                i0 = i
                continue
            record.append([x, i])
            # 原地去重，因为相同的 GCD 都相邻在一起
            j = 0
            for p in record:
                p[0] = math.gcd(p[0], x)
                if record[j][0] != p[0]:
                    j += 1
                    record[j] = p
                else:
                    record[j][1] = p[1]
            del record[j + 1:]
            if record[0][0] == k:  # a[0][0] >= k
                ans += record[0][1] - i0
        return ans

    """ 6216. 使数组相等的最小开销 #hard 对于一个数组, 每次给一个元素 +-1, 需要有不同的开销. 问使得所有元素都相等的最小开销. 限制: n 1e5
思路1: #三分 搜索凸函数最小值
    计算目标值x的开销函数: `f(x) = sum{ |arr_i-x| * cost_i }`. 是一个 #凸函数. 
    如何求凸函数的最小值? 一种基本的方法是 #三分. 
        对于 [l,r] 区间, 分割为 [l, m1, m2, r]. 若 f(m1) < f(m2), 则答案一定是在 [l, m2] 中. 否则在 [m1, r] 中.
        细节: 注意这里的取值是离散空间, 需要进行 #边界 判断!
    复杂度: O(n log(U)), U 为数组元素的最大值.
    思路0: 一开始想错了, 直接将目标函数变为: `f(x) = sum{ (arr_i-x)^2  * cost_i}`. 两者的最优点显然不同! 
思路2: #中位数 #贪心 非常妙的 #转化 O(nlogn)
    考虑代价都相同的情况下最小化 (类似距离和): 结论是选择 #中位数 的开销最小.
        注意: 这里还有一个性知识, 距离和最小的问题, 一定可以取到数组原本的数字上 (也即, 不需要是严格的中位数定义).
    转化: 将这里的 cost 看成是数字的出现次数!!
思路3: 也用到「答案一定在出现过的元素中」的结论, 比较采用不同的目标值下的代价变化情况. 
    考虑从 nums[0] 变成 nums[1] 总开销的变化 (相邻的两个元素)
        目标值变化 d = nums[1] - nums[0]
        变少 (sum_cost - cost[0]) * d
        便多了 cost[0] * d
        因此整体变少 (sum_cost - 2*cost[0]) * d
见灵神视频. 
"""
    def minCost(self, nums: List[int], cost: List[int]) -> int:
        def c(x):
            return sum(abs(a-x) * c for a,c in zip(nums, cost))
        def f(l, r):
            """ 三分搜索凸函数最小值 """
            # 边界 判断!
            if r<=l+2: return min(c(x) for x in range(l, r+1))
            # 这里的取值必须是整数
            d = (r-l)//3
            m1, m2 = l+d, r-d
            c1, c2 = c(m1), c(m2)
            if c1<c2: return f(l, m2)
            else: return f(m1, r)
        l, r = min(nums), max(nums)
        return f(l, r)
    def minCost(self, nums: List[int], cost: List[int]) -> int:
        # 思路2: #中位数 #贪心 非常妙的 #转化 O(nlogn)
        a = sorted(zip(nums, cost))
        mid = sum(cost)//2
        s = 0
        for x,c in a:
            s += c
            if s>=mid:
                # 找到了中位数
                return sum(abs(x-y)*c for y,c in a)
    def minCost(self, nums: List[int], cost: List[int]) -> int:
        # 思路3: 也用到「答案一定在出现过的元素中」的结论, 比较采用不同的目标值下的代价变化情况. 
        a = sorted(zip(nums, cost))
        # 初始化: 全都变成最小的数字    
        ans = total = sum((x - a[0][0])*c for x,c in a)
        sum_cost = sum(cost)
        for (x0,c), (x1,_)  in pairwise(a): # pairwise: 枚举相邻的两个位置
            d = x1-x0
            sum_cost -= c * 2
            total -= d * sum_cost
            ans = min(ans, total)
        return ans
    
    """ 6217. 使数组相似的最少操作次数 #hard 给定两个数组 nums target, 每次可以将nums中 (i,j) 位置一个+2一个-2. 要求使得 multiset(nums)==multiset(target). 问最小操作次数. 限制: n 1e5
思路1: #贪心. 由于题目保证了答案存在, 我们可以直接根据排序的结果找到每个元素对应的目标值. 
    由于增减都是 2, 显然可以将两个数组根据 mod2 各自分成两组.
    分别对于两组排序, 根据贪心的思想匹配每个元素的目标值. 答案就是进行 增/减 的操作数. 
    灵神的说明: 先从 +/-1 的简单情况考虑. 并且指出, 这里用到的贪心思想叫做 #邻项交换. 
[灵神](https://leetcode.cn/problems/minimum-number-of-operations-to-make-arrays-similar/solution/by-endlesscheng-lusx/)
"""
    def makeSimilar(self, nums: List[int], target: List[int]) -> int:
        def split(nums):
            sodd, seven = [], []
            for a in nums:
                if a%2==0: seven.append(a)
                else: sodd.append(a)
        sodd, seven = split(nums)
        todd, teven = split(target)
        # 排序
        sodd.sort(); seven.sort(); todd.sort(); teven.sort()
        # 统计操作数
        cntAdd = 0
        for s,t in zip(sodd, todd):
            if s<t: cntAdd += (t-s)//2
        for s,t in zip(seven, teven):
            if s<t: cntAdd += (t-s)//2
        return cntAdd
    def makeSimilar(self, nums: List[int], target: List[int]) -> int:
        # 灵神的优雅写法. 不需要讨论奇偶性. 
        nums.sort()
        target.sort()
        ans, j = 0, [0, 0]  # 用数组表示两个下标，这样不用讨论奇偶性
        for x in nums:
            p = x % 2   # 元素的奇偶性.
            while target[j[p]] % 2 != p:  # 找 target 中奇偶性相同的元素
                j[p] += 1
            ans += abs(x - target[j[p]])
            j[p] += 1
        return ans // 4


sol = Solution()
result = [
    # sol.haveConflict(event1 = ["01:00","02:00"], event2 = ["01:20","03:00"]),
    # sol.haveConflict(event1 = ["01:15","02:00"], event2 = ["02:00","03:00"]),
    # sol.haveConflict(event1 = ["10:00","11:00"], event2 = ["14:00","15:00"]),
    # sol.haveConflict(["01:15","02:00"], ["02:00","03:00"]), 
    # sol.subarrayGCD(nums = [9,3,1,2,6,3], k = 3),
    # sol.subarrayGCD([1,2,3], 1),
    # sol.subarrayGCD(nums = [4], k = 7),
    # sol.minCost(nums = [1,3,5,2], cost = [2,3,1,14]),
    # sol.minCost(nums = [2,2,2,2,2], cost = [4,2,8,1,3]),
    # sol.minCost([735103,366367,132236,133334,808160,113001,49051,735598,686615,665317,999793,426087,587000,649989,509946,743518], [724182,447415,723725,902336,600863,287644,13836,665183,448859,917248,397790,898215,790754,320604,468575,825614])
    sol.makeSimilar(nums = [8,12,6], target = [2,14,10]),
    sol.makeSimilar(nums = [1,2,5], target = [4,1,3]),
    sol.makeSimilar(nums = [1,1,1,1,1], target = [1,1,1,1,1]),
]
for r in result:
    print(r)
