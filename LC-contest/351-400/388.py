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
https://leetcode.cn/contest/weekly-contest-388
https://leetcode.cn/circle/discuss/58wLhi/

被 T4 搞了一个多小时orz

Easonsi @2023 """
class Solution:
    """ 3074. 重新分装苹果 """
    def minimumBoxes(self, apple: List[int], capacity: List[int]) -> int:
        s = sum(apple)
        capacity.sort(reverse=True)
        ans = 0
        for i,x in enumerate(capacity):
            s -= x
            ans += 1
            if s<=0: break
        return ans
    
    """ 3075. 幸福值最大化的选择方案 """
    def maximumHappinessSum(self, happiness: List[int], k: int) -> int:
        happiness.sort(reverse=True)
        ans = 0; idx = 0
        for i,x in enumerate(happiness):
            a_ = x-idx
            if a_ <= 0: break
            ans += a_
            idx += 1
            if i >= k-1: break
        return ans
    
    """ 3076. 数组中的最短非公共子字符串 #medium #题型 对于一组字符串, 求出每一个字符串的一个最短子串, 要求它不是任意其他字符串的子串 (若有多个, 则求长度最短的)
限制: n 100; m=len(s) <= 20
思路1: #暴力
    对于所有的字符进行计数, 若当前字符串的某一子串计数=1, 则为答案!
    注意, 对于完整的cnt结果, 在检验当前字符串时, 需要「先删去再检查」, 因为字符串中满足要求的相同子串可能出现多次, 例如其他字符串中都没有出现则 zzzz
    复杂度: O(n * m^4)
    from [肖恩]
思路2: 更 #暴力 地check每个字符串, 复杂度 O(n^2 m*4)
from [ling](https://leetcode.cn/problems/shortest-uncommon-substring-in-an-array/solutions/2678694/bao-li-jian-ji-xie-fa-pythonjavacgo-by-e-tjlm/)
    """
    def shortestSubstrings(self, arr: List[str]) -> List[str]:
        cnt = Counter()
        for s in arr:
            for l in range(1,len(s)+1):
                for i in range(len(s)-l+1):
                    cnt[s[i:i+l]] += 1
        ans = []
        for s in arr:
            # remove s
            for l in range(1, len(s)+1):
                for i in range(len(s)-l+1):
                    cnt[s[i:i+l]] -= 1
            # check
            found = False
            found_s = ""
            for l in range(1, len(s)+1):
                for i in range(len(s)-l+1):
                    if cnt[s[i:i+l]] == 0:
                        found = True
                        if (not found_s) or (s[i:i+l] < found_s):
                            found_s = s[i:i+l]
                if found: break
            ans.append(found_s)
            # add s
            for l in range(1, len(s)+1):
                for i in range(len(s)-l+1):
                    cnt[s[i:i+l]] += 1
        return ans
    
    """ 3077. K 个不相交子数组的最大能量值 #hard #题型 可以在原本的arr中找到x个非空子串, 分数为 sum{ (-1)^(i+1) * sum[i] * (x-i-1)) | i=1...x }, 其中 sum[i] 为第i个子串的和. 要求最大值
限制: n 1e4; nk 1e6
思路1: #DP
    记 f[k_,i] 表示利用前i个分割为k段的最大值, 则有转移:
        f[k_,i] = max{
            f[k_,i-1],            # 不取第i个
            max{ f[k-1,j] + w * sum[j+1...i] | 枚举 }
        }
        其中 w = (-1)^(k_+1) * (k-k_+1) 
        sum[j+1...i] = acc[i+1]-acc[j]
    这样复杂度为 O(n^2k) 不太够! 
    对于 f[k_-1,j] + w * sum[j+1...i] = (f[k_-1,j] - w*acc[j]) + w*acc[i+1] 可以在计算的过程中维度前一部分的最大值, 这样复杂度变为 O(nk)
    边界: f[0,i] = 0 —— 不用选; f[i,i-1] = -inf 因为无法满足条件! 
NOTE: 注意需要考虑边界条件 (因此两个维度都需要加哨兵!!)
[ling](https://leetcode.cn/problems/maximum-strength-of-k-disjoint-subarrays/solutions/2678061/qian-zhui-he-hua-fen-xing-dpshi-zi-bian-ap5z5/)

题单：划分型 DP ①
将序列分成（恰好/至多）kkk 个连续区间，求解与这些区间有关的最优值。

410. 分割数组的最大值
813. 最大平均值和的分组 1937
1278. 分割回文串 III 1979
1335. 工作计划的最低难度 2035
2478. 完美分割的方案数 2344
2911. 得到 K 个半回文串的最少修改次数 2608

题单：划分型 DP ②
最小化/最大化分割出的区间个数等。

132. 分割回文串 II
2707. 字符串中的额外字符 1736
2767. 将字符串分割为最少的美丽子字符串 1865
1105. 填充书架 2014
2547. 拆分数组的最小代价 2020
2463. 最小移动总距离 2454
2977. 转换字符串的最小成本 II 2696
2052. 将句子分隔成行的最低成本（会员题）
    """
    def maximumStrength(self, nums: List[int], k: int) -> int:

        n = len(nums)
        acc = list(accumulate(nums, initial=0))
        f = [[0]*(n+1) for _ in range(k+1)]     # 都加了padding
        for k_ in range(1, k+1):
            f[k_][k_-1] = mx = -inf
            w = (-1) ** (k_+1) * (k-k_+1)
            # for i in range(k_-1, n):
            for i in range(k_, n-k+k_+1):
                mx = max(mx, f[k_-1][i-1] - w*acc[i-1])
                f[k_][i] = max(f[k_][i-1], mx+w*acc[i])
        return f[k][n]


sol = Solution()
result = [
    # sol.maximumHappinessSum(happiness = [1,2,3], k = 2),
    # sol.shortestSubstrings(arr = ["cab","ad","bad","c"]),
    # sol.maximumStrength(nums = [1,2,3,-1,2], k = 3),
    # sol.maximumStrength([12,-2,-2,-2,-2], 5),
    sol.maximumStrength([-1,-2,-3], 1),
]
for r in result:
    print(r)
