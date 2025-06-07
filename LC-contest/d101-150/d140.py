from typing import *
# from easonsi.util.leetcode import *

# def testClass(inputs):
#     # 用于测试 LeetCode 的类输入
#     s_res = [None] # 第一个初始化类, 一般没有返回
#     methods, args = [eval(l) for l in inputs.split('\n')]
#     class_name = eval(methods[0])(*args[0])
#     for method_name, arg in list(zip(methods, args))[1:]:
#         r = (getattr(class_name, method_name)(*arg))
#         s_res.append(r)
#     return s_res

""" 
https://leetcode.cn/contest/biweekly-contest-140
Easonsi @2025 """
class Solution:
    """ 3302. 字典序最小的合法序列 #medium 找到一个最小的递增的index序列, 让 word1 的子序列 "几乎等于" word2, 这里的 "几乎等于" 是指最多只相差一个字符
限制: n 3e5
思路1: #前后缀分解
    关联: [2565. 最少得分子序列] 也是找子序列
    预处理: 先计算后缀 suf[i] 表示 words1[i:] 可以匹配 word2 的最长后缀的左下标
    关键是如何 "字典序最小"? 枚举前缀位置i, 同时记录word2的匹配位置j:
        若 word1[i] == word2[j], 直接使用;
        若 不等, 且 suf[i+1] <= j+1, 说明一定要修改了 -- 最小字典序
        注意! 为了避免仅修改一次, 需要用一个flag来标记是否修改过 """
    def validSequence(self, word1: str, word2: str) -> List[int]:
        m,n = len(word1), len(word2)
        
        suf = [0] * (m+1)  # init as 0 for break
        j = n-1
        for i in range(m-1,-1,-1):
            if word1[i] == word2[j]:
                j -= 1
            if j == -1: break
            suf[i] = j+1
        
        ans = []  # record the answer
        j = 0
        changed = False
        for i, c in enumerate(word1):
            if c == word2[j]:
                j += 1
                ans.append(i)
            else:
                if changed and suf[i] > j: return []  # early stop
                elif not changed and suf[i+1] <= j+1:
                    changed = True
                    j += 1
                    ans.append(i)
            if j == n: return ans
        return []

    
sol = Solution()
result = [
    # sol.validSequence(word1 = "vbcca", word2 = "abc"),
    # sol.validSequence(word1 = "bacdc", word2 = "abc"),
    sol.validSequence("cbbccc", "bb")
]
for r in result:
    print(r)
