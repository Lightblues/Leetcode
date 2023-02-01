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
https://www.bilibili.com/video/BV1sd4y1x7KN/

0206. 反转链表 https://leetcode.cn/problems/reverse-linked-list/solutions/1992225/you-xie-cuo-liao-yi-ge-shi-pin-jiang-tou-o5zy/
0092. 反转链表 II https://leetcode.cn/problems/reverse-linked-list-ii/solutions/1992226/you-xie-cuo-liao-yi-ge-shi-pin-jiang-tou-teqq/
0025. K 个一组翻转链表 https://leetcode.cn/problems/reverse-nodes-in-k-group/solutions/1992228/you-xie-cuo-liao-yi-ge-shi-pin-jiang-tou-plfs/
课后作业：
0024. 两两交换链表中的节点 https://leetcode.cn/problems/swap-nodes-in-pairs/
Easonsi @2023 """

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    """ 0206. 反转链表 #easy #题型 给定一个链表, 将其反转.
思路1: 迭代. 经典实现. 维护 pre,cur,next 三个指针会比较清晰.
思路2: 递归 实现
[官答](https://leetcode.cn/problems/reverse-linked-list/solution/fan-zhuan-lian-biao-by-leetcode-solution-d1k2/)
"""
    def reverseList(self, head: ListNode) -> ListNode:
        # 思路1: 迭代.
        pre, cur = None, head
        while cur:
            next = cur.next
            cur.next = pre
            pre, cur = cur, next
        return pre
    def reverseList(self, head: ListNode) -> ListNode:
        # 思路2: 递归 实现
        if not head or not head.next: return head
        newHead = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return newHead

    
    """ 0092. 反转链表 II #medium 给定 left,right, 反转这一部分 """
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        dummy = ListNode()  # 哨兵节点
        dummy.next = head
        # p0 记录 left的上一个节点
        p0 = dummy
        for _ in range(left-1): p0 = p0.next
        # 反转 l,r 之间的边, 再多反转一次 (其实是让 pre,cur 记录边界的位置)
        pre,cur = None,p0.next
        for _ in range(right-left+1):
            next = cur.next
            cur.next = pre
            pre,cur = cur,next
        p0.next.next = cur
        p0.next = pre
        return dummy.next
    
    
    """ 0025. K 个一组翻转链表 #hard #链表 #题型 K个一组翻转链表, 最后剩余的不动
思路1: 先遍历得到链表长度, 然后执行 n//k 次「0092. 反转链表 II」中的反转. 
[灵神](https://leetcode.cn/problems/reverse-nodes-in-k-group/solution/you-xie-cuo-liao-yi-ge-shi-pin-jiang-tou-plfs/)
"""
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        # cnt
        n = 0
        cur = head
        while cur: n = n+1; cur = cur.next
        # 
        dummy = ListNode(next=head)
        p0 = dummy  # 记录上一个位置
        for _ in range(n//k):
            # 下面同 0092. 反转链表 II
            pre,cur = None,p0.next      # 实际上这一行写在for的外面也可以!!
            for _ in range(k):
                nxt = cur.next
                cur.next = pre
                pre,cur = cur,nxt
            tail = p0.next  # 记录当前一组K的头 (翻转后变为尾)
            p0.next.next = cur
            p0.next = pre
            p0 = tail   # 更新 p0
        return dummy.next
    
    """ 0024. 两两交换链表中的节点 #medium 两辆交换, 最后若有剩下的元素不管
思路1: 就是 0025 的 k=2 版本
思路2: 模拟反转, 因为长度为2比较好处理
"""
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return self.reverseKGroup(head,2)
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(next=head)
        p0 = dummy
        while p0:
            if not p0.next or not p0.next.next: break
            first,second = p0.next, p0.next.next
            nxt = second.next
            p0.next = second
            second.next = first
            first.next = nxt
            p0 = first
        return dummy.next
        
sol = Solution()
result = [
    
]
for r in result:
    print(r)
