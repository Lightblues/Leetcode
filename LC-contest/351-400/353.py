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
https://leetcode.cn/contest/weekly-contest-353
https://leetcode.cn/circle/discuss/mmSJFF/
https://www.bilibili.com/video/BV1XW4y1f7Wv/

T3写的时候思维比较乱, 灵神用DP的思路就非常清楚! 另外转为子序列的题目太有意思了!

Easonsi @2023 """
class Solution:
    """ 2769. 找出最大的可达成数字 """
    
    """ 2770. 达到末尾下标所需的最大跳跃次数 #medium 两次可跳跃的限制是 (i<j, |nums[i]-nums[j]|<=target), 问从左跳到右的**最大**次数
思路1: #DP
    """
    def maximumJumps(self, nums: List[int], target: int) -> int:
        n = len(nums)
        f = [-1] * n
        f[0] = 0
        for i in range(n):
            if f[i]==-1: continue
            for j in range(i+1,n):
                if abs(nums[i]-nums[j])<=target: 
                    f[j] = max(f[j], f[i]+1)
        return f[-1]
    
    """ 2771. 构造最长非递减子数组 #medium 从nums1, nums2中对应的位置选择一个数字, 问可得到的最长的递增子数组(连续)的长度 
限制: n 1e5
思路0: #DP 很绕的写法 复杂度 O(n)
    预处理: 假设调整使得 nums1[i] <= nums2[j]
    记上一个位置的元素为 (px,py), 构成的最大序列为 (a,b), 对于当前为之的 x/y, 可知其可以根据与 px/py 的关系, 得到 a+1/b+1/1
    注意到: 上面的预处理是没有必要的!
拓展: 若要求是「非递减子序列」应该怎么做? 
    答案是将对于相应位置的元素降序排列, 拼接得到一个数组, 在其上寻找「最长递增子序列」! 复杂度 O(n logn)
        例如, 对于 1,3,2,1 和 2,2,3,4 两个数组, 拼接得到 2,1, 3,2, 3,2 4,1 (通过逆序保证了相应位置的元素不会被选两个!)
    注意, 若遇到 x,y 相等的情况, 则只加入一个到数组中即可!
见灵神视频. 
    """
    def maxNonDecreasingLength(self, nums1: List[int], nums2: List[int]) -> int:
        # 思路0: #DP 很绕的写法 复杂度 O(n)
        mix = list(map(sorted, zip(nums1, nums2)))
        ans = 1
        a,b = 1,1
        for i in range(1,len(nums1)):
            x,y = mix[i]
            px,py = mix[i-1]
            if x>=py: na = b+1
            elif x>=px: na = a+1
            else: na = 1
            if y>=py: nb = b+1
            elif y>=px: nb = a+1
            else: nb = 1
            ans = max(ans, na, nb)
            a,b = na,nb
        return ans
    def maxNonDecreasingLength(self, nums1: List[int], nums2: List[int]) -> int:
        # from 灵神
        nums = (nums1, nums2)
        @lru_cache(None)
        def dfs(i: int, j: int) -> int:
            if i == 0: return 1
            res = 1
            if nums1[i - 1] <= nums[j][i]:
                res = dfs(i - 1, 0) + 1
            if nums2[i - 1] <= nums[j][i]:
                res = max(res, dfs(i - 1, 1) + 1)
            return res
        return max(dfs(i, j) for j in range(2) for i in range(len(nums1)))


    """ 2772. 使数组中的所有元素都等于零 #medium 每次可以对长k的连续子数组-1, 问能否得到全0 
限制: n 1e5; x 1e6
思路1: #差分 + #贪心
    从左到右, 注意到我们在前面放置了之后要保证后面也是合法的!
    """
    def checkArray(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        acc = [0] * (n+1)
        for i,x in enumerate(nums):
            acc[i] += acc[i-1]
            if acc[i]>x: return False
            d = x - acc[i]
            if d>0:
                acc[i] += d
                if i+k>n: return False
                acc[i+k] -= d
        return True
    
    
sol = Solution()
result = [
    # sol.maximumJumps(nums = [1,3,6,4,1,2], target = 2),
    # sol.maximumJumps(nums = [1,3,6,4,1,2], target = 0),
    # sol.maxNonDecreasingLength(nums1 = [2,3,1], nums2 = [1,2,1]),
    # sol.maxNonDecreasingLength(nums1 = [1,3,2,1], nums2 = [2,2,3,4]),
    # sol.maxNonDecreasingLength(nums1 = [1,1], nums2 = [2,2]),
    # sol.maxNonDecreasingLength([4,2], [10,4]),
    sol.checkArray(nums = [2,2,3,1,1,0], k = 3),
    sol.checkArray(nums = [1,2,2], k = 3),
    sol.checkArray(nums = [1,3,1,1], k = 2),
]
for r in result:
    print(r)
