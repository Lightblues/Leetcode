from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-225
@2022 """
class Solution:
    """ 1736. 替换隐藏数字得到的最晚时间 #easy #题型 
给定一个字符串表示时间, 其中一些位用 `?` 表示未知, 问填充得到最大的时间.
思路1: 纯粹基于规则.
    [官答](https://leetcode.cn/problems/latest-time-by-replacing-hidden-digits/solution/ti-huan-yin-cang-shu-zi-de-dao-de-zui-wa-0s7r/) 中的逻辑更清楚一点.
"""
    def maximumTime(self, time: str) -> str:
        # 实际上的判断不必这么复杂: 按照 0,1,2,3 位分别判断即可
        ans = ""
        if time[:2]=="??": ans += "23"
        elif time[0]=='?':
            if time[1]>'3': ans += '1'+time[1]
            else: ans += '2'+time[1]
        elif time[1]=='?':
            if time[0]=='2': ans += '23'
            else: ans += time[0]+'9'
        else: ans += time[:2]
            
        ans += ":"
        if time[-2:]=="??": ans += '59'
        elif time[-2]=='?':
            ans += '5'+time[-1]
        elif time[-1]=='?':
            ans += time[-2]+'9'
        else:
            ans += time[-2:]
        return ans
    
    
    """ 1737. 满足三条件之一需改变的最少字符数 #medium
给定两个字符串, 每次操作可以修改其中的任一字符为小写字母. 问得到以下三种状态之一, 最少步数. 条件: a的每个字母严格小于b的任意字母; 或者b的每个字母严格大于a的任意字母; 或者a和b都由同一个字母构成.
思路1: #计数, 然后考虑每一种情况.
    debug: 原本直接 [a,z] 遍历了, 但有问题. 因为是 **严格小于关系**, 因此遍历分割字符x的过程中, 要求一个字符串都小于等于x, 另一个都大于x; 因此, 这里的x的实际范围是 `[a,z)`
"""
    def minCharacters(self, a: str, b: str) -> int:
        ca, cb = Counter(a), Counter(b)
        ans = inf
        for ch in string.ascii_lowercase:
            ans = min(ans, len(a)+len(b)-ca[ch]-cb[ch])
        for ch in string.ascii_lowercase[:-1]:
            ans = min(ans,
                sum(v for k,v in ca.items() if k<=ch) + sum(v for k,v in cb.items() if k>ch),
                sum(v for k,v in cb.items() if k<=ch) + sum(v for k,v in ca.items() if k>ch)
            )
        return ans
    
    """ 1738. 找出第 K 大的异或坐标值 #medium #题型
对于一个二维矩阵, 对于每一个 (a,b) 坐标计算的score为, 以 (0,0)和(a,b) 两点确定的矩阵的所有值的异或. 求这些分数中第 K 大的值.
思路1: 采用二维 #前缀和 来存储每个位置的score. 
    需要注意这里前缀和的计算方式: `pre(i,j)=pre(i-1,j) ^ pre(i,j-1) ^ pre(i-1,j-1) ^ matrix(i,j)`. 利用了 x^x=0 这一性质.
    然后要返回第K大的元素, 参见「0215. 数组中的第K个最大元素」.
    [官答](https://leetcode.cn/problems/find-kth-largest-xor-coordinate-value/solution/zhao-chu-di-k-da-de-yi-huo-zuo-biao-zhi-mgick/)
"""
    def kthLargestValue(self, matrix: List[List[int]], k: int) -> int:
        m,n = len(matrix), len(matrix[0])
        xor = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                xor[i][j] = xor[i][j-1]^matrix[i][j] if j>0 else matrix[i][j]
                # if i>0: xor[i][j] ^= xor[i-1][j]
        for i in range(1,m):
            for j in range(n):
                xor[i][j] ^= xor[i-1][j]
        print(xor)
        return sorted(itertools.chain(*xor))[-k]
    
    """ 1739. 放置盒子 #hard #interest #题型
在一个房间放置n个正方体盒子. 只有当底部盒子的四个侧面都是墙壁/其他盒子的情况下, 才能在上面堆叠了. 问最少接触地面的盒子的数量. 图见 [题](https://leetcode.cn/problems/building-boxes/)
提示: 最优的堆叠方式正如题目所示.
思路1: #模拟 堆叠过程, #二分
    先来看最优堆叠情况下, 底层三角形的边长和体积的关系: 
        从上到下每一层的边长分别为 1,2,...,n. 每一层面积为 `s[i] = i*(i+1)/2`. 因此, 体积为 `v[n] = sum{ s[1...n] }` (也可以推导出公式).
    在给定正方形数量n的情况下, 计算最大的满足 `v[j] <= n`  的边长. 然后在其上添加 `remain = n - v[j]` 个正方体即可.
    如何计算需要增加多少个地面元素? 参见下面的演示, 增加关系同样按照三角形面积 s 的方式进行增长. 二分找到最小满足 `remian <= s[j]` 的下标即可.
    
# 底边边长为3的最优堆叠体的顶视图
000
00
0
# 底面增加两个, 可以在上面堆一个. 共 3个
00XX
00X
0
# 再增加一个, 可以另外堆叠两个. 共 6个
0XXX
0XX
0X
"""
    def minimumBoxes(self, n: int) -> int:
        MAX = 10**5
        s = [i*(i+1)//2 for i in range(MAX)]
        v = list(accumulate(s))
        idx = bisect.bisect_right(v, n)
        ans = s[idx-1]
        remain = n - v[idx-1]
        idx = bisect_left(s, remain)
        return ans + idx


    """ 0215. 数组中的第K个最大元素 #medium #题型 #star 给定一个数组, 要求返回其中第k大的元素.
见 [quickSort]
"""

sol = Solution()
result = [
    # sol.minimumBoxes(3),
    # sol.minimumBoxes(4),
    # sol.minimumBoxes(6),
    # sol.minimumBoxes(10),
    
]
for r in result:
    print(r)
