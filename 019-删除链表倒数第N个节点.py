"""
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
"""


# Definition for singly-linked list.
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

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        right = head
        left = head
        for _ in range(n-1):
            right = right.next
        if not right.next:  # 说明被删除的是第一个节点
            return left.next
        right = right.next # 为删除倒数第 N 个节点，需要保留倒数 N-1 的节点
        while right.next:
            right = right.next
            left = left.next
        left.next = left.next.next
        return head

nums = [1,2,3,4,5]; n = 2
head = ListNode(nums[0])
now = head
for num in nums[1:]:
    next = ListNode(num)
    now.next = next
    now = next
res = Solution().removeNthFromEnd(head, n)
res.printList()
