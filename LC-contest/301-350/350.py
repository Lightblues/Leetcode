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
https://leetcode.cn/contest/weekly-contest-350

难度太挺大的. T1就考了一个有意思的小学题目. T3是一道挺难的状压DP, 一开始就想骗了用图来做复杂度妥妥爆炸. T4也是一道比较难的DP题目, 灵神的转换为01背包简直神仙!
TODO: 灵神T3题解中整理了「状压 DP 题单」

Easonsi @2023 """
class Solution:
    """ 2739. 总行驶距离 #easy #数学 有主油箱和辅助邮箱, 每消耗5L可以补充1L, 问最后消耗的油量. 
思路1: #模拟
思路2: #数学
    不进行迭代模拟, 直接从原本的油量考虑可以多行驶的数量. 可知「花费4L可以多行驶1L油」; 
    但是, 注意剩余4的时候不能进行调换, 因此多行驶的油量为 (mainTank-1)//4
    [here](https://leetcode.cn/problems/total-distance-traveled/solution/yi-xing-jie-fa-shu-xue-by-newhar-ratb/)
    """
    def distanceTraveled(self, mainTank: int, additionalTank: int) -> int:
        return (mainTank + min(additionalTank, (mainTank-1)//4)) * 10
    def distanceTraveled(self, mainTank: int, additionalTank: int) -> int:
        ans = 0
        while mainTank>=5:
            a,b = divmod(mainTank, 5)
            ans += a*5
            c = min(additionalTank, a)
            additionalTank -= c
            mainTank = b+c
            if additionalTank==0: break
        ans += mainTank
        return ans * 10
    
    """ 2740. 找出分区值 """
    def findValueOfPartition(self, nums: List[int]) -> int:
        nums.sort()
        diff = [nums[i+1]-nums[i] for i in range(len(nums)-1)]
        return min(diff)
    
    """ 2741. 特别的排列 #medium #题型 但实际上 #hard 对于n个不同的数字, 求满足「相邻数字可以整除」条件的排列数量
限制: n 14, 对结果取模
思路1: #状压 #DP
    问题建模: 图上的所有哈密顿回路数量
    数量级分析: 但是极端情况下是全连通, 复杂度 o(n!) 
    如何解决? #记忆化搜索 接口 dfs(used, i) 表示已经用了used并且最后一个数字为i的方案数
        状态转移: = sum{ dfs(used\{j}}, j) }, 其中要求 j in used, 并且 j,i 以整除
        边界: used==0, 说明找到一个解, 返回 1
    复杂度: 状态个数 O(n2^n), 状态转移 O(n), 因此整体 O(n^2 * 2^n)
思路2:
    展开成for递推? 可能速度会变慢! (TLE边缘), 见灵神视频 https://www.bilibili.com/video/BV1Hj411D7Tr/
[灵神](https://leetcode.cn/problems/special-permutations/solution/zhuang-ya-dp-by-endlesscheng-4jkr/)
关联:「0996. 正方形数组的数目」 #hard 区别在于可重复了! 
    如何删除重复? 对于每个k的重复次数v, 对于ans/v! 即可~
    另外, 对于图上的建模问题, 参见官答!
    """
    def specialPerm(self, nums: List[int]) -> int:
        mod = 10**9+7
        n = len(nums)
        @lru_cache(None)
        def dfs(used:int, i:int):
            # used: 二进制表示的已经使用的数字
            if used==0: return 1
            ans = 0
            for j in range(n):
                if i==j: continue
                mask = 1<<j
                if (mask&used) and (nums[j]%nums[i]==0 or nums[i]%nums[j]==0):
                    ans += dfs(used^mask, j)
            return ans % mod
        return sum(dfs(((1<<n)-1)^(1<<i), i) for i in range(n)) % mod
    """ 0996. 正方形数组的数目 #hard n个数字可能重复, 求满足「相邻数字和为完全平方数」条件的不同序列数量
限制: N 12, 注意相同数字之间认为是一样的 (因此要去重)
    """
    def numSquarefulPerms(self, nums: List[int]) -> int:
        n = len(nums)
        @lru_cache(None)
        def dfs(used:int, i:int):
            if used==0: return 1
            ans = 0
            for j in range(n):
                mask = 1<<j
                if i==j: continue
                if not mask&used: continue
                if (nums[j]+nums[i])**0.5==int((nums[j]+nums[i])**0.5):
                    ans += dfs(used^mask, j)
            return ans
        ans = sum(dfs(((1<<n)-1)^(1<<i), i) for i in range(n))
        for k,v in Counter(nums).items():
            ans //= math.factorial(v)
        return ans


    """ 2742. 给墙壁刷油漆 #hard 有两种粉刷匠, 付费的在一定时间内有代价完成一堵墙 (cost, time), 免费的在1单位时间内完成任意一堵墙, 但是只能在付费的同时进行, 问最小总代价
限制: n 500; time 500
思路1: #选或不选
    记当前付费/免费时间和为 (x,y), 则整体需要满足 `x>=y`
    考虑最后一面墙x付费/免费? 若付费, 状态为 (cost[x], 0); 若免费则为 (0, 1)
    因此, 可以定义状态 f(i, x,y) 表示刷前i面墙, 状态为(x,y)的最小代价! (注意状态需要合法)
    这样状态太多! 优化为 f(i, z=x-y), 则递归终点约束 z>=0. 分类
        付费, 有 f(i-1, z+time[i]) + cost[i]
        免费, 有 f(i-1, z-1)
        答案取两者较小值
思路2: 问题 #转换, 转换成 #0-1 背包
    注意约束为 sum(time[_cost]) >= count(_free) = n - count(_cost), 也即
        sum(time[_cost]+1) >= n. 这样的情况下, 最小化 sum(cost[_cost])
    「至少装满」约束的01背包问题! (一般是「最多装」)
    思路: 依然是 #选或不选, 定义 f(i, x) 表示前i个物品, 体积至少为x的最小代价
        f(i, x) = min{ f(i-1,x), f(i-1,x-time[i]-1)+cost[i] }
        边界: f(-1, x) = inf if x>0 else 0
注意时间复杂度: 若没有加下面的剪枝优化, 则时间复杂度可能为 O(n * n^2) 因为z的范围可能到 n^2
    但实际上, 考虑实际z>n的情况下显然是有解的! 增加剪枝后, 复杂度 O(n^2)
见 [灵神](https://leetcode.cn/problems/painting-the-walls/solution/xuan-huo-bu-xuan-de-dian-xing-si-lu-by-e-ulcd/)
    """
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        @lru_cache(None)  # 记忆化搜索
        def dfs(i: int, z: int) -> int:
            # v1 原本这样, 居然会 MLE!
            # if i<0: return inf if z<0 else 0 # 因为要求最小值
            # v2 加了下面的剪枝 可以过
            if z > i: return 0  # 剩余的墙都可以免费刷
            if i < 0: return inf
            return min(dfs(i - 1, z + time[i]) + cost[i], dfs(i - 1, z - 1))
        return dfs(len(cost) - 1, 0)
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        """ 特殊的 01背包, 改成递推参见灵神 """
        @lru_cache(None)
        def dfs(i: int, x: int):
            # 同样需要加上剪枝优化
            # if i < 0: return inf if x > 0 else 0
            if x<=0: return 0
            if i<0: return inf
            return min(dfs(i - 1, x), dfs(i - 1, x - time[i] - 1) + cost[i])
        n = len(cost)
        return dfs(n - 1, n)
    
sol = Solution()
result = [
    # sol.distanceTraveled(mainTank = 5, additionalTank = 10),
    # sol.distanceTraveled(7,1),
    # sol.distanceTraveled(9,2),

    # sol.specialPerm(nums = [2,3,6]),
    # sol.specialPerm(nums = [1,4,3]),
    # sol.numSquarefulPerms([1,17,8]),
    # sol.numSquarefulPerms([2,2,2]),

    sol.paintWalls(cost = [1,2,3,2], time = [1,2,3,2]),
    sol.paintWalls(cost = [2,3,4,2], time = [1,1,1,1]),
    
]
for r in result:
    print(r)
