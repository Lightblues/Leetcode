from easonsi import utils
from easonsi.util.leetcode import *

""" 



@2022 """
class Solution:
    """ 0050. Pow(x, n) 实现快速幂运算 #题型 #快速幂 #迭代
限制: n的范围在 -2^31 到 2^31 - 1 之间
思路0: 暴力二分, 利用 @cache
思路1: #递归 思路
    对于指数从小到大进行切分. 例如 `x^8` 可以切分为 `x^4 * x^4`, 而 `x^9` 则可以切分为 `x^4 * x^4 * x`
    实现递归函数 `recc(x, k)` 即可
思路2: 将递归展开为 #迭代
    以指数 9 为例, 观察其二进制表示 `1001`, 因此可以将 `x^9` 分解为 `x^(2^3) * x^(2^0)`
    因此, 指数的二进制表示上的每一个数位, 其对应的x的贡献也是一一对应的, 呈指数增长. 因此, 可以采用迭代bit位的方式, 在迭代过程中维护 `x_contribute` 表示每一位的贡献
[官答](https://leetcode.cn/problems/powx-n/solution/powx-n-by-leetcode-solution/)
"""
    @lru_cache(None)
    def myPow(self, x: float, n: int) -> float:
        """ 直接用了cache """
        if n==0: return 1
        elif n<0: return 1/self.myPow(x, -n)
        elif n==1: return x
        else: return self.myPow(x, n//2) * self.myPow(x, n - n//2)
        
    def myPow(self, x: float, n: int) -> float:
        """ 递归 """
        def quickMul(N):
            if N == 0:
                return 1.0
            y = quickMul(N // 2)
            return y * y if N % 2 == 0 else y * y * x
        
        return quickMul(n) if n >= 0 else 1.0 / quickMul(-n)

    def myPow(self, x: float, n: int) -> float:
        """ 迭代 """
        def quickMul(N):
            ans = 1.0
            # 贡献的初始值为 x
            x_contribute = x
            # 在对 N 进行二进制拆分的同时计算答案
            while N > 0:
                if N % 2 == 1:
                    # 如果 N 二进制表示的最低位为 1，那么需要计入贡献
                    ans *= x_contribute
                # 将贡献不断地平方
                x_contribute *= x_contribute
                # 舍弃 N 二进制表示的最低位，这样我们每次只要判断最低位即可
                N //= 2
            return ans
        
        return quickMul(n) if n >= 0 else 1.0 / quickMul(-n)

    """ 0470. 用 Rand7() 实现 Rand10() #medium #题型 #概率 给定一个函数 rand7 可以生成 [1,7] 随机整数, 要求用它来实现 rand10
思路1: #拒绝采样
    依次随机生成两个数字. 则可以构成 7*7=49 种情况, 可以可以利用前面的 40种情况; 对于 41-49, 我们拒绝, 重新生成
    注意: 把两次投掷分别看成一个7位数的高位和低位. 因此 #压缩表示 是 7x+y 的形式 (还要注意范围的变换!)
题解+相关的题目见 [here](https://leetcode.cn/problems/implement-rand10-using-rand7/solution/cong-pao-ying-bi-kai-shi-xun-xu-jian-jin-ba-zhe-da/)
思路1.1: 优化拒绝的部分
    实际上我们可以利用剩下的数字 (作为前一次投掷的结果)
    见 [官答](https://leetcode.cn/problems/implement-rand10-using-rand7/solution/yong-rand7-shi-xian-rand10-by-leetcode-s-qbmd/)
"""
    def rand10(self):
        while True:
            # 把两次投掷分别看成一个7位数的高位和低位
            # 注意, rand7 生成的范围是 [1,7], 而7进制的范围是 [0,6]
            v = (rand7()-1) * 7 + (rand7()-1)
            if v>=40: continue
            return v%10 + 1 # 生成范围 [1,10]

""" 0478. 在圆内随机生成点 #medium #题型 给定 (x,y,r), 在圆内随机生成点
思路1: 在正方形内均匀采样, 然后判断是否在圆内 #拒绝采样
思路2: 分两步随机生成 #逆采样
    先在 [0,2pi] 范围内随机选角度, 然后在 [0,r] 范围内随机选半径
    注意! 第二次随机, 概率密度应该与半径 `radis` 成正比 (圆周长更长)
        因此, 概率密度函数应该是 `f(r) = k * r`; 积分得到 k = 2. 
        因此, 累积分布函数 CDF `F(r) = r^2`
    对于一个给定的累计分布函数, 如果我们想要根据其生成随机变量, 可以通过 $[0,1)$ 的均匀分布生成随机变量 $u$, 找到满足 $F(r)=u$ 的 $r$, 此时 $r$ 即为满足累计分布函数的随机变量。
        从 F(r) = u, F(r) 的单调性, 可以得到 $r = F^{-1}(u) = \sqrt{u}$, 从而得到表达式
[官答](https://leetcode.cn/problems/generate-random-point-in-a-circle/solution/zai-yuan-nei-sui-ji-sheng-cheng-dian-by-qp342/)
"""
import random
class Solution:
    def __init__(self, radius: float, x_center: float, y_center: float):
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center

    def randPoint(self) -> List[float]:
        # 思路1: 在正方形内均匀采样, 然后判断是否在圆内 #拒绝采样
        while True:
            x,y = random.uniform(-1,1), random.uniform(-1,1)
            if x**2 + y**2 <= 1: break
        return self.x_center+self.radius*x, self.y_center+self.radius*y
    def randPoint(self) -> List[float]:
        # 思路2: 分两步随机生成 #逆采样
        d = random.uniform(0, 2*math.pi)
        r = math.sqrt(random.uniform())
        return self.x_center + self.radius*r*math.cos(d), self.y_center + self.radius*r*math.sin(d)

""" 0710. 黑名单中的随机数 #hard 有一个 [0,n) 人员数组, 给定了一组 blacklist, 要求每次随机返回不在黑名单种的用户 
限制: 人数 n <= 10^9, 黑名单长度 m <= 10^5; 
思路0: 当 m很接近n的时候, 拒绝采样的效率会很低, 因为拒绝的概率会很高!
思路1: 注意到, 加入所有的黑名单人id都在 [n-m,n) 范围内, 我们可以直接返回 rand(0,n-m)
    因此, 我们可以把这些人id映射到 [0,n-m) 范围内!
    对于随机生成 x=rand(0,n-m), 若不在映射种则之际返回, 否则返回x映射的值 (替代品)
    [官答](https://leetcode.cn/problems/random-pick-with-blacklist/solution/hei-ming-dan-zhong-de-sui-ji-shu-by-leet-cyrx/)
相较于思路1种神奇的map, 还可以用 #前缀和+#二分 快速找到映射条件? 见[宫水三叶]
"""
class Solution:
    def __init__(self, n: int, blacklist: List[int]):
        self.n = n
        self.bound = n - len(blacklist)
        m = {}; i = self.bound
        for bid in blacklist:
            m[bid] = i
            i += 1
        self.m = m

    def pick(self) -> int:
        x = random.randint(0, self.bound-1) # 注意 randint 是必区间
        return self.m.get(x,x)  # .get 语法

sol = Solution()
result = [
    sol.myPow(0.00001, 2147483647)
    
]
for r in result:
    print(r)
