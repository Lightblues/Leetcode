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
https://leetcode.cn/contest/weekly-contest-348
disscuss: https://leetcode.cn/circle/discuss/p8kMMM/

复健, 虚拟拿了60多排名, 不错子! T3 T4 都有一定的思维~
Easonsi @2023 """
class Solution:
    """ 2716. 最小化字符串长度 """
    def minimizedStringLength(self, s: str) -> int:
        return len(set(s))
    
    """ 2717. 半有序排列 """
    def semiOrderedPermutation(self, nums: List[int]) -> int:
        n = len(nums)
        i1, i2 = nums.index(1), nums.index(n)
        return (i1-0) + (n-1-i2) - (i1>i2)
    
    """ 2718. 查询后矩阵的和 #medium 有两种操作: 分别将矩阵的某一行/列全部设置为x, 为经过了若干操作之后, 矩阵和
限制: n 1e4; 操作次数 5e4
思路1: 每个位置最后的元素由最后一次进行的操作所决定!
    因此, 从后往前遍历. 如何记录此次受到影响的格子数量? 利用 row/col 进行记录!
    """
    def matrixSumQueries(self, n: int, queries: List[List[int]]) -> int:
        rows = [-1] * n
        cols = [-1] * n
        nc = nr = 0
        ans = 0
        for t, i, v in queries[::-1]:
            if t==0:
                if rows[i]!=-1: continue
                rows[i] = v
                ans += v * (n-nc)
                nr += 1
            else:
                if cols[i]!=-1: continue
                cols[i] = v
                ans += v * (n-nr)
                nc += 1
        return ans
    
    """ 2719. 统计整数数目 #hard 统计在 [num1, num2], 范围内的, 数位和在 [min_sum, max_sum] 范围内的数字数量
限制: num2 1e22; max_sum 400. 答案取模
思路1: 分解
    定义 f(MAX, x) 表示在 [0,x] 范围内的数位和最大为MAX的数字数量. 则有 f(MAX, x) = sum{ f(MAX-i), xx }, 其中i为所取的最高位数字, xx表示最高位取i时剩余位的取值范围
    复杂度: O(log(N) * 10)
思路2: #数位DP
    见 [灵神](https://leetcode.cn/problems/numbers-with-repeated-digits/solution/by-endlesscheng-c5vg/)
     """
    def count(self, num1: str, num2: str, min_num: int, max_num: int) -> int:
        mod = 10**9 + 7
        @lru_cache(None)
        def f(m, x):
            if len(x)==0: return 1 if m>=0 else 0
            d,xx = int(x[0]), x[1:]
            r = '9' * len(xx)
            ans = 0
            for i in range(d):
                if m-i<0: break
                ans += f(m-i, r)
            ans += f(m-d, xx) if m-d>=0 else 0
            return ans % mod
        ans = f(max_num, num2) - f(max_num, str(int(num1)-1)) - \
            f(min_num-1, num2) + f(min_num-1, str(int(num1)-1))
        return ans % mod
    
sol = Solution()
result = [
    # sol.semiOrderedPermutation(nums = [2,4,1,3]),
    # sol.semiOrderedPermutation(nums = [1,3,4,2,5]),
    # sol.matrixSumQueries(n = 3, queries = [[0,0,4],[0,1,2],[1,0,1],[0,2,3],[1,2,1]]),
    sol.count(num1 = "1", num2 = "12", min_num = 1, max_num = 8),
    sol.count(num1 = "1", num2 = "5", min_num = 1, max_num = 5),
    sol.count("1000000007","2000000014",1,400),
]
for r in result:
    print(r)
