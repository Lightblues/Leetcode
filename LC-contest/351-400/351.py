from itertools import count
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
https://leetcode.cn/contest/weekly-contest-351
Easonsi @2023 """
class Solution:
    """ 2748. 美丽下标对的数目 """
    def countBeautifulPairs(self, nums: List[int]) -> int:
        n = len(nums)
        a,b = [],[]
        for x in nums:
            a.append(int(str(x)[0]))
            b.append(int(str(x)[-1]))
        ans = 0
        for i,aa in enumerate(a):
            for j in range(i+1,n):
                bb = b[j]
                if math.gcd(aa,bb)==1: ans += 1
        return ans

    """ 2749. 得到整数零需要执行的最少操作数 #medium 对于一个数字a, 问能否经过分解成一些数字之和. 这些数字是, 2^i+b, 其中 i=[0,60] 
限制: a [1,1e9], b [-1e9, 1e9]
思路1: 枚举答案
    问题等价于, 对于操作次数k, 要求的 x = a-k*b 是否可以分解成 k个 2^i 之和
    分类讨论
        x < k, 不可能
        x.bit_count() >= k, 不能
        x.bit_count() < k, 可以! 因为可以分解 2^i = 2 * 2^{i-1}
    边界: 注意当 x < k 时, 说明 num2<0, 这样, 更大的k只会使得x更小! 因此直接break
[灵神](https://leetcode.cn/problems/minimum-operations-to-make-the-integer-zero/solution/mei-ju-da-an-pythonjavacgo-by-endlessche-t4co/)
    """
    def makeTheIntegerZero(self, num1: int, num2: int) -> int:
        # itertools.count(start=0, step=1)
        for k in count(1):
            x = num1 - num2 * k
            # 同时对于 k个 2^i 之和 >=k 进行了检查!
            # 注意边界!! 若出现 x < k, 说明 num2<0
            if x < k: return -1
            if k >= x.bit_count(): return k

    
    """ 2750. 将数组划分成若干好子数组的方式 """
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        mod = 10**9+7
        s = ''.join(map(str, nums))
        # 边界!!
        if '1' not in s: return 0
        s = s.strip('0')
        ss = s.split('1')
        ans =1
        for i in ss:
            ans = (ans * (len(i)+1)) % mod
        return ans
    
    """ 2751. 机器人碰撞 #hard 每个机器人 (pos, health, dir) 按照相同速度移动, 发生碰撞则health小的消失, 大的-1, 问最后剩下的机器人
限制: n 1e5; pos, health 1e9
思路1: #栈 模拟
关联: 「0735. 行星碰撞」
[灵神](https://leetcode.cn/problems/robot-collisions/solution/zhan-mo-ni-by-endlesscheng-fu26/)
     """
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        bots = [(p,i,d) for i,(p,d) in enumerate(zip(positions, directions))]
        bots.sort(key=lambda x: x[0])
        st = []
        for p,i,d in bots:
            if d=="R":
                st.append((i))
            else:
                while st and healths[st[-1]] < healths[i]:
                    idx = st.pop()
                    healths[idx] = 0
                    healths[i] -= 1
                if st:
                    if healths[st[-1]] == healths[i]:
                        idx = st.pop()
                        healths[idx] = 0
                        healths[i] = 0
                    elif healths[st[-1]] > healths[i]:
                        healths[i] = 0
                        healths[st[-1]] -= 1
        return [i for i in healths if i>0]


sol = Solution()
result = [
    # sol.countBeautifulPairs(nums = [2,5,1,4]),

    # sol.numberOfGoodSubarraySplits(nums = [0,1,0,0,1]),
    # sol.numberOfGoodSubarraySplits([0,1,0]),

    sol.survivedRobotsHealths(positions = [1,2,5,6], healths = [10,10,11,11], directions = "RLRL"),
    sol.survivedRobotsHealths(positions = [3,5,2,6], healths = [10,10,15,12], directions = "RLRL"),
    sol.survivedRobotsHealths(positions = [5,4,3,2,1], healths = [2,17,9,15,10], directions = "RRRRR"),
]
for r in result:
    print(r)
