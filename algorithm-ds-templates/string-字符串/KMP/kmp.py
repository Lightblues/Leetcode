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

""" KMP算法
https://oi-wiki.org/string/kmp/
wiki [KMP算法](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
参见 [ling](https://www.zhihu.com/question/21923021/answer/37475572)


题目列表:
    1392. 最长快乐前缀 #hard
    0028. 找出字符串中第一个匹配项的下标 #medium
    3036. 匹配模式数组的子数组数目 II #hard 

"""
class Solution:
    """ 1392. 最长快乐前缀 #hard #KMP 给定一个字符串s, 要求最长的, 既是s的前缀也是后缀的子串.
思路1: #KMP
    显然, 如果知道KMP算法, 那么答案就可由 #部分匹配表 或者 #前缀函数 直接得到, 也即长为 `fail[len-1]+1` 的前缀
    复杂度: O(n)
思路2: #Rabin-Karp 字符串编码   通过字符串编码来判断前后缀是否相同
    注意到, 既可以从左往右也可以从右往左拓展计算编码的字符串长度. 因此我们1...n枚举长度, 每次比较前后缀是否相同即可.
[官答](https://leetcode.cn/problems/longest-happy-prefix/solution/zui-chang-kuai-le-qian-zhui-by-leetcode-solution/)
"""
    def longestPrefix(self, s: str) -> str:
        # 思路1: #KMP
        n = len(s)
        fail = [-1] * n     # 从-1开始, 表示回退到的位置
        for i in range(1, n):
            j = fail[i - 1]
            while j != -1 and s[j + 1] != s[i]:
                j = fail[j]
            if s[j + 1] == s[i]:
                fail[i] = j + 1
        return s[:fail[-1] + 1]

    def longestPrefix(self, s: str) -> str:
        # 另一种写法: 从0开始, 表示当前idx应该匹配的下一个位置 (或者表示前缀后相等的长度)
        n = len(s)
        pre= [0] * n    # 从0开始, 表示当前idx应该匹配的下一个位置 (或者表示前缀后相等的长度)
        for i in range(1,n):
            j = pre[i-1]    # 上一轮匹配中下一个代匹配位置
            while j>0 and s[i] != s[j]:
                j = pre[j-1]
            if s[i] == s[j]:
                j += 1
            pre[i] = j
        return s[:pre[-1]]

    """ 0028. 找出字符串中第一个匹配项的下标 #medium #题型 在字符串a中找到字符串b出现的首个位置 限制: N 1e4
思路1: 暴力匹配, 复杂度 O(L n), 其中L为目标子串长度
    1.1 类似 KMP的优化
思路2: #Rabin Karp 字符串编码
思路3: #KMP [官答](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/solution/shi-xian-strstr-by-leetcode-solution-ds6y/)
    核心是 #前缀函数 
        例如, p='aaa' 的前缀函数是 `pi=[0,1,2]` 
        这里的定义是, 当前位置i所需要匹配的pattern中的位置. 或者说, p的每一个前缀子串中, 真前后缀相等的长度
另见 [Sunday 解法](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/solution/python3-sundayjie-fa-9996-by-tes/)
"""
    def strStr(self, haystack: str, needle: str) -> int:
        # 1.1 好像是自己写的? 类似KMP的思想, 可以完成一定的剪枝, 但无法带来复杂度上的提升.
        L, n = len(needle), len(haystack)
        if L==0: return 0
        
        pn = 0 # pointer in haystack
        while pn < n-L+1:
            # 对齐 needle 第一个元素
            while pn<n-L+1 and haystack[pn]!=needle[0]:
                pn += 1
            # 从头开始匹配 needle，注意此时的 pn 指向的值必然为 needle 第 0 元素，也即 haystack[pn]==needle[pL]
            curr_len = 0    # 记录匹配长度
            pL = 0  # pointer in needle
            while pL<L and pn<n and haystack[pn]==needle[pL]:
                pn += 1
                pL += 1
                curr_len += 1
            if curr_len == L:   # 完整匹配
                return pn-L
            pn = pn-curr_len+1  # 否则回退到
        return -1
    
    def strStr(self, haystack: str, needle: str) -> int:
        # 思路3: #KMP
        # build 
        n = len(needle)
        pre = [0] * n
        for i in range(1,n):
            j = pre[i-1]
            while j>0 and needle[i] != needle[j]:
                j = pre[j-1]
            if needle[i] == needle[j]:
                j += 1
            pre[i] = j
        # 搜索
        i = j = 0   # i: haystack, j: needle
        m = len(haystack)
        while i<m:      # 循环条件
            while j>0 and haystack[i] != needle[j]:
                j = pre[j-1]
            # 部分匹配成功
            if haystack[i] == needle[j]:
                j += 1
            if j == n:  # 找到答案了!!
                return i-n+1
            i += 1  # 注意到, i是不会回退的! 
        return -1
    
sol = Solution()
result = [
    # sol.longestPrefix("level"),
    # sol.longestPrefix(s = "ababab"),
    
    sol.strStr(haystack = "sadbutsad", needle = "sad"),
    sol.strStr(haystack = "leetcode", needle = "leeto"),
]
for r in result:
    print(r)
