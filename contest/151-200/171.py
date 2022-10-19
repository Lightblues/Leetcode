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
https://leetcode.cn/contest/weekly-contest-171

T3之前做过了; T4有点意思.

@2022 """
class Solution:
    """ 1317. 将整数转换为两个无零整数的和 """
    
    """ 1318. 或运算的最小翻转次数 """
    def minFlips(self, a: int, b: int, c: int) -> int:
        ans = 0
        for i in range(32):
            mask = 1<<i
            if c & mask > 0: 
                if not (a&mask or b&mask): ans += 1
            else: ans += (a&mask > 0) + (b&mask>0)
        return ans
    
    """ 1319. 连通网络的操作次数 见并查集 """
    
    """ 1320. 二指输入的的最小距离 #hard #interest 有一个 5*6 的grid记录了ABCD排列的英文字母. 用两个手指输入. 现在给定一个字符串, 问两个手指最小的移动距离. 限制: n 300
思路1: #记忆化 #DP
    记 `f[i, x,y]` 表示输入到第i个字符, 两个手指分别在x,y位置的最小距离. 
    注意到, 很多状态都是没有意义的, 只有 x/y == word[i] 时才有意义. 
    复杂度: 状态 n * C^2, 转移 C, 总复杂度 O(n * C^3). 但会剪枝掉很多.
[官答](https://leetcode.cn/problems/minimum-distance-to-type-a-word-using-two-fingers/solution/er-zhi-shu-ru-de-de-zui-xiao-ju-chi-by-leetcode-so/)
"""
    def minimumDistance(self, word: str) -> int:
        chars = string.ascii_uppercase
        # 计算一个手指从字符 a 到 b 的距离
        def get_pos(c):
            return divmod(chars.index(c), 6)
        @lru_cache(None)
        def dist(a,b):
            x1,y1 = get_pos(a)
            x2,y2 = get_pos(b)
            return abs(x1-x2) + abs(y1-y2)
        
        n = len(word)
        # 记忆化搜索: `f[i, x,y]` 表示输入到第i个字符, 两个手指分别在x,y位置的最小距离. 
        @lru_cache(None)
        def f(i, x,y):
            if i==n: return 0
            ch = word[i]
            # if x!=ch and y!=ch: return inf
            ret = inf
            if x==ch:
                for c in chars: ret = min(ret, f(i+1, c, y) + dist(c, ch))
            if y==ch:
                for c in chars: ret = min(ret, f(i+1, x, c) + dist(c, ch))
            return ret
        # 需要遍历所有的起始位置
        ans = inf
        for x in chars:
            for y in chars:
                ans = min(ans, f(0, x,y))
        return ans
    
sol = Solution()
result = [
    # sol.minFlips(a = 2, b = 6, c = 5),
    sol.minimumDistance(word = "CAKE"),
]
for r in result:
    print(r)
