from typing import *
from math import comb
from collections import defaultdict
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
T3 比较有趣, "枚举右，维护左" 的思路很巧妙, 需要进行一定的转换
T4 组合数学

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

    """ 3404. 统计特殊子序列的数目 #medium 但实际上 #hard 找四元组 (p,q,r,s) 的数量, 要求满足两两index相差至少2, 且元素值 p*r = q*s 
限制: n 1e3
思路1: **枚举右，维护左**
    考虑经典题目: 找到数组中 (i,j) 相等的数对数量. 怎么做? 枚举的时候, 先考虑其作为j和前面匹配的数量, 然后将枚举的位置作为i加入到一个hash表中!
    本题中, 要求 a*c = b*d, 将其变换为 a/b = d/c -- 这样两边的index是分开的比较好枚举
    我们枚举c, 考虑它和d的匹配在前序的数量; 还要将作为b的前序增量加入到hash表中!
    注意! 本题由于有不相邻的要求, 有一个技巧: 先将b加入到hashmap中, 再统计cd!
    复杂度: O(n^2); 空间复杂度 O(min{n^2, U^2}), 参见ling, 主要原因是根据欧拉函数, 互质数字是很常见的, 因此数量很多
    一个问题: 为什么下面可以直接用 浮点数作为 hashmap的key? 
        想想什么情况会产生浮点误差? 考虑两个接近1的浮点数 a/(a+1) 和 (a-1)/a, 
        两者差值 1/a(a+1) < 2^(-52) 的时候才会产生误差, 也即 a > 2^26, 因此本题范围安全
        若担心误差问题, 可以基于 GCD 将key转为最简分数! -- 带来一定的计算开销
思路2: #前后缀分解 先统计cd, 然后枚举ab的过程中 "撤销" 后缀统计, 整体复杂度也为 O(n^2), 见ling
[ling](https://leetcode.cn/problems/count-special-subsequences/solutions/3033284/shi-zi-bian-xing-qian-hou-zhui-fen-jie-p-ts6n/)
"""
    def numberOfSubsequences(self, nums: List[int]) -> int:
        n = len(nums); ans = 0
        cnt = defaultdict(int)
        # 核心是枚举 b,c
        for i in range(4, n-2):  # c 可能的范围
            # 先更新 b
            b = nums[i-2]  # c的位置为i; 此时可考虑的b的位置到 i-2 结束
            for a in nums[:i-3]:
                cnt[a/b] += 1

            # 枚举 c,d
            c = nums[i]
            for d in nums[i+2:]:
                ans += cnt[d/c]
        return ans


    """ 3405. 统计恰好有 K 个相等相邻元素的数组数目 #hard 给定整数 n,m,k, 长度为n的好数组需要满足, 1) 所有元素都在 [1,m] 范围内, 2) 恰好有k个下标满足 arr[i-1] = arr[i]
问好数组的数目, 限制: n 1e5; 结果取模1e9+7
思路1 #组合数学
    注意到, 有k组相同元素值相等, 则长n的数组可以划分为 n-k 个区间, 每个区间内数字相等!
    组合数学, 这样划分方式有 C(n-1, n-k-1) -- 考虑隔板放置位置
        对于每个划分, 放置数字的可能性有 m * (m-1)^(n-k-1)
[ling](https://leetcode.cn/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/solutions/3033292/chun-shu-xue-ti-pythonjavacgo-by-endless-mxj7/)
     """
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        return comb(n-1, n-k-1) * m * pow(m-1, n-k-1, MOD) % MOD


sol = Solution()
result = [
    # sol.answerString(word = "dbca", numFriends = 2),

    # sol.lastSubstring(s = "abab"),

    # sol.numberOfSubsequences(nums = [3,4,3,4,3,4,3,4]),

    sol.countGoodArrays(n = 4, m = 2, k = 2),
]
for r in result:
    print(r)
