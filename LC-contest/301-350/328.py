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
https://leetcode.cn/contest/weekly-contest-328
讨论: https://leetcode.cn/circle/discuss/IAQlrp/
https://www.bilibili.com/video/BV1QT41127kJ/
本周都是比较经典的思路, 灵神总结了一些相似题, 赞. 
T2 二维差分; T3双指针; T4树形DP.

Easonsi @2023 """
class Solution:
    """ 6291. 数组元素和与数字和的绝对差 """
    
    """ 子矩阵元素加 1 见 [prefix-sum] """

    """ 6293. 统计好子数组的数目 #medium 对于一个子数组 (连续), 若满足 (i, j), i < j 且 arr[i] == arr[j] 的下标对数量至少为k, 则称其为好子数组, 问有多少个好子数组 限制: n 1e5
思路1: #双指针. 
    维护左指针为, 满足条件的最右端, 这样在移动右指针的过程中, 每次 +l+1
    具体的维护见代码
"""
    def countGood(self, nums: List[int], k: int) -> int:
        cnt = Counter() # 当前窗口内的数字计数
        pairs = 0   # 当前窗口内的下标对数量
        l=0
        acc = 0 # 累计答案
        for r,num in enumerate(nums):
            pairs += cnt[num]
            cnt[num] += 1
            # 移动左指针. 注意一共用x个数, 那么拿掉第一个数字, 减少的下标对数量为x-1
            while pairs - (cnt[nums[l]]-1) >= k:
                pairs -= cnt[nums[l]]-1
                cnt[nums[l]] -= 1
                l+=1
            if pairs>=k: acc += l+1
        return acc
    
    """ 最大价值和与最小价值和的差值 见 [dp-tree] """
sol = Solution()
result = [
    # sol.countGood(nums = [1,1,1,1,1], k = 10),
    # sol.countGood(nums = [3,1,4,3,2,2,4], k = 2),


]
for r in result:
    print(r)
