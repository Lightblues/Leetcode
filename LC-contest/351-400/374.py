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
https://leetcode.cn/contest/weekly-contest-374
https://leetcode.cn/circle/discuss/XH8i1L/

非常高质量的一场! T2 需要一些intuition; T3因为思路不清晰完全被卡住了; T4 组合数学! 

Easonsi @2023 """

mod = (10 ** 9 + 7)
factorial = [1] * (10 ** 5 + 1)
for i in range(1, 10 ** 5 + 1):
    factorial[i] = factorial[i - 1] * i % mod

@lru_cache(maxsize=None)
def getProductInverse(x, MOD=mod):
    # 计算数字 x 关于质数 MOD 的乘法逆元
    return pow(x, MOD-2, MOD)

class Solution:
    """ 100144. 找出峰值 """
    
    """ 100153. 需要添加的硬币的最小数量 #题型 已有一组硬币, 问最少需要添加多少硬币, 可以组合得到任意 [1...target] 的数额
思路1: 归纳法
见 [灵神](https://leetcode.cn/problems/minimum-number-of-coins-to-be-added/solutions/2551707/yong-gui-na-fa-si-kao-pythonjavacgo-by-e-8etj/)
    """
    def minimumAddedCoins(self, coins: List[int], target: int) -> int:
        coins.sort()
        acc = 0; ans = 0
        idx = 0; n = len(coins)
        while acc < target:
            while idx<n and coins[idx]<=acc+1:
                # 硬币可以直接进行扩充
                acc += coins[idx]
                idx += 1
            if acc < target:
                # coin = pow(2, ceil(math.log2(acc)))       # 注意这里不需要取整
                coin = acc + 1
                acc += coin
                ans += 1
        return ans
    
    """ 100145. 统计完全子字符串 #medium 要求统计「完全字符串」的数量. 其要求: 1] 每个字符出现的次数均为k次; 2] 相邻字符在字母表中最多相差2
限制: n 1e5
思路1: 
    枚举所有长 k,2k,3k... 的子串, 然后判断是否满足条件, 注意一共只有 26个长度!
代码冗长, 参见 [灵神](https://leetcode.cn/problems/count-complete-substrings/solutions/2551743/bao-li-hua-chuang-mei-ju-chuang-kou-nei-31j5m/)
    """
    def countCompleteSubstrings(self, word: str, k: int) -> int:
        # 缝缝补补, TLE
        n = len(word)
        word = [ord(x)-ord('a') for x in word]
        def count(arr, d=1):
            # 统计 arr 中长度为 d*k 的子串中, 满足条件的个数
            if d==0: return 0   # 边界
            n = len(arr)
            ll = d*k
            if n < ll: return 0
            cnt = Counter(arr[:ll])
            # num_diff = sum(1 for x in cnt if cnt[x]!=k)
            # ans = int(num_diff==0)
            ans = int(sum(1 for x in cnt if cnt[x]!=k)==0)
            for idx in range(ll, n):
                cnt[arr[idx-ll]] -= 1
                if cnt[arr[idx-ll]] == 0: del cnt[arr[idx-ll]]
                # if cnt[arr[idx-ll]] in (0, k): num_diff -= 1
                # elif cnt[arr[idx-ll]] == k-1: num_diff += 1
                cnt[arr[idx]] += 1
                # if cnt[arr[idx]] == k: num_diff -= 1
                # elif cnt[arr[idx]] == 1: num_diff += 1
                ans += int(sum(1 for x in cnt if cnt[x]!=k)==0)
            return ans
        # 分割算法, 写地稀烂, 实际上一个for即可
        splits = []
        l, r = 0, 1
        while r <= n:
            while r<n and abs(word[r]-word[r-1])<=2:
                r += 1
            splits.append(word[l:r])
            l, r = r, r+1
        if len(word) == 1: 
            splits = [word]
        # 统计
        ans = 0
        for arr in splits:
            for d in range(1, 27):
                ans += count(arr, d)
        return ans

    def countCompleteSubstrings(self, word: str, k: int) -> int:
        n = len(word)
        word = [ord(x)-ord('a') for x in word]
        def count(arr):
            res = 0
            n = len(arr)
            for i in range(1,27):
                if i * k > n: break
                ll = i * k
                cnt = Counter(arr[:ll])
                cnt_freq = Counter(cnt.values())        # 两重 count, 来记录每个数字出现的次数
                if cnt_freq[k] == i: res += 1
                for idx in range(ll, n):
                    cnt_freq[cnt[arr[idx-ll]]] -= 1
                    cnt[arr[idx-ll]] -= 1
                    cnt_freq[cnt[arr[idx-ll]]] += 1

                    cnt_freq[cnt[arr[idx]]] -= 1
                    cnt[arr[idx]] += 1
                    cnt_freq[cnt[arr[idx]]] += 1
                    if cnt_freq[k] == i: res += 1
            return res
        # 分割
        l = 0
        ans = 0
        for r in range(1, n):
            if abs(word[r]-word[r-1]) > 2:
                ans += count(word[l:r])
                l = r
        ans += count(word[l:])
        return ans


    """ 100146. 统计感冒序列的数目 #hard 有一个序列, 初始有一组人感冒, 每个人可以传给边上一个. 假设每个时间只能传染一个人, 问所有可能的序列数量. 
限制: n 2e5; 对结果取模
思路1: #数学
    考虑例子里面的 [1,0,0,0,1] 这种中间的情况, 可以分析得到可能序列为 2^{d-1} 种
        对于边界的 [1,0,0,0] 情况, 只有一种
    组合多种元素, 例如 [0,1,0,0], 两种之间不相关, 也即 C(3,1)
    计算优化: 对于所有的空格情况, 有 C(n, k1) * C(n-k1, k2) * ... * C(n-k1-k2-...-kn-1, kn)
        = n! / (k1! * k2! * ... * kn!)
    技巧: 需要用到 「乘法逆元」
反思: 一开始用了 `math.comb` 等函数, 但由于没有 MOD选项直接TLE
    而这种自己手动实现效率反而更好, 参见灵神实现的 comb函数! 
参见 [灵神](https://leetcode.cn/problems/count-the-number-of-infection-sequences/solutions/2551734/zu-he-shu-xue-ti-by-endlesscheng-5fjp/)
    """
    def numberOfSequence(self, n: int, sick: List[int]) -> int:
        # TLE
        mod = 10**9+7
        n_space = n - len(sick)
        lls = [sick[i]-sick[i-1]-1 for i in range(1, len(sick)) if sick[i]-sick[i-1] > 1]
        ans = 1
        left = n_space
        for ll in lls:
            ans *= pow(2, ll-1, mod)
            ans *= math.comb(left, ll)
            left -= ll
            ans %= mod
        ans *= math.comb(left, sick[0])
        ans %= mod
        return ans
    def numberOfSequence(self, n: int, sick: List[int]) -> int:
        mod = 10**9+7
        left = n - len(sick)
        lls = [sick[i]-sick[i-1]-1 for i in range(1, len(sick)) if sick[i]-sick[i-1] > 1]
        ans = pow(2, sum(lls)-len(lls), mod)
        ans = (ans * factorial[left]) % mod
        for ll in lls + [sick[0], n-sick[-1]-1]:
            ans *= getProductInverse(factorial[ll])
            ans %= mod
            left -= ll
        return ans
sol = Solution()
result = [
    # sol.minimumAddedCoins(coins = [1,4,10], target = 19),

    sol.countCompleteSubstrings("pwpkkwwkwwlklw", 1),
    sol.countCompleteSubstrings(word = "igigee", k = 2),
    sol.countCompleteSubstrings(word = "aaabbbccc", k = 3),
    sol.countCompleteSubstrings("a", 1),
    sol.countCompleteSubstrings("ba", 1), 

    # sol.numberOfSequence(n = 5, sick = [0,4]),
    # sol.numberOfSequence(n = 4, sick = [1]),
    # sol.numberOfSequence(5, [0,1]), 
]
for r in result:
    print(r)
