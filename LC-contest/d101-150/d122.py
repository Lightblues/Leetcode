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
https://leetcode-cn.com/contest/biweekly-contest-122
Easonsi @2023 """
class Solution:
    """ 3010. 将数组分成最小总代价的子数组 I """
    def minimumCost(self, nums: List[int]) -> int:
        return nums[0] + sum(sorted(nums[1:])[:2])
    
    """ 3011. 判断一个数组是否可以变为有序 #medium 只有相邻两个元素的二进制1数量相同的时候， 两者才可交换，问是否可以构成有序
思路1: 如何实现这种分组的题目？ 
#分组循环 
参见 [ling](https://leetcode.cn/problems/find-if-array-can-be-sorted/solutions/2613051/jiao-ni-yi-ci-xing-ba-dai-ma-xie-dui-on-j3nik/)
    """
    def canSortArray(self, nums: List[int]) -> bool:
        # 两个 for 循环来实现！ 非常优雅
        n = len(nums)
        i = 0
        while i<n:
            start = i
            ones = nums[i].bit_count()
            while i<n and nums[i].bit_count() == ones:
                i += 1
            nums[start:i] = sorted(nums[start:i])
        return all(x<=y for x,y in itertools.pairwise(nums))

    """ 3012. 通过操作使数组长度最小 #medium #思维题 对于数组中两个 >0 的 x,y 可以将其变为 x%y, 问最后最少能剩下几个数字
思路1: 考虑「最小数字」
    显然，可以用小数字消除大数字！因此，若数组中最小数字只有1个，则答案就是1. 
    如何构造最小数字？结论：记原本的最小数字为m，若数字中存在m的非倍数，则可以找到一个比m更小的数字 —— 利用这个数字我们可以将其他数字都消掉。
    情况2: 若所有数字都是m的倍数，则无法消除，答案就是 (c+1)//2
    """
    def minimumArrayLength(self, nums: List[int]) -> int:
        mn = min(nums)
        for x in nums:
            if x%mn != 0:
                return 1
        c = nums.count(mn)
        return (c+1) // 2
    
    """ 3013. 将数组分成最小总代价的子数组 II #hard 需要将一个数字分割成k个子数组，满足第二个数组和最后一个数组的第一个元素相距不超过 dist, 也即 i_{k-1} - i_1 <= dist。每个子数组的代价为第一个数字，问最小代价
限制: k,n 1e5
思路1: 两个有序集合维护前 k-1 小
    问题转化为：找到一个长度在 k+1 范围的数组中的最小 k-1 个元素之和！
    类似题目「0480. 滑动窗口中位数」不过还需要维护滑窗的最小 k-1 个元素和。
    具体来说，用一个L结构维护滑窗中最小的 k-1 个元素，窗口中其他元素放在R中。这个数组结构可以简单用 sortedlist来实现
    """
    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        pass



sol = Solution()
result = [
    sol.canSortArray([3,16,8,4,2]),
]
for r in result:
    print(r)
