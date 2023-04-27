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

""" T3因为数字太大的问题TLE了, 习惯Python的问题; T4带删除的字符串匹配, 自己居然想到了解法. 
https://leetcode.cn/contest/weekly-contest-332
https://leetcode.cn/circle/discuss/ayE0iI/
Easonsi @2023 """
class Solution:
    """ 6354. 找出数组的串联值 """
    def findTheArrayConcVal(self, nums: List[int]) -> int:
        ans = 0
        while nums:
            if len(nums)>=2:
                ans += int(str(nums.pop(0)) + str(nums.pop(-1)))
            else:
                ans += nums.pop()
        return ans
    
    """ 6355. 统计公平数对的数目 #medium 找到满足 lower <= nums[i] + nums[j] <= upper 的数对 """
    def countFairPairs(self, nums: List[int], lower: int, upper: int) -> int:
        nums.sort()
        ans = 0
        for i,x in enumerate(nums):
            l = bisect_left(nums, lower-x, i+1)
            r = bisect_right(nums, upper-x, i+1)
            ans += r-l
        return ans


    """ 6356. 子字符串异或查询 #median 给定一个二进制字符串, 对于一组查询 (a,b), 要求找到最左边的一个子串 s[l...r], 要求子串的值满足 val^a = b
限制: 查询数量 q 1e5; 字符串长度 n 1e4; a,b 1e9
思路1: 构建 val2index 索引
    问题等价于, 对于数字 a^b, 查询其在二进制串中的最左出现位置
    暴力枚举所有的 (l,r), 将得到的值计算好存到字典中
    细节: 二进制串对应的数字可能非常大! Python虽然可以处理但是会 #TLE. 考虑到查询的范围, 我们对于更大的数字直接终止即可!!
"""
    def substringXorQueries(self, s: str, queries: List[List[int]]) -> List[List[int]]:
        LIMIT = 10**10      # 
        s = [int(c) for c in s]
        n = len(s)
        num2idx = {}
        for l,x in enumerate(s):
            if x==0: 
                if 0 not in num2idx: num2idx[0] = (l,l)
                continue
            val = 1
            if val not in num2idx: num2idx[val] = (l,l)
            for r in range(l+1,n):
                val = (val<<1) + s[r]
                # 细节: 枚举的时候需要限制, 防止 TLE
                if val > LIMIT: break
                if val not in num2idx: num2idx[val] = (l,r)
        ans = []
        for a,b in queries:
            if a^b not in num2idx: ans.append((-1,-1))
            else: ans.append(num2idx[a^b])
        return ans
    
    
    """ 6357. 最少得分子序列 #hard 给定两个字符串 s,t 要求删除t中的字符串使其成为s的子序列, score为删除下标的 l-r, 求最小分数
限制: 字符串st长度分别为 m,n 1e5 
思路1: #二分 
    转化问题为「在score为x的基础上, 能否找到一个解?」
    贪心结构: 若代价为x, 我们可以直接删除长度为x的子串, 考虑两个边界字符串是否可以成为s的子串!
    因此, 我们只需要判断 t[:i] 和 t[i+x:] 是否可以成为 s 的子串即可!
        显然, 对于每一次检查 (i,x), 我们可以贪心地尽量靠左右匹配. 
        为此, 可以构建两个 pre, post 映射, 提前计算好t中字符串到s的匹配位置
    复杂度: 构建索引的复杂度 O(m+n), 二分的复杂度为 O(n logn) 
思路2: #前后缀分解
    反过来考虑! 考虑把字符串s分成两段, 分别尝试匹配t的首尾. 
    这样, 假设前后缀分别能匹配到的位置为 pre,suf, 则需要删除的数量为 suf-pre-1
[灵神](https://leetcode.cn/problems/subsequence-with-the-minimum-score/solution/qian-hou-zhui-fen-jie-san-zhi-zhen-pytho-6cmr/)
"""
    def minimumScore(self, s: str, t: str) -> int:
        m,n = len(s),len(t)
        pre = [inf]*(n)
        b = 0
        for i,x in enumerate(s):
            if x==t[b]:
                pre[b] = i
                b+=1
            if b==n: break
        post = [-1]*(n)
        b = n-1
        for j in range(m-1,-1,-1):
            if s[j]==t[b]:
                post[b] = j
                b-=1
            if b==-1: break
        # 二分
        def check(x):
            """ 检查去掉长为x的是否成立 """
            if x==n: return True
            if pre[n-x-1] < m or post[x] > -1: return True
            for i in range(n-x-1):
                if pre[i] < post[i+x+1]: return True
            return False
        l,r = 0,n
        ans = n
        while l<=r:
            mid = (l+r)//2
            if check(mid): 
                ans = mid
                r = mid-1
            else: l = mid+1
        return ans
    def minimumScore(self, s: str, t: str) -> int:
        n, m = len(s), len(t)
        suf = [m] * (n + 1)
        j = m - 1
        for i in range(n - 1, -1, -1):
            if j >= 0 and s[i] == t[j]:
                j -= 1
            suf[i] = j + 1
        ans = suf[0]  # 删除 t[:suf[0]]
        if ans == 0: return 0

        j = 0
        for i, c in enumerate(s):
            if c == t[j]:  # 注意 j 不会等于 m，因为上面 suf[0]>0 表示 t 不是 s 的子序列
                j += 1
                ans = min(ans, suf[i + 1] - j)  # 删除 t[j:suf[i+1]]
        return ans

    
sol = Solution()
result = [
    # sol.findTheArrayConcVal([7,52,2,4]),
    # sol.findTheArrayConcVal([5,14,13,8,12]),
    # sol.countFairPairs(nums = [0,1,7,4,4,5], lower = 3, upper = 6),
    # sol.countFairPairs(nums = [1,7,9,2,5], lower = 11, upper = 11),
    sol.substringXorQueries(s = "101101", queries = [[0,5],[1,2]]),
    sol.substringXorQueries(s = "0101", queries = [[12,8]]),
    sol.substringXorQueries(s = "1", queries = [[4,5]]),
    
    # sol.minimumScore(s = "abacaba", t = "bzaa"),
    # sol.minimumScore(s = "cde", t = "xyz"),
    # sol.minimumScore("cbedceeeccd", "ed"),
]
for r in result:
    print(r)
