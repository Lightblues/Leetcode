from typing import *
# from easonsi.util.leetcode import *

# def testClass(inputs):
#     # 用于测试 LeetCode 的类输入
#     s_res = [None] # 第一个初始化类, 一般没有返回
#     methods, args = [eval(l) for l in inputs.split('\n')]
#     class_name = eval(methods[0])(*args[0])
#     for method_name, arg in list(zip(methods, args))[1:]:
#         r = (getattr(class_name, method_name)(*arg))
#         s_res.append(r)
#     return s_res

""" 
https://leetcode.cn/contest/weekly-contest-430
Easonsi @2025 """
class Solution:
    """ 3402. 使每一列严格递增的最少操作次数 """
    def minimumOperations(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        ans = 0
        for i in range(n):
            pre = grid[0][i]
            for j in range(1,m):
                if grid[j][i] <= pre:
                    ans += pre - grid[j][i] + 1
                    pre += 1
                else:
                    pre = grid[j][i]
        return ans
    
    """ 3403. 从盒子中找出字典序最大的字符串 I #medium 将一个字符串分为k段, 求其中字段序最大的字符串 """
    def answerString(self, word: str, numFriends: int) -> str:
        # 
        if numFriends == 1:
            return word
        # find the largest character
        ch = word[0]; idx = 0
        for i,c in enumerate(word):
            if c > ch:
                ch = c
                idx = i
        # make the largest character as the first
        l = len(word) - (numFriends - 1)
        return word[idx:idx+l]
    
    # TODO:T3, T4
    """ 1163. 按字典序排在最后的子串 #hard 对于一个字符串的所有子串, 找到字典序最大的子串
思路1: 
    显然, 结果一个是一个 "后缀子串"
    #双指针 其中 i 表示当前最大子串的左端点, j 表示目前枚举的左端点. 
    假设这两个子串的公共前缀为 k-1, 对于 s[i+k], s[j+k],
    若 s[i+k] > s[j+k]
        若 i+k <= j, 则下一个枚举 j+1 (平凡的情况)
        若 i+k > j, 我们要证明 j...j+k 都不需要枚举! (下一个枚举 j+k+1)
            可以将其拆成 i+m <= j; i+m > j 两部分
            对于 i+m <= j, 显然有 s[j+m:] < s[i+m:] < s[i:] -- 其中第一个不等式是因为 s[i+k] > s[j+k]; 第二个不等式是沿用递推的结论
    若 s[i+k] < s[j+k]
https://leetcode.cn/problems/last-substring-in-lexicographical-order/solutions/2241014/an-zi-dian-xu-pai-zai-zui-hou-de-zi-chua-31yl/
    """
    def lastSubstring(self, s: str) -> str:
        n = len(s)
        

    
sol = Solution()
result = [
    sol.answerString(word = "dbca", numFriends = 2),
]
for r in result:
    print(r)
