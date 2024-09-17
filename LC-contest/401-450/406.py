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
https://leetcode.cn/contest/weekly-contest-406
https://leetcode.cn/circle/discuss/xM3yVh/
手速场
T4 的切割问题很有意思~ 

Easonsi @2023 """
class Solution:
    """ 3216. 交换后字典序最小的字符串 """
    # def getSmallestString(self, s: str) -> str:
    #     # 看错题目了, 只能交换一次
    #     arr = [int(i) for i in s]
    #     l = 0
    #     arr.append((arr[-1]+1) % 10)
    #     for i,x in enumerate(arr):
    #         if (arr[l]%2) != x%2:
    #             arr[l:i] = sorted(arr[l:i])
    #             l = i
    #     arr.pop()
    #     return "".join(map(str, arr))
    def getSmallestString(self, s: str) -> str:
        for i in range(0, len(s)-1):
            l,r = int(s[i]),int(s[i+1])
            if l%2==r%2 and l>r:
                s = s[:i] + s[i:i+2][::-1] + s[i+2:]
                break
        return s
    
    """ 3217. 从链表中移除在数组中存在的节点 """
    def modifiedList(self, nums: List[int], head: Optional[ListNode]) -> Optional[ListNode]:
        p = dummy = ListNode()
        s = set(nums)
        while head:
            if head.val not in s:
                p.next = ListNode(head.val)
                p = p.next
            head = head.next
        return dummy.next
    
    """ 3218. 切蛋糕的最小总开销 I """
    
    """ 3219. 切蛋糕的最小总开销 II #hard 有一个 (m,n) 的蛋糕需要切成 m*n 块, 每个水平/竖直线切割有代价, 求最小代价. 
限制: m,n 1e5
思路1: #贪心 + #排序
    注意到, 一定会切 m*n-1 次!
    有贪心的想法: 每次切代价最大的那条线! 
    下面做一个简单的推导, 证明横竖的次序无所谓! 假设已经横向和纵向切割的次数为 h,v, 并且对于当前的最大代价x, 需要横向和纵向切割的次数分别为 ch,cv, 
        若先横向切割, 代价为 ch*(v+1) + cv*(v+ch+1)
        若先纵向切割, 代价为 cv*(h+1) + ch*(h+cv+1)
        两者都 = ch*(v+1) + cv*(h+1) + ch*cv
更本质的证明是, 对于任意一组横/纵的切割, 应该先切代价更高的那一个! 见 [ling](https://leetcode.cn/problems/minimum-cost-for-cutting-cake-ii/solutions/2843063/tan-xin-ji-qi-zheng-ming-jiao-huan-lun-z-ivtn/)
    """
    def minimumCost(self, m: int, n: int, horizontalCut: List[int], verticalCut: List[int]) -> int:
        cntH = Counter(horizontalCut)
        cntV = Counter(verticalCut)
        vals = set(cntH) | set(cntV)
        h,v = 0,0
        ans = 0
        for x in sorted(vals, reverse=True):
            ch, cv = cntH.get(x,0), cntV.get(x,0)
            cc = ch*(v+1) + cv*(h+1) + ch*cv
            ans += cc * x
            h += ch
            v += cv
        return ans
    
sol = Solution()
result = [
    # sol.getSmallestString(s = "45320"),
    sol.minimumCost(m = 3, n = 2, horizontalCut = [1,3], verticalCut = [5]),
    sol.minimumCost(m = 2, n = 2, horizontalCut = [7], verticalCut = [4]),
]
for r in result:
    print(r)
