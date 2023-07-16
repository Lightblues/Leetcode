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
https://leetcode.cn/contest/weekly-contest-354
https://leetcode.cn/circle/discuss/FGLo5F/


Easonsi @2023 """
class Solution:
    """ 6889. 特殊元素平方和 """
    def sumOfSquares(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        for i,x in enumerate(nums):
            if n%(i+1)==0: ans += x**2
        return ans
    
    """ 6929. 数组的最大美丽值 """
    def maximumBeauty(self, nums: List[int], k: int) -> int:
        # WA
        nums.sort()
        n = len(nums); ans = 1
        l = r = 0
        for i,x in enumerate(nums):
            while x - nums[l] > k: l += 1
            while r<n and nums[r] - x <= k: r += 1
            ans =  max(ans, r-l)
        return ans
    
    def maximumBeauty(self, nums: List[int], k: int) -> int:
        nums.sort()
        n = len(nums); ans = 1
        l = 0
        for i,x in enumerate(nums):
            while x - nums[l] > 2*k: l += 1
            ans = max(ans, i-l+1)
        return ans
    
    """ 6927. 合法分割的最小下标 """
    def minimumIndex(self, nums: List[int]) -> int:
        n = len(nums)
        cnt = Counter(nums)
        cnt = sorted(cnt.items(), key=lambda x: x[1], reverse=True)
        x,m = cnt[0]
        cntX = 0
        for i,y in enumerate(nums):
            cntX += x==y
            if 2*cntX > (i+1) and 2*(m-cntX) > (n-i-1): return i
        return -1
    
    """ 6924. 最长合法子字符串的长度 #hard 给定一组forbidden的字符串, 问一个word中的最长的不包含forbidden的子串长度. forbidden字符串的长度不超过10!
限制: n 1e5; forbidden 1e5; L 10
思路1: #指针 利用了 #单调性
    贪心性质: 注意到, 对于 [l,r] 的合法子串, 对于其中的任意位置, [x,r] 也一定是合法的. 
    因此, 我们逆序遍历, 对于每一个起始位置, 每一个位置idx出发的最长右边界都会影响idx左边出发的子串的合法性! 
    因此, 维护一个全局指针right, 在递归过程中, 更新这个边界; 然后从每个位置idx出发看以该字符开头的最长合法子串长度.
    记f[i]表示左端点为i位置的最长合法子串的右端点, 则有递归 
        f[i] = max{ right, 以word[i]起始的 [i:i+x] 合法的最大x }. 由于L=10, 这一步复杂度 O(L)
        并且更新 right = min{ right, f[i] }
    复杂度: O(nL)
[灵神](https://leetcode.cn/problems/length-of-the-longest-valid-substring/solution/ha-xi-biao-shuang-zhi-zhen-pythonjavacgo-bcez/)
    """
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        L = 10
        forbidden = set(forbidden)
        n = len(word); ans = 0
        right = n-1
        for i in range(n-1,-1,-1):
            for j in range(i, min(i+L, n)):
                if word[i:j+1] in forbidden:
                    right = min(right, j-1)
                    break
            ans = max(ans, right-i+1)
        return ans
        
sol = Solution()
result = [
    # sol.sumOfSquares(nums = [2,7,1,19,18,3]),
    # sol.maximumBeauty(nums = [4,6,1,2], k = 2),
    # sol.maximumBeauty([1,1,1,1,], 10),
    # sol.maximumBeauty([49,26], 12), 
    # sol.minimumIndex(nums = [1,2,2,2]),
    # sol.minimumIndex(nums = [3,3,3,3,7,2,2]),
    sol.longestValidSubstring(word = "cbaaaabc", forbidden = ["aaa","cb"]),
    sol.longestValidSubstring(word = "leetcode", forbidden = ["de","le","e"]),
]
for r in result:
    print(r)
