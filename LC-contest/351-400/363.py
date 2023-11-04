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
https://leetcode.cn/contest/weekly-contest-363
https://leetcode.cn/circle/discuss/SwCGEn/
T1、T2分别因为思路不清WA了一次, T4考数据, 有意思!!

Easonsi @2023 """
class Solution:
    """ 2859. 计算 K 置位下标对应元素的和 """
    def sumIndicesWithKSetBits(self, nums: List[int], k: int) -> int:
        ans = 0
        for i,x in enumerate(nums):
            if i.bit_count() == k:
                ans += x
        return ans

    """ 2860. 让所有学生保持开心的分组方法数 """
    def countWays(self, nums: List[int]) -> int:
        nums.sort()
        ans = 0; n = len(nums)
        if nums[0]>0: ans += 1
        for i,x in enumerate(nums):
            if (i+1)>x:
                if i==n-1 or nums[i+1]>(i+1): ans += 1
        return ans
    
    """ 2861. 最大合金数 #medium 有一组k个机器, 需要用n中金属 composition[j]来制造1个合金, 原本有stock库存,每种原料购买的话价格为cost, 只能选择其中一个机器生产, 问最多能得到多少合金
限制: n,k 100; budget 1e8. 
思路1: #二分 判断j机器是否可以生成x个合金
    注意 [l,r] 的设计
    """
    def maxNumberOfAlloys(self, n: int, k: int, budget: int, composition: List[List[int]], stock: List[int], cost: List[int]) -> int:
        def check(comp, x):
            # 检查在comp机器上, 是否可以生产x个合金
            left = budget
            for c,s,co in zip(comp, stock, cost):
                if c*x > s:
                    left -= (c*x-s)*co
                    if left<0: return False
            return True
        def mx(comp):
            # 二分检查comp机器最大可生产
            cost_single = sum([s*co for s,co in zip(comp,cost)])
            l = budget//cost_single
            r = (budget + sum([s*co for s,co in zip(stock,cost)]))//cost_single
            ans = l
            while l<=r:
                mid = (l+r)//2
                if check(comp, mid):
                    ans = mid
                    l = mid+1
                else:
                    r = mid-1
            return ans
        
        ans = 0
        for comp in composition:
            ans = max(ans, mx(comp))
        return ans
    
    """ 2862. 完全子集的最大元素和 #hard
对于一个数组, 定义「完全集」为其中每一对元素之积都是完全平方数. 例如 {1,4}, {2,8}, {1,4,9} *2
给定一个数组, 对于所有index为「完全集」的子集, 求其最大和! 
思路1: #数学
    观察在同一组的「完全集」数字有什么特点? 
        定义 core(n) 为 n 除去完全平方因子后的剩余结果. 
[灵神](https://leetcode.cn/problems/maximum-element-sum-of-a-complete-subset-of-indices/solutions/2446037/an-zhao-corei-fen-zu-pythonjavacgo-by-en-i6nu/)
    """   
    def maximumSum(self, nums: List[int]) -> int:
        def core(x):
            res = 1
            for i in range(2,math.isqrt(x)+1):      # math.isqrt 高级!
                if x%i==0:
                    cnt = 0
                    while x%i==0:
                        cnt += 1
                        x //= i
                    if cnt&1: res *= i
            if x>1: res *= x
            return res
        d = defaultdict(int)
        # NOTE: 下标从1开始!
        for i,x in enumerate(nums,1):
            d[core(i)] += x
        return max(d.values())  
    
    
sol = Solution()
result = [
    # sol.countWays(nums = [1,1]),
    # sol.countWays(nums = [6,0,3,3,6,7,2,7]),
    # sol.countWays([1,1,0,1]),
    # sol.maxNumberOfAlloys(n = 3, k = 2, budget = 15, composition = [[1,1,1],[1,1,10]], stock = [0,0,0], cost = [1,2,3]),
    # sol.maxNumberOfAlloys(n = 3, k = 2, budget = 15, composition = [[1,1,1],[1,1,10]], stock = [0,0,100], cost = [1,2,3]),
    sol.maximumSum(nums = [8,7,3,5,7,2,4,9]),
    sol.maximumSum(nums = [5,10,3,10,1,13,7,9,4]),
    
]
for r in result:
    print(r)
