# from easonsi.util.leetcode import *
from typing import *
from math import ceil, factorial
from collections import Counter

# def testClass(inputs):
#     # 用于测试 LeetCode 的类输入
#     s_res = [None] # 第一个初始化类, 一般没有返回
#     methods, args = [eval(l) for l in inputs.split('\n')]
#     class_name = eval(methods[0])(*args[0])
#     for method_name, arg in list(zip(methods, args))[1:]:
#         r = (getattr(class_name, method_name)(*arg))
#         s_res.append(r)
#     return s_res

""" 
https://leetcode.cn/contest/biweekly-contest-138

T3 的排列计数很有难度! 需要基本功
T4 贪心比较容易想到, 自己简单推了一下证明, 还不错
Easonsi @2025 """
class Solution:
    """ 3270. 求出数字答案 """
    def generateKey(self, num1: int, num2: int, num3: int) -> int:
        nums = [f"{d:04d}" for d in [num1, num2, num3]]
        digits = [min(d[i] for d in nums) for i in range(4)]
        return int(''.join(digits))
    
    """ 3271. 哈希分割字符串 """
    def stringHash(self, s: str, k: int) -> str:
        def hash(s: str) -> chr:
            d = sum(ord(ch)-ord('a') for ch in s)
            return chr(ord('a')+d%26)
        return ''.join(hash(s[i:i+k]) for i in range(0, len(s), k))
    
    """ 3272. 统计好整数的数目 #hard 定义好整数为 经过重排 (没有前置0) 后可以变为 1) 被k整除的 2) 回文数
问所有n位数中, 好整数的个数. 限制: n 10; k 9
思路1:
    枚举回文数 "左半边" (包括 n%2==1 时中间的数字). 
    定义: m = floor((n-1)/2); base = 10^m; 统计的范围是 [base, base*10)
        例如, n=2 时, 范围为 [1,10)
        n=3 时, 范围为 [10,100)
        这样, 总枚举的复杂度为 O(base)
    如何减少次数? 
        对于一个满足要求的数字s, 显然我们可以通过 sort(s) 来过滤掉重复枚举. 因此, 引入一个 vis 集合
        s需要满足 s + s[::-1][n%2:] 可以被 k 整除
    对于满足要求的s, 其可以构成多少不重复的 "好整数"?
        (n-cnt[0]) * (n-1)! / prod{cnt[i]!}
        第一项时因为不能有前置0; 其他项是排列数; 分母是去除重复
[ling](https://leetcode.cn/problems/find-the-count-of-good-integers/solutions/2899725/mei-ju-suo-you-hui-wen-shu-zu-he-shu-xue-3d35/)
    """
    def countGoodIntegers(self, n: int, k: int) -> int:
        factorials = [factorial(i) for i in range(n+1)]
        base = 10 ** ((n-1)//2)
        ans = 0
        vis = set()
        for i in range(base, base*10):
            s = str(i)
            s = s + s[::-1][n%2:]
            if int(s) % k != 0:  # 回文数不能被k整除
                continue
            sorted_s = "".join(sorted(s))
            if sorted_s in vis:  # 已经计数过
                continue
            vis.add(sorted_s)
            cnt = Counter(s)
            c = (n-cnt["0"]) * factorials[n-1]  # NOTE: 这里应该是 char
            for i in cnt.values():
                c //= factorials[i]
            ans += c
        return ans
    
    """ 3273. 对 Bob 造成的最少伤害 #hard bob 的伤害为 power. 对于n个敌人, 每个人的伤害为 damage, 血量为 health. 敌人先攻击后bob选择一个攻击, 问如何攻击, 受到的总伤害最小. 
限制: n 1e5
思路1: #贪心 #邻项交换法
    看一个例子:
        damage=(1,2,3,4), count=(1,2,2,2) -> 计算他们的比值 1, 1, 1.5, 2
        猜测: 优先攻击 damage/count 更大的敌人
        10*2 + 6*2 + 3*2 + 1*1 = 39
    规律1: 当两个敌人的 damage/count 相同时, 交换它们的顺序不会影响结果
        damage=(a,b), count=(a,b). 
            (a+b)*a + b*b = (a+b)*b + a*a
    规律2: 需要优先攻击 damage/count 更大的敌人
        damage=(a,b), count=(c,d). 且 a/c > b/d
        先攻击第一个: (a+b)*c + b*d
        先攻击第二个: (a+b)*d + a*c
        两者相减 bc-ad < 0
见 [ling](https://leetcode.cn/problems/minimum-amount-of-damage-dealt-to-bob/solutions/2899709/tan-xin-ji-qi-zheng-ming-lin-xiang-jiao-7lnjf/)
    """
    def minDamage(self, power: int, damage: List[int], health: List[int]) -> int:
        counts = [ceil(h/power) for h in health]
        values = [d/c for d, c in zip(damage, counts)]
        s = sum(damage)
        ll = list(zip(values, damage, counts))
        ll.sort(reverse=True)
        ans = 0
        for _, d, c in ll:
            ans += s * c
            s -= d
        return ans
        

sol = Solution()
result = [
    # sol.generateKey(num1 = 987, num2 = 879, num3 = 798),
    # sol.stringHash(s = "abcd", k = 2),

    sol.countGoodIntegers(n = 3, k = 5),
    sol.countGoodIntegers(n = 5, k = 6),

    # sol.minDamage(power = 4, damage = [1,2,3,4], health = [4,5,6,8]),
]
for r in result:
    print(r)
