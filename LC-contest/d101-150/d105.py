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
https://leetcode-cn.com/contest/biweekly-contest-105
https://leetcode.cn/circle/discuss/fQ58lb/
Easonsi @2023 """
class Solution:
    """ 2706. 购买两块巧克力 """
    def buyChoco(self, prices: List[int], money: int) -> int:
        s = sum(sorted(prices)[:2])
        return money-s if money>=s else money
    
    """ 2707. 字符串中的额外字符 #medium 将s中的包括到一个字典的子串删去, 最少可以保留多少字符?
限制: n 50; 字符串长度 50
思路1: #DP
    复杂度为 O(n^3) 见
    [灵神](https://leetcode.cn/problems/extra-characters-in-a-string/solution/dong-tai-gui-hua-cong-ji-yi-hua-sou-suo-wtd7a/)
    """
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        @lru_cache(None)
        def f(i):
            # s[:i] 子问题
            if i<=0: return 0
            ans = f(i-1) + 1
            for d in dictionary:
                if len(s)>=len(s) and s[i-len(d):i] == d:
                    ans = min(ans, f(i-len(d)))
            return ans
        return f(len(s))
    
    """ 2708. 一个小组的最大实力值 """
    def maxStrength(self, nums: List[int]) -> int:
        a = 1; cnt = 0
        b = -inf
        for x in nums:
            if x!=0: 
                a*=x
                cnt += 1
            if x<0: b=max(b,x)
        if cnt==0: return 0
        if a>0: return a
        else:
            if cnt==1: return b if len(nums)==1 else 0
            else: return a//b

    """ 2709. 最大公约数遍历 #hard 拥有 >1 的gcd的两个数字作为节点相连, 问是否可以连通整个字符串 (所有节点)?
思路1: 转化 + #并查集
    注意到, 若两个数字的primes具有交集, 则 gcd >1
        因此, 问题转化为, 所有的primes是否全连通!
    细节: 注意边界情况! 因为1 WA了两次 (第一行边界; getPrimes不能范围1)
    """
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        # 注意边界!
        if 1 in nums: return len(nums)==1

        @lru_cache(None)
        def getPrimes(x):
            # 返回 x 的所有质因数 注意不包含1
            if x==1: return []
            for i in range(2, int(sqrt(x))+1):
                if x%i==0:
                    while x%i==0: x//=i
                    return getPrimes(x) + [i]
            return [x]
        
        primes = set()
        for x in nums:
            primes |= set(getPrimes(x))
        primes = list(primes)
        p2idx = {p:i for i,p in enumerate(primes)}

        m = len(primes)
        fa = list(range(m))
        def find(x):
            if fa[x]!=x: fa[x] = find(fa[x])
            return fa[x]
        def union(x, y):
            fx, fy = find(x), find(y)
            if fx!=fy: fa[fx] = fy
        for x in nums:
            ps = getPrimes(x)
            ia = p2idx[ps[0]]
            for p in ps[1:]:
                ib = p2idx[p]
                union(ia, ib)
        return len(set([find(i) for i in range(m)]))==1

sol = Solution()
result = [
    # sol.minExtraChar(s = "leetscode", dictionary = ["leet","code","leetcode"]),
    # sol.maxStrength(nums = [3,-1,-5,2,5,-9]),
    # sol.maxStrength(nums = [-4,-5,-4]),
    # sol.maxStrength([0]),
    # sol.maxStrength([0,-1]),
    sol.canTraverseAllPairs(nums = [2,3,6]),
    sol.canTraverseAllPairs(nums = [3,9,5]),
    sol.canTraverseAllPairs(nums = [4,3,12,8]),
    sol.canTraverseAllPairs([51,46,4,3,48,9,49,7,54])
]
for r in result:
    print(r)
