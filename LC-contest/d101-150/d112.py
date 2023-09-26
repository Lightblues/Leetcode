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
https://leetcode-cn.com/contest/biweekly-contest-112
https://leetcode.cn/circle/discuss/IFeyd7/
Easonsi @2023 """
class Solution:
    """ 7021. 判断通过操作能否让字符串相等 I #easy 限制只能位置 i,i+2 的两个元素交换
 """
    def canBeEqual(self, s1: str, s2: str) -> bool:
        return sorted(s1[::2])==sorted(s2[::2]) and sorted(s1[1::2])==sorted(s2[1::2])
    
    """ 7005. 判断通过操作能否让字符串相等 II
 """
    def checkStrings(self, s1: str, s2: str) -> bool:
        return sorted(s1[::2])==sorted(s2[::2]) and sorted(s1[1::2])==sorted(s2[1::2])
    
    """ 2841. 几乎唯一子数组的最大和 #medium 滑窗
 """
    def maxSum(self, nums: List[int], m: int, k: int) -> int:
        s = sum(nums[:k])
        cnt = Counter(nums[:k])
        ans = s if len(cnt)>=m else 0
        for i in range(k, len(nums)):
            cnt[nums[i]] += 1
            s += nums[i] - nums[i-k]
            cnt[nums[i-k]] -= 1
            if cnt[nums[i-k]]==0: del cnt[nums[i-k]]
            if len(cnt) >= m: ans = max(ans, s)
        return ans
    
    
    """ 8050. 统计一个字符串的 k 子序列美丽值最大的数目 #hard 在一个字符串中, 某一个字符的重复次数记作 f(x), 
对于一个长度为k的子序列, 要求其所有的字符都不同, 并且记其「美丽值」为包含的所有字符的 f(x) 之和. 问对于字符串的最大美丽值, 其可能的子序列数目有多少个.
限制: n 2e5
思路1: #贪心 计数
    对于字符串重复度统计, 排序. 注意到, 最迂最多的那些字符, 显然都是要用到的! 
    然后, 比如剩余的k=2, 但是重复度为4的字符有3个, 则可选的数量有 C(3, 2) * 4^2.
 """
    def countKSubsequencesWithMaxBeauty(self, s: str, k: int) -> int:
        mod = 10**9 + 7
        cnt = Counter(s)
        # 重复度为c的字母有多少个
        cnt2dup = Counter(cnt.values())
        cnt2dup = sorted(cnt2dup.items(), key=lambda x: x[0], reverse=True)
        ans = 1
        for c, dup in cnt2dup:
            if k<=0: break
            if k>=dup:
                ans *= pow(c, dup, mod)
                ans %= mod
                k -= dup
            else:
                ans *= math.comb(dup, k) * pow(c, k, mod)
                ans %= mod
                k = 0
        if k>0: return 0
        return ans
        
    
sol = Solution()
result = [
    sol.countKSubsequencesWithMaxBeauty(s = "bcca", k = 2),
    sol.countKSubsequencesWithMaxBeauty(s = "bcca", k = 4),
]
for r in result:
    print(r)
