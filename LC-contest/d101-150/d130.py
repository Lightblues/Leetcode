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
https://leetcode.cn/contest/biweekly-contest-130
T3 的DP, 原本的思路超时了orz, 有一个等价表述! 
T4 数位DP, 试填法 相对比较复杂 -- 但需要细致的分析, 很考验代码基础! 
Easonsi @2025 """
class Solution:
    """ 3142. 判断矩阵是否满足条件 """
    def satisfiesConditions(self, grid: List[List[int]]) -> bool:
        n, m = len(grid), len(grid[0])
        for i in range(m-1):
            if grid[0][i] == grid[0][i+1]: return False
        for i in range(m):
            col = [grid[j][i] for j in range(n)]
            if len(set(col)) != 1: return False
        return True

    """ 3143. 正方形中的最多点数 """
    def maxPointsInsideSquare(self, points: List[List[int]], s: str) -> int:
        dist2cnt = defaultdict(Counter)
        for (x,y),l in zip(points, s):
            dist2cnt[max(abs(x), abs(y))][l] += 1
        labels = set()
        for dist in sorted(dist2cnt):
            cnt = dist2cnt[dist]
            if max(cnt.values()) > 1: break
            if set(cnt.keys()) & labels: break
            labels |= set(cnt.keys())
        return len(labels)
    

    """ 3144. 分割字符频率相等的最少子字符串 #medium 平衡字符串: 出现的字符数量相等. 问一个字符串分隔为平衡字符串的最少数量. 
限制: n 1e3
思路1: #DP
    记 f[i] 表示前i个字符构成的字符串的最少分割数量 (子问题), 则 f[j] = min(f[k]) + 1) for k in range(i,j) if check(k...j)
    如何完成 check(k...j)? 要检查这个子字符串是否满足, 
        一种方法是通过 s[:i] 的所有前缀cnt, 从而检查 k...j 的字符分布情况 -- 下面第一种方案 TLE 了
        另外, 可以从右往左遍历! 通过中间出现情况为 cnt, 记录中间字符出现的最大次数, 则 max_cnt * len(cnt) == i-j+1 的情况正是题解!
ling: https://leetcode.cn/problems/minimum-substring-partition-of-equal-character-frequency/solutions/2775377/hua-fen-xing-dpji-yi-hua-sou-suo-di-tui-s1nq0/
    """
    # def minimumSubstringsInPartition(self, s: str) -> int:
    #     # NOTE: TLE (memory?)
    #     n = len(s)
    #     pre = [None] * (n+1)
    #     cnt = [0] * 26
    #     pre[0] = cnt[:]
    #     for i,x in enumerate(s):
    #         cnt[ord(x)-ord('a')] += 1
    #         pre[i+1] = cnt[:]
    #     # dp
    #     def check(i,j):
    #         c = [pre[j+1][k] - pre[i][k] for k in range(26)]
    #         return len(set(e for e in c if e>0)) == 1
    #     f = [0] * (n+1) # take care of the indexs!
    #     f[1] = 1
    #     for i in range(1, n):
    #         f[i+1] = f[i] + 1
    #         for j in range(i):
    #             if check(j,i):
    #                 f[i+1] = min(f[i+1], f[j] + 1)
    #     return f[-1]
    def minimumSubstringsInPartition(self, s: str) -> int:
        n = len(s)
        f = [0] * (n+1)
        f[1] = 1
        for i in range(1, n):
            f[i+1] = f[i] + 1
            cnt = defaultdict(int)
            max_cnt = 0
            for j in range(i, -1, -1): # 从右往左, 
                cnt[s[j]] += 1
                max_cnt = max(max_cnt, cnt[s[j]])
                if max_cnt * len(cnt) == i-j+1: # 注意这里的边界条件! 
                    f[i+1] = min(f[i+1], f[j] + 1)
        return f[-1]

    """ 3145. 大数组元素的乘积 #hard 定义一个数的二进制分解为: 6 = 2+4, 7 = 1+2+4. 将自然数的二进制分解拼接得到 big_nums = [1, 2, 1,2, 4, ...]
对于每个 query = (from, to, mod), 计算 big_nums[from...to] 累乘 mod 的结果. 
限制: q 500; range 1e15
思路1: #数位DP + #二分
    对于 (from, to), 将两端位数所属的原本的数字记作 L,R, 则可以将其分为3段 (from, l), (l+1,r-1), (r, to). 分别统计. 
    如何找到 L/R? 二分, 我们需要 "[1...x] 所对应的 big_nums 的前缀长度 (数位数量)"
        采用 #试填法. 例如, 对于 0x1100, 我们计算其前缀长度. 
            对于第1位的1, 假设其取0, 后面3位可以任意填, 每一位取1的贡献次数为 2^{3-1}=4, 合计贡献 3*4=12.
            对于第2位的1, 假设其取0, 后面2位可以任意填, 每一位取1的贡献次数为 2^{2-1}=2, 贡献 2*2=4. 注意! 此时前缀 10 贡献 1* 2^2 = 4
            ... 后面0位需要跳过
            最后, 加上 1100 中出现的2次. 共计 12 + (4+4) + 2 = 22
    如何计算 [L+1, R-1] 的二进制分解的乘积? (取log2) 转为位数的累加! 
        f(l,r) = f(1,r) - f(1,l-1)  -> 转为前缀和, 同样 #试填法
        注: 和上面的区分在于, 上面每一位的贡献位1, 现在是其对应的位数了! 
    官方: https://leetcode.cn/problems/find-products-of-elements-of-big-array/solutions/2886821/da-shu-zu-yuan-su-de-cheng-ji-by-leetcod-o0nf/
ling: https://leetcode.cn/problems/find-products-of-elements-of-big-array/solutions/2774549/olog-shi-tian-fa-pythonjavacgo-by-endles-w2l4/
这也太优雅了!!!
    """


sol = Solution()
result = [
    # sol.satisfiesConditions(grid = [[1,0,2],[1,0,2]]),
    # sol.satisfiesConditions(grid = [[1,1,1],[0,0,0]]),
    # sol.satisfiesConditions([[1],[2],[3]]),
    # sol.maxPointsInsideSquare(points = [[2,2],[-1,-2],[-4,4],[-3,1],[3,-3]], s = "abdca"),
    sol.minimumSubstringsInPartition("bb"),
    sol.minimumSubstringsInPartition(s = "fabccddg"),
    sol.minimumSubstringsInPartition("abababaccddb"),
    sol.minimumSubstringsInPartition("etzyyytttttthehhhyssroqnnnwxxcbbzvovroeiijjneeeeeeevuvutthjjrrrrrhepeeeerqqrrqqausstfgffgggfsseppehdhhfnwthktejjkkjkapoxieppppsldccgqqzzzzzzzaaacbzlooeemsxxdvccvwvsskkkkpijkoooooqoqvvvvucpqduuhhkuehghghhzjigjgoqoqqnqnjirrcbckkfeekpnoqolddeeeeennnsuwvttttsvsvkkdcgkljnnjlottttpqgfiitttyqqqfdnnzvveeeemibghssssmmnheggiixxppjqtusvuqhhhijjnjjjgjjifzzzouucjjjggreqoapiccabarrwtstvvtdvnnmfehhgnooglhgfvuumlmlgggsrrsnxssxxxxicceeyrvkfffhffegmhhhhbbhhhqqbbbhlonnmlhnkxwwvvsnnxxxxuobbunpppwaaaallkkkkcssgggfeedullfffbbnnnuzkiiqoqfkqqihijuaavvhhgbbcllffdwvvrrqqqjjeduueedgghifddxxxxxxxgnomlmziggtttxyvvjmkmkknmnikjiiuutuvwxxtuvsvvhhhqpnqooggqnntttqqwwxxtttbbccffeeeeemvwfqprnnnnflwwwwwfggfpppppmtstfffffbjjjuvubstututtttrlzmsbifggfggffeellmvvvvrrcabceeeeeyytshxyzsmlldgggyynnkmljjbbbbwppxhhhhvrccuuuuttvlojjtttsssxwnmmnaaazmmmmdcbuutsssjjoytvvukkwwbbcihhicccxxddbhddbmmggtassxxxxxxbbbwqriigisssjmxwxtnnnnnnnvvymmzzlmwwwwwusssslllllnnnnmmskkkkkeekyydffcjjjaideebaheehfyyytuyyxwrqqpprpoqssqppqfccmjuuuuubbastswww"),

]
for r in result:
    print(r)
