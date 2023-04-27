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

# set maximization recursion limit
import sys
sys.setrecursionlimit(1000000)

""" 
https://leetcode.cn/contest/weekly-contest-339

T1和T3 分别因为边界WA了一次. T4有些难, 用到「平衡树/有序列表」来记录剩余的候选位置, 非常巧妙!
Easonsi @2023 """
class Solution:
    """ 6362. 最长平衡子字符串 """
    def findTheLongestBalancedSubstring(self, s: str) -> int:
        cnt0,cnt1 = 0,0 
        mx = 0
        pre = None
        for ch in s:
            if ch=='0': 
                if pre!='0': cnt0 = 1
                else: cnt0 += 1
                cnt1 = 0
            else:
                cnt1 += 1
                mx = max(mx, min(cnt0,cnt1))
            pre = ch
        return mx*2

    """ 6363. 转换二维数组 """
    def findMatrix(self, nums: List[int]) -> List[List[int]]:
        cnt = Counter(nums)
        ans = []
        while cnt:
            tmp = []
            for k in list(cnt.keys()):
                tmp.append(k)
                cnt[k] -= 1
                if cnt[k]==0:
                    del cnt[k]
            ans.append(tmp)
        return ans


    """ 6364. 老鼠和奶酪 """
    def miceAndCheese(self, reward1: List[int], reward2: List[int], k: int) -> int:
        diff = [r1-r2 for r1,r2 in zip(reward1, reward2)]
        return sum(reward2) + sum(sorted(diff, reverse=True)[:k])


    """ 6365. 最少翻转操作数 #hard #题型 全0数组某一位是1, 每次可以翻转一个长度为k的子数组, 但是不能把1放到ban的位置, 问到达所有位置的最少翻转次数. 
限制: n,k 1e5
k = 4
[1,x,x,0] -> [0,-1,-1,1]
k = 3
[1,0,x,0,x,0] -> [0,-1,-1,-1,-1]
观察: 对于位置i, 其可以移动到的位置受到大小为k的窗口的限制
    假设窗口k的 [l, l+k-1], 则对于在窗口内的元素 i, 有关系 i'+i = 2l+k-1
    窗口的范围: [i-k+1, i], 还要考虑左端点范围 [max(0, i-k+1), min(i,n-k)]
思路0: 从每个候选idx出发, 尝试移动到合法的位置上, 但是 #TLE
    时间复杂度: O(nk)
思路1: 用平衡树来记录候选位置! 
    针对思路0, 如何降低没必要的检查? 我们需要将待检查的元素记录下来/剔除掉
    可以用 #平衡树 (有序列表) 来实现! 
    重新理解上面的「观察」: 对于位置i, 其一次可以到达的范围是 [max(i-k+1,k-1-i), min(i+k-1, 2n-k-1-i)] 步长为2
    因此, 可以分奇偶! 对于剩余的位置进行记录!
[灵神](https://leetcode.cn/problems/minimum-reverse-operations/solution/liang-chong-zuo-fa-ping-heng-shu-bing-ch-vr0z/)
    """
    def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        # TLE
        banned = set(banned)
        ans = [-1] * n
        h = [(0,p)]
        ans[p] = 0
        while h:
            step, i = heappop(h)
            # 直接在下面 if判断更高效
            # if ans[i]!=-1: continue
            # ans[i] = step
            l,r = max(0, i-k+1), min(i,n-k)
            for ll in range(l,r+1):
                ii = 2*ll+k-1-i
                # if ii not in banned: heappush(h, (step+1, ii))
                if (ii not in banned) and (ans[ii]==-1): 
                    ans[ii] = step+1
                    heappush(h, (step+1, ii))
        return ans
    def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        from sortedcontainers import SortedList
        remains = [SortedList(), SortedList()]
        banned = set(banned)
        for i in range(n):
            if i==p: continue
            if i not in banned: remains[i%2].add(i)
        remains[0].add(n); remains[1].add(n)        # 哨兵
        q = deque([(0,p)])
        ans = [-1] * n
        ans[p] = 0
        while q:
            step,i = q.popleft()
            ll = max(i-k+1, k-1-i)
            rr = min(i+k-1, 2*n-k-1-i)
            s = remains[ll%2]
            idx = s.bisect_left(ll)
            while s[idx] <= rr:
                ii = s[idx]
                s.remove(ii)
                ans[ii] = step+1
                q.append((step+1, ii))
        return ans


    
sol = Solution()
result = [
    # sol.findTheLongestBalancedSubstring(s = "01000111"),
    # sol.findTheLongestBalancedSubstring("0011"),
    # sol.findTheLongestBalancedSubstring("11"),
    # sol.findTheLongestBalancedSubstring("01011"),
    # sol.findMatrix(nums = [1,3,4,1,2,3,1]),
    # sol.findMatrix([1,2,3,4]),
    # sol.miceAndCheese(reward1 = [1,1,3,4], reward2 = [4,4,1,1], k = 2),
    # sol.miceAndCheese(reward1 = [1,1], reward2 = [1,1], k = 2),
    # sol.miceAndCheese([4], [5],0),
    # sol.minReverseOperations(n = 4, p = 0, banned = [1,2], k = 4),
    # sol.minReverseOperations(n = 5, p = 0, banned = [2,4], k = 3),
    # sol.minReverseOperations(n = 4, p = 2, banned = [0,1,3], k = 1),
    # sol.minReverseOperations(6,0,[],4),
    sol.sample()
]
for r in result:
    print(r)
