"""
给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。
你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。

输入：head = [1,2,3,4]
输出：[2,1,4,3]

输入：head = [1]
输出：[1]
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def printList(self):
        res = [self.val]
        now = self
        while now.next:
            now = now.next
            res.append(now.val)
        print(res)

def genNode(l):
    root = ListNode(val=l[0])
    pre = root
    for num in l[1:]:
        now = ListNode(val=num)
        pre.next = now
        pre = now
    return root


class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        head_pre = ListNode()
        cur = head_pre
        while head:
            first = head
            head = head.next
            second = None
            if head:
                second = head
                head = head.next
            if not second:
                cur.next = first
                # cur = first
            else:
                cur.next = second
                second.next = first
                cur = first
                cur.next = None     # 注意需要避免循环指针
        return head_pre.next

head = genNode([1,2,3,4])
res = Solution().swapPairs(head)
res.printList()
