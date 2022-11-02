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
https://leetcode.cn/contest/weekly-contest-159
T1, T2, 都算比较经典. T3 用的是滑窗, 不过边界搞了好久. T4 是经典题型, 可惜一开始想歪了, 直接对于结束时间排序然后对idx进行DP即可, 而不需要对时间离散化. 

@2022 """
class Solution:
    """ 1232. 缀点成线 #easy 检查一组点是否在一条直线上 """
    def checkStraightLine(self, coordinates: List[List[int]]) -> bool:
        x0,y0 = coordinates[0]
        dx,dy = coordinates[1][0]-coordinates[0][0],coordinates[1][1]-coordinates[0][1]
        if dy==0: return len(set(i[1] for i in coordinates))==1
        for x,y in coordinates[2:]:
            if (x-x0)*dy != (y-y0)*dx: return False
        return True
    
    """ 1233. 删除子文件夹 #medium 
思路0: #字典树 记录最短的路径
思路1: 排序之后直接检查
"""
    def removeSubfolders(self, folder: List[str]) -> List[str]:
        folder.sort()
        ans = []
        for f in folder:
            if ans and f.startswith(ans[-1]+"/"): continue
            ans.append(f)
        return ans
    
    """ 1234. 替换子串得到平衡字符串 #medium #题型 有一个长4n的包含四种字符的字符串, 可以用任意字符串替换s的字串, 使得四个字符数量相等. 问最短的替换字符串. 限制: n 1e5
思路1: #滑动窗口
    假设替换的子串是 s[i:j], 什么情况下合法? 剩余部分中, 所有字符的数量都不超过n.
    因此, 可以用 #滑动窗口, 保证滑窗外的字符数量不超过n.
    细节: 注意条件检查, 还有 #边界 问题. 
https://leetcode.cn/problems/replace-the-substring-for-balanced-string/
"""
    def balancedString(self, s: str) -> int:
        n = len(s)//4
        chars = "QWER"
        ch2idx = dict(zip(chars, range(4)))
        cnt = [0]*4
        ans = 4*n
        for c in s: cnt[ch2idx[c]] += 1
        def check(): return all(i<=n for i in cnt)
        l = 0
        for r,x in enumerate(s):
            cnt[ch2idx[x]] -= 1
            if not check(): continue
            # 注意, 这里移动l的时候可能出现 l=r+1, 因此允许答案位 0.
            while l<len(s):
                ans = min(ans, r-l+1)
                cnt[ch2idx[s[l]]] += 1
                l += 1
                if not check(): break
        return ans

    """ 1235. 规划兼职工作 #hard #题型 有一组 (s,e, profit), 要求选择不交叉的一组, 使得profit最大. 限制: n 1e5 时间范围 1e9
思路1: 序列 #DP  #二分
    对于end排序, 记 `f(i)` 为前i个兼职的最大收益, 则对于第i个事件 (s,e,p), 有 `f(i) = max(f(i-1), f(idx(s))+p)`, 这里的idx函数要找比s更小结束时间. 
见 [官答](https://leetcode.cn/problems/maximum-profit-in-job-scheduling/solution/gui-hua-jian-zhi-gong-zuo-by-leetcode-so-gu0e/)
"""
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(startTime,endTime,profit), key=lambda x:x[1])
        ends = [i[1] for i in jobs]
        n = len(startTime)
        f = [0]*(n+1)
        for i,(s,e,p) in enumerate(jobs):
            # 找到最后一个结束时间小于s的
            idx = bisect.bisect_right(ends, s, 0, i+1)
            f[i+1] = max(f[i], f[idx]+p)
        return f[-1]
    
sol = Solution()
result = [
    # sol.removeSubfolders(folder = ["/a","/a/b","/c/d","/c/d/e","/c/f"]),
    # sol.removeSubfolders(folder = ["/a/b/c","/a/b/ca","/a/b/d"]),
    # sol.balancedString(s = "QWER"),
    # sol.balancedString("WWEQERQWQWWRWWERQWEQ"),
    sol.jobScheduling(startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]),
    sol.jobScheduling(startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]),
]
for r in result:
    print(r)
