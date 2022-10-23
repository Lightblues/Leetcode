from easonsi.util.leetcode import *

""" 
https://leetcode.cn/contest/weekly-contest-286

回头来看, 那时候写的 T3过分不优雅了些; T4

@20220223 补 """
class Solution:
    """ 2215. 找出两数组的不同 """

    """ 2216. 美化数组的最少删除数 #medium 定义美丽数组: (1) 长度为偶数; (2) 2i, 2i+1 位的数字不相同. 空数组也符合. 要求: 将一组数组转为美丽数组, 最少删除的数字个数
思路: #贪心. 每遇到 **约束对** 不满足的情况, 这两个数字必然是相同的, 随便删除一个即可.
    若出现 [..., 1,1,2,2,3,3, ...] 的情况, 不管是前面删除使得三组相同数字处于不同的约束对, 还是删除最前面的 1, 效果是一样的.
    另外需要注意最后长度必须是偶数
 """
    def minDeletion(self, nums: List[int]) -> int:
        res = 0 
        flip = -1 # 标记目前长度的奇偶
        last = None # 上一个数字
        for num in nums:
            if flip==-1:
                last = num
                flip *= -1
            else:
                if num == last:
                    res += 1
                else:
                    last = num
                    flip *= -1
        if flip == 1: # 保证是偶数长度
            res += 1
        return res

    """ 2217. 找到指定长度的回文数 #medium. 对于所有长度为 l的回文整数, 需要处理Q次查询, 每次得到这些回文数中第 k个 (不存在则返回 -1). 
思路0: 一开始非常朴素的 #递归 代码写得比较冗长. 
    注意这里回文数数量限制有两种: (1) 内部回文数可以以0开始, (2) 回文数定义, 例如长度为3的最小回文数为 101. 可知, 长度为 1/2 的回文数数量为 9, 长度为 3/4 的回文数数量为 90; 内部回文数数量为 10, 100, 1000...
    因此, 实际上是一个「进制」问题, 可以用递归来解.
    需要注意: 题目中要求得到第 ith个回文数, 从1开始; 但是在进制的计算中, 必须应该从0开始. 例如, 进制为10, 则要求得到第11个 (其实是10)回文数, 应该计算 `div(10, 10) = 1, 0`; 在本题中, 外部的需要加上1, 也即 `202`
思路1: 直接计算. 只看回文数的前半部分!
    注意到, 回文数的左半部分是 1000... 开始递增的.
    具体而言, 第q个回文数的左半部分是 10^{(l-1)//2} + q - 1. 
    细节: 对于长度为奇数的, 最后那个字符只出现一次. 
    见 [灵神](https://leetcode.cn/problems/find-palindrome-with-fixed-length/solution/fan-zhuan-hui-wen-shu-zuo-ban-bu-fen-by-4pvs0/)

输入：queries = [1,2,3,4,5,90], intLength = 3
输出：[101,111,121,131,141,999]
解释：
长度为 3 的最小回文数依次是：
101, 111, 121, 131, 141, 151, 161, 171, 181, 191, 201, ...
第 90 个长度为 3 的回文数是 999 。
 """
    def kthPalindrome(self, queries: List[int], intLength: int) -> List[int]:
        maxLen = 15+1 # intLength <=15
        # 辅助
        len2Max = [0]*maxLen # 长度为 l 的回文数的数量
        len2MaxInner = [0]*maxLen # 内部回文数的数量 (没有首位非零的约束)
        for i in range(1, maxLen):
            len2Max[i] = 9 * 10**((i-1)//2)
            len2MaxInner[i] = 10 * 10**((i-1)//2)
        # print(len2Max)

        def get_ith_palindrome_innter(l, ith):
            # 获取长度为 l 的第 ith 个内部回文数 (从0开始)
            # 这里的 ith 是从 0 开始的
            if l<=2:
                return str(ith) * l
            maximumInner = len2MaxInner[l-2]
            x, y = divmod(ith, maximumInner)
            return str(x) + get_ith_palindrome_innter(l-2, y) + str(x)
        
        def get_ith_palindrome(l, ith):
            """ 获取长度为 l 的回文数的第 ith 个
            注意这里的 ith 从1开始
             """
            maximum = len2Max[l]
            if ith > maximum:
                return -1
            if l<=2:
                return str(ith) * l
            maximumInner = len2MaxInner[l-2]
            x, y = divmod(ith-1, maximumInner) # ith 从1开始; 但是做除法的时候一定要从0开始!!!
            return str(x+1) + get_ith_palindrome_innter(l-2, y) + str(x+1)
        
        res = [get_ith_palindrome(intLength, q) for q in queries]
        return [int(i) for i in res]
    def kthPalindrome(self, queries: List[int], intLength: int) -> List[int]:
        # 思路1: 直接计算. 只看回文数的前半部分!
        ans = [-1] * len(queries)
        base = 10 ** ((intLength - 1) // 2)
        for i, q in enumerate(queries):
            if q <= 9 * base:
                s = str(base + q - 1)  # 回文数左半部分
                s += s[-2::-1] if intLength % 2 else s[::-1]
                ans[i] = int(s)
        return ans


    """ 2218. 从栈中取出 K 个硬币的最大面值和 #hard #排列组合 #题型 给定一组栈和可以取的硬币数量k, 要求取到的面值最大. 限制: 栈数量 1e3; 所有栈内元素的总数量 s 2e3; 元素大小 1e5
关联: 221021天池-04. 意外惊喜 #hard
思路1: 转化为 #分组背包 #DP
    dp[i][j] 表示从前 i 个栈中取出 j 个硬币的最大面值. 为了计算方便, 对于 piles 先取前缀和.
    遍历所用栈的数量. 对于第 i 个栈, 更新公式 `dp[i][j] = max(dp[i][j], dp[i-1][j-k] + piles[i][k])` 也即, 尝试从第 i 个栈中取出 k 个硬币.
    复杂度: O(ks). 其中s是所有栈的长度之和; k是所取的硬币数量.
        具体看代码, 可以将主循环中, 外层和内层合起来复杂度为s, 再加上中间层的循环. 
    see [灵神](https://leetcode-cn.com/problems/maximum-value-of-k-coins-from-piles/solution/zhuan-hua-cheng-fen-zu-bei-bao-pythongoc-3xnk/)
参见: https://oi-wiki.org/dp/knapsack/; 《背包九讲》
 """
    def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
        # 前缀和
        for pile in piles:
            for i in range(1, len(pile)):
                pile[i] += pile[i-1]
        # 初始化dp: 仅使用第一个栈的硬币
        dp = [0] * (k+1) # dp[i]表示取i个硬币的最大面值
        prefix = piles[0][:min(k, len(piles[0]))]
        dp[1: len(prefix)+1] = prefix
        
        # 遍历更新 dp
        for pile in piles[1:]:
            # 更新 dp[], 从 k~1
            for i in range(k, 0, -1):
                for j in range(0, min(i, len(pile))):
                    dp[i] = max(dp[i], dp[i-j-1] + pile[j])
        return dp[k]


sol = Solution()
result = [
    # sol.findDifference(nums1 = [1,2,3,3], nums2 = [1,1,2,2]),
    
    # sol.minDeletion(nums = [1,1,2,2,3,3]),
    # sol.minDeletion([1,1,2,3,4]),

    # sol.kthPalindrome(queries = [1,2,3,4,5,90], intLength = 3),
    # sol.kthPalindrome(queries = [62], intLength = 4),
    # sol.kthPalindrome([696771750,62,47,14,17,192356691,209793716,23,220935614,447911113,5,4,72], 4),
    
    sol.maxValueOfCoins(piles = [[1,100,3],[7,8,9]], k = 2),
    sol.maxValueOfCoins(piles = [[100],[100],[100],[100],[100],[100],[1,1,1,1,1,1,700]], k = 7),
]
for r in result:
    print(r)