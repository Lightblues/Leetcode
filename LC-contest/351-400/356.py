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
https://leetcode.cn/contest/weekly-contest-356
T3用了暴力的做法, 因为不考察复杂度~ T4 数位DP好久没写了, 背函数接口!!
Easonsi @2023 """
class Solution:
    """ 2798. 满足目标工作时长的员工数目 """
    def numberOfEmployeesWhoMetTarget(self, hours: List[int], target: int) -> int:
        return sum(1 if x>=target else 0 for x in hours)
    
    """ 2799. 统计完全子数组的数目 #medium 定义完全子数组为, 包含不同元素的数量和完整数组相同. 
    """
    def countCompleteSubarrays(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        mx = len(set(nums))
        for i in range(n):
            j = i
            s = set()
            while j<n and len(s)<mx:
                s.add(nums[j])
                j += 1
            ans += n-(j-1) if len(s)==mx else 0
        return ans
    
    """ 2800. 包含三个字符串的最短字符串 #medium 给定三个字符串, 问包含着三个字符串的最短字符串. 若有多个则取字典序最小的. 
限制: n 100
思路1: 暴力枚举 #全排列
    因为不卡时间, 主要是功能实现
思路2: 灵神提出
    O(n) 的做法是用 KMP 计算 t+"#"+s 的最长相同前后缀。
    """
    def minimumString(self, a: str, b: str, c: str) -> str:
        def merge(a:str, b:str):
            """ 顺序连接 a,b """
            if b in a: return a
            
            n = min(len(a), len(b))
            mx = 0  # 计算最大重叠
            for i in range(1,n+1):
                if a[-i:]==b[:i]: mx = i
            return a + b[mx:]
        mn = inf
        for x,y,z in permutations([a,b,c]):
            t = merge(merge(x,y),z) 
            # 取字典序最小的
            if len(t) < mn or len(t)==mn and t<ans:
                mn = len(t)
                ans = t
        return ans

    """ 2801. 统计范围内的步进数字数目 #hard 定义「步进数字」为每个数位相差都是1, 问在 [l,r] 范围内的数量
限制: 数字大小 1e100
思路1: 通用数位DP
    f(i,pre,isLimit,isNum) 其中 
        pre表示上一个数字, 
        isLimit表示是否在边界上, 若在的话, 当前数字就不能填比 s[i] 更大的数字
        isNum表示是否有前缀, 没有的话当前不能填 0
    函数入口: f(0, x, True, False)
    边界: i==n 时候, 返回 int(isNum)
    具体到这道题, 1] 若非num, 则当前可以填入 1-9, 2] 若是num, 则当前可以填入 pre-1, pre+1. 然后进行过滤, 并更新两个flag
见 [灵神](https://leetcode.cn/problems/count-stepping-numbers-in-range/solution/shu-wei-dp-tong-yong-mo-ban-by-endlessch-h8fj/)
    """        
    def countSteppingNumbers(self, low: str, high: str) -> int:
        mod = 10**9+7
        def count(s:str):
            n = len(s)
            @lru_cache(None)
            def f(i,pre,isLimit,isNum) -> int:
                # 边界
                if i==n: return int(isNum)
                ans = 0
                # cand 为可能可以填入的数字
                if isNum:
                    cand = [pre-1, pre+1]
                    cand = [d for d in cand if 0<=d<=9]
                else:
                    cand = list(range(0,10))
                for d in cand:
                    # 过滤不合法的
                    if isLimit and d>int(s[i]): continue
                    _isLimit = isLimit and (d==int(s[i]))
                    _isNum = isNum or d!=0
                    ans += f(i+1, d, _isLimit, _isNum)
                return ans % mod
            return f(0,0,True,False)
        return (count(high) - count(str(int(low)-1))) % mod



sol = Solution()
result = [
    # sol.countCompleteSubarrays([1,3,1,2,2]),
    # sol.minimumString(a = "abc", b = "bca", c = "aaa"),
    # sol.minimumString("cab","a","b"),
    sol.countSteppingNumbers(low = "1", high = "11"),
    sol.countSteppingNumbers(low = "90", high = "101"),
]
for r in result:
    print(r)
