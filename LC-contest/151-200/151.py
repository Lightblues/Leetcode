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
https://leetcode.cn/contest/weekly-contest-151
T3链表题. T4考虑顺序排列的栈, 需要考虑很多细节. 

@2022 """
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    """ 1169. 查询无效交易 #easy #medium 给定一组交易, 对于 1) 交易金额超过 1000 2) 交易名称相同, 但是城市不同并且交易时间间隔小于 60 分钟的两笔交易 判定无效. 返回所有无效交易的交易字符串. 限制: n 1e3
乱七八糟的 #模拟 题. 暴力两次循环. 
"""
    def invalidTransactions(self, transactions: List[str]) -> List[str]:
        transactions=[i.split(",") for i in transactions]
        res=[]
        for i,v in enumerate(transactions):
            if int(v[2])>1000:
                res.append(",".join(v))
                continue
            for j,u in enumerate(transactions):
                if i==j:
                    continue
                if v[0]==u[0] and v[3]!=u[3] and abs(int(v[1])-int(u[1]))<=60:
                    res.append(",".join(v))
                    break
        return res 

    """ 1170. 比较字符串最小字母出现频次 #medium #二分 
    https://leetcode.cn/problems/compare-strings-by-frequency-of-the-smallest-character/"""
    def numSmallerByFrequency(self, queries: List[str], words: List[str]) -> List[int]:
        def f(word):
            cnt = Counter(word)
            return sorted(cnt.items())[0][1]
        words = sorted([f(word) for word in words])
        ans = []
        for query in queries:
            cnt = f(query)
            # 二分
            ans.append(len(words) - bisect.bisect(words, cnt))
        return ans

    """ 1171. 从链表中删去总和值为零的连续节点 #medium 不断从 #链表 删除连续的和为0的片段. 返回剩余的链表. 限制: N 1e3
思路1: 记录 #前缀和 和 该值所对应的节点位置. 
    可以有一个列表记录 (idx, acc, node_head) 集合. 遇到 `acc_i == acc_j`, 则删除 [j+1, i] 的节点.注意也需要将列表的 arr[j+1:] 删除. 
    复杂度: O(n^2)
"""
    def removeZeroSumSublists(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        accs = [0]
        nodes = [dummy]
        while head:
            acc = accs[-1] + head.val
            for i,x in enumerate(accs):
                if x==acc:
                    nodes[i].next = head.next
                    del accs[i+1:], nodes[i+1:]
                    break
            else:
                accs.append(acc); nodes.append(head)
            head = head.next
        return dummy.next
    
""" 1172. 餐盘栈 #hard #栈 #细节 每个栈的容量为capacity, 要求实现 push(val), pop, popAtStack(index) 三个方法.
具体: push 在最早的一个空位上加入一个元素, 都满了的话新增一个栈; pop 弹出最左的一个元素. popAtStack(index) 把第index个栈的栈顶元素弹出.
思路1: 用 #有序数组 remainIdx 记录所有存在空位的位置. 
    细节: 如何维护 remainIdx 的有效性? 
        删除: 1) 在当前满的时候删除; 2) 当前idx的栈被「撤销」. 
        加入: 新加入的栈; 原本满的栈被弹出. 
https://leetcode.cn/problems/dinner-plate-stacks/
"""
from sortedcontainers import SortedSet
class DinnerPlates:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # 剩下空位的位置
        self.remainIdx = SortedSet()
        self.stacks = []
    
    def push(self, val: int) -> None:
        # 靠左加入元素
        if len(self.remainIdx)==0:
            self.stacks.append([val])
            if self.capacity!=1: self.remainIdx.add(len(self.stacks)-1)
        else:
            idx = self.remainIdx[0]
            self.stacks[idx].append(val)
            if len(self.stacks[idx]) == self.capacity: self.remainIdx.discard(idx)

    def pop(self) -> int:
        # 靠右删除元素
        if len(self.stacks)==0: return -1
        # 这里需要保证, 最右侧的栈是非空的
        ret = self.stacks[-1].pop()
        self.remainIdx.add(len(self.stacks)-1)
        while self.stacks and len(self.stacks[-1])==0:
            self.remainIdx.discard(len(self.stacks)-1)
            self.stacks.pop()
        return ret

    def popAtStack(self, index: int) -> int:
        if index>=len(self.stacks): return -1
        if len(self.stacks[index])==0: return -1
        ret = self.stacks[index].pop()
        self.remainIdx.add(index)
        if index == len(self.stacks)-1:
            while index>0 and len(self.stacks[index])==0:
                self.remainIdx.discard(index)
                self.stacks.pop()
                index -= 1 
        return ret

    
sol = Solution()
result = [
#     testClass("""["DinnerPlates","push","push","push","push","push","popAtStack","push","push","popAtStack","popAtStack","pop","pop","pop","pop","pop"]
# [[2],[1],[2],[3],[4],[5],[0],[20],[21],[0],[2],[],[],[],[],[]]"""),
#     testClass("""["DinnerPlates","push","push","push","popAtStack","pop","pop"]
# [[1],[1],[2],[3],[1],[],[]]"""),
#     testClass("""["DinnerPlates","push","push","popAtStack","pop","push","push","pop","pop"]
# [[1],[1],[2],[1],[],[1],[2],[],[]]"""), 
#     testClass("""["DinnerPlates","push","push","push","push","push","push","push","push","popAtStack","popAtStack","popAtStack","popAtStack","push","push","push","push","push","push","push","push","pop","pop","pop","pop"]
# [[2],[471],[177],[1],[29],[333],[154],[130],[333],[1],[0],[2],[0],[165],[383],[267],[367],[53],[373],[388],[249],[],[],[],[]]"""), 
    sol.invalidTransactions(transactions = ["alice,20,800,mtv","alice,50,100,beijing"]),
    sol.invalidTransactions(transactions = ["alice,20,800,mtv","alice,50,1200,mtv"]),
]
for r in result:
    print(r)
