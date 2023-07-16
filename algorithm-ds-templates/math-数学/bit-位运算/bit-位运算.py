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
位运算: https://oi-wiki.org/math/bit/

数组中两个数的最大异或值
重复的DNA序列 #medium 对于 ACGT组成的核苷酸序列, 找出所有长度为10的重复序列 (至少出现两次) 限制: n 1e5
    哈希表 + 滑动窗口 + 位运算
最大单词长度乘积

@2022 """
class Solution:
    """ 0067. 二进制求和 #easy #二进制 题目不重要, 这里要求不用加减乘除, 实现加法操作
思路1: 用位运算实现加法
    我们用 x,y 表示要加的两个数; 循环过程中, x表示当前结果, y表示进位
    每次循环, 更新
        x_new = x^y
        y_new = (x&y)<<1
    这样, 前者记录无进位的结果, y 记录进位结果. 
    正确性: y每次左移一位, 所以最后肯定会变成0
见 [官答](https://leetcode.cn/problems/add-binary/solution/er-jin-zhi-qiu-he-by-leetcode-solution/)
"""
    def addBinary(self, a, b):
        x, y = int(a, 2), int(b, 2)
        while y:
            answer = x^y
            carry = (x & y) << 2
            x, y = answer, carry
        return bin(x)[2:]       # 注意 bin 返回的是形如 '0b100010' 的字符串
    

    """ 0187. 重复的DNA序列 #medium 对于 ACGT组成的核苷酸序列, 找出所有长度为10的重复序列 (至少出现两次) 限制: n 1e5
思路1: 线性时间窗口切片 + HashSet。就是简单将出现的子串用字典存起来。这样所谓第 i 次「切片」就需要截取 [i:i+L] 部分的子串
    复杂度为 O(NL)
思路2: 字符串哈希 见 [String-hash]
    Rabin-Karp：使用旋转哈希实现常数时间窗口切片。将字符串采用 Rabin-Karp 编码（在 1044最长重复子串 中也用到），想法就是对于长 L 的子串每一位赋权，初始化第一个子串对应的值之后，每次滑动窗口更新增减的字母（所对应的数字）即可。
思路3: 哈希表 + 滑动窗口 + 位运算
    对于长度为4的字符表, 可以用长为2的二进制串来区分! 因此可以用一个整数来表示长L的串, 加上哈希表即可. 
    时间复杂度: O(N)
[官答](https://leetcode.cn/problems/repeated-dna-sequences/solution/zhong-fu-de-dnaxu-lie-by-leetcode-soluti-z8zn/)
关联: 1044. 最长重复子串 #hard
"""
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        L, n = 10, len(s)
        if n <= L: return []
        bin = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

        ans = []
        x = 0
        for ch in s[:L - 1]:
            x = (x << 2) | bin[ch]
        cnt = defaultdict(int)
        for i in range(n - L + 1):
            x = ((x << 2) | bin[s[i + L - 1]]) & ((1 << (L * 2)) - 1)
            cnt[x] += 1
            if cnt[x] == 2:
                ans.append(s[i : i + L])
        return ans

    """ 0318. 最大单词长度乘积 #medium 给定一组单词, 找出其中两个单词长度的最大乘积, 要求这两个单词不含有相同的字母. 限制: n, len(word) 1e3
思路1: 位运算
    对于每个单词, 根据其包含字符的set, 可以计算其 hash. 对于两个单词, 若hash的 & 为0, 则说明两个单词不含有相同的字母
    复杂度: O(n^2)
    优化: 可以保存 {hash:maxlen} 的字典, 要剪枝一些不必要的计算
"""
    def maxProduct(self, words: List[str]) -> int:
        bin = {ch: 1 << i for i, ch in enumerate(string.ascii_lowercase)}
        hash2maxlen = defaultdict(int)
        for word in words:
            h = reduce(operator.or_, [bin[ch] for ch in word])
            hash2maxlen[h] = max(hash2maxlen[h], len(word))
        ans = 0
        hash2maxlen = list(hash2maxlen.items())
        for i, (h1,l1) in enumerate(hash2maxlen):
            for h2,l2 in hash2maxlen[i+1:]:
                if h1 & h2 == 0:
                    ans = max(ans, l1*l2)
        return ans

    """ 0371. 两整数之和 #medium #题型
思路1: #位运算
    根据加法的过程, 可知 a+b = a^b + (a&b)<<1
    如何规避这里的加法? 我们等价 #变换, 使得 a&b==0
[官答](https://leetcode.cn/problems/sum-of-two-integers/solution/liang-zheng-shu-zhi-he-by-leetcode-solut-c1s3/)
    """
    def getSum(self, a: int, b: int) -> int:
        """ 在其他语言里是可以的! 但由于Python无限长度负数, 有问题! """
        while a&b:
            tmp = a
            a = a^b
            b = (tmp&b)<<1
        return a^b
    def getSum(self, a: int, b: int) -> int:
        MASK = 1<<32
        MAX_INT = (1<<31) - 1
        MIN_INT = 1<<31
        a,b = a%MASK, b%MASK
        while b!=0:
            carry = ((a&b)<<1)
            a = (a^b) % MASK
            b = carry % MASK
        # 消除负数最高位, 再将正数部分取反, 再整体取反
        return a if not(a&MIN_INT) else ~((a ^ MIN_INT) ^ MAX_INT)

sol = Solution()
result = [
    # sol.maxProduct(words = ["abcw","baz","foo","bar","xtfn","abcdef"]),
    sol.getSum(a = 1, b = 2),
    sol.getSum(-2,1), 
]
for r in result:
    print(r)

