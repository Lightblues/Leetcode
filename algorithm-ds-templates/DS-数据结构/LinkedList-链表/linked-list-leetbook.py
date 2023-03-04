from easonsi import utils
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

""" @202208
[链表](https://leetcode.cn/leetbook/detail/linked-list/)
技巧: 双指针.
    另外, 对于链表, 加上dummy的技巧也比较常见.
注意; next的时候需要判断是否为None.

= 实现
0707. 设计链表 #medium

= 双指针技巧
0876. 链表的中间结点 #easy 若长度为偶数, 则返回靠右的那个
0141. 环形链表 #easy #题型 判断链表是否有环
    思路1: #快慢指针
0142. 环形链表 II #题型 #medium
    相较于 0141, 需要返回进入环的第一个节点.
    **让slow继续从相遇点走, 同时在起点放置一个速度也为1的指针, 他们恰好会在入环点相遇**.
0019. 删除链表的倒数第 N 个结点 #medium #题型
    思路1: 让第一个指针先走n步. 然后两个指针一起走.
0160. 相交链表 #easy #题型
    给定两个节点, 判断他们是否会相交 (Y字型), 若相交返回相交的那个节点. 保证了无环. 进阶限制: 时间 O(m+n), 空间 O(1)


= 经典问题
0206. 反转链表 #easy #题型
    给定一个链表, 将其反转.
0203. 移除链表元素 #easy 移除所有特定值的节点.
0328. 奇偶链表 #medium #题型
    对于一个链表, 按照奇偶进行分组, 返回 奇+偶 拼起来的结果链表. 限制: 只能使用 O(1) 的额外空间.
0234. 回文链表 #easy #题型 给定一个链表, 判断是否回文. 进阶要求: 空间 O(1)
    思路1: 变为双向链表. 然后从两端开始比较
    思路2: 采用 #快慢指针找中间节点. 然后 #反转 后半部分. 比较. 最后还原链表. (真的烦琐?)

= 小结
0021. 合并两个有序链表 #easy
0023. 合并K个升序链表 #hard 就是基本的堆的使用
0002. 两数相加 #medium
    两个整数以逆序链表的形式存储, 求和.
0430. 扁平化多级双向链表 #medium
    题目设置比较复杂, 总体上类似 DFS. 设计到较多的 #细节.
0138. 复制带随机指针的链表 #medium #题型
    对于一个带有另外指针的链表, 实现深拷贝
    提示: 正如题目中用数组来表示「随机链表」一样, 我们可以为每个节点定一个idx, 从而描述他们的指向关系.
0061. 旋转链表 #medium 给定一个链表, shift(k)
    提示: 对于长 l 的链表, 循环右移 k 位, 则新的head是什么? 倒数第 k 个节点.
 """
class ListNode:
    def __init__(self, x) -> None:
        self.val = x
        self.next = None
class Node:
    # 0430
    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child
class Node:
    # 0138. 复制带随机指针的链表
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
class Solution:
    """ ============================================ 双指针技巧 ============================================ """
    """ 0141. 环形链表 [z-快慢指针] """
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next: return False
        # 快慢指针. 注意下面 while 的条件: 初始时设置 fast = slow.next
        slow, fast = head, head.next
        while slow != fast:
            if not fast or not fast.next: return False
            slow, fast = slow.next, fast.next.next
        return True
    """ 0142. 环形链表 II #题型 #medium [z-快慢指针] """
    def detectCycle(self, head: ListNode) -> ListNode:
        # 思路1: #快慢指针
        if not head: return None
        slow, fast = head, head
        while fast:
            slow = slow.next
            if not fast.next: return None
            fast = fast.next.next
            # 相遇
            if slow == fast:
                p = head
                while p!= slow:
                    p, slow = p.next, slow.next
                return p
        return None

    """ 0019. 删除链表的倒数第 N 个结点 #medium #题型 [z-前后] """



    """ 0160. 相交链表 #easy #题型
给定两个节点, 判断他们是否会相交 (Y字型), 若相交返回相交的那个节点. 保证了无环. 进阶限制: 时间 O(m+n), 空间 O(1)
思路1: 假设AB点到达终点的时间分别为 m,n. 若该节点相同则会相交.
    取差值, 让更长路径上的节点先走 m-n 步.
思路2: 官答给了一个更骚的操作: AB同时走, 若A为空则在B上继续走, B也是同理; 知道两指针同时为空或者相遇.
    这里的核心在于: 它们最多走 m+n 必然会同时为空.
    [官答](https://leetcode.cn/problems/intersection-of-two-linked-lists/solution/xiang-jiao-lian-biao-by-leetcode-solutio-a8jn/)
 """
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        m = n = 0
        p = headA
        while p.next:
            p = p.next; m += 1
        q = headB
        while q.next:
            q = q.next; n += 1
        if p!=q: return None
        # 会相交
        if n>m:
            m,n = n,m
            headA,headB = headB,headA
        for _ in range(m-n): headA = headA.next
        while headA!=headB:
            headA,headB = headA.next,headB.next
        return headA






    """ ============================================ 经典 ============================================ """
    """ 0206. 反转链表 #easy #题型
给定一个链表, 将其反转.
思路1: 迭代. 经典实现. 维护 pre,cur,next 三个指针会比较清晰.
思路2: 递归 实现
"""

    """ 0203. 移除链表元素 #easy 移除所有特定值的节点. """

    """ 0328. 奇偶链表 #medium #题型
对于一个链表, 按照奇偶进行分组, 返回 奇+偶 拼起来的结果链表. 限制: 只能使用 O(1) 的额外空间.
注意避免出现环.
 """
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        h1 = t1 = ListNode(0)
        h2 = t2 = ListNode(0)
        flag = True
        while head:
            if flag: t1.next = head; t1 = head
            else: t2.next = head; t2 = head
            flag = not flag; head = head.next
        t1.next = h2.next
        # 注意避免出现环.
        t2.next = None
        return h1.next

    """ 0234. 回文链表 #easy #题型 给定一个链表, 判断是否回文. 进阶要求: 空间 O(1)
思路1: 变为双向链表. 然后从两端开始比较
思路2: 采用 #快慢指针找中间节点. 然后 #反转 后半部分. 比较. 最后还原链表. (烦琐?)
    反转部分关联「0206. 反转链表」
    [官答](https://leetcode.cn/problems/palindrome-linked-list/solution/hui-wen-lian-biao-by-leetcode-solution/)
性能分析: 思路2看上去更繁琐, 但测试中的运行时间更短? 因为思路1需要对每个节点添加额外的属性?
 """
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        # 思路1: 变为双向链表
        pre,cur = None,head
        while cur:
            next = cur.next
            cur.pre = pre
            pre,cur = cur,next
        p,q = head,pre
        # 注意这里的判断条件: 若为偶数, 要p越过q之后才结束.
        while p!=q and p.pre!=q:
            if q.val!=p.val: return False
            p,q = p.next,q.pre
        return True
    
    def isPalindrome(self, head: ListNode) -> bool:
        # 思路2: 采用 #快慢指针找中间节点. 然后 #反转 后半部分. 比较. 最后还原链表.
        if head is None:
            return True
        # 找到前半部分链表的尾节点并反转后半部分链表
        first_half_end = self.end_of_first_half(head)
        second_half_start = self.reverse_list(first_half_end.next)
        # 判断是否回文
        result = True
        first_position = head
        second_position = second_half_start
        while result and second_position is not None:
            if first_position.val != second_position.val:
                result = False
            first_position = first_position.next
            second_position = second_position.next
        # 还原链表并返回结果
        first_half_end.next = self.reverse_list(second_half_start)
        return result    
    def end_of_first_half(self, head):
        # 快慢指针找中间节点. 对于奇数长度链表, 前半部分较长.
        fast = head
        slow = head
        while fast.next is not None and fast.next.next is not None:
            fast = fast.next.next
            slow = slow.next
        return slow
    def reverse_list(self, head):
        previous = None
        current = head
        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        return previous



    """ ============================================ 小结 ============================================ """

    """ 0021. 合并两个有序链表 #easy
总体思路肯定是一样的. 注意下面循环条件 `while list1 and list2` 和 `while list1 or list2` 的区别.
 """
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        ans = p = ListNode(0)
        while list1 or list2:
            if list1 and list2:
                if list1.val < list2.val:
                    p.next = list1
                    list1 = list1.next
                else:
                    p.next = list2
                    list2 = list2.next
            elif list1:
                p.next = list1
                break
            else:
                p.next = list2
                break
            p = p.next
        return ans.next
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # 用 while list1 and list2 判断可以简化代码
        ans = p = ListNode(0)
        while list1 and list2:
            if list1.val < list2.val:
                p.next = list1
                list1 = list1.next
            else:
                p.next = list2
                list2 = list2.next
            p = p.next
        p.next = list1 or list2
        return ans.next


    """ 0002. 两数相加 #medium
两个整数以逆序链表的形式存储, 求和.
 """
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        ans = p = ListNode(0)
        carry = 0
        while l1 or l2 or carry:
            if l1:
                carry += l1.val
                l1 = l1.next
            if l2:
                carry += l2.val
                l2 = l2.next
            p.next = ListNode(carry%10)
            p = p.next
            carry //= 10
        return ans.next 

    """ 0430. 扁平化多级双向链表 #medium
题目设置比较复杂, 总体上类似 DFS. 设计到较多的 #细节.
参见 [官答](https://leetcode.cn/problems/flatten-a-multilevel-doubly-linked-list/solution/bian-ping-hua-duo-ji-shuang-xiang-lian-b-383h/)
 """
    def flatten(self, head: 'Node') -> 'Node':
        if not head: return None        # 边界.
        ans = p = Node(0,None,None,None)
        def dfs(nd: Node, pre: Node):
            # 修正 pre->nd 的指向关系; 
            # 返回当前链路的最后一个节点 (非空)
            if not nd: return
            # record
            nxt = nd.next
            # 修正 pre->nd 的指向关系
            nd.prev = pre; pre.next = nd
            if nd.child:
                nn = dfs(nd.child, nd)
                nd.child = None
                nd = nn
            if nxt:
                nd = dfs(nxt, nd)
            return nd
        dfs(head, p)
        # 去除 dummy 节点
        ans = ans.next; ans.prev = None
        return ans


    """ 0138. 复制带随机指针的链表 #medium #题型
对于一个带有另外指针的链表, 实现深拷贝
提示: 正如题目中用数组来表示「随机链表」一样, 我们可以为每个节点定一个idx, 从而描述他们的指向关系.
思路1: 分为 「记录」和「重构」 随机链表 两步.
    记录过程中, 用 #哈希表 记录 node2idx 的映射.
    重构过程中, 用 idx2node 的映射.
另见 [官答](https://leetcode.cn/problems/copy-list-with-random-pointer/solution/fu-zhi-dai-sui-ji-zhi-zhen-de-lian-biao-rblsf/) 思路不太一样.
 """
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        # node: val, next, random
        origin_p2idx = {}
        rdm = []
        vals = []
        p = head; idx = 0
        while p:
            origin_p2idx[p] = idx
            rdm.append(p.random)
            # rdm.append(origin_p2idx[p.random] if p.random else -1)
            vals.append(p.val)
            p = p.next; idx += 1
        rdm = [origin_p2idx[p] if p else -1 for p in rdm]
        # 构建新链表
        ans = p = Node(0,None,None)
        new_idx2p = {}
        for i in range(idx):
            nxt = Node(vals[i],None,None)
            new_idx2p[i] = nxt
            p.next = nxt; p = nxt
        # 构建新的 random 指针
        for i, r in enumerate(rdm):
            new_idx2p[i].random = new_idx2p[r] if r != -1 else None
        return ans.next


    """ 0061. 旋转链表 #medium 给定一个链表, shift(k)
提示: 对于长 l 的链表, 循环右移 k 位, 则新的head是什么? 倒数第 k 个节点.
    考虑链表的单向性, 通过正向找第 l-k 个节点就是新的head.
思路1: 先得到链表长度, 从而找到新的head, 然后修复链表. #细节较多.
    注意这里的k可能很大, 显然要 #取模.
 """
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head: return head

        tail = head; ll = 1
        while tail.next:
            ll += 1
            tail = tail.next
        # 注意这里得到的范围, 外面重新取模之后范围 [0,ll)
        # 否则, ll -  (k % ll) 的范围为 (0,ll], 下面的if判断就要改为 shift==ll
        shift = (ll -  (k % ll)) % ll
        if shift==0: return head        # 边界.
        newH = head
        for i in range(shift-1):
            newH = newH.next
        # 上面的检查保证了 newT,newH 都非空
        newT,newH = newH.next,head
        newT.next = None
        tail.next = head
        return newH


    """ 0023. 合并K个升序链表 #hard 就是基本的堆的使用 """
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        ans = p = ListNode(0)
        # h = [(nd.val, nd) for nd in lists if nd]
        h = [(nd.val, i) for i,nd in enumerate(lists) if nd]
        # 注意, 不能直接放node进行, 因为在val相同的情况下无法比较!
        heapq.heapify(h)
        while h:
            _, i = heappop(h)
            node = lists[i]
            p.next = node; p = p.next
            if node.next:
                heappush(h, (node.next.val, i))
                # 
                lists[i] = node.next
        return ans.next





    
""" 0707. 设计链表 #medium
实现一个链表 (可以是 单向/双向). 实现接口: get(index), addAtHead(val), addAtTail(), addAtIndex(index, val), deleteAtIndex(index)
思路1: 采用 #单链表
    注意 哨兵 sentinel; 和链表大小的维护
    复杂度: head 操作 O(1); tail O(n); 其他获取 index 的操作 O(k)
思路2: #双链表
    注意, 根据index距离头尾的远近选择更快的方向.
    实现起来比单链表复杂, 性能上要好一些.
    复杂度: head, tail 操作 O(1); 其他获取 index 的操作 O(min{k, n-k})
[official](https://leetcode.cn/problems/design-linked-list/solution/she-ji-lian-biao-by-leetcode/)
 """
class ListNode:
    def __init__(self, x) -> None:
        self.val = x
        self.next = None
class MyLinkedList:
    # 思路1: 单链表
    def __init__(self):
        self.size = 0
        self.head = ListNode(0)     # sentinel node as pseudo-head

    def get(self, index: int) -> int:
        # Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        if index<0 or index>=self.size:
            return -1
        curr = self.head
        for _ in range(index+1):        # sentinel
            curr = curr.next
        return curr.val

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        # Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        if index<0 or index>self.size:  return
        pred = self.head
        for _ in range(index): pred = pred.next
        to_add = ListNode(val)
        to_add.next = pred.next
        pred.next = to_add
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        # Delete the index-th node in the linked list, if the index is valid.
        if index<0 or index>=self.size: return
        pred = self.head
        for _ in range(index): pred = pred.next
        pred.next = pred.next.next
        self.size -= 1

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next, self.prev = None, None
class MyLinkedList:
    # 思路2: 双链表
    def __init__(self):
        self.size = 0
        # sentinel nodes as pseudo-head and pseudo-tail
        self.head, self.tail = ListNode(0), ListNode(0) 
        self.head.next = self.tail  # 初始化为空
        self.tail.prev = self.head
        

    def get(self, index: int) -> int:
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        """
        # if index is invalid
        if index < 0 or index >= self.size:
            return -1
        
        # choose the fastest way: to move from the head
        # or to move from the tail
        if index + 1 < self.size - index:
            curr = self.head
            for _ in range(index + 1):
                curr = curr.next
        else:
            curr = self.tail
            for _ in range(self.size - index):
                curr = curr.prev
                
        return curr.val
            

    def addAtHead(self, val: int) -> None:
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        """
        pred, succ = self.head, self.head.next
        
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """
        succ, pred = self.tail, self.tail.prev
        
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        

    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        """
        if index > self.size or index < 0:
            return
        
        # find predecessor and successor of the node to be added
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next
        else:
            succ = self.tail
            for _ in range(self.size - index):
                succ = succ.prev
            pred = succ.prev
        
        # insertion itself
        self.size += 1
        to_add = ListNode(val)
        to_add.prev = pred
        to_add.next = succ
        pred.next = to_add
        succ.prev = to_add
        

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """
        # if the index is invalid, do nothing
        if index < 0 or index >= self.size:
            return
        
        # find predecessor and successor of the node to be deleted
        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next.next
        else:
            succ = self.tail
            for _ in range(self.size - index - 1):
                succ = succ.prev
            pred = succ.prev.prev
            
        # delete pred.next 
        self.size -= 1
        pred.next = succ
        succ.prev = pred


sol = Solution()
result = [
    
]
for r in result:
    print(r)
