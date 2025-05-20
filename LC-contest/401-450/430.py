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
T2 看了 "计算字典序最大的后缀" 又一个让人惊艳的算法!!!
    # TODO:T3, T4

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
    
    """ 3403. 从盒子中找出字典序最大的字符串 I #medium 将一个字符串分为k段, 求其中字段序最大的字符串 
限制: n 5e3
思路1: 暴力枚举
    复杂度: O(n*(n-k+1))
思路2: 计算字典序最大的后缀, 见 [1163]
    复杂度: O(n)
ling https://leetcode.cn/problems/find-the-lexicographically-largest-string-from-the-box-i/solutions/3033286/mei-ju-zuo-duan-dian-tan-xin-pythonjavac-y2em/
    """
    def answerString(self, word: str, numFriends: int) -> str:
        # special case
        if numFriends == 1:
            return word
        # find the largest character
        n = len(word); l = len(word) - numFriends + 1
        return max(word[i:i+l] for i in range(n))
    def answerString(self, word: str, numFriends: int) -> str:
        if numFriends == 1:
            return word
        i,j,n = 0,1,len(word)
        while j<n:
            k = 0
            while j+k < n and word[i+k] == word[j+k]:
                k += 1
            if j+k < n and word[i+k] < word[j+k]:
                i, j = j, max(j+1, i+k+1)
            else:
                j += k+1
        return word[i:i+len(word)-numFriends+1]
    
    """ 1163. 按字典序排在最后的子串 #hard 对于一个字符串的所有子串, 找到字典序最大的子串
思路1: #双指针 -- 这里的核心是递推!
    显然, 结果一个是一个 "后缀子串"
    #双指针 其中 i 表示当前最大子串的左端点, j 表示目前枚举的左端点. 
    假设这两个子串的公共前缀为 k-1, 对于 s[i+k], s[j+k],
    若 s[i+k] < s[j+k]
        显然要更新 i=j, 对于 j,
        若 i+k <= j, 则下一个枚举 j+1 (平凡的情况)
        若 i+k > j, 我们要证明 i...i+k 都不需要枚举! (下一个枚举 i+k+1)
            对于 i...j 的部分之前考虑过了! 对于 j+1...i+k, 考虑拆成 i+m+(j-i) <= i+k, i+m+(j-i) > i+k 两部分
            - 对于后者, 也即 m > k-(j-i), 有 s[i+m:] < s[j+m:] 这个是因为一开始的分类条件, 而 j+m > i+k, 我们之后会考虑!
            - 对于前者, 也即 m <= k-(j-i), 因为我们总有 s[i+m] < s[j+m], 也即将考虑的坐标加上了 j-i, 因为连续不等式总会将考虑的坐标放在后续比较的范围内, 因此也不需要考虑! (转为情况1)
        综上, 下一个要枚举的对象为 max(i+k+1, j+1)
    若 s[i+k] > s[j+k]:
        我们要证明 j...j+k 都不需要枚举! (下一个枚举 j+k+1)
            类似上面, 我们同样有 s[j+m] < s[j-(j-i)+m:] < ... 因为总能将比较的对象转为我们已经考虑过的情况!
    复杂度: O(n), 因为每k次比较, i/j 至少一个会向右移动k! 总移动至多 2n
参考下面的图!
https://leetcode.cn/problems/last-substring-in-lexicographical-order/solutions/2241014/an-zi-dian-xu-pai-zai-zui-hou-de-zi-chua-31yl/
    """
    def lastSubstring(self, s: str) -> str:
        n = len(s)
        i,j = 0,1
        while j<n:
            k = 0
            while j+k < n and s[i+k] == s[j+k]:
                k += 1
            if j+k < n and s[i+k] < s[j+k]:
                i, j = j, max(j + 1, i + k + 1)  # NOTE here!
            else:
                j = j+k+1
        return s[i:]

    
sol = Solution()
result = [
    # sol.answerString(word = "dbca", numFriends = 2),

    sol.lastSubstring(s = "abab"),
]
for r in result:
    print(r)
