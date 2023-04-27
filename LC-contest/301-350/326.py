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
https://leetcode.cn/contest/weekly-contest-326


@2022 """
class Solution:
    """ 6278. 统计能整除数字的位数 基本模拟 """
    def countDigits(self, num: int) -> int:
        cnt = 0
        for d in str(num):
            if num%int(d)==0: cnt += 1
        return cnt
    
    """ 6279. 数组乘积中的不同质因数数目 #medium 计算一组数字的不同质因子的个数 """
    def distinctPrimeFactors(self, nums: List[int]) -> int:
        def getPrime(x):
            # 对x进行质因数分解
            primes = set()
            for i in range(2, x+1):
                while x%i==0:
                    primes.add(i)
                    x //= i
                if x==1: break
            return primes
        return len(reduce(lambda x,y: x|y, map(getPrime, nums)))
    
    """ 6196. 将字符串分割成值不超过 K 的子字符串 例如给定字符川 "165462", 在限制 k=60 的条件下, 可以分割为 16/54/6/2
思路1: #贪心. 注意到, 对于本题, 贪心策略是合法的! 
"""
    def minimumPartition(self, s: str, k: int) -> int:
        # 边界: 可能无法完成分割
        if k<10 and max(map(int, s)) > k: return -1
        # 贪心进行分割
        ints = list(map(int, s))
        cnt = 0
        x = 0   # 当前累计的数字
        for i in ints:
            if x*10+i > k:
                cnt += 1
                x = i
            else:
                x = x*10+i
        if x: cnt += 1
        return cnt
    
    """ 6280. 范围内最接近的两个质数 找到在 [l,r] 范围内最接近的两个质数. 限制: n 1e6
思路1: 找到范围内的所有质数.
    如何找质数? 例如可以采用 #埃拉托斯特尼筛法, 见 wiki
    https://oi-wiki.org/math/number-theory/sieve/
"""
    def closestPrimes(self, left: int, right: int) -> List[int]:
        def getPrimes(n):
            # 得到 n 范围内的所有质数. 暴力做法, 会超时!!
            ps = [2,]
            for i in range(3, n+1, 2):
                for p in ps:
                    if i%p==0: break
                    if p*p>i:
                        ps.append(i)
                        break
            return ps
        def eratosthenes(n):
            # 埃拉托斯特尼筛法 https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes 
            is_prime = [True] * (n + 1)
            for i in range(2, int(n ** 0.5) + 1):
                if is_prime[i]:
                    for j in range(i * i, n + 1, i):
                        is_prime[j] = False
            return [x for x in range(2, n + 1) if is_prime[x]]
        # 得到范围内的所有质数
        # primes = getPrimes(right)
        primes = eratosthenes(right)
        primes = [p for p in primes if p>=left]
        # 找到最接近的两个数
        if len(primes)<2: return [-1,-1]
        diff = inf
        for i in range(1, len(primes)):
            if primes[i]-primes[i-1] < diff:
                diff = primes[i]-primes[i-1]
                res = [primes[i-1], primes[i]]
        return res
    
sol = Solution()
result = [
    # sol.countDigits(num = 1248),
    # sol.countDigits(121),
    # sol.distinctPrimeFactors(nums = [2,4,3,7,10,6]),
    # sol.distinctPrimeFactors([2,4,8,16]),
    # sol.minimumPartition(s = "238182", k = 5),
    # sol.minimumPartition(s = "165462", k = 60),
    sol.closestPrimes(left = 10, right = 13),
    sol.closestPrimes(4,6),
    sol.closestPrimes(1, 10**6),
    sol.closestPrimes(958995, 959083),
]
for r in result:
    print(r)
