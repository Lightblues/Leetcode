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

@2022 """
class Solution:
    """ 0785. 判断二分图 #medium 给定一张图, 判断是否二分. 限制: 节点数 n 100.
思路1: 由于仅仅要判断是否二分, 可以随便从那个节点开始DFS, 对于相邻节点涂上另一种颜色即可.
    """
    def isBipartite(self, graph: List[List[int]]) -> bool:
        # 1. 颜色标记法
        # 2. 深度优先搜索
        n = len(graph)
        color = [0] * n
        def dfs(node, c):
            color[node] = c
            for next in graph[node]:
                if color[next] == c:
                    return False
                if color[next] == 0 and not dfs(next, -c):
                    return False
            return True
        for i in range(n):
            if color[i] == 0:
                if not dfs(i, 1):
                    return False
        return True
    
    """ 0403. 青蛙过河 #hard 有一组石头, 开始在位置0, 只能跳单位1. 假设前一次跳跃k, 那么下一次可以跳跃k-1, k, k+1. 问是否能跳到最后一个石头.
限制: n 2e3; 石头位置 2e31.
思路1: #记忆化 搜索. f(i, k) 表示跳跃k到达第i个石头, 能够到达终点.
    复杂度: 考虑记忆化的状态数为 O(n^2)
[官答](https://leetcode.cn/problems/frog-jump/solutions/746996/qing-wa-guo-he-by-leetcode-solution-mbuo/) 还介绍了展开为 dp 的解法.
"""
    def canCross(self, stones: List[int]) -> bool:
        n = len(stones)
        s2idx = {s:i for i,s in enumerate(stones)}
        # 记忆化 搜索
        @lru_cache(None)
        def f(i, dis, k):
            # 边界: 要向前跳
            if i==n-1: return True
            for pos in range(k-1, k+2):
                if pos <= 0: continue
                if dis+pos in s2idx and f(s2idx[dis+pos], dis+pos, pos): return True
            return False
        # 有了上面的边界判断, 可以直接 f(0,0,0) 了
        # if stones[1] != 1: return False
        # return f(1,1,1)
        return f(0,0,0)
    
    
    """ 0769. 最多能完成排序的块 #medium #题型
给定一个长n的数组, 表示 0...n-1 元素的一个排列. 我们对于该排列进行分快, 使得每块内部排序之后, 整体是有序的. 问最多能分成多少快? 限制: n 10
思路1: #贪心
    考虑哪些位置(前缀)是可能的? 细想可知, 若 arr[:i] 是 0...i 的一个排列, 该区域可以分成一块.
    [官答](https://leetcode.cn/problems/max-chunks-to-make-sorted/solution/zui-duo-neng-wan-cheng-pai-xu-de-kuai-by-gc4k/)
"""
    def maxChunksToSorted(self, arr: List[int]) -> int:
        mx = 0
        cnt = 0
        for i,a in enumerate(arr):
            mx = max(mx, a)
            if mx==i: cnt += 1
        return cnt

""" 0146. LRU 缓存 #medium  但其实挺 #hard 要求实现一个LRU缓存. (最远没有使用的) 
也即, 给定限制的 capacity空间用于存储. 在插入的时候若超过了限制, 则删除「最远没有使用」的记录.
限制: 插入, 查询 复杂度均为 O(1)
关键在于: 如何记录
思路0: 原本打算记录插入和查询 #时间戳. 但想了半天似乎不太可行!
思路1: 采用 Python自带的 `OrderedDict`, 来记录键值对的插入顺序, 超过容量则删除最早插入的键值对.
    相关API: move_to_end(key), popitem(last=False).
思路2: 采用 #双向链表+#哈希表.
    如何记录顺序关系, 还有可以置顶? 可以采用双向链表. 为了快速查找元素, 用一个哈希表记录 {key:node} 的映射.
    双向链表的操作: addToHead(node), removeNode(node), moveToHead(node).
see [official](https://leetcode.cn/problems/lru-cache/solution/lruhuan-cun-ji-zhi-by-leetcode-solution/)

"""
class LRUCache(collections.OrderedDict):
    # 直接基于 OrderedDict
    def __init__(self, capacity: int):
        super().__init__()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self:
            return -1
        self.move_to_end(key)
        return self[key]

    def put(self, key: int, value: int) -> None:
        if key in self:
            self.move_to_end(key)
        self[key] = value
        if len(self) > self.capacity:
            self.popitem(last=False)

# 双向链表节点
class DLinkedNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
# 思路2: 采用 #双向链表+#哈希表.
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cache = dict()
        # 使用伪头部和伪尾部节点  
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity
        self.size = 0
    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        # 如果 key 存在，先通过哈希表定位，再移到头部
        node = self.cache[key]
        self.moveToHead(node)
        return node.value
    def put(self, key:int, value:int) -> None:
        if key not in self.cache:
            node = DLinkedNode(key, value)
            self.cache[key] = node
            self.addToHead(node)
            self.size += 1
            if self.size > self.capacity:
                removed = self.removeTail()
                self.cache.pop(removed.key)
                self.size -= 1
        else:
            node = self.cache[key]
            node.value = value
            self.moveToHead(node)
    # 双向链表的操作
    def addToHead(self, node: DLinkedNode) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    def removeNode(self, node: DLinkedNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
    def moveToHead(self, node):
        self.removeNode(node)
        self.addToHead(node)
    def removeTail(self):
        node = self.tail.prev
        self.removeNode(node)
        return node

sol = Solution()
result = [
    # sol.isBipartite(graph = [[1,2,3],[0,2],[0,1,3],[0,2]]),
    # sol.isBipartite(graph = [[1,3],[0,2],[1,3],[0,2]]),
#     testClass("""["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
# [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]"""),
    # sol.canCross(stones = [0,1,3,5,6,8,12,17]),
    # sol.canCross(stones = [0,1,2,3,4,8,9,11]),
    # sol.canCross([0,2]),
    sol.maxChunksToSorted([3,2,1,0]),
    sol.maxChunksToSorted([1,0,2,3,4])
]
for r in result:
    print(r)
