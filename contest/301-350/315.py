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
https://leetcode.cn/contest/weekly-contest-315

前三题划水, 5min做出来, 结果T4想了一个小时做不出Orz.

@2022 """
class Solution:
    """ 6204. 与对应负数同时存在的最大正整数 """
    def findMaxK(self, nums: List[int]) -> int:
        ans = -1
        s = set(nums)
        for a in nums:
            if a>0 and -a in s: ans = max(ans, a)
            # s.add(a)
        return ans
    
    """ 6205. 反转之后不同整数的数目 """
    def countDistinctIntegers(self, nums: List[int]) -> int:
        s = set(nums)
        for a in nums:
            s.add(int(str(a)[::-1]))
        return len(s)
    
    """ 6219. 反转之后的数字和 """
    def sumOfNumberAndReverse(self, num: int) -> bool:
        for a in range(num+1):
            if a + int(str(a)[::-1]) == num: return True
        return False
    
    """ 6207. 统计定界子数组的数目 #hard #题型 给定一个数组. 通过给定 mn, mx 问所有子数组中, 其最小最大值分别是这两个数字的数量.
限制: n 1e5;
关联: 2281. 巫师的总力量和
"""
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        n = len(nums)
        
        # 求左右边界, 注意这里的边界都是开区间
        rMin = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and stack[-1][0] >= nums[i]:
                stack.pop()
            rMin[i] = stack[-1][1] if stack else n
            stack.append((nums[i], i))
        lMin = [-1] * n
        stack = []
        for i in range(n):
            while stack and stack[-1][0] > nums[i]:
                stack.pop()
            lMin[i] = stack[-1][1] if stack else -1
            stack.append((nums[i], i))
        # print(f"lMin={lMin}, rMin={rMin}")
        rMax = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and stack[-1][0] < nums[i]:
                stack.pop()
            rMax[i] = stack[-1][1] if stack else n
            stack.append((nums[i], i))
        lMax = [-1] * n
        stack = []
        for i in range(n):
            while stack and stack[-1][0] <= nums[i]:
                stack.pop()
            lMax[i] = stack[-1][1] if stack else -1
            stack.append((nums[i], i))
        # print(f"lMax={lMax}, rMax={rMax}")
        
        idxMin = [i for i in range(n) if nums[i]==minK]
        minRange = {}
        for i in idxMin: minRange[i] = (lMin[i]+1, rMin[i]-1)
        idxMax = [i for i in range(n) if nums[i]==maxK]
        maxRange = {}
        for i in idxMax: maxRange[i] = (lMax[i]+1, rMax[i]-1)
        print()
        
    # def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
    #     n = len(nums)

    #     idxMin = [i for i in range(n) if nums[i]==minK]
        
sol = Solution()
result = [
    sol.countSubarrays(nums = [1,1,1,1], minK = 1, maxK = 1),
    sol.countSubarrays(nums = [1,3,5,2,7,5], minK = 1, maxK = 5),
]
for r in result:
    print(r)
