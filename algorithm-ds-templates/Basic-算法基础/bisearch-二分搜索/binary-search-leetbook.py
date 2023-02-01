from easonsi import utils
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
[二分查找](https://leetcode.cn/leetbook/detail/binary-search/)

总结了三套模板, 三者之间的区别见 [分析](https://leetcode.cn/leetbook/read/binary-search/xewjg7/)
感觉没啥用? 感觉这里的模版并没啥啥实质的区分度, 更多的技巧上的炫技.
    选做了最后的一组难题, 发现利用我最常用的框架完全可以过.
    总结: 其实, **重要的是对于问题的理解**, 例如是「满足条件的最小idx」. 更多是要看问题的转化.
    又: 看看 bisect 的官方实现, 优雅至极.

背框架如下: 
        l,r = 0,len(nums)-1     # [l,r] 闭区间
        # 1) 手动实现逻辑;
        ans = 0
        while l<=r:
            m = (l+r)>>1
            # 下面的更新逻辑根据题意做修改.
            # 例如, 这里查找满足条件的最小idx
            if check(m): l = m+1
            else: r = m-1; ans = m
        return ans
        # 2) 很多时候, 直接调用 bisect_left/right;
        return bisect_left(nums,*,*)

= 难题
0287. 寻找重复数 #medium
    一个长 n+1 的数组仅包含 1...n. 其中只有一个元素有重复(两次或多次!). 要求不修改, 只能 O(1) 空间的条件下找到.
0004. 寻找两个正序数组的中位数 #hard 经典 #题型
    给定两个长分别为 m,n 的有序数组, 要求中位数. 限制复杂度 O(m+n)
    思路1: 对于转化的问题, 通过二分查找.
    思路2: 直接利用到中位数的性质. 也是 #二分
 0719. 找出第 K 小的数对距离 #hard #题型 #二分
    给定一个数组, 每个数对构成「绝对差值」. 问第k小的差值. 限制: 长度 n 1e4. 数字大小 C 1e6.  
    思路1: 排序 + #二分 查找
0410. 分割数组的最大值 #hard #题型.
    对于一个非负数组, 要求分割成m个非空连续子数组, 使得这些子数组的区间和最大值 最小. 限制: 数组长度 1E3; 数组元素 C 1e6; m 50



 """
class Solution:
    """ 0704. 二分查找 #easy 基本题型, 有序不重复数组中找目标值 """
    def search(self, nums: List[int], target: int) -> int:
        l,r = 0, len(nums)-1
        while l <= r:
            m = (l+r)//2
            if nums[m] == target: return m
            elif nums[m] < target: l = m+1
            else: r = m-1
        return -1
    
    
    
    
    """ 0287. 寻找重复数 #medium
一个长 n+1 的数组仅包含 1...n. 其中只有一个元素有重复(两次或多次!). 要求不修改, 只能 O(1) 空间的条件下找到.
限制: n <= 10^5
提示: 假设重复的元素是x, 则比x大的元素最多 n-x个, 因此 cnt(arr<=x) > x; 进一步, 有 cnt(arr<=x-1) < x-1.
    因此, 要找的是满足 `cnt(arr<=x) > x` 的最小元素
思路: 二分. 复杂度 O(n logn)
 """
    def findDuplicate(self, nums: List[int]) -> int:
        def f(x): return sum(1 for i in nums if i<=x) > x
        # 注意是到 [1,2,...n] 上搜索, 要返回的值, 而 bisect 返回的是 idx, 因此有一个差值.
        idx = bisect_left(range(1, len(nums)), 1, key=f)
        return idx+1
        l,r = 1,len(nums)-1
        ans = -1
        while l<=r:
            m = (l+r)>>1
            if f(m): r = m-1; ans = m
            else: l = m+1
        return ans
    
    """ 0004. 寻找两个正序数组的中位数 #hard 经典 #题型
给定两个长分别为 m,n 的有序数组, 要求中位数. 限制复杂度 O(m+n)
思路1: 对于转化的问题, 通过二分查找.
    提示: 转化问题为「求这样的两个有序数组中, 第k大的数值」.
    再转化, 考虑在 nums1[idx1:] 和 nums2[idx2:] 两个字数组上找第k大的数值.
    注意边界.
思路2: 直接利用到中位数的性质. 也是 #二分
    转化问题: 我们希望找到两个分割点 i,j. 将两个数组分成了两半. 我们希望前半部分的数量恰好是一半, 也即 `i+j+2 = (m+n+1)//2`
    并且希望, nums[i] <= nums[j+1] and nums[j] <= nums[i+1]. 也即这样的划分也是符合全局划分的.
    这样, 我们要求的中位数就由左半部分的最大值 (和右半部分的最小值) 决定.
    由于 i,j 之和固定了, 我们只需要在 nums1 上二分搜索i即可. 复杂度 O(m). 我们进一步可以通过调换两数组的形式将复杂度降低为 O(min(m,n)).
[官答](https://leetcode.cn/problems/median-of-two-sorted-arrays/solution/xun-zhao-liang-ge-you-xu-shu-zu-de-zhong-wei-s-114/)
总结: 这是第三次做这道题了, 从一开始完全不会, 到现在顺着思路可以较快写出来, 还算有点进步.
 """
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # 提示: 转化问题为「求这样的两个有序数组中, 第k大的数值」.
        def findKth(k: int) -> int:
            # 找到 nums1+nums2 中第k大的数字.
            idx1 = idx2 = 0
            while k:
                # 边界
                if idx1==m: return nums2[idx2+k-1]
                if idx2==n: return nums1[idx1+k-1]
                if k==1: return min(nums1[idx1], nums2[idx2])
                # 在 nums1,nums2 上各拓展 k//2
                # 注意, 要确保第k个数字不会被漏掉! 
                # 若采用 [idx1, idx+k//2] , 则不算 p1 长为 k//2. 可能会漏掉!!
                p1 = min(idx1 + k//2 - 1, m-1)
                p2 = min(idx2 + k//2 - 1, n-1)
                if nums1[p1] > nums2[p2]:
                    k -= (p2-idx2+1)
                    idx2 = p2+1
                else:
                    k -= (p1-idx1+1)
                    idx1 = p1+1
        m,n = len(nums1), len(nums2)
        total = m+n
        if total&1: return findKth(total//2+1)
        else: return (findKth(total//2+1) + findKth(total//2))/2

    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(nums1) > len(nums2):
            return self.findMedianSortedArrays(nums2, nums1)

        infinty = 2**40
        m, n = len(nums1), len(nums2)
        left, right = 0, m
        # median1：前一部分的最大值
        # median2：后一部分的最小值
        median1, median2 = 0, 0

        while left <= right:
            # 前一部分包含 nums1[0 .. i-1] 和 nums2[0 .. j-1]
            # // 后一部分包含 nums1[i .. m-1] 和 nums2[j .. n-1]
            i = (left + right) // 2
            j = (m + n + 1) // 2 - i

            # nums_im1, nums_i, nums_jm1, nums_j 分别表示 nums1[i-1], nums1[i], nums2[j-1], nums2[j]
            nums_im1 = (-infinty if i == 0 else nums1[i - 1])
            nums_i = (infinty if i == m else nums1[i])
            nums_jm1 = (-infinty if j == 0 else nums2[j - 1])
            nums_j = (infinty if j == n else nums2[j])

            if nums_im1 <= nums_j:
                median1, median2 = max(nums_im1, nums_jm1), min(nums_i, nums_j)
                left = i + 1
            else:
                right = i - 1

        return (median1 + median2) / 2 if (m + n) % 2 == 0 else median1

    """ 0719. 找出第 K 小的数对距离 #hard #题型 #二分
给定一个数组, 每个数对构成「绝对差值」. 问第k小的差值. 限制: 长度 n 1e4. 数字大小 C 1e6.  
思路1: 排序 + #二分 查找
    考虑问题「对于给定的d问差值小于d的数对有多少」, 可以通过排序+bisct解决. 每次检查的复杂度为 `O(n log(n))`.
    搜索空间为 [0,C]. 因此可以用二分来查找, 总体复杂度 `O(log(C) * n log(n))`.
    [上面的写法蠢了] 仔细思考, **本题所要求的就是一个 `bisect_left`. 因为本质上还是在数组上进行查找**.
    例如, 假设数组对的所有差值集合为 [1,1,3], 则查询 「小于等于d的差值有多少个」时, f(1/2) 都返回2, 但我们想要的是较小者1.
思路2: #双指针 优化
    在上述思路中, 计数函数的时间复杂度为 `O(n log(n))`. 
    而实际上, 基于边界的递增性质, 可以采用 #双指针 进行优化, 不算排序的时间复杂度 `O(n)`. 因此总时间复杂度 `O(n (logn+logC))`.
[official](https://leetcode.cn/problems/find-k-th-smallest-pair-distance/solution/zhao-chu-di-k-xiao-de-shu-dui-ju-chi-by-xwfgf/)
"""
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        # 思路1: 排序 + #二分 查找
        nums.sort()
        def f(diff) -> int:
            # 统计nums中差值 <=d 的组数, O(n log(n))
            cnt = 0
            for j,b in enumerate(nums):
                # 枚举右端点! 
                i = bisect_left(nums, b-diff, 0,j)
                cnt += j-i
            return cnt
        l,r = 0,nums[-1]-nums[0]
        return bisect_left(range(l,r+1), k, key=f)
        # 1) 直接调用 bisect_left; 2) 等价于下面的实现
        ans = 0
        while l<=r:
            m = (l+r)>>1
            cnt = f(m)
            if cnt<k: l = m+1
            else: r = m-1; ans = m
        return ans
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        # 思路2: #双指针 优化
        nums.sort()
        def f(diff) -> int:
            # 双指针统计差值 <=d 的组数, 复杂度 O(n)
            cnt = 0
            i = 0
            for j,b in enumerate(nums):
                while b-nums[i]>diff: i+=1
                cnt += j-i
            return cnt
        l,r = 0,nums[-1]-nums[0]
        return bisect_left(range(l,r+1), k, key=f)
    
    """ 0410. 分割数组的最大值 #hard #题型.
对于一个非负数组, 要求分割成m个非空连续子数组, 使得这些子数组的区间和最大值 最小. 限制: 数组长度 1E3; 数组元素 C 1e6; m 50
思路1: 二分.
    对于「检查数组是否可以分成成m个和小于x的子数组」这一问题, 可以通过 #贪心 在 O(n) 内得到.
    因此, 可以二分在 [min(nums), sum(nums)] 范围内查找. 复杂度约为 `O(n log(nC))`.
思路2: #DP 记 `f(i,j)` 表示前i个数字分成j个子数组的最大和最小值.
    则有递推公式 `f(i,j) = min{ max{ f(k,j-1), sum[k+1...j] }`
    复杂度: `O(n^2 m)`.
[官答](https://leetcode.cn/problems/split-array-largest-sum/solution/fen-ge-shu-zu-de-zui-da-zhi-by-leetcode-solution/)
总结: 乍一看题型和范围很像DP题, 但一开始考虑 f(l,r,m) 的形式感觉不可行, 果然DP还需要练习. (虽然复杂度比二分高了好多!!)
 """
    def splitArray(self, nums: List[int], m: int) -> int:
        # 思路1: 二分.
        def check(x):
            cnt = 0
            acc = 0
            for n in nums:
                # 特殊: 单个元素也比 limit 大.
                if n>x: return False
                if acc + n > x:
                    cnt += 1
                    if cnt >= m: return False
                    acc = n
                else: acc += n
            return True
        l,r = min(nums),sum(nums)
        ans = inf
        while l<=r:
            mid = (l+r)>>1
            if check(mid): ans = mid; r = mid-1
            else: l = mid+1
        return ans

    def splitArray(self, nums: List[int], m: int) -> int:
        # 思路2: #DP 记 `f(i,j)` 表示前i个数字分成j个子数组的最大和最小值.
        n = len(nums)
        f = [[10**18] * (m + 1) for _ in range(n + 1)]
        acc = list(accumulate(nums, initial=0))
        
        f[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, min(i, m) + 1):
                # 求最大值的最小值
                # 下面的官答 TLE 了... 下面利用单调性进行优化过了!
                # for k in range(i):
                #     f[i][j] = min(f[i][j], max(f[k][j - 1], acc[i] - acc[k]))
                for k in range(1, i + 1):
                    val = max(f[i - k][j - 1], acc[i] - acc[i - k])
                    if val <= f[i][j]: f[i][j] = val # 单调性
                    else: break
        return f[n][m]

    """ 0644. 子数组最大平均数 II #hard #题型
给定一个数组, 要求找到 「长度大于等于k的连续子数组的最大平均数」, 精确度 1e-5. 限制: n 1e4; 整数元素范围 +/- 1e4
思路1: #二分 查找该平均数.
    搜索范围 [mn,mx], 为了确保搜索精度, 也即从 1e4 到 1e-5. C=1e9. 因此复杂度: O(n logC)
    如何在 O(n) 时间check?
        提示: 要判断 nums[l,r] 平均值大于等于 x, 等价差值数组 a = nums-x 的 a[l,r] 的区间和非负.
        因此, 问题转化为「判断是否有长度至少为k的子数组, 其区间和非负」.
        采用 #前缀和. **为了找到非负区间, 可以记录「此前的前缀和的最小值」**!!! 注意在维护过程中保证数组长度k的限制.
    see [official](https://leetcode.cn/problems/maximum-average-subarray-ii/solution/zui-da-ping-jun-zi-duan-he-ii-by-leetcode/)
补充: 利用单调栈的 O(n) [解法](https://leetcode.cn/problems/maximum-average-subarray-ii/solution/fu-za-du-wei-onde-dan-diao-zhan-fa-by-li-trzz/)
"""
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        n = len(nums)
        def check(x):
            # 检查nums中是否存在长度至少k的平均值>=x的子数组
            arr = [a-x for a in nums]
            acc = sum(arr[:k])
            if acc>=0: return True
            accDiffK = 0    # 距离差 k 的前缀和
            accMin = 0      # 距离差 k 的前缀和的最小值
            for i in range(k,n):
                acc += arr[i]
                accDiffK += arr[i-k]
                accMin = min(accMin, accDiffK)
                if acc>=accMin: return True
            return False
        l,r = min(nums),max(nums)
        delta = 1e-5
        # 二分类型: 找到满足条件的最大值
        pre = l
        while r-pre>delta:      # 连续区间
            mid = (l+r)/2
            if check(mid): l = mid; pre = mid
            else: r = mid
        return pre
    
sol = Solution()
result = [
    # sol.findDuplicate(nums = [1,3,4,2,2]),
    # sol.findDuplicate(nums = [3,1,3,4,2]),
    # sol.findMedianSortedArrays(nums1 = [1,3], nums2 = [2]),
    # sol.findMedianSortedArrays([1,2],[3,4]),
    # sol.splitArray(nums = [7,2,5,10,8], m = 2),
    sol.findMaxAverage(nums = [1,12,-5,-6,50,3], k = 4),
]
for r in result:
    print(r)
