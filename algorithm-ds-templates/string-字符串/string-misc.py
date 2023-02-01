from easonsi import utils
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
== 字典序
1754. 构造字典序最大的合并字符串 #medium #题型
    给定两个字符串. 每次选择其中一个取最左边的字符. 要求得到的合并字符串字典序最大.
    思路: 双指针, 贪心选较大的, 相同的话比较剩余子串的字典序.

(其实不算字符串)
0942. 增减字符串匹配 #easy #题型
    有一个未知的 0...n 排序, 现在给定一个长n的 0/1 序列表示每个相邻位置的数字的大小关系. 要求构造一个复合条件的.


@2022 """
class Solution:
    """ 1754. 构造字典序最大的合并字符串 #medium #题型
给定两个字符串. 每次选择其中一个取最左边的字符. 要求得到的合并字符串字典序最大.
限制: 长度  3e3
思路1: #贪心
    用两个指针记录在两字符串上遍历的位置, 若不同时显然贪心选择较大的那一个.
    难点是相同的时候? 例如: "aa", "ab" 显然应该选择后者. 因此, 直观的想法从i,j顺序向后, 直到直线不同的.
        一开始走到死胡同: 想要直接用 i:ii 这一段遍历的部分. 但这样有问题: 例如 "babb", "baa", 最大merge应该是 `bbabbaa`, 若直接用的话会变成 `bab...`
        转换思路: 比较结束之后, 只使用当前的开始char即可. 然后从新开始比较即可.
        事实上, 这样的话, 可以直接用内置的字符串比较函数 `word1[i:]>word2[j:]` 即可
    see [here](https://leetcode.cn/problems/largest-merge-of-two-strings/solution/27zhou-sai-gou-zao-zi-dian-xu-zui-da-de-u0fhx/)
"""
    def largestMerge(self, word1: str, word2: str) -> str:
        n1, n2 = len(word1), len(word2)
        i,j = 0,0
        ans = ""
        while i<n1 or j<n2:
            # 一个用完了
            if i>=n1: ans += word2[j:]; break
            if j>=n2: ans += word1[i:]; break
            # 选择较大的
            if word1[i]>word2[j]:
                ans += word1[i]
                i+=1
            elif word1[i]<word2[j]:
                ans += word2[j]
                j += 1
            else:
                # 1.1 直接比较后续字符串的字典序
                if word1[i:]>word2[j:]:
                    ans += word1[i]; i+= 1
                else: ans += word2[j]; j+= 1
        return ans
    
    """ 0942. 增减字符串匹配 #easy #题型
有一个未知的 0...n 排序, 现在给定一个长n的 0/1 序列表示每个相邻位置的数字的大小关系. 要求构造一个复合条件的.
思路0: 由于关系只是相邻元素的大小关系, 先假设一个元素是0, 然后按照大小关系, 可以依次append最大/最小值. 
    这样构造的的元素会包括负数值, 将结果统一减去这一bias即可
思路1: 事实上有更为「优雅」的方式: 假如第一个关系是 `arr[0]>arr[1]`, 那么我们可以直接取第一个元素为n, 这样无论第二个元素是什么都符合条件.
    因此, 直接用两个数来记录剩余的最大/最小值即可.
    [官答](https://leetcode.cn/problems/di-string-match/solution/zeng-jian-zi-fu-chuan-pi-pei-by-leetcode-jzm2/)
"""
    def diStringMatch(self, s: str) -> List[int]:
        mn, mx = 0, 0
        ans = [0]
        for ch in s:
            if ch=='I':
                mx += 1; ans.append(mx)
            else:
                mn -= 1; ans.append(mn)
        return [i-mn for i in ans]
    def diStringMatch(self, s: str) -> List[int]:
        # 思路1
        lo = 0
        hi = n = len(s)
        perm = [0] * (n + 1)
        for i, ch in enumerate(s):
            if ch == 'I':
                perm[i] = lo
                lo += 1
            else:
                perm[i] = hi
                hi -= 1
        perm[n] = lo  # 最后剩下一个数，此时 lo == hi
        return perm


    """ 0012. 整数转罗马数字 #medium #题型 将整数转为罗马数字
规则: I,V, X,L, C,D, M 分别表示 1,5,10,50,100,500,1000
    特殊: 4,9,40,90,400,900 分别表示 IV, IX, XL, XC, CD, CM
思路1: 注意需要将 4,9... 这些看作特殊的base
"""
    def intToRoman(self, num: int) -> str:
        roman_digits = []
        digits = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I")
        ]
        for value, symbol in digits:
            count, num = divmod(num, value)
            roman_digits.append(symbol*count)
            if not num:
                break
        return "".join(roman_digits)
    """ 0013. 罗马数字转整数 #medium 反过来 """
    def romanToInt(self, s: str) -> int:
        result = 0
        digits = {
            "M": 1000,
            "CM": 900,
            "D": 500,
            "CD": 400,
            "C": 100,
            "XC": 90,
            "L": 50,
            "XL": 40,
            "X": 10,
            "IX": 9,
            "V": 5,
            "IV": 4,
            "I": 1
        }
        for symbol, value in digits.items():
            while s.startswith(symbol):
                result += value
                s = s[len(symbol):]
        return result
    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
