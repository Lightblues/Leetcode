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
https://leetcode.cn/contest/weekly-contest-321
题解: https://leetcode.cn/circle/discuss/D1fgh9/
手速场. T3 考了少见的链表; T4因为思路不清楚WA了一次

@2022 """

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    """ 6245. 找出中枢整数 计算前缀和, 遍历即可
O(1) 做法: https://leetcode.cn/problems/find-the-pivot-integer/solution/o1-zuo-fa-by-endlesscheng-571j/
"""
    def pivotInteger(self, n: int) -> int:
        acc = list(accumulate(range(n+1)))
        for i in range(1,n+1):
            if acc[i] == acc[-1]-acc[i-1]: return i
        return-1
    
    """ 6246. 追加字符以获得子序列 #medium 等价于, 求s中t的最长前缀子序列 #贪心 匹配 """
    def appendCharacters(self, s: str, t: str) -> int:
        n,m = len(s),len(t)
        # 从s中查找t的最长前缀子序列
        i=j=0
        while True:
            if j==m or i==n: break
            if s[i]==t[j]: j+=1; i+=1
            else: i+=1
        return m-j
    
    """ 6247. 从链表中移除节点 #medium 移除节点, 保证链表非递增 #题型 #链表
思路0: 直接 #单调栈 更简单些. 或者用单调栈来保存节点也行
思路1: #递归 实现
思路2: #迭代
    如何非递归实现? 可以「两次反转链表」
见 [灵神](https://leetcode.cn/problems/remove-nodes-from-linked-list/solution/di-gui-jian-ji-xie-fa-by-endlesscheng-jfwi/)
"""
    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 单调栈 记录链表元素, 保证非递增
        # 或者用单调栈来保存节点也行. 
        h = []
        while head:
            val = head.val
            while h and h[-1]<val: h.pop()
            h.append(val)
            head = head.next
        # 根据元素重构需要返回的链表
        dummy = p = ListNode()
        for val in h:
            p.next = ListNode(val)
            p = p.next
        return dummy.next
    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 思路1: #递归 实现
        if not head or not head.next: return head
        
        # v1: 鹿儿优雅的代码! 
        head.next = self.removeNodes(head.next)
        return head if head.val>=head.next.val else head.next
        
        # v2: 笨笨的代码
        # 递归, 返回的 nxt 头是后续链表中的最大元素
        # 因为有了上面的判断, 这里返回的元素非空
        nxt = self.removeNodes(head.next)
        # 返回逻辑
        if head.val>=nxt.val: 
            head.next = nxt
            return head
        else: 
            return nxt
        
    """ 6248. 统计中位数为 K 的子数组 #hard 对于 1...n 的一个排列, 统计子数组中中位数为k的数量 (对于偶数情况, 定义中位数为靠左的那个元素). 限制 n 1e5
思路1: 先在数组中找到元素k的位置. 枚举左右: 分别记 diffR, diffL 为左右的, 比k大的元素数量比k小的元素数量, 则当 diffR==diffL (+1) 的时候, 中位数为k.
    因此, 可以用一个 Counter 来记录一边的diff出现情况, 匹配另一边, 复杂度 O(n)
    [灵神](https://leetcode.cn/problems/count-subarrays-with-median-k/solution/deng-jie-zhuan-huan-pythonjavacgo-by-end-5w11/) 的思路一致
"""
    def countSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        idx = nums.index(k)
        # 统计右侧差值
        cntRight = Counter()
        diffRight = 0
        for i in range(idx, n):
            # 注意遍历需要从 idx 开始, 在dix位置不更新diff
            if nums[i]>k: diffRight+=1
            elif nums[i]<k: diffRight-=1
            cntRight[diffRight]+=1
        ans = 0
        # 统计左侧差值, 进行匹配
        diffLeft = 0
        for i in range(idx, -1,-1):
            if nums[i]>k: diffLeft+=1
            elif nums[i]<k: diffLeft-=1
            ans += cntRight[-diffLeft] + cntRight[-diffLeft+1]
        return ans


def list2LinkedList(data):
    """ 根据 [5,2,13,3,8] 的列表构造链表 """
    if isinstance(data, str): data = eval(data)
    dummy = p = ListNode()
    for val in data:
        p.next = ListNode(val)
        p = p.next
    return dummy.next

def linkedList2List(head: ListNode):
    """ 根据链表构造列表 """
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

sol = Solution()
result = [
    # sol.pivotInteger(8),
    # sol.pivotInteger(1),
    # sol.pivotInteger(4),
    # sol.appendCharacters(s = "coaching", t = "coding"),
    # sol.appendCharacters(s = "abcde", t = "a"),
    # sol.appendCharacters(s = "z", t = "abcde"),
    # sol.countSubarrays(nums = [3,2,1,4,5], k = 4),
    # sol.countSubarrays(nums = [2,3,1], k = 3),
    # sol.countSubarrays([1,2,3], 2),
    # sol.countSubarrays([2,5,1,4,3,6], 1), 
    linkedList2List(
        sol.removeNodes(list2LinkedList([5,2,13,3,8]))
    )
    
]
for r in result:
    print(r)
