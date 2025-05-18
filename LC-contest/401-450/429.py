from math import ceil
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
https://leetcode.cn/contest/weekly-contest-429
T4 想到了二分, 但需要考虑一些边界情况!
Easonsi @2024 """
class Solution:
    """ 3396. 使数组元素互不相同所需的最少操作次数 """
    def minimumOperations(self, nums: List[int]) -> int:
        n = len(nums)
        s = set()
        for i in range(n-1,-1,-1):
            if nums[i] in s:
                return ceil((i+1)/3)
            s.add(nums[i])
        return 0
    
    """ 3397. 执行操作后不同元素的最大数量 #medium 可以对于每个元素增加 [-k,k] 范围内的整数, 问最终数组中不同元素的最大数量 """
    def maxDistinctElements(self, nums: List[int], k: int) -> int:
        nums.sort()
        mx = -inf; cnt = 0
        for x in nums:
            if x-k > mx:  # 贪心, 每次选尽可能小的数字
                mx = x-k
                cnt += 1
            elif x+k > mx:
                mx += 1
                cnt += 1
        return cnt

    """ 3398. 字符相同的最短子字符串 I #hard 对于一个二进制字符串, 最多反转 ops 次, 问结果中, 最长相同子字符串的长度 
限制: n 1e5
思路1: #二分
    首先, 发现不能贪心地 "修改最后一个最后一个不符合的元素". 例如, 对于 [1,1,1,0,0], ops=1 的情况下, 若目标长度为2, 则变为 [1,1,0,0,1] 发现需要2次不符合!
    一个重要启发: 不能修改区间边缘! 
        例如 [0,0,0,0], 对于目标长度2, 可以划分为 [0,0,1,0]
            [0,0,0], 目标长度2, 划分为 [0,1,0]
        这样, 对于一个长度为 l 的区间, 目标最大长度为 m, 则需要划分 l//(m+1) 次!
    注意, 由于 "不能修改区间边缘" 的限制, 我们实际上没有考虑目标长度 =1 的情况!
        例如 [0,0,0,1,1,0,0,0], 目标长度=1, 分区间计算的话需要3次, 但实际上最少需要4次!
        特判! 可以暴力统计变为 [0,1,0,1...] 或 [1,0,1,0...] 的操作数
ling: https://leetcode.cn/problems/smallest-substring-with-identical-characters-ii/solutions/3027031/er-fen-da-an-tan-xin-gou-zao-pythonjavac-3i4f/
    """
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        # special for 1
        cnt = sum(int(c)==(i%2) for i,c in enumerate(s))
        if min(cnt, n-cnt) <= numOps: return 1
        # binary search
        lens = []; l = -1
        for i,c in enumerate(s):
            if i==n-1 or c!=s[i+1]:
                lens.append(i-l)
                l = i
        def check(m):
            return sum(l//(m+1) for l in lens) <= numOps
        l,r = 2,n; ans = n
        while l<=r:
            m = (l+r)//2
            if check(m):
                ans = m
                r = m-1
            else: l = m+1
        return ans
    
    

    
sol = Solution()
result = [
    # sol.minimumOperations(nums = [1,2,3,4,2,3,3,5,7]),
    # sol.maxDistinctElements(nums = [4,4,4,4], k = 1),
    sol.minLength(s = "000001", numOps = 1),
    sol.minLength(s = "0000", numOps = 2),
]
for r in result:
    print(r)
