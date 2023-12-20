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
https://leetcode.cn/contest/weekly-contest-375
https://leetcode.cn/circle/discuss/3ml97X/
手速场! 非常顺利的一次, 15分钟左右完成!
Easonsi @2023 """
class Solution:
    """  """
    def countTestedDevices(self, batteryPercentages: List[int]) -> int:
        cnt = 0
        for b in batteryPercentages:
            if b > cnt: cnt += 1
        return cnt
    
    """ 2961. 双模幂运算 """
    def getGoodIndices(self, variables: List[List[int]], target: int) -> List[int]:
        ans = []
        for i,(a,b,c,m) in enumerate(variables):
            if pow(pow(a,b, 10), c, m) == target:
                ans.append(i)
        return ans
    
    """ 2962. 统计最大元素出现至少 K 次的子数组 """
    def countSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        mx = max(nums)
        idxs = [i for i in range(len(nums)) if nums[i] == mx]
        ans = 0
        for r in range(k-1, len(idxs)):
            l = r-k+1
            num_l = idxs[l]+1 if l==0 else idxs[l]-idxs[l-1]
            num_r = n-idxs[r]
            ans += num_l*num_r
        return ans
    
    """ 2963. 统计好分割方案的数目 #hard 
可以有O(n) 的做法, 见 [灵神](https://leetcode.cn/problems/count-the-number-of-good-partitions/solutions/2560938/he-bing-qu-jian-pythonjavacgo-by-endless-yxhw/)
       """
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        num2range = {}
        for i,x in enumerate(nums):
            if x not in num2range:
                num2range[x] = [i,i]
            else:
                num2range[x][1] = i
        ranges = sorted(num2range.values())
        cnt = 0
        pre = -1
        for l,r in ranges:
            if l>pre:
                cnt += 1
                pre = r
            else:
                pre = max(pre, r)
        mod = 10**9+7
        return pow(2,cnt-1, mod)
    
sol = Solution()
result = [
    # sol.countSubarrays(nums = [1,3,2,3,3], k = 2),
    # sol.countSubarrays(nums = [1,4,2,1], k = 3),
    sol.numberOfGoodPartitions([1,2,3,4]),
    sol.numberOfGoodPartitions([1,1,1]),
    sol.numberOfGoodPartitions(nums = [1,2,1,3]),
]
for r in result:
    print(r)
