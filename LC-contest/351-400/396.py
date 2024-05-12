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
https://leetcode.cn/contest/weekly-contest-396
T4 hard!!!

Easonsi @2023 """
class Solution:
    """ 3136. 有效单词 """
    def isValid(self, word: str) -> bool:
        if len(word) < 3: return False
        vowels = 'aeiou' + 'AEIOU'
        non_vowels = set(string.ascii_lowercase + string.ascii_uppercase) - set(vowels)
        valid_chars = set(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        if set(word) - valid_chars: return False
        if not set(word).intersection(vowels): return False
        if not set(word).intersection(non_vowels): return False
        return True
        
    """ 3137. K 周期字符串需要的最少操作次数 """
    def minimumOperationsToMakeKPeriodic(self, word: str, k: int) -> int:
        n = len(word)
        total = n // k
        cnt = Counter()
        for i in range(0,n,k):
            cnt[word[i:i+k]] += 1
        return total - max(cnt.values())
    
    """ 3138. 同位字符串连接的最小长度 """
    def minAnagramLength(self, s: str) -> int:
        n = len(s)
        for l in range(1,n+1):
            if n % l: continue
            target = sorted(s[:l])
            flag = True
            for i in range(l, n, l):
                if sorted(s[i:i+l]) != target: 
                    flag = False
                    break
            if flag: return l
    
    """ 3139. 使数组中所有元素相等的最小开销 #hard 对于一个数组, 要求用两个操作来使得所有数字都相同. 问最小开销.
操作1: 一个位置+1, 代价为 c1. 操作2: 选择两个位置+1, 代价为 c2
限制: n 1e6. 对于结果取模
思路0: 分类讨论
    容易想到, 1] 若n=2, 只能用操作1; 2] 若 c2 >= 2*c1, 则无脑都用操作1即可. 否则:
    考虑 [3,4,5] 的情况, 若 c1=100; c2=1. 最优情况是用3次操作2变为 [6,6,6]
        这个目标值怎么求? 假设执行次数为 x, 最后变为 mx+in. 记 d=mx-mn; gap=mx*n - sum(nums \ {mn}). 则需要满足:
            2x = gap + d + in*n     [可能还需要最多一次操作1]
            x >= d + in         [mn 比较小 (d比较大) 的情况] 
        可以解得, in >= (d-gap)/(n-2)
            [注意要满足 x, in 都是整数]
    接下来呢? 
思路1:
    接下来, 可以枚举所有可能的 in (目标值). 注意到, 根据上面可以计算目标值为 [mx, ... mx+in], 枚举每个目标值对应的开销即可! 
具体见 [ling](https://leetcode.cn/problems/minimum-cost-to-equalize-array/solutions/2766600/fen-lei-tao-lun-on-zuo-fa-pythonjavacgo-9bsb4/)

关联:
1753. 移除石子的最大得分 1488
1953. 你可以工作的最大周数 1804
    """
    def minCostToEqualizeArray(self, nums: List[int], cost1: int, cost2: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n==1: return 0
        mx, mn = max(nums), min(nums)
        d = mx - mn
        if n==2: return (d * cost1) % MOD
        gap = mx*(n-1) - (sum(nums)-mn)
        if cost2 >= 2*cost1: return ((gap+d) * cost1) % MOD
        # main
        min_possibel_in = max(0, ceil((d-gap)/(n-2))) + 1       # NOTE: 这里需要有余量! 
        def cacl(in_) -> int:
            ava = gap + (n-1)*in_
            d_mx = d + in_
            if ava >= d_mx:
                c2, c1 = divmod(ava+d_mx, 2)
            else:
                c2, c1 = ava, d_mx-ava
            return c2*cost2 + c1*cost1
        # ans = MOD     # NOTE: 智障了!
        ans = inf
        for in_ in range(min_possibel_in+1):
            ans = min(ans, cacl(in_))
        return ans % MOD


sol = Solution()
result = [
    # sol.isValid(word = "234Adas"),
    # sol.minimumOperationsToMakeKPeriodic(word = "leetcoleet", k = 2),
    # sol.minAnagramLength(s = "abba")
    sol.minCostToEqualizeArray(nums = [4,1], cost1 = 5, cost2 = 2),
    sol.minCostToEqualizeArray(nums = [2,3,3,3,5], cost1 = 2, cost2 = 1),
    sol.minCostToEqualizeArray(nums = [3,4,5], cost1 = 100, cost2 = 1),
    sol.minCostToEqualizeArray([3,5,3], 1, 3),
    sol.minCostToEqualizeArray([45,20,14,21,9], 68, 2),
    sol.minCostToEqualizeArray([60,19,53,31,57], 60, 2),
    sol.minCostToEqualizeArray([1000000,2,1,2,1000000], 10000, 4000),
]
for r in result:
    print(r)
