"""
输入: 1->2->3->4->5->NULL
输出: 5->4->3->2->1->NULL
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
    root_pre = ListNode()
    curr = root_pre
    for num in l:
        now = ListNode(val=num)
        curr.next = now
        curr = now
    return root_pre.next

class Solution:
    """
    思路一：迭代
    维护两个指针，pre 记录前一个节点，curr 记录当前节点；然后递归 curr 指针，直至 curr 指向 None；最后返回 pre 即可
    """
    def reverseList(self, head: ListNode) -> ListNode:
        pre = None
        curr = head
        while curr:

            next = curr.next
            curr.next = pre
            pre = curr
            curr = next
        return pre
    """
    思路二：递归
    思路稍微绕一点：假设递归函数为 `recursion(node)->head`，那么我们在其中要实现什么？
    首先在每一次递归过程中（对于第 k 个节点），我们对 curr.next 调用 recursion，其返回的 newhead 应该作为此次递归的返回（新的头部）
    我们利用 newhead 对于 curr 的指向进行翻转
    """
    def reverse_recursion(self, head: ListNode):
        def recursion(curr: ListNode)->ListNode:
            if not curr or (not curr.next):
                # 条件 1：curr.next 为空，链表到达尾端
                # 条件 2：curr 为空，调用 recursion 时传入的 head 本身为空
                return curr
            new_head = recursion(curr.next)     # 接受递归调用返回的新 head
            curr.next.next = curr   # 注意 curr 的 next 指针并未变化，利用其修改 curr.next 的 next 指针
            curr.next = None    # 这里需要将其置空，以免出现环
            return new_head
        return recursion(head)
l = [1,2,3,4,5]
# l = []
head = genNode(l)
# res = Solution().reverseList(head)
res = Solution().reverse_recursion(head)
if res:
    res.printList()
else:
    print()

