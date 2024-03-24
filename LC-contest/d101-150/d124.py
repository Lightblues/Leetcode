from easonsi.util.leetcode import *
import sys
sys.setrecursionlimit(10**6)

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
https://leetcode-cn.com/contest/biweekly-contest-124
状态还行! DP场


Easonsi @2023 """
class Solution:
    """ 3038. 相同分数的最大操作数目 I """
    def maxOperations(self, nums: List[int]) -> int:
        x = sum(nums[:2])
        ans = 1
        for i in range(3, len(nums), 2):
            if sum(nums[i-1:i+1]) != x: break
            ans += 1
        return ans
    
    """ 3039. 进行操作使字符串为空 """
    def lastNonEmptyString(self, s: str) -> str:
        mx = max(Counter(s).values())
        res = ""
        cnt = Counter()
        for c in s:
            cnt[c] += 1
            if cnt[c] == mx:
                res += c
        return res
    
    """ 3040. 相同分数的最大操作数目 II #medium 每次可以选择从前/从后/前后各一删除两个数字, 要求之和都相等. 问最多删除多少次.
限制: n 2e3
思路1: DFS, 其实叫 #区间DP
    记 f(l,r, x) 表示从 [l...r] 按照要求得到x的最大数量, 则
        f(l,r, x) = max(f(l+2,r,x), f(l+1,r-1,x), f(l,r-2,x)) + 1 其中要求操作是合法的
    """
    def maxOperations(self, nums: List[int]) -> int:
        xs = set([sum(nums[:2]), sum(nums[-2:]), nums[0]+nums[-1]])
        # NOTE: 考虑 nums = [2]*2000 的情况, 需要加 cache!
        @lru_cache(None)
        def f(l, r, x):
            if l>=r: return 0
            ans = 0
            if sum(nums[l:l+2]) == x:
                ans = max(ans, f(l+2, r, x)+1)
            if nums[l] + nums[r] == x:
                ans = max(ans, f(l+1, r-1, x)+1)
            if sum(nums[r-1:r+1]) == x:
                ans = max(ans, f(l, r-2, x)+1)
            return ans
        return max(f(0, len(nums)-1, x) for x in xs)
    
    """ 3041. 修改数组后最大化数组中的连续元素数目 #hard 对于每个元素最多可以 +1, 问修改后的子序列得到连续数组的最大长度. 
限制: n 1e5
思路1:
参见 [ling](https://leetcode.cn/problems/maximize-consecutive-elements-in-an-array-after-modification/)
    """
    def maxSelectedElements(self, nums: List[int]) -> int:
        nums.sort()
        n = len(nums)
        f = [[1,1] for _ in range(n)]
        for i in range(1,n):
            if nums[i] == nums[i-1]+2:
                f[i][0] = f[i-1][1]+1
            elif nums[i] == nums[i-1]+1:
                f[i][0] = f[i-1][0]+1
                f[i][1] = f[i-1][1]+1
            elif nums[i] == nums[i-1]:
                f[i][0] = f[i-1][0]
                f[i][1] = f[i-1][0]+1
        return max(max(f[i]) for i in range(n))

    def maxSelectedElements(self, nums: List[int]) -> int:
        # from ling
        nums.sort()
        f = defaultdict(int)
        for x in nums:
            f[x + 1] = f[x] + 1
            f[x] = f[x - 1] + 1
        return max(f.values())


sol = Solution()
result = [
    # sol.lastNonEmptyString(s = "aabcbbca"),
    # sol.lastNonEmptyString("abcd"),
    # sol.maxOperations(nums = [3,2,1,2,3,4]),
    # sol.maxOperations(nums = [3,2,6,1,4]),

    sol.maxSelectedElements(nums = [2,1,5,1,1]),
    sol.maxSelectedElements([1,4,7,10]),
    sol.maxSelectedElements([8,10,6,12,9,12,2,3,13,19,11,18,10,16]),
]
for r in result:
    print(r)
