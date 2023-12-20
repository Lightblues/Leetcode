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
https://leetcode-cn.com/contest/biweekly-contest-116
https://leetcode.cn/circle/discuss/SwnhNk/

Easonsi @2023 """
class Solution:
    """ 2913. 子数组不同元素数目的平方和 I #easy 对于所有的子数组, 求不同元素的个数的平方和
 """
    def sumCounts(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            s = set()
            for j in range(i, n):
                s.add(nums[j])
                ans += len(s)**2
        return ans
    
    """ 2914. 使二进制字符串变美丽的最少修改次数
 """
    def minChanges(self, s: str) -> int:
        ans = 0
        for i in range(1, len(s), 2):
            if s[i]!=s[i-1]:
                ans += 1
        return ans
    
    
    """ 2915. 和为目标值的最长子序列的长度 #DP #题型 对于和为target的子序列, 求最大长度
限制: n 1e3; target 1e3
思路1
    定义 f[i][j] 表示前i个数字得到j的最大长度. 
    f[i][j] = max{f[i-1][j], f[i-1][j-nums[i]]+1}
 """
    def lengthOfLongestSubsequence(self, nums: List[int], target: int) -> int:
        n = len(nums)
        f = [-1] * (target+1)
        f[0] = 0
        for i in range(n):
            for j in range(target, nums[i]-1, -1):
                f[j] = max(f[j], -1 if f[j-nums[i]]==-1 else f[j-nums[i]]+1)
        return f[target]
 
    
    """ 2916. 子数组不同元素数目的平方和 II 同 2913 #hard TODO: 完成
限制: n 1e5; 对答案取模
[灵神](https://leetcode.cn/problems/subarrays-distinct-element-sum-of-squares-ii/solutions/2502897/yi-bu-bu-ti-shi-ni-si-kao-ben-ti-pythonj-zhhs/)
 """
    def sumCounts(self, nums: List[int]) -> int:
        pass
    
sol = Solution()
result = [
    # sol.sumCounts(nums = [1,2,1]),
    
    # sol.lengthOfLongestSubsequence(nums = [1,2,3,4,5], target = 9),
    sol.lengthOfLongestSubsequence(nums = [1,1,5,4,5], target = 3),
]
for r in result:
    print(r)
