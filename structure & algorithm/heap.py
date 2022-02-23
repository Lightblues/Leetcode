""" 
from [Python实现最大堆（大顶堆）](https://cloud.tencent.com/developer/article/1570953)

这里的 MaxHeap 类实现了 add, pop, 等方法, 具体的操作为 shift_up, shift_down 进行调整顺序.

另外, 在 heapq 中还有常用的操作 heapify, 思路为: 对于一个堆中的所有非叶子节点开始, 从后向前遍历i, 每次使得i后面的子树为合法的. 注意这里的 shift_up 的方法比较简单, 和其中的 _sift_up 方法不一样.
 """

import heapq

class MaxHeap:
    def __init__(self) -> None:
        self.data = []
        self.count = 0
    def size(self) -> int:
        return self.count
    def is_empty(self) -> bool:
        return self.count == 0

    def add(self, item):
        self.data.append(item)
        self.count += 1
        self.shift_up(self.count - 1)
    def pop(self):
        if self.is_empty():
            return None
        item = self.data[0]
        # 用最后一个元素替代, 然后 shift_down
        self.data[0] = self.data[self.count - 1]
        self.count -= 1
        self.shift_down(0)
        return item
    
    def shift_up(self, index):
        # 上移self._data[index]，以使它不大于父节点
        parent = (index - 1) // 2
        while index > 0 and self.data[index] > self.data[parent]:
            self.data[index], self.data[parent] = self.data[parent], self.data[index]
            index = parent
            parent = (index - 1) // 2
    def shift_down(self, index):
        # 下移self._data[index]，以使它不小于子节点
        child = index * 2 + 1 # 左孩子
        while child < self.count:
            # 右孩子较大
            if child + 1 < self.count and self.data[child] < self.data[child + 1]:
                child += 1
            if self.data[child] <= self.data[index]:
                break
            self.data[index], self.data[child] = self.data[child], self.data[index]
            index = child
            child = index * 2 +1


import random

# 元素是元祖类型
# (12471, '12471')
""" 注意
(1,2) < (2,)
"aaa" < "aaab"
 """
def testTupleValue():
    for iTimes in range(10):
        iLen = random.randint(1,300)
        listData= random.sample(range(iLen*100), iLen)
        # 注意：key作为比较大小的关键
        allData = dict(zip(listData, [str(e) for e in listData]))
        print('\nlen =',iLen)
        print('allData: ', allData)
        
        oMaxHeap = MaxHeap()
        arrDataSorted = sorted(allData.items(), key=lambda d:d[0], reverse=True)
        print('dataSorted:', arrDataSorted)
        for (k,v) in allData.items():
            oMaxHeap.add((k,v)) # 元祖的第一个元素作为比较点
        heapData = []    
        for i in range(iLen):
            iExpected = arrDataSorted[i]
            iActual = oMaxHeap.pop()
            heapData.append(iActual)
            print('{0}, expected: {1}, actual: {2}'.format(iExpected==iActual, iExpected, iActual))
            assert iExpected==iActual, "ERROR"
        print('dataSorted:', arrDataSorted)
        print('heapData:  ',heapData)

# 元素是自定义类    
def testClassValue():
    
    class Model4Test(object):
        '''
        用于放入到堆的自定义类。注意要重写__lt__、__ge__、__le__和__cmp__函数。
        '''
        def __init__(self, sUid, value):
            self._sUid = sUid
            self._value = value
        
        def getUid(self):
            return self._sUid
        
        def getValue(self):
            return self._value
        
        # 类类型，使用的是小于号_lt_
        def __lt__(self, other):#operator < 
            # print('in __lt__(self, other)')
            return self.getValue() < other.getValue()
       
        def __ge__(self,other):#oprator >=
            return self.getValue() >= other.getValue()
     
        #下面两个方法重写一个就可以了
        def __le__(self,other):#oprator <=
            return self.getValue() <= other.getValue()
         
        def __cmp__(self,other):
            #call global(builtin) function cmp for int
            return super.cmp(self.getValue(),other.getValue())
        
        def __str__(self):
            # 定义print输出
            return '({0}, {1})'.format(self._value, self._sUid)
            
    for iTimes in range(10):
        iLen = random.randint(1,300)
        listData = random.sample(range(iLen*100), iLen)
        allData = [Model4Test(str(value), value) for value in listData]
        print('allData:   ', [str(e) for e in allData])
        iLen = len(allData)
        print('\nlen =',iLen)

        oMaxHeap = MaxHeap()
        arrDataSorted = sorted(allData, reverse=True)
        print('dataSorted:', [str(e) for e in arrDataSorted])
        for i in allData:
            oMaxHeap.add(i)
        heapData = []    
        for i in range(iLen):
            iExpected = arrDataSorted[i]
            iActual = oMaxHeap.pop()
            heapData.append(iActual)
            print('{0}, expected: {1}, actual: {2}'.format(iExpected==iActual, iExpected, iActual))
            assert iExpected==iActual, ""
        print('dataSorted:', [str(e) for e in arrDataSorted])
        print('heapData:  ', [str(e) for e in heapData])

if __name__=="__main__":
    # testTupleValue()
    testClassValue()