"""
给定一个排序链表，删除所有含有重复数字的节点，只保留原始链表中 没有重复出现 的数字。

输入: 1->2->3->3->4->4->5
输出: 1->2->5

输入: 1->1->1->2->3
输出: 2->3
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
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        res = ListNode()
        p = res
        pre = head
        # 可能 head=[]，或者长度为 1
        if not head or not head.next:
            return head
        head = head.next
        repeated = False
        while head:
            if head.val == pre.val:
                repeated = True
            else:
                if not repeated:
                    p.next = pre
                    p = pre
                pre = head
                repeated = False
            head = head.next
        if not repeated:
            p.next = pre
            p = p.next
        p.next = None
        return res.next

l = genNode([1,1,1,2,3])
res = Solution().deleteDuplicates(l)
res.printList()
