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
https://leetcode.cn/contest/weekly-contest-376
https://leetcode.cn/circle/discuss/BYHexE/
Easonsi @2023 """


# 生成所有的 回文数
palindrome = []
for i in range(1, 10**5 + 1):
    palindrome.append(int(str(i) + str(i)[::-1]))
    palindrome.append(int(str(i) + str(i)[::-1][1:]))
palindrome.sort()

class Solution:
    """  """
    def findMissingAndRepeatedValues(self, grid: List[List[int]]) -> List[int]:
        n = len(grid)
        vis = [0] * (n**2+1)
        for i,row in enumerate(grid):
            for j,x in enumerate(row):
                vis[x] += 1
        ans = [0] * 2
        for i,x in enumerate(vis):
            if x==0: ans[1] = i
            if x>1: ans[0] = i
        return ans
    
    """ 2966. 划分数组并满足最大差限制 """
    def divideArray(self, nums: List[int], k: int) -> List[List[int]]:
        n = len(nums)
        nums.sort()
        ans = []
        for i in range(1,n):
            if i%3 == 2:
                if nums[i]-nums[i-2] > k: return []
                ans.append(nums[i-2:i+1])
        return ans
    
    """ 2967. 使数组成为等数数组的最小代价 #将所有的数字都变成一个回文数, 代价为差值之和, 问最小代价.
思路1: 找到「中位数」「最接近」的数字
    细节: 「最接近」只是抽象的描述. 注意到, 「代价最小在中位数」这样的结果, 并不能拓展为「最接近中位数的那个可选项」
    例如, [109,113,115,122,128] 中, 距离中位数最近的两个点是 111, 121 —— 但其实121的代价 34 小于111的代价 36
        这是因为选在115的时候有最小值28. 把点往右移动到 121, 左右各两个数字增减抵消, 151的代价 +6
        而往左移动到111, 会经过113, 以你增加的代价是 +2 + 2*3 = 8, 因为过了点113之后左右无法抵消了!
    因此, 需要从两遍的数字都检查一下!
    参见 [灵神](https://leetcode.cn/problems/minimum-cost-to-make-array-equalindromic/solutions/2569308/yu-chu-li-hui-wen-shu-zhong-wei-shu-tan-7j0zy/)

这题是 564. 寻找最近的回文数，注意数据范围。
中位数贪心题单（右边数字为难度分）
462. 最小操作次数使数组元素相等 II
2033. 获取单值网格的最小操作数 1672
2448. 使数组相等的最小开销 2005
2607. 使子数组元素和相等 2071
1703. 得到连续 K 个 1 的最少相邻交换次数 2467
    """
    def minimumCost(self, nums: List[int]) -> int:
        # WA: 不能找「最接近」的那个数字! 
        nums.sort()
        n = len(nums)
        if n%2 == 1:
            mid = nums[n//2]
        else:
            mid = (nums[n//2-1]+nums[n//2]) / 2
        # 找到相较于mid最接近的回文数
        idx_mn = idx = bisect_left(palindrome, mid)
        mm = palindrome[idx] - mid
        if idx > 0 and abs(palindrome[idx-1] - mid) < mm:
            idx_mn = idx-1
        if idx < len(palindrome)-1 and abs(palindrome[idx+1] - mid) < mm:
            idx_mn = idx+1
        return sum(abs(x-palindrome[idx_mn]) for x in nums)
    def minimumCost(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)
        mid_l = (n-1)//2
        idx_r = bisect_left(palindrome, nums[mid_l])
        if palindrome[idx_r] <= nums[n//2]:
            return sum(abs(x-palindrome[idx_r]) for x in nums)
        return min(
            sum(abs(x-palindrome[idx_r-1]) for x in nums),
            sum(abs(x-palindrome[idx_r]) for x in nums),
        )

    """ 2968. 执行操作使频率分数最大 #hard #题型 在操作限制k的基础上, 使得数组中众数的频率最大
限制: n 1e5; m 1e9; k 1e14
思路1: 排序 + #滑动窗口
    1. 对于排序好的 [i:j] 我们可以计算出代价; 2. 根据限制k移动滑窗.
    对于 i:j 我们可以计算 #中位数 mid, 代价为两部分之和! (见下)
[lingshen](https://leetcode.cn/problems/apply-operations-to-maximize-frequency-score/solutions/2569301/hua-dong-chuang-kou-zhong-wei-shu-tan-xi-nuvr/)
    """
    def maxFrequencyScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        nums.sort()
        acc = list(accumulate(nums, initial=0))
        ans = 0
        l = 0
        for r in range(n):
            while True:
                mid = (r+l)//2    # 找到左边那个即可
                left = nums[mid] * (mid-l+1) - (acc[mid+1]-acc[l])
                right = (acc[r+1]-acc[mid+1]) - nums[mid] * (r-mid)
                if left+right <= k:
                    ans = max(ans, (r-l+1))
                    break
                else:
                    l += 1
        return ans
    
sol = Solution()
result = [
    # sol.findMissingAndRepeatedValues(grid = [[9,1,7],[8,9,2],[3,4,6]]),
    # sol.divideArray(nums = [1,3,4,8,7,9,3,5,1], k = 2),
    # sol.minimumCost(nums = [1,2,3,4,5]),
    # sol.minimumCost(nums = [10,12,13,14,15]),
    # sol.minimumCost([109,113,115,122,128]),

    sol.maxFrequencyScore(nums = [1,2,6,4], k = 3),
    sol.maxFrequencyScore(nums = [1,4,4,2,4], k = 0),

]
for r in result:
    print(r)
