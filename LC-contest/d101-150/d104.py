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
https://leetcode-cn.com/contest/biweekly-contest-104
https://leetcode.cn/circle/discuss/OMJd2e/


Easonsi @2023 """
class Solution:
    """ 2678. 老人的数目 """
    
    """ 2679. 矩阵中的和 """
    def matrixSum(self, nums: List[List[int]]) -> int:
        n,m = len(nums),len(nums[0])
        for i in range(n):
            nums[i] = sorted(nums[i])
        ans = 0
        for col in itertools.zip_longest(*nums):
            ans += max(col)
        return ans
    

    """ 2680. 最大或值 #medium 可以对于数组中的数字进行k次 <<1 操作, 问可能得到的最大 or值 
限制: n 1e5; k 15
思路1: #贪心 + #前后缀
    显然所有操作都应该加到一个数字上! 
        但可能不是的最大元素, 例如 [1001, 1100] 两个数字 k=1 情况下, 应该移位操作加到 1001
    那么需要快速得到其他元素的 or值? 可以利用前后缀! (自己之前想的暴力方法是记录每一位上的1的个数)
[灵神](https://leetcode.cn/problems/maximum-or/submissions/)
    """
    def maximumOr(self, nums: List[int], k: int) -> int:
        n = len(nums)
        suf = [0] * (n + 1)
        for i in range(n - 1, 0, -1):
            suf[i] = suf[i + 1] | nums[i]
        ans = pre = 0
        for i, x in enumerate(nums):
            ans = max(ans, pre | (x << k) | suf[i + 1])
            pre |= x
        return ans


    
    """ 2681. 英雄的力量 #hard 对于一个数字, 求所有非空子数组的分数和. 分数定义为, 数组 max^2 * min
限制: n 1e5; 对结果取模
思路1: #贡献法 下面写了自己的模拟过程. #TODO 灵神整理的 「贡献法」 专题
    来看 1,2,3,4
        首先, 1作为最大值只有 [1] 一种情况, 求和 a1 = 1^2 * [1]
        2作为最大值, a2 = 2^2 * [2 + 1*1]
        3, a3 = 3^2 * [3 + 2*1 + 1*2]
        4, a4 = 4^2 * [4 + 3*1 + 2*2 + 1*3]
    仅考虑匹配的最小值和, 记为 bi, 有
        b[i] = 2 * b[i-1] + (arr[i] - arr[i-1])
[灵神](https://leetcode.cn/problems/power-of-heroes/solution/gong-xian-fa-pythonjavacgo-by-endlessche-d4jx/)
关联: 「2281. 巫师的总力量和」
    """
    def sumOfPower(self, nums: List[int]) -> int:
        mod = 10**9 + 7
        nums.sort()
        b = nums[0]
        # ans = nums[0] ** 3    # 注意若 [1000000] 的情况, 返回不在int范围内!
        ans = pow(nums[0], 3, mod)
        for i in range(1, len(nums)):
            b = (b * 2 + nums[i] - nums[i-1]) % mod
            ans = (ans + b * nums[i]**2) % mod
        return ans


    
sol = Solution()
result = [
    # sol.matrixSum(nums = [[7,2,1],[6,4,2],[6,5,3],[3,2,1]]),

    sol.sumOfPower([2,1,4]),
    sol.sumOfPower(nums = [1,1,1]),
]
for r in result:
    print(r)
