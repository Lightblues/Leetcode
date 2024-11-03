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
https://leetcode.cn/contest/biweekly-contest-127
T3 利用到了 OR 递增的性质, 参见ling
T4 考虑子序列的最小绝对差, 思路有趣
Easonsi @2023 """
class Solution:
    """ 3095. 或值至少 K 的最短子数组 I """
    def minimumSubarrayLength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = inf
        for i,x in enumerate(nums):
            if x >= k: return 1
            j = i+1
            for j in range(i+1,n):
                x |= nums[j]
                if x >= k: 
                    ans = min(ans, j-i+1)
                    break
                j += 1
        return -1 if ans==inf else ans
    
    """ 3096. 得到更多分数的最少关卡数目 """
    def minimumLevels(self, possible: List[int]) -> int:
        possible = [i if i==1 else -1 for i in possible]
        s = sum(possible)
        for i, a in enumerate(accumulate(possible[:-1])):
            if a > s-a: return i+1
        return -1
    
    """ 3097. 或值至少为 K 的最短子数组 II #medium 定义 "特别数组" 为所有元素 OR >= k. 给定一个数组, 判断最短的特别数组的长度. 
限制: n 1e5; x 1e9
思路1:
    从左往右遍历 i, 我们考虑 0...i 作为左端点可以构成的最大OR. 则, 将i和i-1,i-2,...0进行组合, 得到的结果是递增的! 
    因此, 可以对于 i 从右往左, 若不增加的话break! 
    复杂度? 考虑OR的性质, 每个位置往前最多回溯 log(U), 因此 O(n logU)
[ling](https://leetcode.cn/problems/shortest-subarray-with-or-at-least-k-ii/solutions/2716483/zi-shu-zu-orandgcd-tong-yong-mo-ban-pyth-n8xj/)
参见里面介绍的模板! 
    """
    def minimumSubarrayLength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = inf
        for i,x in enumerate(nums):
            if x >= k: return 1
            for j in range(i-1, -1, -1):
                _can = x | nums[j]
                if _can == nums[j]: break
                if _can >= k: 
                    ans = min(ans, i-j+1)
                    break
                nums[j] = _can
        return -1 if ans==inf else ans
    
    """ 3098. 求出所有子序列的能量和 #hard 子序列的能量定义为任意两个元素差的绝对值的最小值. 求nums中所有长为k的子系列能量之和. 取模. 
限制: n 50; x +-1e8
思路1: 考虑每组数对的贡献! 
    因为要考虑的是序列中临近元素的最小差, 因此显然可以先排序! 
    假设答案中的最小绝对差是 (i,j) 元素构成的 v = nums[j] - nums[i], 考虑它的贡献? -- 需要求出在 i 之前的相邻元素差 > v 的子序列数量; 以及 j 之后的 >= v 的子序列数量.
        考虑到可能有多个构成 v 的间隔, 因此这里前后分别用来  >, >=
    考虑子问题: "(子)数组中有多少子序列, 满足所有元素的绝对差至少为v" -- 显然可以用 DP 求解
    复杂度: 外层枚举 O(n^2), 内层 O(n^2 ~ n^3)
[小羊](https://leetcode.cn/problems/find-the-sum-of-subsequence-powers/solutions/2719517/xiao-yang-xiao-en-on4-gao-xiao-qiu-jie-z-qy5g/)
    """
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        nums.sort(); n = len(nums)
        MOD = 10**9+7
    
sol = Solution()
result = [
    sol.minimumSubarrayLength(nums = [2,1,8], k = 10),
    sol.minimumSubarrayLength(nums = [2,1,8], k = 100),
    # sol.minimumLevels(possible = [1,0,1,0]),
    # sol.minimumLevels(possible = [0,0]),
]
for r in result:
    print(r)
