""" 
https://oi-wiki.org/math/number-theory/sieve/
"""

class Solution:
    @staticmethod
    def eratosthenes(n):
        # 埃拉托斯特尼筛法 https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes 
        # 复杂度 O(n loglogn)
        is_prime = [True] * (n + 1)
        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        return [x for x in range(2, n + 1) if is_prime[x]]
    
    @staticmethod
    def euler(n):
        # 线性筛法 也称为 Euler 筛法（欧拉筛法）。 https://oi-wiki.org/math/number-theory/sieve/
        # 复杂度 O(n)
        vis = [False] * (n+1)
        pri = [0] * (n+1)
        cnt = 0
        for i in range(2, n+1):
            if vis[i] == False:
                pri[cnt] = i
                cnt += 1
            # 匹配所有的质数
            for j in range(0, cnt):
                if i*pri[j] > n:
                    break
                vis[i*pri[j]] = True
                # i 已经被 pri[j] 筛掉过了!!
                if i % pri[j] == 0:
                    break
        return pri[:cnt]

sol = Solution()
result = [
    sol.eratosthenes(100),
    sol.euler(100),
]
for r in result:
    print(r)
