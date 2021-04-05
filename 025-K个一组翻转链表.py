"""
将一个链表每 k 个节点为一组进行翻转；k 小于等于链表长度；
若链表长度不能被 k 整除，剩余部分保持原有顺序

进阶：你可以设计一个只使用常数额外空间的算法来解决此问题吗？
你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。

输入：head = [1,2,3,4,5], k = 3
输出：[3,2,1,4,5]
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
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        if k==1:
            return head

        result_pre = ListNode()
        current = result_pre    # current 指向目前已经排好序的最后一个元素

        while head:
            head_of_k_nodes = head  # 先保留目前的位置，k 个 node 的头部
            # 判断剩余的是否还有 k 个 node
            count  = k-1
            # for count in range(k):
            while count>0 and head.next:
                head = head.next
                count -= 1
            # head = head.next        # 注意前面的 while 循环只走了 k-1 步，因此需要再往后一步

            # count>0 说明不满 k 个 node 了。因需要更新 current
            if count>0:
                current.next = head_of_k_nodes
                head = head.next  # 注意前面的 while 循环只走了 k-1 步，因此需要再往后一步
            else:
                """
                currend -> head_of_k_nodes(the head of k nodes) ->...-> head(the tail of k nodes)
                利用上面的三个指针，需要做：
                1. 对 pre-head 这一序列进行反转；
                2. 更新 current：先将原来的 current.next 指向排好序的 k 个元素的头部，然后将 current 指向逆序的 k 长序列的末尾 end_of_reversed
                # head 已经在前面更新过了，可能是下一个 k 组元素的头部，也可能为空
                3. 更新 head：目前指向 k 个元素的尾部（因为在迭代反转的时候需要判断是否到了 k 个）
                4. 更新 end_of_reversed=head_of_k_nodes：事实上就是更新后的 current 节点，将其 next 指针置空，或者指向 head.next
                """
                end_of_reversed = head_of_k_nodes
                head_of_next_k = head.next
                pre, curr = head_of_k_nodes, head_of_k_nodes.next
                while curr!=head:
                    next = curr.next
                    curr.next = pre
                    pre, curr = curr, next
                curr.next = pre     # 注意循环条件：curr 遍历到末尾（head）的时候，curr 的 next 需要指向 pre 但还未反向

                current.next = curr # curr==head, 现在 head 指向 k 个元素末尾
                current = end_of_reversed
                current.next = None
                # 注意到此时的 head 肯定不为 None，不需要判断
                # if head.next:
                #     head = head.next
                head = head_of_next_k

        return result_pre.next

    def reverse(self, head: ListNode, tail: ListNode):
        # 官方实现，可以应对 k=1 边界情况
        # prev = tail.next
        # p = head
        # while prev != tail:
        #     nex = p.next
        #     p.next = prev
        #     prev = p
        #     p = nex
        # return tail, head

        # 但还是觉得下面自己写的代码更清楚些，增加了（0）部分的判断
        pre, curr = head, head.next
        while curr!=tail:
            nex = curr.next
            curr.next = pre
            pre, curr = curr, nex
        curr.next = pre
        # 以上未改变原本的 head.next，因此是有环的。
        # 因此下一行避免出现环（在测试过程中有用） —— 但实际上在 reverseKGroup2() 中会对 head.next 进行处理
        head.next = None
        return tail, head

    def reverseKGroup2(self, traverse: ListNode, k: int):
        if k==1:    # （0）处理边界情况，若 reverse 用的是标答则不需要这一判断
            return traverse
        hair = ListNode()
        hair.next = traverse
        pre = hair  # （1）已排序的最后一个 node

        while traverse:
            tail = pre
            for i in range(k):
                tail = tail.next
                if not tail:
                    return hair.next

            nex = tail.next # （2）记录 k 个节点后的下一个 node
            head, tail = self.reverse(traverse, tail)
            """
            把子链表重新接回原链表
            将（1）所记录的之前部分的处理好的最后一个节点的 next 指针指向（新的反向的）子链表头
            将子链表为的 next 指针指向（2）所记录的 k 个节点后的第一个节点（可能为 None）
            """
            pre.next = head
            tail.next = nex

            pre = tail      # （1）重新记录

            traverse = nex  # 还需要更新 head
        return hair.next

head = genNode([1,2,3,4,5])
# res = Solution().reverseKGroup(head, k=1)
# res.printList()

# tail = head
# while tail.next:
#     tail = tail.next
# rev_head, _ = Solution().reverse(head, tail)
# rev_head.printList()

res2 = Solution().reverseKGroup2(head, k=1)
res2.printList()