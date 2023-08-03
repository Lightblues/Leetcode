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

""" 
[🔥 LeetCode 热题 HOT 100](https://leetcode.cn/problem-list/2cktkvj/)
Easonsi @2023 """

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    
    """ 0394. 字符串解码 #medium #细节 对于 10[a2[bc]] 解析成 abcbcabcbc... 的形式
[official](https://leetcode.cn/problems/decode-string/solution/zi-fu-chuan-jie-ma-by-leetcode-solution/)
"""
    def decodeString(self, s: str) -> str:
        st = []
        ans = ""
        for ch in s:
            if ch==']':
                tmp = []
                while st[-1] != '[': tmp.append(st.pop())
                st.pop()
                times = []
                while st and st[-1].isdigit(): times.append(st.pop())
                times = int("".join(times[::-1]))
                new = tmp * times
                if st:
                    # for c in new: st.append(c)
                    st += new[::-1]
                else:
                    ans += "".join(new[::-1])
                # st += list(new)
            else:
                if st or ch.isdigit():
                    st.append(ch)
                else:
                    ans += ch
        return ans
    
    """ 0406. 根据身高重建队列 #medium #排序 对于一个 (h,k), h 表示身高, k 表示前面有 k 个人身高大于等于 h, 求重建队列 
限制: n 2e3
思路1: #排序, 我们考虑从高到低排序, 这样的话, 对于当前的第i个人, 已经安排好位置的人都 >=它, 只需要插入位置k即可. 
    考虑相同身高的情况, 因此实际上是按照 (-h, k) 排序
    这样, 对于相同身高的, 先将k较小的安排后, 再插入k值更大的元素
    复杂度: 插入 O(n^2)
细节: 注意, Python 的 .insert 操作是比较robust的, 例如 a的长度为0, 允许 a.insert(2,xx) 插入最后
[here](https://leetcode.cn/problems/queue-reconstruction-by-height/solution/xian-pai-xu-zai-cha-dui-dong-hua-yan-shi-suan-fa-g/)
    """
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        people.sort(key=lambda x: (-x[0], x[1]))
        ans = []
        for h,k in people:
            # Python的 insert很棒~
            ans.insert(k, [h,k])
        return ans
    
    """ 0437. 路径总和 III #medium 求从上往下的路径和为x的数量
思路: 递归
    """
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        if not root: return 0
        ans = 0
        def dfs(root):
            nonlocal ans
            s = Counter()
            for c in root.left, root.right:
                s = s + dfs(c) if c else s
            ret = Counter()
            for k,v in s.items():
                ret[k+root.val] += v
            ret[root.val] += 1
            ans += ret[targetSum]
            return ret
        dfs(root)
        return ans
    
    """ 0438. 找到字符串中所有字母异位词 #medium 
思路1: #滑窗, 为了优化比较是否相同的代价, 可以用一个diff记录相差的绝对数量
    """
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n = len(s); m = len(p)
        ref = Counter(p)
        now = Counter(s[:m])
        diff = sum(abs(ref[k]-now[k]) for k in ref+now)
        ans = []
        if diff==0: ans.append(0)
        for i in range(m, n):
            c = s[i]
            if ref[c] > now[c]: diff-=1
            else: diff+=1
            now[c] += 1
            c2 = s[i-m]
            if ref[c2] < now[c2]: diff-=1
            else: diff += 1
            now[c2] -= 1
            # ans += int(diff==0)
            if diff==0: ans.append(i-m+1)
        return ans

    """ 0448. 找到所有数组中消失的数字 #easy #集合 """
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        n = len(nums)
        s = set(nums)
        ans = []
        for i in range(1,n+1):
            if i not in s:
                ans.append(i)
        return ans
    
    """ 0461. 汉明距离 #easy #二进制 距离 """
    def hammingDistance(self, x: int, y: int) -> int:
        ans = 0
        while x or y:
            x,a = divmod(x,2)
            y,b = divmod(y,2)
            ans += int(a!=b)
        return ans
    
    """ 0543. 二叉树的直径 #easy #题型 注意距离针对的是边的数量! """
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        ans = 0
        def dfs(r:TreeNode) -> int:
            nonlocal ans
            if not r: return 0
            a = dfs(r.left) if r.left else 0
            b = dfs(r.right) if r.right else 0
            ans = max(ans, a+b, a, b)
            return max(a,b) + 1     # 注意只有在上传的时候才 +1 计算距离!
        dfs(root)
        return ans
    
    """ 0538. 把二叉搜索树转换为累加树 #medium #题型 对于一颗二叉搜索树, 转为累加树, 即每个节点的值为原来的值加上所有大于它的值之和 """
    def convertBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(r:TreeNode, vright=0)->int:
            # vright: 已经遍历的树上 >= 该节点的值和
            if r is None: return vright
            # 先遍历 right
            val = dfs(r.right, vright) + r.val 
            # 加上当前节点!
            r.val = val
            # 遍历 left, 并 return!
            return dfs(r.left, val)
        dfs(root)
        return root
    
    """ 0617. 合并二叉树 #easy #题型 对应的值相加
    细节: 如何处理空节点的情况? 与其对于 left/right 都要写一遍, 下面直接在dfs中创建节点! 注意这时候需要回传节点指针
    """
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(p,q):
            if q is None: return p
            if p is None: p = TreeNode()
            p.val += q.val
            # 注意传回赋值!
            p.left = dfs(p.left, q.left)
            p.right = dfs(p.right, q.right)
            return p
        return dfs(root1, root2)
    
    """ 0581. 最短无序连续子数组 #medium """
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        snums = sorted(nums)
        n = len(nums)
        acc = 0
        l = 0; r = n-1
        while l<n and nums[l]==snums[l]:
            acc += 1
            l += 1
        while r>l and nums[r]==snums[r]:
            acc += 1
            r -= 1
        return n-acc
    
    """ 0621. 任务调度器 #medium #题型 #贪心 给定一组字母代表的任务, 约束两个相同任务之间至少间隔距离为n, 问完成所有任务所需最短时间
思路1: #贪心 对于 aaabbbccdde 这种形式, 有贪心的填充方式: 
abc..
abc..
ab
也即, 按照出现次数最多的, 从上往下开始填充! 对于 cnt(b) = mx 的情况, 只能填满所有行; 否则有限前 mx-1 行
    """
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # 转为任务类型计数
        nums = list(sorted(Counter(tasks).values(), reverse=True))
        # 最大重复数量
        mx = nums[0]
        n_mx = Counter(nums)[mx]
        # 计算前 mx-1 行的空余数量
        space = (mx-1) * max(0, n-n_mx+1)
        return mx * n_mx +  + max(space, sum(nums[n_mx:]))
    
    """ 0647. 回文子串 #medium 统计数量, 应该只哟 O(n^2) 的做法 """
    def countSubstrings(self, s: str) -> int:
        cnt = 0
        n = len(s)
        for i in range(n):
            l=r=i
            while 0<=l and r<n and s[l]==s[r]:
                cnt += 1
                l,r = l-1,r+1
            l,r = i,i+1
            while 0<=l and r<n and s[l]==s[r]:
                cnt += 1
                l,r = l-1,r+1
        return cnt
    
    """ 0148. 排序链表 #medium #hard #题型 进阶要求是在 O(n logn) 时间, O(1) 空间内完成
思路1: 自底向下的 #归并排序
[official](https://leetcode.cn/problems/sort-list/solution/pai-xu-lian-biao-by-leetcode-solution/)
"""
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        def merge(a,b):
            dummy = p = ListNode()
            while a or b:
                if a is None or b is None:
                    p.next = a or b
                    while p.next: p = p.next
                    break
                if a.val < b.val:
                    p.next = a
                    a = a.next; p = p.next
                else:
                    p.next = b
                    b = b.next; p = p.next
            p.next = None
            # 返回 head, tail
            return dummy.next, p
        def getLen(head):
            cnt = 0
            while head:
                cnt += 1
                head = head.next
            return cnt
        dummy = ListNode(next=head)
        step = 1
        n = getLen(head)
        while step < n:
            # pre: 上一个节点
            pre = dummy; cur = dummy.next
            while cur:
                # cur: 第二段的开始位置
                for _ in range(step-1): 
                    if cur: cur = cur.next
                if cur is None or cur.next is None: break
                # cur 现在在当前段的最后位置, 需要设置 .next=None
                _tmp = cur.next; cur.next = None; cur = _tmp
                # nxt: 指向两段之后的元素
                nxt = cur
                for _ in range(step-1): 
                    if nxt: nxt = nxt.next
                if nxt is None or nxt.next is None: nxt = None
                else:
                    _tmp = nxt.next; nxt.next = None; nxt = _tmp
                _head, _tail = merge(pre.next, cur)
                pre.next = _head
                _tail.next = nxt
                pre = _tail; cur = nxt
            step <<=1
        return dummy.next
    
    """ 0238. 除自身以外数组的乘积 #medium 计算每个元素除自身以外的乘积, 不能用除法
思路1: 两次遍历, 分别计算前缀积和后缀积. 下面用了一些技巧
"""
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        suffix = [1] * (n+1)
        for i in range(n-1,-1,-1):
            suffix[i] = suffix[i+1] * nums[i]
        pre = 1
        for i,x in enumerate(nums):
            if i<n-1:
                tmp = pre * suffix[i+1]
            else:
                tmp = pre
            pre *= x
            nums[i] = tmp
        return nums
    
    """ 0253. 会议室 II #medium 给定一组 (s,e) 定义的会议, 问最少需要多少个会议室
思路1: 利用 #前缀和 来确定最大重叠
    复杂度: O(MAX)
思路2: 模拟「安排会议」的过程, 利用 #优先队列 来记录当前会议的所有结束时间
    复杂度: O(n logn)
    """
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        mx = max(map(max, intervals))
        acc = [0] * (mx+2)
        for s,e in intervals:
            acc[s] += 1
            acc[e] -= 1
        ans = 0
        for i in range(1, mx):
            acc[i]  += acc[i-1]
            ans = max(ans, acc[i])
        return ans
    
    """ 0240. 搜索二维矩阵 II #medium #题型 矩阵满足, 从左到右、从上到下是递增的. 问是否存在目标值
思路1: #Z字 搜索, 从右上角开始, 每次排除一行或者一列
    复杂度: O(m+n)
"""
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m,n = len(matrix),len(matrix[0])
        x,y = 0,n-1
        while x<m and y>=0:
            if matrix[x][y]==target: return True
            elif matrix[x][y]>target: y-=1
            else: x += 1
        return False


""" 0155. 最小栈 #medium 在实现一个栈的情况下, 要求能够早 O(1) 时间内返回最小值
思路1: 用一个辅助栈来记录最小值!
    复杂度: 所有操作都是 O(1)
"""
class MinStack:
    def __init__(self):
        self.st = []
        self. minst = [inf]

    def push(self, val: int) -> None:
        self.st.append(val)
        self.minst.append(min(val, self.minst[-1]))

    def pop(self) -> None:
        self.minst.pop()
        return self.st.pop()

    def top(self) -> int:
        return self.st[-1]

    def getMin(self) -> int:
        return self.minst[-1]
    
sol = Solution()
result = [
    # sol.decodeString("3[z]2[2[y]pq4[2[jk]e1[f]]]ef"),
    # sol.reconstructQueue(people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]),
    # sol.findAnagrams(s = "cbaebabacd", p = "abc"),
    sol.productExceptSelf([1,2,3,4]),
    
]
for r in result:
    print(r)

# printLCLinkedList(sol.sortList(genLCLinkedList([4,2,1,3]))) 
