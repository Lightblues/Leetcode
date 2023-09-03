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
    """ 0032. 最长有效括号 #hard #题型 给定一个括号序列, 找到其中最长有效的子串长度
思路1: #DP
    记 f[i] 表示以i位置结尾的合法串的长度. 对于新的位置, 在其为 ) 时考虑:
        若 s[i-1]=='(' 则 f[i] = f[i-2] + 2
        若 s[i-1]==')' 时, 只有在 i-1 位置合法, 并且合法匹配部分再前面的元素是 ( 的时候才有转移
            f[i] = f[i-1]+ 2 + f[i-1-f[i-1]-1] 
            其中, f[i-1-f[i-1]-1] 是指匹配了 i-1-f[i-1] 位置的(之后, 可能连接前面的合法元素! 
    复杂度: O(n)
思路2: 用 #栈 来记录. 巧妙地将栈底元素作为边界!!
    维护栈底元素为「最后一个没有被匹配的 `)`」; 栈内其他元素为待匹配的 `(` 位置.
    这样, 我们将遇到的 `(` 入栈待匹配; 把 `)` 尝试跟栈内元素匹配, 若匹配不上则将其作为栈底元素 (不可能匹配上, 表示下一段合法序列的边界). 
思路3: 贪心 #两次遍历, 不需要额外的空间
    我们从左往右看, 尽量选择最长区间. 记 l,r 分别是 `()` 出现的次数, 
        则 `l<r` 时左右显然不能连上! 我们重新开始计数!
        当 `l==r` 时我们统计长度 (实际上是, 以idx结尾的合法串长度)
    但这会忽略 `(()` 这样的情况! 解决的方法是从右往左再来一遍
[官答](https://leetcode.cn/problems/longest-valid-parentheses/solution/zui-chang-you-xiao-gua-hao-by-leetcode-solution/)
自己的想法: 分别记左右括号为 +1,-1, 那么问题等价于求一段区间和为0, 并且前缀和都非负!
"""
    def longestValidParentheses(self, s: str) -> int:
        # 思路1: #DP
        dp = [0 for _ in range(len(s))]
        for i in range(1, len(s)):
            if s[i] == ')':
                if s[i-1] == '(':
                    dp[i] = (dp[i-2] if i>=2 else 0) + 2
                else:
                    if i-dp[i-1]>0 and s[i-dp[i-1]-1] == '(':
                        dp[i] = dp[i-1] + (dp[i - dp[i - 1] - 2] if i - dp[i - 1]>=2 else 0) + 2
        maxans = max(dp)
        return maxans
    def longestValidParentheses(self, s: str) -> int:
        # 思路2: 用 #栈 来记录. 巧妙地将栈底元素作为边界!!
        st = [-1]       # 栈底元素为「最后一个没有被匹配的 `)`」
        mx = 0
        for i,c in enumerate(s):
            if c=='(': st.append(i)
            else:
                st.pop()
                if not st: st.append(i)         # 无法匹配, 作为栈底 (边界)
                else: mx = max(mx, i-st[-1])    # 合法匹配
        return mx
    def longestValidParentheses(self, s: str) -> int:
        # 思路3: 贪心 #两次遍历, 不需要额外的空间
        mx = 0
        l=r = 0
        for c in s:
            if c=='(': l+=1
            else:
                r += 1
                if l==r: mx = max(mx, 2*r)
                if r>l: l=r=0
        l=r = 0
        for c in s[::-1]:
            if c==')': r+=1
            else:
                l += 1
                if l==r: mx = max(mx, 2*l)
                if l>r: l=r=0
        return mx
    
    

    
sol = Solution()
result = [
    sol.longestValidParentheses(s = ")()())"),
]
for r in result:
    print(r)
