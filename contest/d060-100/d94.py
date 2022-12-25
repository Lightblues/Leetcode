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
https://leetcode.cn/contest/biweekly-contest-94
讨论: https://leetcode.cn/circle/discuss/YeBDQY/
T1 感觉有点不太好处理... T2是基本的双指标排序. T3的二分比较难想到? T4考了概率统计, 对于自己相对好想到一些. 

@2022 """
class Solution:
    """ 6273. 最多可以摧毁的敌人城堡数目 #easy 要找到最大的 [1, 0,0...,0, -1] 也即首尾为 1/-1, 中间为 0 的子串 
思路1: 「对每个 1，向左向右找 -1，且中间的必须都是 0。」, 见 [灵神](https://leetcode.cn/problems/maximum-enemy-forts-that-can-be-captured/solution/mo-ni-by-endlesscheng-is4i/)
"""
    def captureForts(self, forts: List[int]) -> int:
        pre_m1 = -1; pre_1 = -1
        ans = 0
        for i,x in enumerate(forts):
            if x==1:
                if pre_m1>pre_1:
                    ans = max(ans, i-pre_m1-1)
                pre_1 = i
            elif x==-1:
                if pre_1>pre_m1:
                    ans = max(ans, i-pre_1-1)
                pre_m1 = i
        return ans
    
    """ 6274. 奖励最顶尖的 K 名学生 #medium 模拟打分, 按照双指标排序 """
    def topStudents(self, positive_feedback: List[str], negative_feedback: List[str], report: List[str], student_id: List[int], k: int) -> List[int]:
        ps = set(positive_feedback)
        ns = set(negative_feedback)
        def f(s):
            score = 0
            for w in s.split():
                if w in ps: score += 3
                if w in ns: score -=1
            return score
        scores = [(f(s), i) for s,i in zip(report, student_id)]
        scores.sort(key=lambda x: (-x[0], x[1]))
        return [i[1] for i in scores[:k]]
    
    """ 6295. 最小化两个数组中的最大值 #medium 要求从尽可能小的自然数中, 放在两个数组中, 分别要求有 uniqueCnt1/2 个不同的数字, 其中的每个数字不能被 divisor1/2 整除
限制: divisor1/2 1e5; 元素数量 1e9
思路1: #二分 
    如何检查前x个自然是是否可以满足条件? 一开始纠结如何对每个数字进行分配, 后来想到, 问题等价于: 总体数量满足; 两个分组的数量都满足即可. 
    二分的范围? 下届是 uniqueCnt1+uniqueCnt2, 上届不好确实, 直接取了 10*(uniqueCnt1+uniqueCnt2)
见 [灵神](https://leetcode.cn/problems/minimize-the-maximum-of-two-arrays/solution/er-fen-da-an-by-endlesscheng-y8fp/)
"""
    def minimizeSet(self, divisor1: int, divisor2: int, uniqueCnt1: int, uniqueCnt2: int) -> int:
        # 两个除数的共同因子
        divisor12 = math.lcm(divisor1, divisor2)
        def check(x):
            # 检查: 总体数量满足; 两个分组的数量都满足
            if x - x//divisor12 < uniqueCnt1+uniqueCnt2: return False
            if x - x//divisor1 < uniqueCnt1: return False
            if x - x//divisor2 < uniqueCnt2: return False
            return True
        l,r = uniqueCnt1+uniqueCnt2, 10*(uniqueCnt1+uniqueCnt2)
        ans = inf
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = min(ans, mid)
                r = mid-1
            else:
                l = mid+1
        return ans
    
    """ 6276. 统计同位异构字符串数目 #hard 问题等价于, 对于一个字符串, 求其「同位异构字符串」的数量, 也即 b 可以由 a 通过重排列得到. 限制: n 1e5
思路1: #排列 
    显然, 用统计的语言来说, 就是有 n1,n2,...nr 个相同的字符, 一共有多少中排列方式? 
    可以通过乘法原理分解计算.
见 [灵神](https://leetcode.cn/problems/count-anagrams/solution/zu-he-ji-shu-by-endlesscheng-leem/)
"""
    def countAnagrams(self, s: str) -> int:
        mod = 10**9 + 7
        def f(chCnts):
            # r个字符分别有 n1,n2,...nr 个, 一共有多少中排列方式?
            # 乘法原理
            ans = 1
            s = sum(chCnts)
            for cnt in chCnts:
                ans = ans*math.comb(s, cnt) %mod
                s -= cnt
            return ans
        # 累计整个字符串
        ans = 1
        words = s.split()
        for word in words:
            chsCnt = Counter(word).values()
            ans = ans*f(chsCnt) % mod
        return ans
    
    

    
sol = Solution()
result = [
    # sol.captureForts(forts = [1,0,0,-1,0,0,0,0,1]),
    # sol.topStudents(positive_feedback = ["smart","brilliant","studious"], negative_feedback = ["not"], report = ["this student is studious","the student is smart"], student_id = [1,2], k = 2),
    # sol.minimizeSet(divisor1 = 2, divisor2 = 7, uniqueCnt1 = 1, uniqueCnt2 = 3),
    # sol.minimizeSet(divisor1 = 2, divisor2 = 4, uniqueCnt1 = 8, uniqueCnt2 = 2),
    sol.countAnagrams(s = "too hot"),
    sol.countAnagrams('aa'),
]
for r in result:
    print(r)
