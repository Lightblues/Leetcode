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



Easonsi @2023 """
class Solution:
    """  """
    
    
    
    
    
""" 1825. 求出 MK 平均值 #hard 对于数据流, 计算最后m个元素的去除最大最小k个元素的平均数. 限制: m 1e5, 操作次数 1e5
思路1: 三个 #有序数组+#队列 [官答](https://leetcode.cn/problems/finding-mk-average/solution/qiu-chu-mk-ping-jun-zhi-by-leetcode-solu-sos6/)
    利用一个队列记录q最近的数据; 利用三个长度分别为 k,m-2k,k 的有序队列 sl1,sl2,sl3 存储有序的数据; 再记录中间数组的和acc2
    对于未满m个元素的情况, 需要直接返回-1. 直接根据q的长度返回. 
    每次addElement: 先将其加入q, 加入后: 
        若q的长度 <=m, 初始化过程, 方法任意. 
        若q长度 =m+1, 是一般的情况. 
            将新元素new根据大小加入sl1,sl2,sl3中. 调整元素使得三个数组连起来仍然有序, 并且长度分别为 k,m-2k+1,k
            将需要弹出的元素old从中删除: 需要判断是在那个有序数组中, 删除并调整长度分别为 k,m-2k,k
思路2: 一个 #有序数组 #环形数组
    考虑实际情况, 用一个大小为m的 #环形数组 latestM 来存储最近的m个数据. 并且动态更新数组和
    用 有序数组 直接记录最近的m个元素, 然后动态维护 sum(sl[:]) 和 sum(sl[k:-k])
        也即, 根据每次插入/删除的位置来 #分类 讨论. 例如, 当插入第idx个数字. 我们在有序列表中找到该数字的位置 idxNew, 则: 
        1) 若 `idxNew<k` 则 k-1...m-k-1 部分会发生右移, 因此 midSum += sl[k-1]-sl[m-k-1]; 
        2) 若 `k<=idxOld<m-k`, 则 `midSum += num-sl[m-k-1]`; 
        3) 否则, 对于midSum不影响. (一开始还要删除第idx-m个数字, 思路一致.)
    见 [here](https://leetcode.cn/problems/finding-mk-average/solution/by-981377660lmt-5hhm/)
总结: 本题的设置符合实际应用场景需求; 在试错的过程中逐步推导出所需记录的数据结构的过程很有意思.
"""
from sortedcontainers import SortedList
class MKAverage:
    def __init__(self, m: int, k: int):
        self.m = m
        self.k = k
        self.q = deque()
        self.sl1 = SortedList()
        self.sl2 = SortedList()
        self.sl3 = SortedList()
        self.acc = 0

    def addElement(self, num: int) -> None:
        self.q.append(num)
        if len(self.q) <= self.m:
            self.sl2.add(num)
            if len(self.q) == self.m:
                self.sl1 = SortedList(self.sl2[:self.k])
                self.sl3 = SortedList(self.sl2[-self.k:])
                self.sl2 = SortedList(self.sl2[self.k:-self.k])
                self.acc = sum(self.sl2)
        elif len(self.q)==self.m+1:
            # add new
            if num<self.sl1[-1]:
                self.sl1.add(num)
                t = self.sl1.pop()
                self.sl2.add(t); self.acc += t
            elif num>self.sl3[0]:
                self.sl3.add(num)
                t = self.sl3.pop(0)
                self.sl2.add(t); self.acc += t
            else: self.sl2.add(num); self.acc += num
            # delete old
            old = self.q.popleft()
            if old in self.sl1:
                self.sl1.remove(old)
                t = self.sl2.pop(0); self.acc -= t
                self.sl1.add(t)
            elif old in self.sl2:
                self.sl2.remove(old); self.acc -= old
            else:
                self.sl3.remove(old)
                t = self.sl2.pop(); self.acc -= t
                self.sl3.add(t)

    def calculateMKAverage(self) -> int:
        if len(self.q) < self.m:
            return -1
        return self.acc // (self.m-2*self.k)

class MKAverage:
    def __init__(self, m: int, k: int):
        self.m = m
        self.k = k
        self.latestM = [-1] * m # 循环数组, 记录最近的元素
        self.latestSum = 0      # 循环数组的和
        self.cnt = 0            # 当前流数据的个数


    def addElement(self, num: int) -> None:
        # 先处理 latestM 和 latestSum
        vOld = self.latestM[self.cnt % self.m]
        self.latestM[self.cnt % self.m] = num
        self.cnt = self.cnt+1
        self.latestSum += num - vOld if vOld!=-1 else num
        # 在长度达到 m 的时候建立 SL
        if self.cnt==self.m:
            # self.flag = True
            self.sl = SortedList(self.latestM)
            self.midSum = sum(self.sl[self.k:self.m-self.k])
        # 需要对于 SL 进行维护了
        elif self.cnt>self.m:
            # 删除序列中 idx-m 个元素
            idxOld = self.sl.index(vOld)
            if idxOld<self.k:
                self.midSum += -self.sl[self.k]+self.sl[-self.k]
            elif idxOld<self.m-self.k:
                self.midSum += -vOld+self.sl[-self.k]
            self.sl.pop(idxOld)
            # 添加新的 idx 个元素
            idxNew = self.sl.bisect_right(num)
            if idxNew<self.k:
                self.midSum += self.sl[self.k-1]-self.sl[self.m-self.k-1]
            elif idxNew<self.m-self.k:
                self.midSum += num-self.sl[self.m-self.k-1]
            self.sl.add(num)

    def calculateMKAverage(self) -> int:
        if self.cnt>=self.m: return self.midSum // (self.m-2*self.k)
        else: return -1
    
sol = Solution()
result = [
    testClass("""["MKAverage", "addElement", "addElement", "calculateMKAverage", "addElement", "calculateMKAverage", "addElement", "addElement", "addElement", "calculateMKAverage"]
[[3, 1], [3], [1], [], [10], [], [5], [5], [5], []]""")
]
for r in result:
    print(r)
