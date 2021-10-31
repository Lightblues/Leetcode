
"""
输入: 1->1->2->3->3
输出: 1->2->3
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
        pre = None
        while head:
            if head.val != pre:
                p.next = head
                p = p.next
                pre = head.val
            head = head.next
        p.next = None
        return res.next

l = genNode([1,1,2,3,3,])
res = Solution().deleteDuplicates(l)
res.printList()
