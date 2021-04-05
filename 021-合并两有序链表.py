
"""
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
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
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        result_pre = ListNode() # 一个空指针
        now = result_pre
        while l1 or l2:
            # 链接 l1 指针的条件：首先 l1 非空，其次 1. l2 为空；2. 或者 l2.val>l1.val
            if l1 and (not l2 or (l2 and l1.val<l2.val)):
                now.next = l1
                now = l1
                l1 = l1.next
            else:
                now.next = l2
                now = l2
                l2 = l2.next
        now.next = None
        return result_pre.next

l1 = genNode([1,2,4])
l2 = genNode([1,3,4])
res = Solution().mergeTwoLists(l1, l2)
res.printList()

