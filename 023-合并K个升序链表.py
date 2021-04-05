
"""
给你一个链表数组，每个链表都已经按升序排列。
请你将所有链表合并到一个升序链表中，返回合并后的链表。

输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
  1->4->5,
  1->3->4,
  2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6

输入：lists = []
输出：[]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/merge-k-sorted-lists
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
    # def mergeKLists(self, lists: List[ListNode]) -> ListNode:
    """
    思路一：「分治」思想，将 k 个链表合并的问题递归转化为两链表合并问题
    """
    def mergeKLists(self, lists):

        # 两个链表合并函数
        def merge2(l1, l2):
            head_pre = ListNode()   # 虚头部
            now = head_pre
            while l1 and l2:
                if l1.val < l2.val:
                    now.next = l1
                    l1 = l1.next
                else:
                    now.next = l2
                    l2 = l2.next
                now = now.next
            l = l1 if l1 else l2
            now.next = l
            return head_pre.next

        def mergeKgen(lists):
            if len(lists)==0:
                return None
            if len(lists)==1:
                return lists[0]
            k = len(lists)//2
            return merge2(mergeKgen(lists[:k]), mergeKgen(lists[k:]))

        return mergeKgen(lists)

    """
    思路二：维护一个 PriorityQueue
    """
    def mergeKLists2(self, lists):

        from heapq import heappush, heappop

        head_pre = ListNode()
        now = head_pre
        pq = []
        for i, l in enumerate(lists):
            if l:   # 可能有输入 [[]]
                heappush(pq, (l.val, i))        # 注意不能把 l 直接人进去，因为无法比较大小
        while pq:
            _, index = heappop(pq)
            l = lists[index]
            now.next = l
            now = now.next
            if l.next:
                lists[index] = l.next
                heappush(pq, (l.next.val, index))
        return head_pre.next




# ls = []
ls =  [[1,4,5],[1,3,4],[2,6]]
lists = [genNode(l) for l in ls]
res = Solution().mergeKLists2(lists)
res.printList()