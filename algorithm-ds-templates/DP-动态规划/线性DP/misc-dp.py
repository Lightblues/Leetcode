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
Easonsi @2023 """
from functools import cache
class Solution:
    """ 0221. 最大正方形 #medium 0/1矩阵中最大的全1正方形面积. 限制: n 300
思路1: #DP
    f[i,j] 表示以 (i,j) 为右下角的最大正方形边长
    递推: min(f(i-1,j),f(i,j-1),f(i-1,j-1))+1
     """
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        m,n = len(matrix),len(matrix[0])
        @cache
        def f(i,j):
            if i<0 or j<0 or matrix[i][j]=='0': return 0
            return min(f(i-1,j),f(i,j-1),f(i-1,j-1))+1
        return max(f(i,j) for i in range(m) for j in range(n))**2
    
    """ 1458. 两个子序列的最大点积 #hard #题型 给定两个数组, 要求他们的一对相同长度的非空子序列的最大点积. 限制: 长度n 500, 数值范围 -100~100
思路1: #DP 注意非空!
    f[i,j] 表示子问题, 则有转移 max{ f(i-1,j), f(i,j-1), max{f(i-1,j-1),0} + nums1[i]*nums2[j] } 注意这里可以不用 (i-1,j-1) 转移
    """
    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
        m,n = len(nums1),len(nums2)
        @cache
        def f(i,j):
            # 注意非空! 有负数! 
            if i==j==0: return nums1[i]*nums2[j]
            elif i==0: return max(f(i,j-1), nums1[i]*nums2[j])
            elif j==0: return max(f(i-1,j), nums1[i]*nums2[j])
            return max(
                f(i-1,j), f(i,j-1),
                f(i-1,j-1)+nums1[i]*nums2[j], nums1[i]*nums2[j]
            )
        return f(m-1,n-1)
    
    """ 0727. 最小窗口子序列 #hard 对于目标字符串T, 要从S中找到最短的子串, 是的T是其子序列. 
限制: S 长度 2e4; T 100
思路1: #滑动窗口 在每次匹配完成之后, 从后往前匹配! 
思路2: #DP 
    定义 f[i,j] 表示 S[:i] 完成 T[:j] 匹配的最右start位置
    递推: f[i,j] = max{ f[i-1,j], f[i-1,j-1] if S[i]==T[j] else -1 }
    如何记录子序列? 只有在 S[i]==T[j] 的时候才更新
2.1 如何展开成迭代形式? 注意到 递推式中仅依赖于 f[i-1,j] 和 f[i-1,j-1], 因此可以用滚动数组优化
    边界: j==0
[官答](https://leetcode.cn/problems/minimum-window-subsequence/solution/zui-xiao-chuang-kou-zi-xu-lie-by-leetcode/)
    """
    def minWindow(self, s1: str, s2: str) -> str:
        # 思路2; 但是爆栈了! 
        n,m = len(s1),len(s2)
        mnLen = inf; mnStr = ''
        @cache
        def f(i,j):
            if i<0 or j<0: return -1
            nonlocal mnLen, mnStr
            ans = f(i-1,j)
            if s1[i]==s2[j]:
                # 注意边界
                if j==0: ans = i
                ans = max(ans, f(i-1,j-1))
                if ans>=0 and j==m-1 and i-ans+1<mnLen:
                    mnLen = i-ans+1
                    mnStr = s1[ans:i+1]
            return ans
        f(n-1,m-1)
        return mnStr
    
    def minWindow(self, s1: str, s2: str) -> str:
        n,m = len(s1),len(s2)
        # 边界
        # if m==1: return s2 if s2 in s1 else ''
        
        cur = [-1]*n
        for j,c in enumerate(s2):
            old = cur
            cur = [-1]*n
            start = -1
            for i,cc in enumerate(s1):
                if cc==c:
                    if j==0: start = i
                    else:
                        if i>0: start = max(start, old[i-1])
                cur[i] = start
        
        mnLen = inf; mnStr = ''
        for i in range(n):
            if cur[i]>=0 and i-cur[i]+1<mnLen:
                mnLen = i-cur[i]+1
                mnStr = s1[cur[i]:i+1]
        return mnStr
    
    """ 0486. 预测赢家 #medium 轮流从数组两侧选择取数字, 问先手是否能赢? (相等分数也算赢) 限制: n 20
    f[i,j] 表示在区间 [i,j] 中先手与后手的分数差 
    """
    def PredictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)
        @cache
        def f(i,j):
            if i==j: return nums[i]
            return max(nums[i]-f(i+1,j), nums[j]-f(i,j-1))
        return f(0,n-1)>=0

    
    """ 0312. 戳气球 #hard 倒过来看变成放气球 f[i,j] 表示填充开区间 (i,j) 可以获得的最大分数
思路1: #DP
    递推: f[i,j] = max{ val[i]*val[mid]*val[j] + f[i,mid] + f[mid,j] }
    复杂度: O(n^3)
[官答](https://leetcode.cn/problems/burst-balloons/solution/chuo-qi-qiu-by-leetcode-solution/)
    """
    def maxCoins(self, nums: List[int]) -> int:
        n = len(nums)
        nums = [1] + nums + [1]
        @cache
        def f(i,j):
            if i+1==j: return 0
            return max(
                nums[i]*nums[mid]*nums[j] + f(i,mid) + f(mid,j)
                for mid in range(i+1,j)
            )
        return f(0,n+1)
    
    """ 0471. 编码最短长度的字符串 #hard 对于重复的子串可以进行压缩表示, 例如 ababab 可以表示为 3[ab], 问字符串的最小表示; 限制: n 150
思路1: #DP 
    假设我们知道了如何得到字符串的最小循环长度 [0459. 重复的子字符串], 函数g返回编码得到的长度
    f[i,j] 表示最小编码. 递推 f[i,j] = min{ f[i,k]+f[k+1,j] } 如果 g[i,j] 可以的话加一项
    
    """
    def encode(self, s: str) -> str:
        n = len(s)
        @cache
        def g(i,j):
            """ 检测 sub 是否为重复子字符串, 返回最优编码 """
            sub = s[i:j+1]
            if j-i+1 <= 4: return sub
            idx = (sub+sub).find(sub,1)
            # if idx!=j-i+1: return f"{len(sub)//idx}[{sub[:idx]}]"
            # 注意到对于sub需要递归编码!!
            if idx!=j-i+1: return f"{len(sub)//idx}[{f(i,i+idx-1)}]"
            return sub
        @cache
        def f(i,j):
            if j-i+1 <= 4: s[i:j+1]
            ans = g(i,j)        # 先检测是否有重复子字符串
            for k in range(i,j):
                a = f(i,k) + f(k+1,j)
                if len(a)<len(ans): ans = a
            return ans
        return f(0,n-1)
    
    
    """ 1594. 矩阵的最大非负积 #题型
给定一个grid, 问从左上角到右下角的所有路径中, 最大的非负积是多少?
提示: 应该存储的信息不是「能取到的最大正数/最小负数是多少」, 而应该是以当前点结束的路径值的范围.
思路1: 用DP存储路径中的最大和最小值 (注意, 不是大于/小于零的部分). 
    这是因为, 假设长为l-1的路径可以取到的范围 `[mn,mx]`, 若当前数值x为正, 则不管该区间范围是正是负, 新的范围总是 `[x*mn, x*mx]`, 反之亦然.
    见 [官答](https://leetcode.cn/problems/maximum-non-negative-product-in-a-matrix/solution/ju-zhen-de-zui-da-fei-fu-ji-by-leetcode-solution/)
"""
    def maxProductPath(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])
        @cache
        def dp(i, j):
            """ 返回到 (i,j) 的路径 mx,mn """
            # 边界条件
            if i==0 and j==0:
                return grid[0][0], grid[0][0]
            # 访问越界
            if i < 0 or j < 0:
                # return -inf, inf
                return None, None
            else:
                results = []
                for x in dp(i, j-1)[0], dp(i, j-1)[1], dp(i-1, j)[0], dp(i-1, j)[1]:
                    # if -inf < x < inf:
                    if x is not None:
                        results.append(grid[i][j] * x)
                return (
                    max(results),
                    min(results)
                )
        res = dp(rows-1, cols-1)[0]
        if res < 0: return -1
        # else: return int(res % (1e9 + 7))
        else: return res % (10**9 + 7)


    """ 0459. 重复的子字符串 #easy #题型 #hard 给定一个字符串, 判断它是否由重复的子串拼接构成 限制: n 1e4
思路0: 暴力尝试, 复杂度 O(n^2)
思路1: 
    假设字符串 s = tt..t 拼接起来的, 我们拼接两个s, 那么 ss = tt...tt
    这样, 我们取出ss的头尾两个字符, 如果s仍然是该字符串的子串, 那么就是可以的! 并且找到的第一个位置就是循环节! 
    复杂度: 利用了Python自带的 find函数, 应该是 O(n)?
    """
    def repeatedSubstringPattern(self, s: str) -> bool:
        return (s+s).find(s,1) != len(s)

    """ 0120. 三角形最小路径和 #medium f(i,j) 表示到 (i,j) 的最小路径
    转移方程: f[i,j] = min{ f[i-1,j], f[i-1,j-1] } + tri[i][j]
    """
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        n = len(triangle)
        @cache
        def f(i,j):
            # 边界条件
            if i==j==0: return triangle[0][0]
            # 访问不合法
            if i<0 or j<0 or i<j: return inf
            # 状态转移
            return triangle[i][j] + min(f(i-1,j-1), f(i-1,j))
        return min(f(n-1,j) for j in range(n))

    """ 0005. 最长回文子串 #medium `f[i,j]` 表示是否回文 """
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        @cache
        def f(i,j):
            if i>=j-1: return s[i]==s[j]
            return s[i]==s[j] and f(i+1,j-1)
        mx,ans = 0,""
        for i in range(n):
            for j in range(i,n):
                if f(i,j) and j-i+1>mx:
                    mx = j-i+1
                    ans = s[i:j+1]
        return ans
    
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        flag = [[False]*n for _ in range(n)]
        for i in range(n):
            flag[i][i] = True
        for l in range(2, n+1):
            for i in range(n-l+1):
                j = i+l-1
                if l==2:
                    flag[i][j] = s[i]==s[j]
                else:
                    flag[i][j] = s[i]==s[j] and flag[i+1][j-1]
        mxL, ans = 0, ""
        for i in range(n):
            for j in range(i,n):
                if flag[i][j] and j-i+1>mxL:
                    mxL = j-i+1
                    ans = s[i:j+1]
        return ans 

sol = Solution()
result = [
    # sol.maxDotProduct(nums1 = [2,1,-2,5], nums2 = [3,0,-6]),
    # sol.maxDotProduct([-1,-1], [1,1]),
    # sol.minWindow("abcdebdde", "bde"),
    # sol.minWindow("jmeqksfrsdcmsiwvaovztaqenprpvnbstl","k"), 
    # sol.minWindow("cnhczmccqouqadqtmjjzl", "mm"), 
    # sol.maxCoins(nums = [3,1,5,8]),
    # sol.encode("aaaaa"),
    # sol.encode( "abbbabbbcabbbabbbc"),
    # sol.minimumTotal(triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]),
    # sol.maxProductPath(grid = [[-1,-2,-3],
    #          [-2,-3,-3],
    #          [-3,-3,-2]]),
    # sol.maxProductPath(grid = [[1,-2,1],
    #          [1,-2,1],
    #          [3,-4,1]]),
    sol.longestPalindrome(s = "babad"),
    sol.longestPalindrome("gphyvqruxjmwhonjjrgumxjhfyupajxbjgthzdvrdqmdouuukeaxhjumkmmhdglqrrohydrmbvtuwstgkobyzjjtdtjroqpyusfsbjlusekghtfbdctvgmqzeybnwzlhdnhwzptgkzmujfldoiejmvxnorvbiubfflygrkedyirienybosqzrkbpcfidvkkafftgzwrcitqizelhfsruwmtrgaocjcyxdkovtdennrkmxwpdsxpxuarhgusizmwakrmhdwcgvfljhzcskclgrvvbrkesojyhofwqiwhiupujmkcvlywjtmbncurxxmpdskupyvvweuhbsnanzfioirecfxvmgcpwrpmbhmkdtckhvbxnsbcifhqwjjczfokovpqyjmbywtpaqcfjowxnmtirdsfeujyogbzjnjcmqyzciwjqxxgrxblvqbutqittroqadqlsdzihngpfpjovbkpeveidjpfjktavvwurqrgqdomiibfgqxwybcyovysydxyyymmiuwovnevzsjisdwgkcbsookbarezbhnwyqthcvzyodbcwjptvigcphawzxouixhbpezzirbhvomqhxkfdbokblqmrhhioyqubpyqhjrnwhjxsrodtblqxkhezubprqftrqcyrzwywqrgockioqdmzuqjkpmsyohtlcnesbgzqhkalwixfcgyeqdzhnnlzawrdgskurcxfbekbspupbduxqxjeczpmdvssikbivjhinaopbabrmvscthvoqqbkgekcgyrelxkwoawpbrcbszelnxlyikbulgmlwyffurimlfxurjsbzgddxbgqpcdsuutfiivjbyqzhprdqhahpgenjkbiukurvdwapuewrbehczrtswubthodv"),
]
for r in result:
    print(r)
