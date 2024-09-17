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
https://leetcode.cn/contest/weekly-contest-398
Easonsi @2023 """
class Solution:
    """ 3151. 特殊数组 I """
    def isArraySpecial(self, nums: List[int]) -> bool:
        flag = nums[0] % 2
        for i in range(1, len(nums)):
            if nums[i] % 2 == flag:
                return False
            flag = 1-flag
        return True

    """ 3152. 特殊数组 II """
    def isArraySpecial(self, nums: List[int], queries: List[List[int]]) -> List[bool]:
        n = len(nums)
        l = 0
        left = [0] * n
        pre = nums[0] % 2
        for i in range(1, n):
            if nums[i] % 2 == pre:
                l = i
            pre = nums[i] % 2
            left[i] = l
        ans = []
        for l,r in queries:
            if left[r] <= l:
                ans.append(True)
            else:
                ans.append(False)
        return ans

    """ 3153. 所有数对中数位不同之和 """
    def sumDigitDifferences(self, nums: List[int]) -> int:
        ans = 0
        nums = [str(x) for x in nums]
        n = len(nums)
        ll = len(nums[0])
        for i in range(ll):
            cnt = Counter([x[i] for x in nums])
            for k,v in cnt.items():
                ans += v * (n - v)
        return ans //  2
    
    """ 3154. 到达第 K 级台阶的方案数 #hard 需要从台阶1跳到台阶k, 问有多少可能. (从0开始, 但没有负)
在台阶i可以执行: 1) 到 i-1, 但不能连续使用操作1; 2) 跳到 i + 2^jump, 然后 jump += 1
    """
    def waysToReachStair(self, k: int) -> int:

    
sol = Solution()
result = [
    # sol.isArraySpecial(nums = [4,3,1,6], queries = [[0,2],[2,3]]),
    sol.sumDigitDifferences(nums = [13,23,12]),
]
for r in result:
    print(r)
