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
https://leetcode.cn/contest/weekly-contest-183

T3之前每日一题写过, 庆幸写出了一个更简洁的代码, 不过官答的逻辑更清楚些. T4乍一碰到还是懵逼, 但实际上的难度其实不大, 有时间总结一下「博弈」的题目吧~

@2022 """
class Solution:
    """ 1403. 非递增顺序的最小子序列 """
    
    """ 1404. 将二进制表示减到 1 的步骤数 """
    
    """ 1405. 最长快乐字符串 #medium 给定三个数字 a,b,c 分别是字符 abc 的数量, 构造最长字符串, 满足其中不包含三个连续的相同子字符串, 例如 aaa
思路1: #贪心. 每次选择剩下的数量最多的字符串, (超过1个的话) 放置2个. 
    细节: 注意避免连续两次取到相同字符的情况.
    另一种贪心的思路是, 每次选择剩余最多的字符串, 避免连续取到三个. 见 [官答](https://leetcode.cn/problems/longest-happy-string/solution/zui-chang-kuai-le-zi-fu-chuan-by-leetcod-5nde/).
另见 [daily2202] 写了一个比较繁琐的分解.
"""
    def longestDiverseString(self, a: int, b: int, c: int) -> str:
        q = []
        for i,v in zip('abc', [a,b,c]):
            if v: heappush(q, (-v, i))
        ret = ""
        while q:
            c,ch = heappop(q)
            if ret and ch==ret[-1]:
                if not q: return ret
                c2,ch2 = heappop(q)
                ret += ch2; c2+=1
                if c2<0: heappush(q, (c2,ch2))
            cnt = min(-c, 2)
            ret += ch*cnt; c+=cnt
            if c<0: heappush(q, (c,ch))
        return ret
    
    """ 1406. 石子游戏 III #hard #题型 #博弈 有一个数列表示分数, AB轮流取, 每次可以选择取1/2/3个数字. 在最优策略下问谁会赢. 限制: n 5e4. 元素大小 +/-1e3
思路1: #DP 考虑还剩下 i... 石子时的最优解. 双方地位对等.
    我们用 `f[i]` 表示还剩下 i... 位置的分数, 某玩家进行决策得到的最优分数.
    分类: 假设选择1个数字, 则对方得到的分数为 `f[i+1]`. 因此 `arr[i] + sum(i...n) - f[i+1] = sum(i...n) - f[i+1]` 是当前玩家得到的分数.
        根据三种情况, 可知我们的最优解为 `max{ sum(i...n) -f[i+x] }` 这里x的取值为1/2/3.
    因此, 我们倒序计算f, 并且可以利用前缀和优化.
思路2: 还可以令 `f[i]` 表示还剩 i... 石子, 「当前玩家比下一位玩家最多能多拿到的石子数目」
    这样, 若拿一个, 则为 `arr[i] - f[i+1]`.
    因此, 转移 `f[i] = max{ sum(i,i+x) - f[i+x] }` 这里x的取值为1/2/3.
参见 [官答](https://leetcode.cn/problems/stone-game-iii/solution/shi-zi-you-xi-iii-by-leetcode-solution/)
"""
    def stoneGameIII(self, values: List[int]) -> str:
        n = len(values)
        acc = list(accumulate(values, initial=0))
        f = [0] * (n+3)     # 为了避免越界, 多开3个空间
        for i in range(n-1,-1,-1):
            s = acc[n] - acc[i]
            f[i] = max(s - f[i+x] for x in range(1,4))
        if f[0] > acc[n] - f[0]: return "Alice"
        elif f[0] < acc[n] - f[0]: return "Bob"
        else: return "Tie"

    
sol = Solution()
result = [
    # sol.longestDiverseString(a = 1, b = 1, c = 7),
    # sol.longestDiverseString(a = 2, b = 2, c = 1),
    # sol.longestDiverseString(a = 7, b = 1, c = 0),
    sol.stoneGameIII(values = [1,2,3,7]),
    sol.stoneGameIII(values = [1,2,3,-9]),
    sol.stoneGameIII(values = [1,2,3,6]),
    sol.stoneGameIII(values = [1,2,3,-1,-2,-3,7]),
]
for r in result:
    print(r)
