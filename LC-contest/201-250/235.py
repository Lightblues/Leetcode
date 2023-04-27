from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-235
@2022 """
class Solution:
    """ 1816. 截断句子 """
    def truncateSentence(self, s: str, k: int) -> str:
        return " ".join(s.split()[:k])
    
    """ 1817. 查找用户活跃分钟数 """
    def findingUsersActiveMinutes(self, logs: List[List[int]], k: int) -> List[int]:
        id2set = defaultdict(set)
        for i,t in logs:
            id2set[i].add(t)
        ans = [0] * k
        for i,s in id2set.items():
            ans[len(s)-1] += 1
        return ans
    
    """ 1818. 绝对差值和 #medium
给两个长度为n的数组, 最多可以用nums1中的i元素替换nums1中另一位置的元素, 目标要求 abs(nums2-nums1) 之和最小化.
思路1: 先将原数组的绝对差值和算出来, 再减去「通过最多可以减小的绝对值」大小即可.
    为了计算最多可以减小的绝对差值, 先对nums1排序, 然而对于目标值muns2的每一个位置, 在排序结果中 #二分 找到最接近的元素, 并且原本相应位置的绝对差比较, 看减小了多少.
"""
    def minAbsoluteSumDiff(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        diff = [abs(a-b) for a,b in zip(nums1, nums2)]
        nums1.sort()
        mx = 0  # 最大减小量
        for i,b in enumerate(nums2):
            # 从 nums1 中找到最接近的两个元素, 从而使得绝对差值最小
            idx = bisect.bisect_right(nums1, b)
            a = abs(nums1[idx-1] - b)
            if idx<n:
                a = min(a, abs(nums1[idx] - b))
            mx = max(mx, diff[i]-a) # diff[i] >= a 因为a是最小可能值
        mod = 10**9 + 7
        ans = (sum(diff) - mx) % mod
        return ans

    """ 1819. 序列中不同最大公约数的数目 [gcd] """

sol = Solution()
result = [
    # sol.findingUsersActiveMinutes(logs = [[0,5],[1,2],[0,2],[0,5],[1,3]], k = 5),
    # sol.minAbsoluteSumDiff(nums1 = [1,7,5], nums2 = [2,3,5]),
    # sol.minAbsoluteSumDiff(nums1 = [2,4,6,8,10], nums2 = [2,4,6,8,10]),
    # sol.minAbsoluteSumDiff(nums1 = [1,10,4,4,2,7], nums2 = [9,3,5,1,7,4]),

]
for r in result:
    print(r)
