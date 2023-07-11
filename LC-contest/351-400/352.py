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
https://leetcode.cn/contest/weekly-contest-352
https://leetcode.cn/circle/discuss/501Jzp/
https://www.bilibili.com/video/BV1ej411m7zV/

T1 代码比较难写 (繁琐); T2因为质数计算写到里面TLE了一次; T3/4 都是子数组计数问题, 比较难!

Easonsi @2023 """
class Solution:
    """ 2760. 最长奇偶子数组 从数组中找到最长的 [o,e,o,e,...] 的并且都 <=th 的子数组长度 限制: N 100
思路1: #贪心 O(n) 
    下面的代码比较繁琐
    还可以采用指针的方案, 灵神叫做「分组循环」
    [灵神](https://leetcode.cn/problems/longest-even-odd-subarray-with-threshold/solution/on-fen-zu-xun-huan-by-endlesscheng-iu94/)
思路2: 直接 #暴力 尝试所有的左端点 O(n^2) 
    """
    def longestAlternatingSubarray(self, nums: List[int], threshold: int) -> int:
        ans = 0
        pre = -1; now = 0
        for i,x in enumerate(nums):
            if x<=threshold:
                if x%2==0:
                    if pre==1: now += 1; pre=x%2
                    else: pre=0; now=1
                else:
                    if pre==0: now += 1; pre=x%2
                    else: pre = -1; now = 0
                ans = max(ans, now)
            else:
                pre = -1; now = 0
        return ans
    def longestAlternatingSubarray(self, a: List[int], threshold: int) -> int:
        ans, i, n = 0, 0, len(a)
        while i < n:
            if a[i] % 2 or a[i] > threshold:
                i += 1
            else:
                i0 = i
                i += 1
                while i < n and a[i] <= threshold and a[i] % 2 != a[i - 1] % 2:
                    i += 1  # i 是全局变量，二重循环 i+=1 至多执行 O(n) 次
                ans = max(ans, i - i0)
        return ans


    """ 2761. 和等于目标值的质数对 #medium
思路1: 外部的 #质数筛
如何观察这个序列的趋势? 还介绍了 OEIS 这个网站
[灵神](https://leetcode.cn/problems/prime-pairs-with-target-sum/solution/yu-chu-li-zhi-shu-mei-ju-by-endlesscheng-cq9b/)
    """
    def findPrimePairs(self, n: int) -> List[List[int]]:
        # @lru_cache(None)
        # def isPrime(x):
        #     if x<2: return False
        #     for i in range(2, int(x**0.5)+1):
        #         if x%i==0: return False
        #     return True
        # primes = [i for i in range(2, n+1) if isPrime(i)]
        # primes = set(primes)
        # NOTE: 放到外面才通过
        ans = []
        for i in range(2, n//2+1):
            if i in primes and n-i in primes:
                ans.append([i, n-i])
        return ans
    
    """ 2762. 不间断子数组 #medium 找到所有子数组数量, 满足 [i,j] 范围内任意元素的差值不超过2. 
限制: n 1e5
思路1: #滑窗 + 记录窗口内元素
    注意到这里的差值不超过2! 因此窗口里的元素最多只有3个~ 考虑滑窗
关联: 更一般的情况, 「1438. 绝对差不超过限制的最长连续子数组」 (注意用了sortedlist) #平衡树
[灵神](https://leetcode.cn/problems/continuous-subarrays/solution/shuang-zhi-zhen-ping-heng-shu-ha-xi-biao-4frl/)
    """
    def continuousSubarrays(self, nums: List[int]) -> int:
        cnt = {}
        ans = 0; l = 0
        def check(c, x):
            vals = list(c.keys())+[x]
            mn,mx = min(vals), max(vals)
            return mx-mn <= 2
        for r,x in enumerate(nums):
            while not check(cnt, x):
                cnt[nums[l]] -= 1
                if cnt[nums[l]]==0: del cnt[nums[l]]
                l += 1
            cnt[x] = cnt.get(x, 0) + 1
            ans += r-l+1
        return ans
    
    
    """ 2763. 所有子数组中不平衡数字之和 #hard 计算所有子数组的「不平衡数字」之和. 定义不平衡数字为, sorted之后, 相邻之差 >1 的数量. 
限制: n 1e3; 数组元素范围 [1,n]
[灵神](https://leetcode.cn/problems/sum-of-imbalance-numbers-of-all-subarrays/solution/bao-li-mei-ju-pythonjavacgo-by-endlessch-2r7p/)
思路1: 枚举左端点, 记录范围内数据 复杂度 O(n^2)
    考虑从 l出发枚举右端点的情况, 记当前范围内的数字集合为set, 当前新加入的x: 1] 若在set中, 可知不平衡度不变; 2] 若不在, 则和x左右两边的数字相关, 根据>1的约束, 只需要看 x-1, x+1
思路2: #贡献法 复杂度 O(n)
    考虑x=nums[i]作为较小值 (数组里没有x+1) 产生贡献的次数: 也即包含x的并且没有x+1的子数组 [l,r] 的数量!
        为了避免相同元素「重复计数」, 我们规定最左边的那个x产生贡献
        因此, 对于x=nums[i], 我们需要找到i左侧的x+1, 以及i右侧的x或x+1
    注意到, 上面的讨论没有考虑x是子数组最大值的情况! 然而, 事实上我们在计数过程中已经考虑了所有x作为最大值的情况! 而所有的子数组只有一个最大值! 因此, 在整体上减去所有的子数组数量 n(n+1)/2
    那么, 如何找到「位置i左侧的x+1」? 
        我们可以顺序遍历, 用一个 #哈希表 记录每一个元素出现的位置
参见灵神视频. [here](https://leetcode.cn/problems/sum-of-imbalance-numbers-of-all-subarrays/solution/onde-by-dengyun-yyl3/) 更简洁
    """
    def sumImbalanceNumbers(self, nums: List[int]) -> int: 
        # 枚举左端点, 记录范围内数据 复杂度 O(n^2)
        ans = 0; n = len(nums)
        for l in range(n):
            t = 0; s = set()
            s.add(nums[l])
            for r in range(l+1, n):
                x = nums[r]
                if x not in s: 
                    # 注意, 这里包含了边界情况!
                    t += 1 - (x-1 in s) - (x+1 in s)
                ans += t
                s.add(x)
        return ans
    def sumImbalanceNumbers(self, nums: List[int]) -> int: 
        # 思路2: #贡献法 复杂度 O(n)
        n = len(nums)
        left = [-1] * n
        idx = defaultdict(lambda: -1)
        for i,x in enumerate(nums):
            left[i] = idx[x+1]
            idx[x] = i
        right = [n] * n
        idx = defaultdict(lambda: n)
        for j in range(n-1,-1,-1):
            x = nums[j]
            right[j] = min(idx[x+1], idx[x])
            idx[x] = j
        ans = 0
        for i,(l,r) in enumerate(zip(left, right)):
            ans += (i-l)*(r-i)
        return ans - n*(n+1)//2
            
    
# @lru_cache(None)
# def isPrime(x):
#     if x<2: return False
#     for i in range(2, int(x**0.5)+1):
#         if x%i==0: return False
#     return True
# primes = set([i for i in range(2, 1000000) if isPrime(i)])
    

    
sol = Solution()
result = [
    # sol.longestAlternatingSubarray(nums = [3,2,5,4], threshold = 5),
    # sol.longestAlternatingSubarray(nums = [1,2], threshold = 0),
    # sol.longestAlternatingSubarray(nums = [2,3,4,5], threshold = 4),
    # sol.longestAlternatingSubarray([4,10,3],10),
    # sol.findPrimePairs(10),
    # sol.findPrimePairs(2),
    # sol.findPrimePairs(999996),
    # sol.continuousSubarrays(nums = [5,4,2,4]),
    # sol.continuousSubarrays([1,2,3]),
    sol.sumImbalanceNumbers(nums = [1,3,3,3,5]),
    sol.sumImbalanceNumbers(nums = [2,3,1,4]),
]
for r in result:
    print(r)
