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
https://leetcode.cn/contest/weekly-contest-417
T3 自己搞了个比较复杂的分析, 代码写起来很多细节
T4 的数学求解自己还算满意
Easonsi @2023 """

Map = dict(zip(string.ascii_lowercase, string.ascii_lowercase[1:]+'a'))
S = 'a'
while len(S) < 500:
    ns = ''.join(Map[i] for i in S)
    S += ns
class Solution:
    """ 3304. 找出第 K 个字符 I #easy 开始的字符串为a, 每次操作, 将每个字符串变为下一个字符 (z->a) 然后将其拼到原本字符串后面, 问第k个字符是什么? 
限制: k 500
    """
    def kthCharacter(self, k: int) -> str:
        return S[k-1]
    
    """ 3305. 元音辅音字符串计数 I #medium 对于s的所有子串, 统计 "aeiou至少出现一次, 并且辅音恰好有k个" 数量
限制: n 250
3306. 元音辅音字符串计数 II. 限制: n 2e5
思路1: 比较复杂的 #滑窗
思路2: 转化为 
    "每个元音字母至少出现一次，并且至少包含 k 个辅音字母的子串个数" - "每个元音字母至少出现一次，并且至少包含 k+1 个辅音字母的子串个数"
    -- 从而避免 "恰好等于" 这样的判断
[ling](https://leetcode.cn/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/solutions/2934309/liang-ci-hua-chuang-pythonjavacgo-by-end-2lpz/)
"""
    def countOfSubstrings(self, word: str, k: int) -> int:
        n = len(word)
        # build vowel index-length
        vowel_idx = []; vowel_len = []
        is_in = False
        for i,x in enumerate(word + 'b'):
            if x in 'aeiou':
                if not is_in:
                    vowel_idx.append(i)
                is_in = True
            else:
                if is_in and vowel_idx:
                    vowel_len.append(i-vowel_idx[-1])
                is_in = False
        # 
        ans = 0; r = 0
        cntV = Counter(); cntU = 0
        for l in range(n):
            if l>0:
                if word[l-1] in 'aeiou': 
                    cntV[word[l-1]] -= 1
                    if cntV[word[l-1]] == 0: del cntV[word[l-1]]
                else: cntU -= 1
            while r<n and (cntU<k or len(cntV)<5):
                if cntU==k and word[r] not in 'aeiou': break    # to avoid cntU > k
                if word[r] in 'aeiou': 
                    cntV[word[r]] += 1
                else: 
                    cntU += 1
                r += 1
            if cntU==k and len(cntV)==5:
                if r == n: ans += 1
                else: # r is the nex token
                    if word[r] not in 'aeiou': ans += 1
                    else:
                        # 若为元音, 则再往后的元音都可以包括进来! 
                        idx = bisect_right(vowel_idx, r) - 1
                        ans += vowel_idx[idx] + vowel_len[idx] - r + 1
        return ans
    
    """ 3307. 找出第 K 个字符 II #hard 开始的字符串为a, 有两种操作, 问操作若干次之后, 第k个字符是什么? 
1) 直接将原本的字符串复制一份加到后面; 
2) 将每个字符串变为下一个字符 (z->a) 然后将其拼到原本字符串后面, 
限制: k 1e14; n 100
思路1: #数学
    注意到, 生成的序列经过的操作次数 [1] [2] [3,4] [5,6,7,8] 分别是经过0/1/2/3次操作得到的. 
    例如 k=7, 它是经过 ceil(log2(7))=3 次操作得到的 -- op[3]
        k -= 4 得到 3, 它是经过 ceil(log2(3))=2 次操作得到的 -- op[2]
        k -= 2 得到 1, 没有经过操作! 也就是原本的 [1] 位置的 'a'
    假设 ops = [1,1,1], 那么生成的字符串是 a b bc bccd, 我找我们的计算为 'a' + 2 = 'c' 符合!
[ling](https://leetcode.cn/problems/find-the-k-th-character-in-string-game-ii/solutions/2934284/liang-chong-zuo-fa-di-gui-die-dai-python-5f6z/)
直接用 递归/迭代的思路来求解, 简化了思考过程
    """
    def kthCharacter(self, k: int, operations: List[int]) -> str:
        acc = 0
        while k > 1:
            op_idx = ceil(log2(k)) - 1
            acc += operations[op_idx]
            k -= 2**op_idx
        acc = acc % 26
        return chr(ord('a') + acc)
    
sol = Solution()
result = [
    # sol.kthCharacter(5),
    # sol.countOfSubstrings(word = "aeioqq", k = 1),
    # sol.countOfSubstrings(word = "aeiou", k = 0),
    # sol.countOfSubstrings(word = "ieaouqqieaouqq", k = 1),
    # sol.countOfSubstrings("iqeaouqi", 2),
    sol.kthCharacter(k = 5, operations = [0,0,0]),
    sol.kthCharacter(k = 10, operations = [0,1,0,1]),
]
for r in result:
    print(r)
