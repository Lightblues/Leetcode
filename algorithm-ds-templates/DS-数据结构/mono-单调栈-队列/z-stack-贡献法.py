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

== 贡献法 todo
0907. 子数组的最小值之和 #medium #题型 #单调栈
    求所有子数组的最小值的和
1856. 子数组最小乘积的最大值 #medium 
    定义一个子数组的score: 为 **数组元素和 * 最小元素**. 现给定一个数组, 要求返回最大的score.
    思路1: #单调栈 #前缀和 类似 0907 寻找左右边界; 子数组和可以通过前缀和求得.
    代码: 可以将寻找左右边界合并到一个单调栈上, 但注意一个是开一个是闭区间.
2104. 子数组范围和 #medium
    定义子数组的score为 **最大最小元素的差值**. 要求返回一个数组中所有子数组score和.
2281. 巫师的总力量和 #hard #单调栈 #前缀和 #题型
    对一个子数组, 定义score为 **最小元素 * 子数组元素和**, 现给定一个数组求所有子数组的score之和.

Easonsi @2023 """
class Solution:


    """ 0907. 子数组的最小值之和 #medium #题型 #单调栈
对于一个数组的所有(连续)子数组定义一个分数: 为这一子数组中的最小元素的值. 要求返回该数组所有子数组的分数之和.
思路1: #单调栈 记录每一个元素作为最小值的(左右)边界.
    考虑一个元素可以作为哪些子数组的最小值? [-100, 2,3,0,1, -100] 为例, 中间0作为子数组最小值的情况被两侧比0小的元素所确定.
    因此, 可以记录每一个元素的左右边界 (左右比该元素小的下一个位置), 经典的单调栈问题.
    注意, 需要考虑重复数值的问题, 例如 [1,3,1,2] 中, 可以将第一个1负责 [1,3,1,2] 这里范围, 而第二个1负责 [3,1,2] 范围. 也即, 右侧边界是严格小, 左侧边界是小于等于.
    具体计算最小值所出现的子数组数量, 假设idx位置元素的左右边界分别为l,r, 则有 `(idx-l) * (r-idx)` 个子数组. 例如 [1,2,0,1] 中的0作为子数组最小值的情况就有 3*2=6 种.
    因此答案就是 sum(arr[idx] * (idx-l) * (r-idx)) 对于每一个idx遍历求和.
思路2: #DP #单调栈
    相较于上面考虑每一个元素在哪些部分作为最小值, 这里考虑从左到右, 每一个增加的元素所增加的子数组. 对于增加的第j个元素, 遍历所有 [i,j] 区间, 这些区间的最小值有什么规律?
    例如, 对于数组 `A = [1,7,5,2,4,3,9]` 考虑元素 9 (j=6) 所新增的子数组, 这些数组的最小值分别为 `B = [1,2,2,2,3,3,9]`.
    有什么规律? 递增! 可以用递增栈的形式存储 (val, count) 元素, 例如 `(1,1), (2,3), (3,2)`. 每次更新时时, 尝试压入 (arr[j], 1).
    为了得到栈内信息 (数组B的和), 可以维护一个变量 `dot = sum(val*count)`.
[here](https://leetcode.cn/problems/sum-of-subarray-minimums/solution/zi-shu-zu-de-zui-xiao-zhi-zhi-he-by-leetcode/)
"""
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(arr)
        # 记录下一个比 idx 小 (严格小) 的元素的 idx
        right = [n] * n
        s = []
        for i in range(n-1, -1, -1):
            while s and s[-1][0] >= arr[i]:
                s.pop()
            right[i] = s[-1][1] if s else n
            s.append((arr[i], i))
        # 记录上一个比 idx 小 (小于等于) 的元素的 idx
        left = [-1] * n
        s = []
        for i in range(n):
            while s and s[-1][0] > arr[i]:
                s.pop()
            left[i] = s[-1][1] if s else -1
            s.append((arr[i], i))
        
        ans = 0
        for i in range(n):
            # 注意, 这个元素所在的子数组数量为 (idx-l) * (r-idx)
            ans += (arr[i] * (i - left[i]) * (right[i] - i)) % MOD
            ans %= MOD
        return ans

    def sumSubarrayMins(self, arr: List[int]) -> int:
    # https://leetcode.cn/problems/sum-of-subarray-minimums/solution/zi-shu-zu-de-zui-xiao-zhi-zhi-he-by-leetcode/
        MOD = 10**9 + 7
        n = len(arr)
        
        stack = []
        ans = dot = 0
        for i,num in enumerate(arr):
            count = 1
            while stack and num < stack[-1][0]:
                v, c = stack.pop()
                dot -= v*c
                count += c
            stack.append((num, count))
            dot += num*count
            dot %= MOD
            ans += dot
        return ans % MOD


    """ 1856. 子数组最小乘积的最大值 #medium 
定义一个子数组的score: 为数组元素和 * 最小元素. 现给定一个数组, 要求返回最大的score.
思路1: #单调栈 #前缀和 类似 0907 寻找左右边界; 子数组和可以通过前缀和求得.
    通过单调栈来计算每一个元素作为最小值的左右边界
思路2: 在代码层面, 除了用两次单调栈来得到所有边界, 实际上只需要一个单调栈即可同时求出
    具体来说, 若在遍历位置i的过程中, 假如遵循的是 `nums[s[-1]] >= nums[i]`, 则对于每一个栈顶元素来说, 其下一个更小元素为位置i; 而对于while循环后将i入栈, 则此时的栈顶元素 j 是左侧第一个满足大于等于 nums[i] 的元素.
    注意, 这里求的 right是严格小于 nums[i] 的元素位置, 而left则是小于等于 nums[i] 的元素位置. 但 **这不影响结果, 因为左右边界中总有一个得到了最长的数组**.
关联: 「2281. 巫师的总力量和」

输入：nums = [1,2,3,2]
输出：14
解释：最小乘积的最大值由子数组 [2,3,2] （最小值是 2）得到。
2 * (2+3+2) = 2 * 7 = 14 。
"""
    def maxSumMinProduct(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # 记录下一个比 idx 小 (严格小) 的元素的 idx
        right = [n] * n
        s = []
        for i in range(n-1, -1, -1):
            while s and s[-1][0] >= nums[i]:
                s.pop()
            right[i] = s[-1][1] if s else n
            s.append((nums[i], i))
        # 记录上一个比 idx 小 (严格小) 的元素的 idx
        left = [-1] * n
        s = []
        for i in range(n):
            while s and s[-1][0] >= nums[i]:
                s.pop()
            left[i] = s[-1][1] if s else -1
            s.append((nums[i], i))
        
        cumsum = list(itertools.accumulate(nums, initial=0))
        ans = 0
        for a,l,r in zip(nums, left, right):
            ans = max(ans, a * (cumsum[r] - cumsum[l+1]))
        return ans%MOD
    
    def maxSumMinProduct(self, nums: List[int]) -> int:
        n = len(nums)
        left = [0]*n; right = [n-1]*n
        s = []
        for i, num in enumerate(nums):
            # 注意下面的 right, left 都不包含边界点
            while s and nums[s[-1]] >= num:
                j = s.pop()
                right[j] = i-1   # nums[j] < nums[j+1,...,i-1]
            if s:
                left[i] = s[-1] + 1  # nums[i] >= nums[s[-1]+1,...,i-1]
            s.append(i)
        acc = list(accumulate(nums, initial=0))
        return max(v * (acc[r+1]-acc[l]) for v,l,r in zip(nums, left, right)) % (10**9 + 7)
    
    """ 2104. 子数组范围和 #medium  定义子数组的score为 **最大最小元素的差值**. 要求返回一个数组中所有子数组score和.
限制: `n <= 1000` 因此可以暴力求解, 进阶的要求是 O(n) 的实现.
思路1: #单调栈 记录每一个元素作为最大/最小值的次数 (计算左右边界).
    整体的分数为 `sum(max(i:j) - min(i:j)) = sum(max(i:j)) - sum(min(i:j))` 这里的最大最小是针对子数组 arr[i:j] 的.
    因此, 可以将原问题, 分解为求每一个元素作为最大/最小的次数, 求和相减即可.
    如何计算idx位置的元素在多少子数组中为最小元素? 类似0907, 维护左右两个边界即可. 注意出现的子数组数量是 `(idx-l) * (r-idx)` 乘法交互.
    see [here](https://leetcode.cn/problems/sum-of-subarray-ranges/solution/zi-shu-zu-fan-wei-he-by-leetcode-solutio-lamr/)
"""
    def subArrayRanges(self, nums: List[int]) -> int:
        def tmp(nums):
            n = len(nums)
            # 记录下一个比 idx 小 (严格小) 的元素的 idx
            right = [n] * n
            s = []
            for i in range(n-1, -1, -1):
                while s and s[-1][0] >= nums[i]:
                    s.pop()
                right[i] = s[-1][1] if s else n
                s.append((nums[i], i))
            # 记录上一个比 idx 小 (小于等于) 的元素的 idx
            left = [-1] * n
            s = []
            for i in range(n):
                while s and s[-1][0] > nums[i]:
                    s.pop()
                left[i] = s[-1][1] if s else -1
                s.append((nums[i], i))
                
            # cumsum = list(itertools.accumulate(nums, initial=0))
            ans = 0
            for idx, (val,l,r) in enumerate(zip(nums, left, right)):
                # 注意, 这个元素所在的子数组数量为 (idx-l) * (r-idx)
                ans += val * (r - idx)*(idx - l)
            return ans
            
        return  -tmp([-x for x in nums]) - tmp(nums)

    """ 2281. 巫师的总力量和 #hard #单调栈
对一个子数组, 定义score为 **最小元素 * 子数组元素和**, 现给定一个数组求所有子数组的score之和.
    结合了 0907 和 1856
    复杂度: 长度 1e5, 每个元素 1e9
思路1: #单调栈 #前缀和
    考虑「一个元素在哪些子数组作为最小值」? 类似 0907, 利用单调栈求左右的边界.
    这些子数组的和如何计算? 参见下面的公式分析, 通过「前缀和的前缀和」.
    另外注意 cumsum的使用: 为了得到 arr[l:r] 的和, 可以使用 cumsum[r+1] - cumsum[l]
        例如, 对于数组 [1,2,3], 通过 `itertools.accumulate(arr, initial=0))` 得到前缀和 [0,1,3,6], 则 arr[0:2] = cumsum[3] - cumsum[0] = 6
总结: 利用数学公式进行严谨的推导 (和思维方式).
from [here](https://leetcode.cn/problems/sum-of-total-strength-of-wizards/solution/dan-diao-zhan-qian-zhui-he-de-qian-zhui-d9nki/)

设子数组右端点为 $r$, 左端点为 $l$, 当前枚举的元素下标为 $i$, 那么有 $l \leq i \leq r$ 。 设 strength 数组的前缀和为 $s$, 在范围 $[L, R]$ 内的所有子数组的元素和的和为
$$
\begin{aligned}
& \sum_{r=i+1}^{R+1} \sum_{l=L}^{i} s[r]-s[l] \\
=& \sum_{r=i+1}^{R+1}\left((i-L+1) \cdot s[r]-\sum_{l=L}^{i} s[l]\right) \\
=&(i-L+1) \cdot \sum_{r=i+1}^{R+1} s[r]-(R-i+1) \cdot \sum_{l=L}^{i} s[l]
\end{aligned}
$$
因此我们还需要计算出前缀和 $s$ 的前缀和 $s s$, 上式即为
$$
(i-L+1) \cdot(s s[R+2]-s s[i+1])-(R-i+1) \cdot(s s[i+1]-s s[L])
$$
累加所有贡献即为答案。
"""
    def totalStrength(self, strength: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(strength)
        
        # 求左右边界, 注意这里的边界都是开区间
        right  = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and stack[-1][0] >= strength[i]:
                stack.pop()
            right[i] = stack[-1][1] if stack else n
            stack.append((strength[i], i))
        left = [-1] * n
        stack = []
        for i in range(n):
            while stack and stack[-1][0] > strength[i]:
                stack.pop()
            left[i] = stack[-1][1] if stack else -1
            stack.append((strength[i], i))
        
        # len(s) == n+1; len(ss) == n+2
        s = list(itertools.accumulate(strength, initial=0))
        ss = list(itertools.accumulate(s, initial=0))
        ans = 0
        for idx, (val,l,r) in enumerate(zip(strength, left, right)):
            l,r = l+1, r-1
            ans += val * ((idx-l+1)*(ss[r+2] - ss[idx+1]) -  (r-idx+1)*(ss[idx+1] - ss[l]))
        return ans % MOD


    
    
    
    
    
    

    
sol = Solution()
result = [
    # sol.sumSubarrayMins(arr = [3,1,2,4]),
    # sol.sumSubarrayMins(arr = [11,81,94,43,3]),
    
    sol.maxSumMinProduct(nums = [1,2,3,2]),
    sol.maxSumMinProduct(nums = [2,3,3,1,2]),
    
    # sol.subArrayRanges(nums = [1,2,3]),
    # sol.subArrayRanges(nums = [1,3,3]),
    # sol.subArrayRanges(nums = [4,-2,-3,4,1]),
    
    # sol.totalStrength(strength = [1,3,1,2]),
    # sol.totalStrength(strength = [5,4,6]),
]
for r in result:
    print(r)
