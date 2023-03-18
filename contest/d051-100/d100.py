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
https://leetcode.cn/contest/weekly-contest-d100
https://leetcode-cn.com/contest/biweekly-contest-81
Easonsi @2023 """
class Solution:
    """ 6323. 将钱分给最多的儿童 #easy WA了好多次 """
    def distMoney(self, money: int, children: int) -> int:
        if money<children or (children==1 and money==4): return -1
        ans = 0
        for x in range(1, min(ceil(money/8)+1, children+1)):
            m = money - x*8
            c = children - x
            if m<c: continue
            if c==1 and m==4: continue
            if c==0 and m>0: continue
            ans = x
        return ans
    
    """ 6324. 最大化数组的伟大值 """
    def maximizeGreatness(self, nums: List[int]) -> int:
        nums.sort()
        ans = 0
        # for i in range(1, len(nums)):
        #     ans += nums[i]>nums[i-1]
        n = len(nums)
        i = 0
        for j in range(1, n):
            if nums[j]>nums[i]:
                ans += 1
                i += 1
        return ans
    
    """ 6351. 标记所有元素后数组的分数 """
    def findScore(self, nums: List[int]) -> int:
        n = len(nums)
        arr = [(x,i) for i,x in enumerate(nums)]
        arr.sort()
        ans = 0
        for x,i in arr:
            if nums[i]==-1: continue
            ans += x
            for idx in range(i-1,i+2):
                if 0<=idx<n:
                    nums[idx] = -1
        return ans
        
    
    """ 6325. 修车的最少时间 #hard 能力为r的工人完成x个工作需要 r*x^2 时间, 给定一组工人和要完成的数量x, 问最少时间. 限制: 1<=ranks[i]<=10^5, 1<=cars<=10^6
思路1: #二分 给定一个时间, 可以在 O(n) 时间检查是否可行, 二分答案
    注意范围! 这里的最大应该在 1e6^2 * 100 数量级
     """
    def repairCars(self, ranks: List[int], cars: int) -> int:
        """ 尝试用堆来做, TLE """
        q = [(r, r, 1) for r in ranks]
        heapify(q)
        ans = 0
        for _ in range(cars):
            t, r, n = heappop(q)
            ans = t
            heappush(q, (r*(n+1)**2, r, n+1))
        return ans
    def repairCars(self, ranks: List[int], cars: int) -> int:
        cnt = Counter(ranks)
        def check(x):
            cc = 0
            for r,c in cnt.items():
                cc += floor((x/r)**0.5) * c
            return cc>=cars
        l,r = 0, 10**14
        ans = inf
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                r = mid-1
            else:
                l = mid+1
        return ans


sol = Solution()
result = [
    # sol.distMoney(20,3),
    # sol.distMoney(16,2),
    # sol.maximizeGreatness([1,3,5,2,1,3,1]),
    # sol.maximizeGreatness([1,2,3,4]),
    # sol.findScore([2,1,3,4,5,2]),
    # sol.findScore([2,3,5,1,3,2]),
    sol.repairCars(ranks = [4,2,3,1], cars = 10),
    sol.repairCars(ranks = [5,1,8], cars = 6),
]
for r in result:
    print(r)
