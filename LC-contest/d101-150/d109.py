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
https://leetcode-cn.com/contest/biweekly-contest-109
https://leetcode.cn/circle/discuss/STuFVw/
T3因为没有理解题意WA了2次, 思路还是不够清楚~  T4 也是经典的DP类型~

Easonsi @2023 """
class Solution:
    """ 2784. 检查数组是否是好的 """
    def isGood(self, nums: List[int]) -> bool:
        mx = max(nums)
        cnt = Counter(nums)
        for i in range(1, mx):
            if cnt[i]!=1: return False
        if cnt[mx]!=2: return False
        return len(nums)==mx+1
    
    """ 2785. 将字符串中的元音字母排序 """
    def sortVowels(self, s: str) -> str:
        s = list(s)
        idxs = []; vowels = []
        for i,x in enumerate(s):
            if x in 'aeiouAEIOU':
                idxs.append(i)
                vowels.append(x)
        vowels.sort()
        for i,v in zip(idxs, vowels):
            s[i] = v
        return ''.join(s)
    
    """ 2786. 访问数组中的位置使分数最大 #medium 
一开始在位置0, 可以访问右边的任意位置, 到达某位置得到arr[i] 分数, 但是如果跳跃前后位置的奇偶性不同需要损失 -x 分数. 问可以得到的最大分数
思路1: #DP
    记录至今到奇/偶位置可得的最大分数!
    注意限制(从idx=0开始)! 因此不能初始化 mxO, mxE 为 0! 
"""
    def maxScore(self, nums: List[int], x: int) -> int:
        # mxO, mxE = 0, 0
        # ans = 0
        # 注意! 必须从位置0开始!
        xx = nums[0]
        ans = xx
        if xx%2: mxO, mxE = xx, -inf
        else: mxO, mxE = -inf, xx
        for xx in nums[1:]:
            mx = max(
                mxO - (xx%2==0)*x, 
                mxE - (xx%2==1)*x
            ) + xx
            ans = max(ans, mx)
            if xx%2: mxO = max(mxO, mx)
            else: mxE = max(mxE, mx)
        return ans
    
    """ 2787. 将一个数字表示成幂的和的方案数 #medium 对于数字n, 将其分解为若干正整数x幂次 i^x 之和 
限制: n 300; x=[1,5], 对答案取模
思路1: #DP
    问题化简为, 从数组arr中选取不同的若干数字, 构成n的方案数
    记 f[i,x] 表示从arr[:i] 中构成数字x的方案数, 则有
        f[i,x] = f[i-1,x] + f[i-1, x-arr[i]] if arr[i] <=x
    边界: x==0; i==0
"""
    def numberOfWays(self, n: int, x: int) -> int:
        mod = 10**9+7
        s = []
        for i in range(1, n+1):
            if i**x > n: break
            s.append(i**x)
        @lru_cache(None)
        def f(i,x):
            # 注意边界
            if x==0: return 1
            if i==0: return x==1
            ans = f(i-1, x)
            if s[i]<=x:
                ans += f(i-1, x-s[i])
            return ans%mod
        return f(len(s)-1, n)
        
sol = Solution()
result = [
    # sol.maxScore(nums = [2,3,6,1,9,2], x = 5),
    # sol.maxScore(nums = [2,4,6,8], x = 3),
    # sol.maxScore([8,50,65,85,8,73,55,50,29,95,5,68,52,79],74),
    sol.numberOfWays(n = 10, x = 2),
    sol.numberOfWays(n = 4, x = 1),
]
for r in result:
    print(r)
