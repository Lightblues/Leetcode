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
https://leetcode.cn/contest/weekly-contest-411
https://leetcode.cn/circle/discuss/eDAQ8s/

T3 的 DFS+DP 非常精彩! 之后可以强化一下~ 另外TLE也非常值得警惕! 
T4 很综合, 有很多细节的地方, 详见ling的题解. 

Easonsi @2023 """
class Solution:
    """ 3258. 统计满足 K 约束的子字符串数量 I #easy 问 01 字符串的所有子串中, 满足0/1两个计数中较小值 <= k 的个数
限制: L 50
"""
    def countKConstraintSubstrings(self, s: str, k: int) -> int:
        n = len(s)
        ans = 0
        c0,c1 = 0,0
        l = 0
        for i,x in enumerate(s):
            if x == '0': c0 += 1
            else: c1 += 1
            while c0>k and c1>k:
                if s[l]=='0': c0 -= 1
                else: c1 -= 1
                l += 1
            ans += i-l+1
        return ans
        
    """ 3259. 超级饮料的最大强化能量 """
    def maxEnergyBoost(self, energyDrinkA: List[int], energyDrinkB: List[int]) -> int:
        n = len(energyDrinkA)
        ansA = energyDrinkA[:]
        ansB = energyDrinkB[:]
        ansA[1] += ansA[0]
        ansB[1] += ansB[0]
        for i in range(2, n):
            ansA[i] = max(ansA[i-1], ansB[i-2]) + energyDrinkA[i]
            ansB[i] = max(ansB[i-1], ansA[i-2]) + energyDrinkB[i]
        return max(ansA[-1], ansB[-1])
    
    """ 3260. 找出最大的 N 位 K 回文数 #hard #题型 找到长度为n的回文数字, 并且能够被k整除 
限制: n 1e5; k<=9
思路1: #DP 通过 #DFS 找到第一个满足条件的 (#贪心)
    注意到, 对于填了前缀 18 or 45, 其他位置设置为0, 假如它们 1800...0081, 4500...0054 % k 得到的数字相等, 那么中间填的就不关心了! -- 丢掉 18
    因此, DP状态为: f(i,j) 表示当前填到第i位, mod=j 时候的 (可能的) 最大回文数 -- 我们从9~1进行填, 找到第一个直接返回
        返回什么? 可以通过 DFS 找到第一个满足条件的答案! 如何记录? 可以用一个ans数组来记录! 
        边界: f(m, 0) 其中 m=n//2
        入口: f(0,0)
[ling](https://leetcode.cn/problems/find-the-largest-palindrome-divisible-by-k/solutions/2884548/tong-yong-zuo-fa-jian-tu-dfsshu-chu-ju-t-m3pu/)
"""
    def largestPalindrome(self, n: int, k: int) -> str:
        pow10 = [1] * n         # just for accelerate
        for i in range(1,n):
            pow10[i] = 10 * pow10[i-1] % k
            
        ans = [''] * n
        mid = (n+1)//2
        @lru_cache(None)
        def f(i:int, j:int) -> bool:
            if i==mid: return j==0
            
            for x in range(9,-1,-1):        # 从9开始, 贪心
                if n%2==1 and i==n//2:
                    nj = (j + x * pow10[i]) % k
                else:
                    nj = (j + x * pow10[i] + x * pow10[-1-i]) % k
                if f(i+1, nj):      # 找到第一个符合条件的即可返回
                    ans[i] = ans[-1-i] = str(x)
                    return True
            return False
        f(0, 0)
        return ''.join(ans)
    
    """ 3261. 统计满足 K 约束的子字符串数量 II #hard 继承 T1 中对于01字符串k约束的定义, 现在要求对于 q 个 [l,r] 查询 (所对应的子串) 返回结果. 
    k约束: 0/1两种字符的计数中, 较小值 <= k
    对于每个查询, 要求找到 s[l...r] 的所有k约束子串的数量. 
限制: L 1e5; q 1e5;
思路1: 确定每个位置的右边界, 然后尝试计数 (二分查找, 分成两部分相加)
    看例子: 010101, k=1
        对于每个位置作为左边界, 我们可以找到其右边界, 也即 [2,3,4,5,5,5]
    假设查询为 [1,4] 我们可以从 [3,4,5,5] 中找到4出现的位置, 这样可以分成 [3,4] 和 [5,5] 两部分 (4出现在哪个位置不重要)
        对于左边的部分, 从左边界到右边界可以全部取到, a1 = (3-1+1) + (4-2+1) = 6
        对于右边的部分, 累积 a2 = 1+2 = 3
        答案就是两部分之和 = 9
    复杂度: O(n + qlogn)
[ling](https://leetcode.cn/problems/count-substrings-that-satisfy-k-constraint-ii/solutions/2884463/hua-dong-chuang-kou-qian-zhui-he-er-fen-jzo25/)
> 下面的写法不知道为啥会 TLE? 
    原本以为复杂度: O(n+qlogn), 灵神提醒 "right[l:r+1] 是 O(n) 的，不是 O(1)。" 所以 O(qn) 就TLE了 
    """
    def countKConstraintSubstrings(self, s: str, k: int, queries: List[List[int]]) -> List[int]:
        # TLE!
        s = [int(i) for i in s]
        n = len(s)
        
        # bi-pointer to search the right bound
        right = [n-1] * n
        c = [0,0]
        r = 0
        c[s[0]] += 1
        for l,x in enumerate(s):
            if l>0: 
                c[s[l-1]] -= 1
                right[l] = right[l-1]
            while (c[0]<=k or c[1]<=k) and r<n:
                right[l] = r
                r += 1
                if r==n: break
                c[s[r]] += 1
        # 
        adds = list(x-i+1 for i,x in enumerate(right))
        acc = list(accumulate(adds, initial=0))
        # 
        ans = []
        for l,r in queries:
            idx = bisect.bisect_left(right[l:r+1], r)  # TLE 的原因在这里! right[l:r+1] 是 O(n) 的，不是 O(1)。
            a = 0
            if idx > 0: # add acc[l...l+idx)
                a += acc[l+idx] - acc[l]
            if idx <= r-l:
                _l = r-l - idx + 1 # 1+2+..._l
                a += _l * (_l+1)//2
            ans.append(a)
        return ans
    
    def countKConstraintSubstrings(self, s: str, k: int, queries: List[List[int]]) -> List[int]:
        n = len(s)
        left = [0] * n
        pre = [0] * (n + 1)
        cnt = [0, 0]
        l = 0
        for i, c in enumerate(s):
            cnt[ord(c) & 1] += 1
            while cnt[0] > k and cnt[1] > k:
                cnt[ord(s[l]) & 1] -= 1
                l += 1
            left[i] = l
            # 计算 i-left[i]+1 的前缀和
            pre[i + 1] = pre[i] + i - l + 1

        ans = []
        for l, r in queries:
            j = bisect_left(left, l, l, r + 1)
            ans.append(pre[r + 1] - pre[j] + (j - l + 1) * (j - l) // 2)
        return ans

    
sol = Solution()
result = [
    # sol.countKConstraintSubstrings(s = "10101", k = 1),
    # sol.maxEnergyBoost(energyDrinkA = [4,1,1], energyDrinkB = [1,1,3]),
    # sol.largestPalindrome(n = 3, k = 5),
    sol.countKConstraintSubstrings(s = "010101", k = 1, queries = [[0,5],[1,4],[2,3]]),
    sol.countKConstraintSubstrings("1", 1, [[0,0]]),
]
for r in result:
    print(r)
