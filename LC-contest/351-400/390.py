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
https://leetcode.cn/contest/weekly-contest-390
https://leetcode.cn/circle/discuss/XFODhH/


Easonsi @2023 """
class Solution:
    """ 3090. 每个字符最多出现两次的最长子字符串 """
    def maximumLengthSubstring(self, s: str) -> int:
        cnt = Counter()
        l = 0; ans = 2
        for r,c in enumerate(s):
            cnt[c] += 1
            while cnt[c] > 2:
                cnt[s[l]] -= 1
                l += 1
            ans = max(ans, r-l+1)
        return ans
    
    """ 3091. 执行操作使数据元素之和大于等于 K. 原本只有 [1], 可选择操作 1] 元素 +1, 2] 选择某一个元素, 复制添加在最后 
限制: k 1e5
思路1: #贪心
    观察 k=11 的时候, 操作为 1 -> 1+3=4 -> 4*3=12
    显然, 执行步骤1直到变为 sqrt{k} 然后执行步骤二
    """
    def minOperations(self, k: int) -> int:
        target = ceil(sqrt(k))
        time_mul = ceil(k/target)
        return target + time_mul - 2

    """ 3092. 最高频率的 ID #medium 每次增加/减少 (f,x) 个元素, 问每个步骤操作后出现频次最高值 
限制: n, m 1e5
思路1: 需要维护「可以删除、添加元素」的有序数据结构, 这里方面直接用了 SortedList
思路2: 如何用 #懒删除堆 ?
    可以将key一起存进去! 然后取出的时候检查堆顶元素是否还成立! 也即堆内元素 (-cnt[x], x)
    [ling](https://leetcode.cn/problems/most-frequent-ids/solutions/2704858/ha-xi-biao-you-xu-ji-he-pythonjavacgo-by-7brw/)
    """
    def mostFrequentIDs(self, nums: List[int], freq: List[int]) -> List[int]:
        from sortedcontainers import SortedList
        sl = SortedList()
        cnt = Counter()
        ans = []
        for x,f in zip(nums, freq):
            if cnt[x]:      # for the first time
                sl.remove(cnt[x])
            cnt[x] += f
            sl.add(cnt[x])
            ans.append(sl[-1] if sl else 0)
        return ans
    
    """ 3093. 最长公共后缀查询 #hard 对于每次q, 返回数组中和它有最长公共后缀的字符串. 若相同, 返回长度最短的. 再相同, 返回idx更小的. 
限制: q, n 1e4. 所有字符串的长度之和 5e5
思路1: #字典树
    如何简化代码? 可以在插入的时候直接更新最小idx!
    参见 [ling](https://leetcode.cn/problems/longest-common-suffix-queries/solutions/2704763/zi-dian-shu-wei-hu-zui-duan-chang-du-he-r3h3j/)
        还有讨论中的 [小羊]
    """
    def stringIndices(self, wordsContainer: List[str], wordsQuery: List[str]) -> List[int]:
        lens = [len(w) for w in wordsContainer]
        class Node():
            def __init__(self):
                self.children = {}
                self.idx = -1
                self.mnIdx = -1
        root = Node()
        def insert(word, idx):
            node = root
            for c in word[::-1]:
                if c not in node.children:
                    node.children[c] = Node()
                node = node.children[c]
            if node.idx == -1:
                node.idx = idx
        for idx, word in enumerate(wordsContainer):
            insert(word, idx)
        def build(node) -> [int,int]:
            mnIdx, l = inf, inf
            for c, child in node.children.items():
                mnIdx_, len_ = build(child)
                if len_ < l or (len_ == l and mnIdx_ < mnIdx):
                    mnIdx, l = mnIdx_, len_
            if node.idx != -1:
                mnIdx, l = node.idx, lens[node.idx]
            node.mnIdx = mnIdx
            return node.mnIdx, l
        build(root)
        def query(word):
            node = root
            for c in word[::-1]:
                if c not in node.children:
                    return node.mnIdx
                node = node.children[c]
            return node.mnIdx
        ans = []
        for q in wordsQuery:
            ans.append(query(q))
        return ans

    
sol = Solution()
result = [
    # sol.maximumLengthSubstring(s = "bcbbbcba"),
    # sol.minOperations(11),
    # sol.mostFrequentIDs(nums = [5,5,3], freq = [2,-2,1]),
    sol.stringIndices(wordsContainer = ["abcd","bcd","xbcd"], wordsQuery = ["cd","bcd","xyz"]),
    sol.stringIndices(wordsContainer = ["abcdefgh","poiuygh","ghghgh"], wordsQuery = ["gh","acbfgh","acbfegh"]),
]
for r in result:
    print(r)
