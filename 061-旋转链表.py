"""
给定一个链表，旋转链表，将链表每个节点向右移动 k 个位置，其中 k 是非负数。

输入: 0->1->2->NULL, k = 4
输出: 2->0->1->NULL
解释:
向右旋转 1 步: 2->0->1->NULL
向右旋转 2 步: 1->2->0->NULL
向右旋转 3 步: 0->1->2->NULL
向右旋转 4 步: 2->0->1->NULL

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/rotate-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
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
    def rotateRight(self, head: ListNode, k: int) -> ListNode:
        if not head:
            # head 还可能是 []？
            return None
        if k==0:
            return head
        p = head
        # 快指针先向前 k 步
        length = -1
        for i in range(k):
            p = p.next
            if p is None:
                # nonlocal length
                length = i+1
                break
        if length != -1:
            # 说明链表的长度小于 k
            k = k%length
            return self.rotateRight(head, k)
        else:
            q = head
            # tail = p
            while p.next:
                # tail = p
                p = p.next
                q = q.next
            p.next = head
            newhead = q.next
            q.next = None
            return newhead
head = genNode([1,2,3,4,5])
res = Solution().rotateRight(head, 5)
res.printList()
