""" 
https://oi-wiki.org/string/kmp/
参见 [ling](https://www.zhihu.com/question/21923021/answer/37475572)

注意前缀函数 pi 的定义?
    pi[i] 表示 s[0...i] 的前缀和后缀相等的最大长度! 
    利用前缀函数, 在匹配的时候可以快速跳过不匹配的部分
"""


def prefix_function(s):
    """ 前缀函数. pi从0开始 """
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi



class KMP:
    def __init__(self, pattern) -> None:
        self.pattern = pattern
        self.pi = self.prefix_function(pattern)
        self.n = len(pattern)
    
    def prefix_function(self, pattern) -> list:
        # 前缀函数. pi从0开始 —— 当前后缀和前缀匹配的长度!
        n = len(pattern)
        pi = [0] * n
        for i in range(1, n):
            j = pi[i - 1]
            while j > 0 and pattern[i] != pattern[j]:
                j = pi[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            pi[i] = j
        return pi
    
    def match(self, s):
        """ 找到和s中pattern出现的位置 """
        res = []
        pi = self.pi
        pattern = self.pattern
        j = 0
        for i in range(len(s)):
            while j > 0 and s[i] != pattern[j]:
                j = pi[j - 1]
            if s[i] == pattern[j]:
                j += 1
            if j == len(pattern):
                res.append(i - len(pattern) + 1)
                j = pi[j - 1]
        return res

# full_word = "ABABAABAABAC"
# pattern = "ABAABAC"
# pattern = "AB"

full_word = 'aaaa'
pattern = 'aa'
kmp = KMP(pattern)
print(kmp.pi)
print(kmp.match(full_word))