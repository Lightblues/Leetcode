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
https://leetcode-cn.com/contest/biweekly-contest-111
T4的数位DP有意思

Easonsi @2023 """
class Solution:
    """ 2824. 统计和小于目标的下标对数目 """
    def countPairs(self, nums: List[int], target: int) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            for j in range(i+1,n):
                if nums[i]+nums[j] < target: ans += 1
        return ans
    
    """ 2825. 循环增长使字符串子序列等于另一个字符串 #medium 对于字符串1, 可以选择一组下标, 将这些字符循环+1, 问能够使得字符串2是其子数组. 
思路1: #双指针
 """
    def canMakeSubsequence(self, str1: str, str2: str) -> bool:
        m,n  = len(str1), len(str2)
        idx = 0
        for i,x in enumerate(str1):
            ii = (ord(x)-ord('a')+1) % 26
            x2 = chr(ord('a')+ii)
            if x==str2[idx] or x2==str2[idx]:
                idx += 1
                if idx==n: return True
        return False
    
    """ 2826. 将三个组排序 #medium 问题等价于, 最少修改多少个元素, 使得数组为递增的
 """
    def minimumOperations(self, nums: List[int]) -> int:
        n = len(nums)
        @lru_cache(None)
        def f(i,x):
            if i<0: return 0
            ans = min(f(i-1, j) for j in range(x+1))
            ans += int(nums[i]!=x)
            return ans
        return min(f(n-1,x) for x in range(1,4))
    
    """ 2827. 范围中美丽整数的数目 #hard 对于一个数字, 若 1] 数位的奇数/偶数数量相同; 2] 可以被k 整除, 则称为美丽整数. 为 [low, high] 范围内的数量. 
思路1: #数位DP 
    对于约束1, 是经典数位DP的问题; 关键是约束2, **可以利用取模的性质**. 
    具体可以递归 f(i, diff, mod, isNum, isLimit)
见 [灵神](https://leetcode.cn/problems/number-of-beautiful-integers-in-the-range/solutions/2396206/shu-wei-dppythonjavacgo-by-endlesscheng-4gvw/)
 """
    def numberOfBeautifulIntegers(self, low: int, high: int, k: int) -> int:
        from functools import lru_cache
        def calc(x):
            s = list(map(int, str(x)))
            n = len(s)
            @lru_cache(None)
            def f(i, diff, mod, isNum, isLimit):
                # mod: 余数; diff: 差值even-odd; isNum: 是否已经是数字; isLimit: 是否受限制 
                if i==n: return int(isNum and diff==0 and mod==0)
                ans = 0
                # 非num (直至第i位)
                if not isNum:
                    ans += f(i+1, 0, 0, False, False)
                # 是num
                mn = 0 if isNum else 1
                mx = s[i] if isLimit else 9
                for ii in range(mn, mx+1):
                    ans += f(i+1, diff+(1 if (ii%2)==0 else -1), (mod*10+ii)%k, True, isLimit and ii==mx)
                return ans
            return f(0, 0, 0, False, True)
        return calc(high) - calc(low-1)
            
    
sol = Solution()
result = [
    # sol.canMakeSubsequence(str1 = "abc", str2 = "ad"),
    # sol.minimumOperations(nums = [2,1,3,2,1]),
    
    sol.numberOfBeautifulIntegers(low = 10, high = 20, k = 3),
    sol.numberOfBeautifulIntegers(low = 1, high = 10, k = 1),
]
for r in result:
    print(r)
