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
https://leetcode.cn/contest/weekly-contest-381
一共只有两道题, T4 的边界情况有点复杂! 

Easonsi @2023 """
class Solution:
    """ 3014. 输入单词需要的最少按键次数 I """
    def minimumPushes(self, word: str) -> int:
        N = 8
        cnt = Counter(word)
        ans = 0
        tmp = N; vv = 1
        for c in sorted(cnt.values(), reverse=True):
            if tmp > 0:
                ans += vv * c
                tmp -= 1
            else:
                vv += 1
                tmp = N-1
                ans += vv * c
        return ans
    
    """ 3015. 按距离统计房屋对数目 I """
    
    """ 3016. 输入单词需要的最少按键次数 II """
    
    """ 3017. 按距离统计房屋对数目 II 有 1...n 个房屋, 相邻之间有路, 另外还有一个 (x,y) 一条捷径. 要求计算所有的 (i,j) 房间对中, 距离分别为 1...n 的房屋对数目
限制: n 1e5
    可以画个图演示一下, 例如 x=2,y=5, 并讨论 i=1/3/4 等情况
思路1: 考虑时间复杂度与不同区域计算距离的方式——一段段的线段
    见 [小羊](https://leetcode.cn/circle/discuss/EKRE68/)
    化简为 x<=y, 同时仅仅考虑 i<j 的情况 (答案*2即可)
    首先, 什么情况下走捷径更快? 注意到, **对于一个点j, 若某一点i到j需要走捷径, 那么i左侧的点一定都走捷径** (反过来也成立)! 因此, 下面就是找到那个「关键点」
    考虑 i...x...y... 的情况, 我们需要找到 [x,y] 中间的点a, 其右边的点通过xy捷径可以更快!
        也即, a-i <= |x-i| + 1 + y-a, 化简得到 2a <= |x-i| + 1 + i + y 的情况下, 从i直接走到点a更快!
        根据点a分成三段: 第一段是 [i+1,a], 距离为 [1...a-i]; 第二段是 [a+1,y], 距离为 |a-i|+1 + [0...y-(a+1)]; 第三段是 [y+1,n-1], 距离为 |a-i|+1 + [1...(n-1)-(y+1)]
    什么情况下可以走捷径? 显然边界点在 x...y 之间!, 满足的条件是 y-aa <= aa-x+1, 也即 aa>=(y+x-1)/2
        此时, 需要计算的距离为 [1...(n-1)-i]
[ling](https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-ii/solutions/2613373/yong-che-xiao-de-fang-shi-si-kao-pythonj-o253/)
    """
    def countOfPairs(self, n: int, x: int, y: int) -> List[int]:
        if x==y:
            # 对于下面的「第三段」, 不加这个特殊判断会出错!
            ans = [0] * n
            for i in range(n):
                ans[-i-1] = 2*(i)
            return ans
        if x > y:
            x, y = y, x
        x,y = x-1,y-1
        # 
        acc = [0] * (n+1)
        for i in range(n):
            if i>=y or i>=(y+x-1)/2:
                # 距离为 [1...(n-1)-i]
                acc[1] += 1
                acc[n-i] -= 1
            else:
                a = (abs(x-i)+1+i+y) // 2
                dist = abs(i-x)

                # 第一段是 [i+1,a], 距离为 [1...a-i]
                acc[1] += 1
                acc[a-i+1] -= 1
                # 第二段是 [a+1,y], 距离为 |a-i|+1 + [0...y-(a+1)]
                if a+1<=y:
                    acc[dist+1] += 1
                    acc[dist+1 + y-a] -= 1
                # 第三段是 [y+1,n-1], 距离为 |a-i|+1 + [1...(n-1)-y]
                if y+1<=n-1:
                    acc[dist+1 + 1] += 1
                    acc[dist+1 + n-y] -= 1
        for i in range(1, n+1):
            acc[i] += acc[i-1]
        return [2*i for i in acc[1:]]




    
sol = Solution()
result = [
    # sol.minimumPushes(word = "xycdefghij"),
    # sol.minimumPushes(word = "aabbccddeeffgghhiiiiii"),
    # sol.countOfPairs(n = 3, x = 1, y = 3),
    sol.countOfPairs(n = 5, x = 2, y = 4),
    # sol.countOfPairs(n = 4, x = 1, y = 1),
    sol.countOfPairs(3,2,2),

]
for r in result:
    print(r)
