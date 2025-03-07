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
https://leetcode.cn/contest/biweekly-contest-133
T4 的DP有趣! 逆序对的变换需要一定的思维量. 
Easonsi @2025 """
class Solution:
    """ 3190. 使所有元素都可以被 3 整除的最少操作数 """
    def minimumOperations(self, nums: List[int]) -> int:
        return sum(1 for num in nums if num % 3 != 0)
    
    """ 3191. 使二进制数组全部等于 1 的最少操作次数 I #medium 给定一个二进制数组, 每次操作可以将任意连续的三个比特翻转, 问将所有翻转为1的最小次数. 
无法的话返回 -1. 
限制: n 1e5
思路1: 模拟 贪心
"""
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        cnt = 0
        for i in range(n-2):
            if nums[i] == 0:
                cnt += 1
                for j in range(i, i+3):
                    nums[j] ^= 1
        if nums[-2]==0 or nums[-1]==0: return -1
        return cnt

    """ 3192. 使二进制数组全部等于 1 的最少操作次数 II #medium 每次操作可以翻转i到最后的位, 求最少操作次数 
限制: n 1e5
"""
    def minOperations(self, nums: List[int]) -> int:
        i = 0; n = len(nums)
        # while nums[i]==1: i += 1
        cnt = 0; pre = 1
        for j in range(i,n):
            if nums[j] != pre:
                cnt += 1
                pre = nums[j]
        return cnt

    """ 3193. 统计逆序对的数目 #hard 给定一组 requirements, 每个 (end, cnt) 表示在前缀 prem[0...end] 中存在cnt个逆序对.
对于 0...n-1, 问符合所有requirements的排列有多少个
限制: n 300, requirements.length <= n
    题目保证了对于 n-1 位是有约束的
思路1: #DP #记忆化搜索 从右往左
    看例子1: 对于 perm[0,1,2] 需要2个逆序对
    看最右一位, 
        若填入2, 则和前面构成2个, 前面的两位需要贡献0个
        若填入1, 则和前面构成1个, 前面的两位需要贡献1个
        若填入0, 则和前面构成0个, 前面的两位需要贡献2个
        因此有 f(2,2) = f(1,0)+f(1,1)+f(1,2)
    然后, 问题可以递归! 
    从右往左递推: f(i,j) 表示到 ...i 位构成j个逆序对的数量
        f(i,j) = sum{ f(i-1,j-k) for k in range(0,min(i,j)+1) }
        这里枚举k表示填入的第i位和前面的数字构成逆序对的数量
    边界: f(0,0) = 1
    ---> 上面没考虑 requirements, 若前缀 i-1 有约束 r, 对于 f(i,j) 的约束在于:
        首先, 需要满足 1) j>=r; 2) i位提供j-r个逆序对, 也即 j<=i+r
        此时, 可以递推
            f(i,j) = f(i-1,r)
[official](https://leetcode.cn/problems/count-the-number-of-inversions/solutions/2946689/tong-ji-ni-xu-dui-de-shu-mu-by-leetcode-qsk7r/)
    """
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        MOD = 10**9+7
        req = [-1] * n
        for i,r in requirements:
            req[i] = r

        @cache
        def f(i,j)->int:
            if i==0: return 1 if j==0 else 0
            r = req[i-1]
            if r != -1: 
                if not (r <= j <= i+r): return 0
                else: return f(i-1,r) 
            else:
                return sum(f(i-1,j-k) for k in range(0,min(i,j)+1)) % MOD
        return f(n-1, req[-1])

    
sol = Solution()
result = [
    # sol.minOperations(nums = [0,1,1,1,0,0]),
    # sol.minOperations(nums = [0,1,1,1]),

    # sol.minOperations(nums = [0,1,1,0,1]),
    sol.numberOfPermutations(n = 3, requirements = [[2,2],[0,0]]),
    sol.numberOfPermutations(n = 3, requirements = [[2,2],[1,1],[0,0]]),
]
for r in result:
    print(r)
