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
class Solution:

    """ 0010. 正则表达式匹配 #hard #题型 #star 实现可以有 `.*` 两个符号规则的正则表达式. 规则: `.` 匹配任意单个字符; `*` 匹配零个或多个前面的那一个元素
思路1: #DP 记 `f(i,j)` 表示 `s[:i]` 和 `p[:j]` 是否匹配.
    然后 #分类: 1) p[j] 为一般字符, 只有当 `s[i]==p[j]` 且 `f(i-1,j-1)` 成立时, 才匹配. 2) 若为 `.`, 忽略 `s[i]==p[j]` 这一条件.
        3) 若为 `*`, 再次根据 `p[i-1]` 的情况分类: 若为一般字符, 向前搜索 s[i,i-1...] 是否为 p[i-1], 若遇到 `f(x, j-2)` 成立, 则匹配; 若为 `.` 则匹配条件放宽.
    细节: 注意 #空字符串 的情况, 引入哨兵.
参见 [官答](https://leetcode.cn/problems/regular-expression-matching/solution/zheng-ze-biao-da-shi-pi-pei-by-leetcode-solution/), 更为简洁.
"""
    def isMatch(self, s: str, p: str) -> bool:
        m,n = len(s), len(p)
        f = [[False] * (n+1) for _ in range(m+1)]
        f[0][0] = True
        for i in range(m+1):
            for j in range(1, n+1):
                if p[j-1]=='.': f[i][j] = f[i-1][j-1] if i>0 else False
                elif p[j-1]=='*':
                    # 2) 重点是 `*` 的匹配
                    if p[j-2]=='.': f[i][j] = any(f[k][j-2] for k in range(i+1))
                    else:
                        # 匹配所有和 ch = p[j-2] 相同的字符.
                        ch = p[j-2]; idx = i
                        while idx>0:
                            if f[idx][j-2]: f[i][j] = True; break
                            if s[idx-1]!=ch: break
                            else: idx -= 1
                        # 最后的边界: 匹配到空字符串.
                        else: f[i][j] = f[0][j-2]
                else: f[i][j] = f[i-1][j-1] if (i>0 and s[i-1]==p[j-1]) else False
        return f[m][n]
    def isMatch(self, s: str, p: str) -> bool:
        # from 官答, 更为简洁.
        m, n = len(s), len(p)
        def match(i, j):
            # 辅助函数，判断 s[i-1] 是否等于 p[j-1]。成立条件：1. p[j-1] == '.'则可匹配任意非空字符；2. 或者 s[i-1]=p[j-1]
            # 考虑边界条件：i>=0, j>=1
            if i == 0:
                # 加上这一行的目的在于：例如 "" 无法被 "." 匹配，但不加的话因为 p[j-1] == '.' 而返回 True
                return False
            if p[j-1] == '.':
                return True
            return s[i-1] == p[j-1]

        f = [[False] * (n+1) for _ in range(m+1)]
        f[0][0] = True
        for i in range(m+1):
            # 注意 0 长度的 s 是可能和如 'a*' 的 p 匹配的，因此要从开始循环
            for j in range(1, n+1):
                # 而 0 长度 p 只能和 0 长 s 匹配
                if p[j-1] != '*':
                    if match(i, j):
                        f[i][j] |= f[i-1][j-1]
                    # else:
                    #     f[i][j] = False
                else:
                    # if match(i, j-1):
                    #     f[i][j] |= f[i][j-2] | f[i-1][j]
                    # else:
                    #     f[i][j] |= f[i][j-2]
                    f[i][j] |= f[i][j - 2]
                    if match(i, j - 1):
                        f[i][j] |= f[i-1][j]
        return f[m][n]

    """ 0044. 通配符匹配 #hard #题型 #star. 检查p是否可以完全匹配s. 符号: `?` 匹配任意单个字符, `*` 匹配任意字符串 (包括空)
e.g.: s = "adceb", p='*a*b' 是匹配的
思路1: #DP. 注意对于空字符的匹配, #细节.
    记 `f(i,j)` 表示 `s[:i]` 和 `p[:j]` 是否匹配.
    #分类 讨论: 1) 若 p[j] 为一般字符, 只有当 `s[i]==p[j]` 且 `f(i-1,j-1)` 成立时, 才匹配. 2) 若为 `?`, 忽略 `s[i]==p[j]` 这一条件.
        3) 若为 `*`, 只需要 `p[:j-1]` 能与之前的任意前缀匹配即可, 也即 `f(i,j) = any( f(0...i,j-1))` 
    复杂度: O(mn)
思路2: #贪心. 基本思想是, 本题中特殊字符只有 `*` 可以匹配任意子串.
    因此, 可以基于 * 对于 p进行分割, 剩余部分 `u_i` 是一定要匹配到的. 
    具体而言, 我们可以将 p 表示为 `*, u_1, *, u_2, *, .... u_i, *` 的形式 (首尾的非 * 可以预处理先匹配掉).
    如何对于这些子表达式进行匹配? 基本思路是, 我们在 s中尝试找到 `u_1` (记录匹配位置 `sRecord, pRecord`), 并接着继续找 `u_2` 若失败, 则回到记录位置重新开始找 `u_1`,....
    具体见代码.
本题与「0010. 正则表达式匹配」非常类似，但相比较而言，本题稍微容易一些。因为在本题中，模式 p 中的任意一个字符都是独立的，即不会和前后的字符互相关联，形成一个新的匹配模式。因此，本题的状态转移方程需要考虑的情况会少一些。
[官方](https://leetcode-cn.com/problems/wildcard-matching/solution/tong-pei-fu-pi-pei-by-leetcode-solution/)
"""
    def isMatch(self, s: str, p: str) -> bool:
        # 思路1: #DP. 注意对于空字符的匹配, #细节.
        m,n = len(s), len(p)
        # 由于需要匹配空字符, 所以至少 s维度 需要引入哨兵.
        f = [[False] * (n+1) for _ in range(m+1)]
        f[0][0] = True
        for i in range(m+1): # 注意从空字符开始匹配.
            for j in range(1,n+1):
                if p[j-1]=='?': f[i][j] = f[i-1][j-1] if i>0 else False
                elif p[j-1]=='*': f[i][j] = any(f[k][j-1] for k in range(i+1))
                else: f[i][j] = (s[i-1]==p[j-1] and f[i-1][j-1]) if i>0 else False
        return f[-1][-1]
    
    def isMatch(self, s: str, p: str) -> bool:
        # 思路2: #贪心. #hardhard
        def allStars(st: str, left: int, right: int) -> bool:
            return all(st[i] == '*' for i in range(left, right))
        
        def charMatch(u: str, v: str) -> bool:
            return u == v or v == '?'

        sRight, pRight = len(s), len(p)
        # 1) 匹配掉尾部, 直到 p[pRight - 1] == '*'
        while sRight > 0 and pRight > 0 and p[pRight - 1] != '*':
            if charMatch(s[sRight - 1], p[pRight - 1]):
                sRight -= 1
                pRight -= 1
            else:
                return False
        # 边界
        if pRight == 0:
            return sRight == 0
        # 2) 经过处理后 p 以 * 结尾 ( `*, u_1, *, u_2, *, .... u_i, *` 的形式), 将其与 s 进行匹配.
        sIndex, pIndex = 0, 0       # 用 sIndex 和 pIndex 表示当前遍历到 s 和 p 的位置
        sRecord, pRecord = -1, -1   # 此时我们正在 s 中寻找某个 u_i (被 * 分割的段), 其在 s 和 p 中的起始位置为 sRecord 和 pRecord
        while sIndex < sRight and pIndex < pRight:
            if p[pIndex] == '*':
                # 如果遇到星号，说明找到了 u_i，开始寻找 u_i+1
                pIndex += 1
                sRecord, pRecord = sIndex, pIndex
            elif charMatch(s[sIndex], p[pIndex]):
                # 如果两个字符可以匹配，就继续寻找 u_i 的下一个字符
                sIndex += 1
                pIndex += 1
            elif sRecord != -1 and sRecord + 1 < sRight:
                # 如果两个字符不匹配，那么需要重新寻找 u_i 枚举下一个 s 中的起始位置
                sRecord += 1
                sIndex, pIndex = sRecord, pRecord
            else:
                # 如果不匹配并且下一个起始位置不存在，那么匹配失败
                return False
        # 3) 将s匹配完毕之后, p剩余的部分只能是全 *
        return allStars(p, pIndex, pRight)


    
    
    
    
    
    

    
sol = Solution()
result = [
    # sol.isMatch1(s = "aa", p='a'),
    # sol.isMatch1(s = "aa", p='*'),
    # sol.isMatch1(s = "adceb", p='*a*b'),
    # sol.isMatch1("", '***'),
    
    sol.isMatch(s = "aa", p = "a"),
    sol.isMatch(s = "ab", p = ".*"),
    sol.isMatch(s = '', p = '.'),     #边界
    sol.isMatch(s = "aaaab", p = "a*ab"),   #懒惰匹配
    sol.isMatch("ipp", "ip*"),
    sol.isMatch("mississippi", "mis*is*ip*.")
]
for r in result:
    print(r)
