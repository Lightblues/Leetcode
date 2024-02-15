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
https://leetcode.cn/contest/weekly-contest-378
https://leetcode.cn/circle/discuss/zgYIvt/

T4的有意思! 模拟!
Easonsi @2023 """
class Solution:
    """ 2980. 检查按位或是否存在尾随零 """
    
    """ 2982. 找出出现至少三次的最长特殊子字符串 II 定义连续相同自负为「特殊子串」, 问出现数量超过3次的最长子串长度
思路1: 对于不同的字符分别计数. 需要处理出现的可能性. 
    例如, 分别出现 (2,4,5) 次, 每个span中取一段, 因此为 2; 
        而考虑 (4,5), 第一个span中取4 后一个分别取大小为4的滑动窗口, 则最大为4;
        只考虑 (5), 最最大为 5-2 = 3

    """
    def maximumLength(self, s: str) -> int:
        ch2cnts = defaultdict(list)
        pre = s[0]; cnt = 1
        for x in s[1:] + ' ':
            if x!=pre:
                ch2cnts[pre].append(cnt)
                cnt = 1
                pre = x
            else:
                cnt += 1
        mx = -1
        for ch,cnts in ch2cnts.items():
            cnts.sort()
            # 对于不同情况进行考虑
            if len(cnts)>=3:
                mx = max(mx, cnts[-3])
            if len(cnts)>=2:
                if cnts[-1] == cnts[-2]:
                    mx = max(mx, cnts[-1]-1)
                else:
                    mx = max(mx, cnts[-2])
            if cnts[-1] >= 3:
                mx = max(mx, cnts[-1]-2)
        return mx if mx>0 else -1

    """ 2983. 回文串重新排列查询 #hard 对于一个字符串, 每次给查询 (a,b,c,d), 问能够对于 [a,b] 前一半的某区间 和后一般的区间 [c,d] 进行重排后, 整体字符串变为回文. 
限制: n 1e5; q 1e5 #模拟
思路1: 问题转换 + 分类讨论
    问题转化为, 对于两个相同长度的字符串 s1,s2. 给定调换区间 [l1,r1], [l2,r2] 问可否变得相同. 
    不妨假设 l1<=l2, 分类讨论:
        1. 包含关系, 也即 r2<=r1. 此时要求区间[l1,r1]外字符每个位置相同, 区间内字符重排相同. 
        2. 相交关系, 也即部分重叠, l2<=r1<=r2. (其他条件下) 要求 s1[l1,r1] 范围内有 s2[l1,l2-1] 的所有字符; s2[l2,r2] 范围内有 s1[r1+1,r2] 的所有字符.
        3. 不相交关系, 也即 r1<=l2, 类似情况1, 要求覆盖区域重排相同, 其他位置原本就相同. 
    如何实现上面要求的数量统计? 可以分别构建「前缀字符数量」, 以及两个字符串「前缀不同的字符数量」
参见 [灵神](https://leetcode.cn/problems/palindrome-rearrangement-queries/solutions/2585862/fen-lei-tao-lun-by-endlesscheng-jxg0/)
    """
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        m = n//2
        s ,t = s[:m], s[m:][::-1]
        if sorted(s) != sorted(t):
            return [False]*len(queries)
        # preprocess
        preDiff = [0] * (m+1)   # 前缀不同的字符数量
        for idx,(a,b) in enumerate(zip(s,t)):
            if a!=b: preDiff[idx+1] = 1 + preDiff[idx]
            else: preDiff[idx+1] = preDiff[idx]
        preSum1 = [[0]*26 for _ in range(m+1)]
        for idx,a in enumerate(s):
            preSum1[idx+1] = preSum1[idx][:]
            preSum1[idx+1][ord(a)-ord('a')] += 1
        preSum2 = [[0]*26 for _ in range(m+1)]
        for idx,a in enumerate(t):
            preSum2[idx+1] = preSum2[idx][:]
            preSum2[idx+1][ord(a)-ord('a')] += 1
        # query
        def test_equal(l,r):
            if r<l: return True
            return preDiff[r+1] - preDiff[l] == 0
        def test_equal_re(l,r):
            """ 检查是否可经过重排相等 """
            if r<l: return True
            for idx in range(26):
                if preSum1[r+1][idx] - preSum1[l][idx] != preSum2[r+1][idx] - preSum2[l][idx]:
                    return False
            return True
        def test_contain(l1,r1,l2,r2, ps1,ps2):
            """ 判断 s1[l1,r1] 是否包含 s2[l2,r2] 中的元素 """
            for idx in range(26):
                if ps1[r1+1][idx] - ps1[l1][idx] < ps2[r2+1][idx] - ps2[l2][idx]:
                    return False
            return True
        def query(l1,r1,l2,r2):
            ps1,ps2 = preSum1, preSum2
            if l1 > l2:
                l1,r1,l2,r2 = l2,r2,l1,r1
                ps1,ps2 = preSum2, preSum1
            # 1. 包含
            if r2<=r1:
                return test_equal(0,l1-1) and test_equal(r1+1, m-1) and \
                    test_equal_re(l1,r1)
            # 2. 相交
            elif l2<=r1<=r2:
                return test_equal(0,l1-1) and test_equal(r2+1, m-1) and \
                    test_contain(l1,r1,l1,l2-1, ps1,ps2) and test_contain(l2,r2,r1+1,r2, ps2,ps1)
            # 3. 不相交
            else:
                return test_equal(0,l1-1) and test_equal(r1+1,l2-1) and test_equal(r2+1, m-1) and \
                    test_equal_re(l1,r1) and test_equal_re(l2,r2)
        ans = []
        for l1,r1,l2,r2 in queries:
            l2,r2 = n-1-r2, n-1-l2
            ans.append(query(l1,r1,l2,r2))
        return ans
    

    
sol = Solution()
result = [
    # sol.maximumLength("accccerrrc"),
    # sol.maximumLength('aaaa'),
    # sol.maximumLength("abcdef"),
    # sol.maximumLength("abcaba"),
    # # sol.maximumLength("aaba"),
    sol.canMakePalindromeQueries(s = "abcabc", queries = [[1,1,3,5],[0,2,5,5]]),
    sol.canMakePalindromeQueries(s = "abbcdecbba", queries = [[0,2,7,9]]),
    sol.canMakePalindromeQueries(s = "acbcab", queries = [[1,2,4,5]]),
]
for r in result:
    print(r)
