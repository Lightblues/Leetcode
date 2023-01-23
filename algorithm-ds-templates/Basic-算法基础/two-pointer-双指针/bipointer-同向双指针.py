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
https://oi-wiki.org/misc/two-pointer/

灵神 [同向双指针](https://www.bilibili.com/video/BV1hd4y1r7Gq/)
== 同向双指针
下面是灵神的代码
    0209. 长度最小的子数组; 
    0713. 乘积小于 K 的子数组; 
    0003. 无重复字符的最长子串 #medium
等价转换 (取两端要求满足一定条件, 等价于中间的子数组满足一定条件)
    1658. 将 x 减到 0 的最小操作数 #medium
    6270. 每种字符至少取 K 个 #medium


Easonsi @2023 """
class Solution:
    """ 0209. 长度最小的子数组 #medium 正整数数组, 求和至少为s的最短子数组长度
关联: 「0862. 和至少为 K 的最短子数组」 #hard
思路1: #同向双指针. 
"""
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        ans = n + 1  # 也可以写 inf
        s = left = 0
        for right, x in enumerate(nums):
            s += x
            # 下面两种写法都可以
            # while s - nums[left] >= target:
            #     s -= nums[left]
            #     left += 1
            # if s >= target:
            #     ans = min(ans, right-left+1)
            while s >= target:  # 满足要求
                ans = min(ans, right - left + 1)
                s -= nums[left]
                left += 1
        return ans if ans <= n else 0

    """ 0713. 乘积小于 K 的子数组 #medium 都是正数的数组, 求连续子数组的乘积小于k的子数组数量 """
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0
        ans = left = 0
        prod = 1
        for right, x in enumerate(nums):
            prod *= x
            while prod >= k:  # 不满足要求
                prod /= nums[left]
                left += 1
            ans += right - left + 1
        return ans
    
    """ 0003. 无重复字符的最长子串 #medium #题型 给定一个字符串, 要求找到不包含重复字符的子串的最大长度
关联: 「0340. 至多包含 K 个不同字符的最长子串」 #medium
"""
    def lengthOfLongestSubstring(self, s: str) -> int:
        ans = left = 0
        cnt = Counter()
        for right, c in enumerate(s):
            cnt[c] += 1
            while cnt[c] > 1:  # 不满足要求
                cnt[s[left]] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans


    """ 1658. 将 x 减到 0 的最小操作数 #medium 给定一个整数x, 可以从数组两端选择数组, 求两端之和为x的最小数字数量.
思路1: 分别计算前缀后缀和, 用字典来记录 {presum: idx}, 进行匹配, 复杂度 O(n)
思路2: #逆向 等价转换
    可以等价转换为, 求和为 `sum-x` 的最长子数组
    可以 #同向双指针 复杂度 O(n)
"""
    def minOperations(self, nums: List[int], x: int) -> int:
        # 思路2: #逆向 等价转换
        target = sum(nums) - x
        if target < 0: return -1  # 全部移除也无法满足要求
        ans = -1
        left = s = 0
        for right, x in enumerate(nums):
            s += x
            while s > target:  # 缩小子数组长度
                s -= nums[left]
                left += 1
            if s == target:
                ans = max(ans, right - left + 1)
        return -1 if ans < 0 else len(nums) - ans
    
    """ 6270. 每种字符至少取 K 个 #medium #题型 字符串仅由 abc 三个字符构成, 要从首尾取一些字符, 每种至少k个, 问最小需要取多少个? 限制: 字符串长度 1e5; 0<=k<=len(s)
思路1: #同向双指针 复杂度 O(n)
    问题等价于, 要求最长的子数组, 使得其中包含的字符数量都不大于 cnt[ch]-k
"""
    def takeCharacters(self, s: str, k: int) -> int:
        c = Counter(s)
        for ch in 'abc':
            if c[ch]<k: return -1
            c[ch] -=k
        # 找到最长符合条件子数组
        ans = 0
        l = 0
        curr = Counter()
        for r,ch in enumerate(s):
            curr[ch] += 1
            while curr[ch] > c[ch]:
                curr[s[l]] -= 1
                l += 1
            ans = max(ans, r-l+1)
        return len(s)-ans

    
sol = Solution()
result = [
    sol.takeCharacters(s = "aabaaaacaabc", k = 2),
    sol.takeCharacters("a", 1),
]
for r in result:
    print(r)
