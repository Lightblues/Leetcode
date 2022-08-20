
def prefix_function(s):
    # 前缀函数, 注意和一般教材不同, 这里下标从1开始!
    # from https://oi-wiki.org/string/kmp/
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
    def __init__(self, B, A) -> None:
        self.b = B
        self.a = A
        self.nxt = []
    
    """ 部分匹配表，又称为失配函数，作用是让算法无需多次匹配S中的任何字符。能够实现线性时间搜索的关键是在主串的一些字段中检查模式串的初始字段，可以确切地知道在当前位置之前的一个潜在匹配的位置。换句话说，在不错过任何潜在匹配的情况下，"预搜索"这个模式串本身并将其译成一个包含所有可能失配的位置对应可以绕过最多无效字符的列表。
例如, 对于 aaa, 字符串的前缀函数应该是 pi=[0,1,2], 定义为 s[0...i] 的真前缀和后缀相等的最大长度 (显然 pi[0]=0) 
而其 nxt=[-1,0,1], 这是为了和编程语言中数组从0开始index保持一致. 例如当要匹配第2个元素时, 若失败, 可知 s[0...2] 的前缀函数值为2
在下面的 search函数中, 遍历的j表示当前匹配到了字符串a的多少长度
"""
    def build_nxt(self) -> None:
        self.nxt.append(-1)
        for i in range(1, len(self.a)):
            j = self.nxt[i - 1]
            while j != -1 and self.a[i] != self.a[j + 1]:
                j = self.nxt[j]
            if self.a[i] == self.a[j + 1]:
                self.nxt.append(j + 1)
            else:
                self.nxt.append(-1)

    def search(self) -> list:
        self.build_nxt()
        i, j = 0, 0
        res = []
        while i < len(self.b):
            """ 也注意这里迭代计算下一个匹配的过程! """
            while j != -1 and self.b[i] != self.a[j + 1]:
                j = self.nxt[j]
            if self.b[i] == self.a[j + 1]:
                j += 1
            # 匹配成功
            if j == len(self.a) - 1:
                res.append(i - j)
                j = self.nxt[j]
            i += 1
        return res

full_word = "ABABAABAABAC"
pattern = "ABAABAC"
kmp = KMP(full_word, pattern)
res = kmp.search()
print(res)
print(kmp.nxt)
print(prefix_function(pattern))