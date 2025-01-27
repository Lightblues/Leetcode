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
https://leetcode.cn/contest/weekly-contest-424

T4 简洁的题设, 有点看数学~
Easonsi @2024 """
class Solution:
    """ 3354. 使数组元素等于零 """
    def countValidSelections(self, nums: List[int]) -> int:
        s = sum(nums)
        is_odd = s % 2 == 1
        if is_odd:
            target = s // 2 + 1
        else:
            target = s // 2
        acc = 0; ans = 0
        for x in nums:
            if x > 0:
                acc += x
                if acc > target: return ans
            elif x == 0:
                if not is_odd and acc == target: ans += 2
                elif is_odd and acc in [target-1, target]: ans += 1
        return ans
    
    """ 3355. 零数组变换 I #medium 对于每个 (l,r) 查询, 可以在 nums[l...r] 中选择任意子数组 -1, 问是否可以使得 nums 全为 0 """
    def isZeroArray(self, nums: List[int], queries: List[List[int]]) -> bool:
        acc = [0] * (len(nums)+1)
        for l,r in queries:
            acc[l] += 1
            acc[r+1] -= 1
        for i in range(1, len(acc)):
            acc[i] += acc[i-1]
        return all(x<=a for x,a in zip(nums, acc))
    
    """ 3356. 零数组变换 II #medium 对于每个 (l,r,val) 可以将 nums[l...r] 中的元素最多减去 val, 问顺序处理queries最快可以使得 nums 全为 0 吗 
思路: 二分 + 差分
    """
    def minZeroArray(self, nums: List[int], queries: List[List[int]]) -> int:
        n = len(nums); R = len(queries)
        def check(k):
            diff = [0] * (n+1)
            for l,r,val in queries[:k]:
                diff[l] += val
                diff[r+1] -= val
            for i in range(1, n+1):
                diff[i] += diff[i-1]
            return all(x-diff[i]<=0 for i,x in enumerate(nums))
        left, right = 0, R
        while left < right:
            mid = (left + right) // 2
            if check(mid): right = mid
            else: left = mid + 1
        return left if check(left) else -1
    
    """ 3357. 最小化相邻元素的最大差值 #hard 数组中部分缺失, 可以选择 (x,y) 两个数字, 填在空缺处. 要求最小化填入数字之后, 数组相邻元素的最大差值 
限制: n 1e5; x 1e9
思路1: 二分 + 贪心
    基本思路: 
    1. 要最小化最大值, 一般可以尝试二分! 
    2. 对于一个固定的限制 k, 如何确定 (x,y)? -- 可以先找出所有的临近空缺的左右区间!
    https://leetcode.cn/circle/discuss/UNYN0e/
思路2: 
    更加理论的分析
    灵神: https://leetcode.cn/problems/minimize-the-maximum-adjacent-element-difference/solutions/2991784/on-tan-xin-pythonjavacgo-by-endlesscheng-1bxe/
    """
    def minDifference(self, nums: List[int]) -> int:
        pass

    
sol = Solution()
result = [
    # sol.countValidSelections(nums = [1,0,2,0,3]),
    # sol.countValidSelections(nums = [16,13,10,0,0,0,10,6,7,8,7]),
    # sol.isZeroArray(nums = [1,0,1], queries = [[0,2]]),
    
    sol.minZeroArray(nums = [4,3,2,1], queries = [[1,3,2],[0,2,1]]),
    sol.minZeroArray(nums = [2,0,2], queries = [[0,2,1],[0,2,1],[1,1,3]]),
    sol.minZeroArray([5], [[0,0,5],[0,0,1],[0,0,3],[0,0,2]]),
    sol.minZeroArray([4,3,2,1], [[1,3,2],[0,2,1]]),
]
for r in result:
    print(r)
