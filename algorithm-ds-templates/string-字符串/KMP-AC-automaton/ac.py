

""" 
from https://oi-wiki.org/string/ac-automaton/
思路很清楚, 不过下面的实现有问题;
下面另一篇的实现比较简单 """
def v0():
    from collections import deque
    q = deque()

    N = 100000 # 节点最大数量
    tr = [[0] * 26 for i in range(0, N)]
    e = [0] * N # 该节点结束的单词数
    fail = [0] * N # fail 跳转边

    def insert(s):
        u = 0
        for char in s:
            c = ord(char) - ord('a')
            if tr[u][c] == 0: # 没有这个前缀, 创建新节点
                u = tr[u][c]
            u = tr[u][c]
            tr.append([0] * 26)
        e[u] += 1 # 尾为节点 u 的串的个数

    def build():
        for i in range(0, 26):
            if tr[0][i] == 1:
                q.append(tr[0][i])
        while len(q) > 0:
            u = q[0]
            q.popleft()
            for i in range(0, 26):
                if tr[u][i] == 1:
                    fail[tr[u][i]] = tr[fail[u]][i]
                    q.append(tr[u][i])
                else:
                    tr[u][i] = tr[fail[u]][i]

    def query(t):
        u, res = 0, 0
        i = 1
        while t[i] == False:
            u = tr[u][t[i] - ord('a')] # 转移
            j = u
            while j == True and e[j] != -1:
                res += e[j]
                e[j] = -1
                j = fail[j]
            i += 1
        return res

    dic = "anyway fantastic however".split()
    for pattern in dic:
        insert(pattern)
    build()
    print(query("anyway, just fantastic"))


""" 
from [地铁十分钟 | AC自动机](https://zhuanlan.zhihu.com/p/146369212)
 """
import collections

class node:
    def __init__(self, value) -> None:
        self.value = value # 当前字符
        self.childvalue = []
        self.child = []
        self.fail = None # 指针
        self.tail = 0 # 节点的表示

class AC:
    def __init__(self) -> None:
        self.root = node("")
        self.count = 0

    def insert(self, strkey):
        self.count += 1
        p = self.root
        for i in strkey:
            if i not in p.childvalue:
                child = node(i)
                p.child.append(child)
                p.childvalue.append(i)
                p = child
            else:
                p = p.child[p.childvalue.index(i)]
        # p.tail = self.count
        p.tail = strkey
    
    def build_fail(self):
        queue = [self.root]
        while len(queue) > 0:
            tmp = queue.pop(0)
            for i in tmp.child:
                if tmp == self.root:
                    i.fail = self.root
                else:
                    p = tmp.fail
                    while p != None:
                        if i.value in p.childvalue:
                            i.fail = p.child[p.childvalue.index(i.value)]
                            break
                        p = p.fail
                    if p == None:
                        i.fail = self.root
                queue.append(i)
    
    def query(self, strkey):
        p = self.root
        result = collections.defaultdict(int)

        for i in strkey:
            while i not in p.childvalue and p != self.root:
                p = p.fail
            if i in p.childvalue:
                p = p.child[p.childvalue.index(i)]
            else:
                p = self.root
            tmp = p
            while tmp != self.root:
                if tmp.tail != 0:
                    result[tmp.tail] += 1
                    # return tmp.tail
                tmp = tmp.fail
        return result

def test():
    ac = AC()
    dic = "aa bb cc".split()
    for pattern in dic:
        ac.insert(pattern)
    ac.build_fail()
    querys = [
        "aa bb cc",
        "aaaabbccc",
        ""
    ]
    for query in querys:
        print(ac.query(query))
test()