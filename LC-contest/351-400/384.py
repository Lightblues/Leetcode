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
https://leetcode.cn/contest/weekly-contest-384
https://leetcode.cn/circle/discuss/xrMOAr/

Easonsi @2023 """

class Solution:
    """ 3033. 修改矩阵 """
    def modifiedMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        m,n = len(matrix), len(matrix[0])
        ans = [[0] * n for _ in range(m)]
        for j in range(n):
            mx = max(matrix[i][j] for i in range(m))
            for i in range(m):
                if matrix[i][j] == -1:
                    ans[i][j] = mx
                else:
                    ans[i][j] = matrix[i][j]
        return ans
    
    """ 3034. 匹配模式数组的子数组数目 I """

    """ 3035. 回文字符串的最大数量 #medium 给定一组字符串, 每个字符串的长度不变, 元素可以任意交换, 问最多的到多少回文
限制: n 1e3; 长度 1e2
思路1: 贪心先做最小长度的
    """
    def maxPalindromesAfterOperations(self, words: List[str]) -> int:
        lens = [len(w) for w in words]
        cnt_odd = cnt_even = 0
        for w,c in Counter(reduce(lambda x,y: x+y, words)).items():
            a,b = divmod(c, 2)
            cnt_odd += b
            cnt_even += a*2
        ans = 0
        for l in sorted(lens):
            a,b = divmod(l, 2)
            if a*2 > cnt_even: break
            ans += 1
            cnt_even -= a*2
            if b:
                if cnt_odd == 0:
                    cnt_even -= 2
                    cnt_odd += 1
                else:
                    cnt_odd -= 1
        return ans


    """ 3036. 匹配模式数组的子数组数目 II #hard 对于一个长m的pattern数组, 只包含 1/0/-1 标记相邻像个元素的大小关系, 定义和一个长 m+1 的子数组是否是匹配的, 计算所给的 nums 的匹配数量
限制: n,m 1e6
思路1: #KMP
    """
    def countMatchingSubarrays(self, nums: List[int], pattern: List[int]) -> int:
        s = []
        for i in range(1, len(nums)):
            x = 0
            if nums[i] > nums[i - 1]:
                x = 1
            elif nums[i] < nums[i - 1]:
                x = -1
            s.append(x)
        kmp = KMP(pattern)
        return len(kmp.match(s))
    
class KMP:
    def __init__(self, pattern) -> None:
        self.pattern = pattern
        self.pi = self.prefix_function(pattern)
        self.n = len(pattern)
    
    def prefix_function(self, pattern) -> list:
        # 前缀函数. pi从0开始 —— 当前后缀和前缀匹配的长度!
        n = len(pattern)
        pi = [0] * n
        for i in range(1, n):
            j = pi[i - 1]
            while j > 0 and pattern[i] != pattern[j]:
                j = pi[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            pi[i] = j
        return pi
    
    def match(self, s):
        """ 找到和s中pattern出现的位置 """
        res = []
        pi = self.pi
        pattern = self.pattern
        j = 0
        for i in range(len(s)):
            while j > 0 and s[i] != pattern[j]:
                j = pi[j - 1]
            if s[i] == pattern[j]:
                j += 1
            if j == len(pattern):
                res.append(i - len(pattern) + 1)
                j = pi[j - 1]
        return res
    
sol = Solution()
result = [
    # sol.maxPalindromesAfterOperations(words = ["abbb","ba","aa"]),
    # sol.maxPalindromesAfterOperations(words = ["cd","ef","a"]),
    # sol.maxPalindromesAfterOperations(["aa","bc"]),

    sol.countMatchingSubarrays(nums = [1,2,3,4,5,6], pattern = [1,1]),
    sol.countMatchingSubarrays(nums = [1,4,4,1,3,5,5,3], pattern = [1,0,-1]),
]
for r in result:
    print(r)
