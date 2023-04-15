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
2193. 得到回文串的最少操作次数 #hard #贪心
    给一个字符串, 仅有的操作为交换相邻两个字符, 要求转为回文串的最小交换次数
2484. 统计回文子序列数目 #hard 统计由数字组成的字符串中, 长度为5的 #回文 子序列的数量. 限制: n 1e4
1930. 长度为 3 的不同回文子序列 #medium 


Easonsi @2023 """
class Solution:
    """ 2193. 得到回文串的最少操作次数 #hard #贪心
给一个字符串, 仅有的操作为交换相邻两个字符, 要求转为回文串的最小交换次数
     """
    def minMovesToMakePalindrome0(self, s: str) -> int:
        pass
    
    """ 2484. 统计回文子序列数目 #hard 统计由数字组成的字符串中, 长度为5的 #回文 子序列的数量. 限制: n 1e4
思路0: 枚举所有的中间数字, 统计左右符合对称的长尾2的数字川数量. 复杂度 O(d^2 n), 其中d为字符数量
    细节: 注意 left, right 两个计数器的更新. 重点是如何撤销?
    [灵神](https://leetcode.cn/problems/count-palindromic-subsequences/solution/qian-hou-zhui-fen-jie-o100-chang-shu-kon-51cv/) 思路一致, 但代码简洁许多!
关联: 「1930. 长度为 3 的不同回文子序列」
 """
    def countPalindromes(self, s: str) -> int:
        #  from 灵神
        suf = [0] * 10  # 当前后缀中, 每个d的出现次数
        suf2 = [0] * 100
        for d in map(int, reversed(s)):
            for j, c in enumerate(suf):
                suf2[d * 10 + j] += c
            suf[d] += 1

        ans = 0
        pre = [0] * 10
        pre2 = [0] * 100
        for d in map(int, s):
            suf[d] -= 1
            for j, c in enumerate(suf):
                suf2[d * 10 + j] -= c  # 撤销
            ans += sum(c1 * c2 for c1, c2 in zip(pre2, suf2))  # 枚举所有字符组合
            for j, c in enumerate(pre):
                pre2[d * 10 + j] += c
            pre[d] += 1
        return ans % (10 ** 9 + 7)
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
