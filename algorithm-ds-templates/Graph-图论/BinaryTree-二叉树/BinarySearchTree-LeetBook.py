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

""" 
二叉搜索树 https://leetcode.cn/leetbook/detail/introduction-to-data-structure-binary-search-tree/
== 引入
验证二叉搜索树; 0173. 二叉搜索树迭代器 其中考察了迭代形式的中序遍历.

== 基本
二叉搜索树中的搜索; 二叉搜索树中的插入操作
0450. 删除二叉搜索树中的节点: 重点是删除操作, 画图理解.

== 拓展: 高度平衡的二叉搜索树
一些实现: 
*   [红黑树](https://baike.baidu.com/item/%E7%BA%A2%E9%BB%91%E6%A0%91/2413209?fr=aladdin)
*   [AVL树](https://baike.baidu.com/item/AVL%E6%A0%91/10986648?fr=aladdin)
*   [伸展树](https://baike.baidu.com/item/%E4%BC%B8%E5%B1%95%E6%A0%91/7003945)
*   [树堆](https://baike.baidu.com/item/Treap/4321536?fr=aladdin)
性质: 可以在 `O(logN)` 时间复杂度内执行所有搜索、插入和删除操作
应用: Set 和 Map 中. 相似, 这里就介绍集合.
    `树集合`，Java 中的 `Treeset` 或者 C++ 中的 `set`，是由高度平衡的二叉搜索树实现的。
    `散列集合`，Java 中的 `HashSet` 或者 C++ 中的 `unordered_set`，是由哈希实现的。但发生哈希碰撞的时候, 使用高度平衡的二叉搜索树可以简化在相同哈希值的元素中的搜索复杂度.
    哈希集和树集之间的本质区别在于树集中的键是`有序`的。
相关简单题: 0110. 平衡二叉树 (判断是否为); 0108. 将有序数组转换为二叉搜索树


== 其他
0703. 数据流中的第K大元素: 更优的DS是最小堆.
0235. 二叉搜索树的最近公共祖先: 利用二叉搜索树性质简化问题
0220. 存在重复元素 III: 更优的DS是有序列表, 或者用桶排序

@2022 """

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 验证二叉搜索树 判断给定的二叉搜索树是否合法
思路1: 递归函数 `valid(root: TreeNode, l:int, r:int)` 传入合法的区间 [l, r]
"""
    
    """ 二叉搜索树中的搜索 """
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        while root and root.val!=val:
            if root.val > val: root = root.left
            else: root = root.right
        return root
    
    """ 二叉搜索树中的插入操作 """
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if root is None: return TreeNode(val)
        p = root
        while p:
            if p.val > val: 
                if p.left: p = p.left
                else: p.left = TreeNode(val); break
            else: 
                if p.right: p = p.right
                else: p.right = TreeNode(val); break
        return root
    
    """ 0450. 删除二叉搜索树中的节点 #medium #题型
难点是找到的p节点左右孩子都非空的情况, 需要找到 successor 并进行修改.
思路1: 递归写法
思路2: 迭代写法
[官答](https://leetcode.cn/problems/delete-node-in-a-bst/solution/shan-chu-er-cha-sou-suo-shu-zhong-de-jie-n6vo/)
"""
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        # 思路2: 迭代写法
        p = root; fa = None
        while p and p.val!=key:
            if p.val > key: fa, p = p, p.left
            else: fa, p = p, p.right
        if not p: return root   # not found
        # 修正p的子树
        if p.left is None and p.right is None: p = None
        elif p.left is None: p = p.right
        elif p.right is None: p = p.left
        else:
            # 找到 p 的 successor
            nxt, nxtFa = p.right, p
            while nxt.left: nxtFa, nxt = nxt, nxt.left
            # successor 的左孩子一定是空, 将右孩子挂到 successor 的父节点上
            if nxtFa.val==p.val:
                nxtFa.right = nxt.right
            else:
                nxtFa.left = nxt.right
            # 注意, 下面的操作不等于 p.val = nxt.val (递归时可以这么写)! 因为要保留 fa.left/right 的值, 来辅助最后的判断.
            nxt.left = p.left
            nxt.right = p.right
            p = nxt
        # 将fa的某个子节点指向p
        if fa is None: return p     # 被删除的是 root
        if fa.left and fa.left.val==key: fa.left = p
        else: fa.right = p
        return root
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        # 递归写法, 返回当前 root 节点 (修改过的)
        if root is None: return None
        if root.val > key: 
            root.left = self.deleteNode(root.left, key)
        elif root.val < key:
            root.right = self.deleteNode(root.right, key)
        else:   # root.val == key, 找到了!
            # 若左右孩子至少一个为空, 则直接指向另一个孩子
            if root.left is None: return root.right
            elif root.right is None: return root.left
            # 都不为空, 需要找到 successor
            else:
                nxt, nxtFa = root.right, root
                while nxt.left: nxtFa, nxt = nxt, nxt.left
                # successor 的左孩子一定是空, 将右孩子挂到 successor 的父节点上
                if nxtFa.val==root.val:
                    nxtFa.right = nxt.right
                else:
                    nxtFa.left = nxt.right
                # 注意, 此时的 nxt 已经从树结构中移除了, 直接修改 root 的值即可 (root.val == key)
                root.val = nxt.val
        return root
    
    
    """ 0220. 存在重复元素 III #hard #题型
给定一个数组, 要求判断是否有一个下标对 (i,j), 满足间距 <=k, 两者的值相差 <=t. 限制: 数组长度 2e4
思路0: 强行用二叉树来做, 理想的时间复杂度为 `O(n logk)`, 但最坏情况要 O(n^2)
    维护滑动窗口, 二叉树支持插入删除操作.
    关键是如何检查要求? 可以实现一个函数查询树上是否有 `[x-t, x+t]` 范围内的元素.
思路1: 维护长度为 k+1 的 #滑动窗口. 每次需要插入删除元素, 并且需要得到插入元素临近的两个元素大小. 可以用 #有序列表, 复杂度 `O(n logk)`
思路2: #桶排序 #star
    将数字范围分割成大小为 k+1 的桶. 遍历的过程中, 只需要检查对应的桶以及左右桶是否有符合要求的元素即可.
    具体而言, 用一个 #哈希表 来记录目前为止包含元素的那些桶. 遍历过程中, 假设 `id(x)` 表示当前元素对应的桶, 若 `id(x)` 已存在则直接返回true; 并检查相邻的 `id(x)+/-1` 中存储的元素是否满足条件.
    如何计算 id? 假设所有的数字表示为 `x = a*(t+1) + b`, 可知Python中的整除操作就是符合要求的函数.
[官答](https://leetcode.cn/problems/contains-duplicate-iii/solution/cun-zai-zhong-fu-yuan-su-iii-by-leetcode-bbkt/)
"""
    def containsNearbyAlmostDuplicate(self, nums: List[int], k: int, t: int) -> bool:
        # 思路1: 维护长度为 k+1 的 #滑动窗口
        from sortedcontainers import SortedList
        sl = SortedList()
        for i,x in enumerate(nums):
            # 删除过期的元素
            if i>k:
                sl.remove(nums[i-k-1])
            # 找到最接近的数字
            idx = sl.bisect_right(x)
            if idx>0 and x-sl[idx-1]<=t: return True
            if idx<len(sl) and sl[idx]-x<=t: return True
            sl.add(x)
        return False
    def containsNearbyAlmostDuplicate00(self, nums: List[int], k: int, t: int) -> bool:
        # 思路2: #桶排序 #star
        def getID(x): return x//(t+1)
        h = {}
        for i,num in enumerate(nums):
            if i>=k+1: 
                pid = getID(nums[i-k-1])
                del h[pid]
            iid = getID(num)
            if iid in h: return True
            if iid-1 in h and num-h[iid-1]<=t: return True
            if iid+1 in h and h[iid+1]-num<=t: return True
            h[iid] = num
        return False

    
    """ 0110. 平衡二叉树. #easy 平衡二叉树定义: 「每个节点的左右子树高度差不超过1」 """

    
    """ 0108. 将有序数组转换为二叉搜索树 """
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def f(l,r):
            if l>r: return None
            mid = (l+r)//2
            root = TreeNode(nums[mid])
            root.left = f(l,mid-1)
            root.right = f(mid+1,r)
            return root
        return f(0,len(nums)-1)
    
    
""" 0173. 二叉搜索树迭代器
给定一棵二叉树, 要求返回一个迭代器, 要求实现接口 `next()` 和 `hasNext()`. 限制: 节点数 O(n)
进阶要求: 限制两个操作的均摊代价为 O(1), 并且仅使用 `O(h)` 的内存
思路1: 直接中序遍历, 用数组存储访问的顺序. 这样的内存开销为 `O(n)`
思路2: 除了递归写法, 还可以利用栈将其展开为迭代写法. 参见 [二叉树 中序遍历]
[官答](https://leetcode.cn/problems/binary-search-tree-iterator/solution/er-cha-sou-suo-shu-die-dai-qi-by-leetcod-4y0y/)
"""
class BSTIterator:
    # 思路1: 直接中序遍历
    def __init__(self, root: Optional[TreeNode]):
        self.vals = []
        def f(root: TreeNode):
            if root is None: return
            f(root.left)
            self.vals.append(root.val)
            f(root.right)
        f(root)
        self.n = len(self.vals)
        self.idx = -1

    def next(self) -> int:
        self.idx += 1
        return self.vals[self.idx]

    def hasNext(self) -> bool:
        return self.idx < self.n - 1

class BSTIterator:
    # 思路2: 利用栈展开.
    def __init__(self, root: Optional[TreeNode]):
        self.s = []
        self.cur = root
    def next(self) -> int:
        # 将当前节点的左子树顺序入栈
        while self.cur:
            self.s.append(self.cur)
            self.cur = self.cur.left
        # 最下的没有左孩子的节点, 是当前 val
        self.cur = self.s.pop()
        val = self.cur.val
        self.cur = self.cur.right       # 更新 cur 为右子树
        return val
    def hasNext(self) -> bool:
        # 终止条件: 由指针和栈共同决定
        return bool(self.cur or self.s)
        # 注意 76 or [] == 76, 需要进行类型转换; 或者下面的形式更规范.
        # return self.cur is not None or len(self.s)>0
    

""" 0703. 数据流中的第K大元素 #easy #二叉搜索树 但是强行用二叉搜索树来做
要求实现一个DS, 支持插入数据, 查询数据流中第k大的元素. 限制: 插入, 查询操作 1e4
思路0: 强行用二叉搜索树来做, 见 [here](https://leetcode.cn/leetbook/read/introduction-to-data-structure-binary-search-tree/xpbmwd/)
思路1: 正常的思路应该是用 #优先队列 来实现
    也即, 维护一个大小为k的优先队列 (#最小堆), 若堆大小 >k 则弹出, 每次查询返回堆顶元素.
    复杂度: `O(n log k)`
    [官答](https://leetcode.cn/problems/kth-largest-element-in-a-stream/solution/shu-ju-liu-zhong-de-di-k-da-yuan-su-by-l-woz8/)
"""
class Node:
    def __init__(self, val=0, cnt=0, left=None, right=None):
        self.val = val
        self.cnt = cnt
        self.left = left
        self.right = right
class KthLargest:
    root = None
    def insert(self, val: int, root: Optional[Node]) -> Node:
        # 递归插入
        if root is None:
            root = Node(val, cnt=0)
        elif val < root.val:
            root.left = self.insert(val, root.left)
        else: root.right = self.insert(val, root.right)
        root.cnt += 1
        return root

    def searchK(self, val:int, k:int, root:TreeNode) -> int:
        # return the kth largest element in the BST.
        if root.right is None:
            return root.val if k==1 else self.searchK(val, k-1, root.left)
        if root.right.cnt >= k:
            return self.searchK(val, k, root.right)
        else:
            return root.val if k==1+root.right.cnt else self.searchK(val, k-1-root.right.cnt, root.left)
        
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        for n in nums:
            self.root = self.insert(n, self.root)
    def add(self, val: int) -> int:
        self.root = self.insert(val, self.root)
        return self.searchK(val, self.k, self.root)

class KthLargest:
    # 思路1: 优先队列 (#最小堆),
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.q = []
        for a in nums:
            self.insert(a)
    def insert(self, val):
        heappush(self.q, val)
        if len(self.q) > self.k:
            heappop(self.q)
    def add(self, val: int) -> int:
        self.insert(val)
        return self.q[0]

sol = Solution()
result = [
#     testClass("""["KthLargest", "add", "add", "add", "add", "add"]
# [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]"""),
    sol.containsNearbyAlmostDuplicate(nums = [1,2,3,1], k = 3, t = 0),
    sol.containsNearbyAlmostDuplicate(nums = [1,5,9,1,5,9], k = 2, t = 3),
    sol.containsNearbyAlmostDuplicate([4,1,6,3],4,1),

]
for r in result:
    print(r)
