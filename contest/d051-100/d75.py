from easonsi import utils
from easonsi.util.leetcode import *
""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220428 补 """
class Solution:
    """ 2220. 转换数字的最少位翻转次数
利用 Python 遍历直接转为字符串了
正规的思路应该是用位运算, 异或
    """
    def minBitFlips0(self, start: int, goal: int) -> int:
        s1, s2 = bin(start)[2:], bin(goal)[2:]
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        s1 = "0"*(len(s2)-len(s1)) + s1
        return sum(1 if s1[i] != s2[i] else 0 for i in range(len(s2)))
    
    def minBitFlips(self, start, goal):
        a = start ^ goal
        # return bin(a).count('1')
        
        # 标准
        ans = 0
        while a:
            ans += a & 1
            a >>= 1
        return ans
    
    """ 2221. 数组的三角和
对于一个数组, 重复进行如下操作, 直到长度为 1, 返回最后的数据
将相邻两个元素相加, 得到新的长度 -1 的数组. 

就是杨辉三角, 调用 math.comb(n-1, i) 即可.

图示参见 https://leetcode-cn.com/problems/find-triangular-sum-of-an-array/
    """
    def triangularSum(self, nums: List[int]) -> int:
        n = len(nums)
        res = 0
        for i in range(n):
            res += math.comb(n-1, i) * nums[i]
        return res % 10
    
    """ 2222. 选择建筑的方案数
有两类建筑, 要求从中选择三栋, 选择的三个中相邻的类别不能相同. 返回所有方案的数量.

思路: 1) 考虑中间的那栋楼, 则两侧的选择必须是另外一个类型; 2) 为了计数, 考虑 cumsum; 3) 为了避免确定变量, 可以讲 "001101" 转为 [2,2,1,1] 的形式
具体而言, 可以分别从左到右, 从右到左计算累加和, 然后直接 `cumsumLeft[i-1] * newS[i] * cumsumRight[i+1]` 即可.

写得复杂了, 由于形式只可能为 010/101, 实际上遍历一次index即可; 记录下目前已有的 1, 则遇到0时, 以这个0为中间数的方案数为 `count_a * total_a - count_a`, 
参见 [here](https://leetcode-cn.com/problems/number-of-ways-to-select-buildings/solution/xuan-ze-jian-zhu-de-fang-an-shu-by-leetc-jhup/)
"""
    def numberOfWays(self, s: str) -> int:
        # 转换 s 形式, 例如 "001101" 转为 [2,2,1,1]
        newS = []
        last = ""
        count = 0
        for i,ch in enumerate(s+"-"):
            if ch!=last:
                last = ch
                if i!=0:
                    newS.append(count)
                count = 1
            else:
                count += 1
        # 计算累加和
        cumsumLeft, cumsumRight = newS[:], newS[:]
        for i in range(2, len(newS)):
            cumsumLeft[i] += cumsumLeft[i-2]
            cumsumRight[-i-1] += cumsumRight[-i+1]
        # 累计
        ans = 0
        for i in range(1, len(newS)-1):
            ans += cumsumLeft[i-1] * newS[i] * cumsumRight[i+1]
        return ans
    
    """ 2223. 构造字符串的总得分和
对于一个字符串, 从右往左得到长度为 1,2,... 的连续子串, 分别计算该子串与原字符串的最大前缀长.

输入：s = "babab"
输出：9
解释：
s1 == "b" ，最长公共前缀是 "b" ，得分为 1 。
s2 == "ab" ，没有公共前缀，得分为 0 。
s3 == "bab" ，最长公共前缀为 "bab" ，得分为 3 。
s4 == "abab" ，没有公共前缀，得分为 0 。
s5 == "babab" ，最长公共前缀为 "babab" ，得分为 5 。
得分和为 1 + 0 + 3 + 0 + 5 = 9 ，所以我们返回 9 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sum-of-scores-of-built-strings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

Z 函数（扩展 KMP） 参见 https://oi-wiki.org/string/z-func/
我们定义 Z 函数为: z[i] 为 s[i:n-1] 与原字符串 s 的最长前缀匹配长度.
核心是要维护一个匹配区间 [l,r] (闭区间) 满足该区间为前缀; 在遍历过程中, 维护 `l<=i`.
    对于遍历到的 i, 若 `i<=r`, 此时有 `s[i:r] = s[i-l:r-l]` (闭区间),
        若还满足 z[i-l]<r-i+1 (区间 [i,r] 的长度为 r-i+1, 我们已经在遍历 i-l 时发现了前缀匹配长度比它小), 则有 z[i] = z[i-l]
        否则, 说明 [i,r] 区间是前缀, 从 r+1 开始继续匹配
    若不满足 `i<=r`, 则从 i+1 开始继续匹配 (和上面的情况2一样)
    注意当我们遍历超过 r 时需要更新 `l, r = i, i+z[i]-1` (显然维护的条件 `i<=l` 仍满足)
复杂度分析 (看下面的代码): 外层 i 循环一遍, 内部的 while 训练每执行一次都会使得 r 向后移动, 因此最多执行 O(n) 次; 所以总的复杂度为 O(n).
    """
    def sumScores_v0(self, s: str) -> int:
        """ 暴力方法, 时间复杂度 O(n^2) 会超时 """
        n = len(s)
        z = [0] * n
        for i in range(1, n):
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                z[i] += 1
        return sum(z) + n

    def sumScores(self, s: str) -> int:
        n = len(s)
        z = [0] * n
        l,r = 0,0
        for i in range(1,n):
            if i<=r and z[i-l]<r-i+1:
                z[i] = z[i-l]
            else:
                z[i] = max(0, r-i+1)
                while i+z[i]<n and s[z[i]]==s[i+z[i]]:
                    z[i] += 1
            if i+z[i]-1 > r:
                r = i+z[i]-1
                l = i
        return sum(z) + n
        

sol = Solution()
result = [
    # sol.minBitFlips(start = 10, goal = 7),
    # sol.minBitFlips(start = 3, goal = 4),
    
    # sol.numberOfWays(s = "001101"),
    
    sol.sumScores(s = "babab"),
    sol.sumScores(s = "azbazbzaz"),
]
for r in result:
    print(r)
