import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, cache, reduce, partial
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement
import string
from string import ascii_lowercase, ascii_uppercase
import sys, os
# sys.setrecursionlimit(10000)

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)

# from utils_leetcode import testClass
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-78
@20220223 补 """
class Solution:
    """ 2269. 找到一个数字的 K 美丽值 """
    def divisorSubstrings(self, num: int, k: int) -> int:
        num = str(num)
        l = len(num)
        ans = 0
        for i in range(l-k+1):
            if int(num[i:i+k])==0: continue
            if int(num) % int(num[i:i+k]) == 0:
                ans += 1
        return ans
    
    """ 2270. 分割数组的方案数 """
    def waysToSplitArray(self, nums: List[int]) -> int:
        s = sum(nums)
        ans = 0
        cumsum = 0
        for num in nums[:-1]:
            cumsum += num
            ans += cumsum >= s-cumsum
        return ans
    
    
    """ 2271. 毯子覆盖的最多白色砖块数
    - 给定一组 [l,r] 所定义的白色砖块 (闭区间), 这些区间之间不重叠. 给一个长度为 carpetLen 的地毯, 要求返回最多可以覆盖的地砖数.
    - 思路: #贪心 注意到, 如果毯子覆盖多个区域, 我们手动令毯子的最左侧放在最左边那个区间的左端点上即可.
        - 具体而言, 可以用双指针 (i,j) 来记录毯子可以覆盖的范围, 并且用一个数字记录当前指针范围内的白色砖块数量. 遍历 j:
            - 当 `tiles[j][1] - tiles[i][0] + 1 <= carpetLen` 时, 说明足够长 j+=1
            - 否则, 需要更新答案 `ans = max(ans, tmp + max(0, carpetLen + tiles[i][0] - tiles[j][0]))` 并更新 i+=1#贪心 注意到, 如果毯子覆盖多个区域, 我们手动令毯子的最左侧放在最左边那个区间的左端点上即可.

输入：tiles = [[1,5],[10,11],[12,18],[20,25],[30,32]], carpetLen = 10
输出：9
解释：将毯子从瓷砖 10 开始放置。
总共覆盖 9 块瓷砖，所以返回 9 。
注意可能有其他方案也可以覆盖 9 块瓷砖。
可以看出，瓷砖无法覆盖超过 9 块瓷砖。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/maximum-white-tiles-covered-by-a-carpet
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
    """
    def maximumWhiteTiles(self, tiles: List[List[int]], carpetLen: int) -> int:
        tiles.sort()
        # 加一个哨兵
        tiles.append([carpetLen+tiles[-1][1],carpetLen+tiles[-1][1]])
        ans = 0
        i,j = 0, 0
        tmp = 0     # 记录 [i, j-1] 的区间和
        while j < len(tiles):
            # 第j个区间可以被包含
            if tiles[j][1] - tiles[i][0] + 1 <= carpetLen:
                tmp += tiles[j][1] - tiles[j][0] + 1
                j += 1
            else:
                ans = max(ans, tmp + max(0, carpetLen + tiles[i][0] - tiles[j][0]))
                tmp += - (tiles[i][1] - tiles[i][0] + 1)
                i += 1
        return ans
        
    """ 2272. 最大波动的子字符串 #题型 #hard
定义字符串的波动为「出现次数 最多 的字符次数与出现次数 最少 的字符次数之差」. 要求计算一个字符串中, 所有可能的连续子串的波动最大值.
注意, 这里有一个限制是, 加入最多最少的字符是 a/b, 则要求b一定要在子串中出现.
复杂度: 长度为 1e4
思路1: 转为 #最大子数组和 问题 + 变形
    注意到, 假若我们关注的是 a/b 次数之差, 则将它们记作 +1/-1, 其他字符记作 0, 则问题转为求子数组最大和问题. 题目复杂度为 1e4, 暴力遍历 a/b 的组合即可.
    需要注意的是, 与原问题不同之处在于, 题目要求子串中一定要包括 b: 而原本 最大子数组和 的DP: `dp[i+1] = dp[i] + nums[i+1] * (nums[i+1] > 0)` 无法记录是否包含了b.
    为此, 相较于记录两数字之差的 `diff` (dp迭代的数字), 这里加了一个辅助变量.
        当遇到 b时, 我们先 `diff -= 1` 并且用 `diff_with_b = diff` 记录, 然后再 `diff = max(diff, 0)` 更新;
        当遇到 a时, 直接对于 `diff, diff_with_b` +1.
    注意到, 相较于 diff>=0, 这里的变量 diff_with_b 最小值为 -1 (延后执行了 max(0, diff)), 因此是「包含了b的a/b最大差」.
    优化: 上面的时间复杂度为 O(n * 26^2), 空间复杂度 O(1)
        注意到这里 a/b 之外的字母取值都为 0, 而我们每次是针对 a/b 更新的, 因此实际上计算浪费了.
        可以用 diff[a][b] 记录两字母的差值, 随着对于字符串的遍历更新矩阵中的相关元素. 这样, 计算复杂度为 O(n * 26).
        具体见 [here](https://leetcode.cn/problems/substring-with-largest-variance/solution/by-endlesscheng-5775/)
思路2: 动态规划
    [这里](https://leetcode.cn/problems/substring-with-largest-variance/solution/mei-ju-chu-xian-zui-duo-he-zui-shao-de-z-g9gz/) 给出了更容易想到的思路
    我们用 dp0 正常求解最大子数组和; 另外用一个 dp1 记录「以第i个字符结尾的, 至少包括一个b的的最大差值」.
    注意两者的更新公式区别在于, `nums[i+1]==b` 时后者需要考虑 dp0[i] 的转移.

输入：s = "aababbb"
输出：3
解释：
所有可能的波动值和它们对应的子字符串如以下所示：
- 波动值为 0 的子字符串："a" ，"aa" ，"ab" ，"abab" ，"aababb" ，"ba" ，"b" ，"bb" 和 "bbb" 。
- 波动值为 1 的子字符串："aab" ，"aba" ，"abb" ，"aabab" ，"ababb" ，"aababbb" 和 "bab" 。
- 波动值为 2 的子字符串："aaba" ，"ababbb" ，"abbb" 和 "babb" 。
- 波动值为 3 的子字符串 "babbb" 。
所以，最大可能波动值为 3 。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/substring-with-largest-variance
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def largestVariance(self, s: str) -> int:
        import string
        ans = 0
        for a in string.ascii_lowercase:
            for b in string.ascii_letters:
                if b==a: continue
                # 这里用 diff_ab 记录 max(0, count(a) - count(b)), 用 count_b 记录 b 出现的次数 (为了避免全为a的子序列的情况)
                # 但是有问题: 对于 "baaaa" 的情况无法处理
                # diff_ab, count_b = 0, 0
                # if a=="a" and b=="l":
                #     print()
                # for ch in s:
                #     if ch == a: 
                #         diff_ab += 1
                #         if count_b > 0: ans = max(ans, diff_ab) 
                #     elif ch ==b:
                #         if diff_ab > 0: 
                #             diff_ab -= 1
                #             count_b += 1
                #         else:
                #             # 否则从头开始计数
                #             diff_ab = 0
                #             count_b = 0
                
                """ 换一种思路: 每次
                diff 记录目前为止的 max(0, count(a) - count(b)), 而 diff_with_b 记录了每次遇到 b 的时候的 diff"""
                diff, diff_with_b = 0, -float("inf")
                for ch in s:
                    if ch == a:
                        diff += 1
                        diff_with_b += 1
                    elif ch == b:
                        diff -= 1       # diff 最小为 -1
                        # 记录每一次出现 b 的时候的 diff
                        diff_with_b = diff
                        diff = max(diff, 0)
                    # 包含了: diff_with_b >= 0
                    if diff_with_b > ans:
                        ans = diff_with_b
        return ans
    
    
sol = Solution()
result = [
    # sol.divisorSubstrings(num = 430043, k = 2),
    
    # sol.waysToSplitArray(nums = [10,4,-8,7]),
    
    # sol.maximumWhiteTiles(tiles = [[1,5],[10,11],[12,18],[20,25],[30,32]], carpetLen = 10),
    # sol.maximumWhiteTiles(tiles = [[10,11],[1,1]], carpetLen = 2),
    
    sol.largestVariance(s = "aababbb"),
    sol.largestVariance("abcde"),
    sol.largestVariance("lripaa"),
]
for r in result:
    print(r)
