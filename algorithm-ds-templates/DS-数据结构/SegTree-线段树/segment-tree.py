from easonsi.util.leetcode import *

""" 线段树
[单点更新, 区间查询, 就可以考虑线段树]
https://oi-wiki.org/ds/seg/
[wiki](https://zh.wikipedia.org/wiki/%E7%B7%9A%E6%AE%B5%E6%A8%B9)
[zero 如何学习可以解决本题的算法与数据结构](https://leetcode.cn/problems/count-of-range-sum/solution/xian-ren-zhi-lu-ru-he-xue-xi-ke-yi-jie-jue-ben-ti-/)
- 灵神 [301](https://www.bilibili.com/video/BV1it4y1L7kL); [D79](https://www.bilibili.com/video/BV18t4y1p736)
[D98](https://www.bilibili.com/video/BV15D4y1G7ms/)


基本思想: 通过更多的空间来存储区间信息(区间长度以二进制增长), 从而对于一个查询, 可以快速分解为多个子查询.
核心: 将一个区间查询切分到子区间上. 这里的切分方式是固定的, 例如当前节点o管辖 [l,r] 区间, 则o的两个子节点分别管辖 `[l,m], [m+1,r]`, 其中 `m = (l+r)//2`. 
    为什么要开 4n 的数组? 假设是满二叉树, 则节点数量为 2n; 但这是在n个数字正好可以被划分的情况下的; 如果不能被划分则需要更多的多余节点, 但最多不会超过 4n!
    对于第o个节点, 其子节点的位置是 2*o, 2*o+1; 显然这里要求o的计数从1开始. 因此, 线段树一般的查询都是 `f(1, n,1, args)` 的形式, 第1个节点管辖 [1,n] 整个区间.
函数写法: `f(o,l,r, args)` 这里的o是当前管辖 [l,r] 的节点, 后面的 args可以是 对idx位置元素增加value, 也可以是统计 [left, right] 区间内的元素个数等.

两大思想
1. 挑选 O(n) 个 **特殊区间**, 使得任意区间可以拆分成 O(logn) 个特殊区间
    O(n) <= 4n
2. lazy/延迟 更新
    lazy tag: 用一个数组维护每个区间需要更新的值. 
    如果==0, 表示不需要更新; 如果!=0, 表示更新操作在这个区间停住了 (不递归)
    如果又来了一个区间更新破坏了 lazy tag 区间, 则需要递归的更新子区间, 并且更新 lazy tag.


TODO: https://leetcode.cn/problems/count-of-range-sum/solution/by-ac_oier-b36o/

0327. 区间和的个数 #hard #题型 #线段树
    给定一个数组, 要求其所有的子区间中, 区间和在 [lower, upper] 范围内的数量


2407. 最长递增子序列 II #hard #题型 对于给定的数组, 找到其中最长的严格递增子序列, 要求相邻元素差值不超过 k. 限制: n 1e5; k 1e5
    思路1: 建立 {val: LIS} 的字典记录以val结尾的LIS 长度. 遍历过程中, 对于val, 在 [val-k,val] 范围内查询最大值.

0729. 我的日程安排表 I #medium
    给定一组左开右闭的区间表示课程. 对于一个课程序列, 依次判断是否会与之前的产生冲突 (不冲突的就加入课程集合).
0731. 我的日程安排表 II
    相较于 0729, 这里的限制是三个课程不能同时进行, 也即重叠时间不能超过2.

1964. 找出到每个位置为止最长的有效障碍赛跑路线 #hard #DP
    问题定义: 给定一个序列, 对于其中的每一个值, 计算以其结尾的递增序列的最大长度
    实际上可以用更为简单的思路; 但是线段树也能做, 注意代码书写.

2213. 由单个字符重复的最长子字符串 #hard #线段树
    给定一个长n的字符串, 每次操作中, 对某一位置的元素修改为另一字符, 问每次操作后字符串中有的最长重复子字符串的长度.
    思路1: 利用线段树来记录每一个区间中, pre,suf,mx 的连续最大长度. 
    关联: [洛谷 P4513 小白逛公园](https://leetcode.cn/link/?target=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP4513) 就是线段路记录动态更新的区间最大值.

"""


def testClass(inputs):
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res


class SegTree_0():
    """ 改写自 0327 题官答.
    这里新定义了一个 struct 包括了其所管辖的 l,r 位置, 实际上可以通过参数的形式传入, 这样可以提升性能, 参见 SegTree """
    class Node():
        def __init__(self) -> None:
            """ 线段树节点, 记录了 [l,r] 区间内的数字数量为 val """
            self.val = 0
            self.l = None
            self.r = None
    
    def __init__(self, n) -> None:
        self.t = [self.Node() for _ in range(n)]
    
    def build(self, o, l,r):
        """ 递归建树 """
        self.t[o].l = l
        self.t[o].r = r
        if l==r: return
        m = (l+r)//2
        self.build(2*o, l, m)
        self.build(2*o+1, m+1, r)
    
    def inc(self, o, i):
        """ 递归对于第i个元素 +1, o为当前访问的节点 """
        if self.t[o].l==self.t[o].r:
            self.t[o].val += 1
            return
        if i <= (self.t[o].l + self.t[o].r)//2:
            self.inc(2*o, i)
        else:
            self.inc(2*o+1, i)
        self.t[o].val = self.t[2*o].val + self.t[2*o+1].val
    
    def query(self, o, l,r):
        """ 查询 [l,r] 范围内的元素个数 """
        if l<=self.t[o].l and r>=self.t[o].r: return self.t[o].val
        m = (self.t[o].l+self.t[o].r)//2
        if r <= m: return self.query(2*o, l, r)
        if l >= m+1: return self.query(2*o+1, l, r)
        return self.query(2*o, l, m) + self.query(2*o+1, m+1, r)

class SegTree:
    """ 
    更为简洁的线段树实现, 可以查询在 [left, right] 区间元素个数
    调用的时候需要输入 o,l,r, 即当前的位置 o 的节点及其所管辖的区间 [l,r]. 一般而言, 对于一个总长度为 n的线段树而言, 调用形式都是 (1,1,n), 也即从根节点出发, 其所管辖的范围为 [1,n]
    from [灵神](https://leetcode.cn/problems/booking-concert-tickets-in-groups/solution/by-endlesscheng-okcu/)
    """
    def __init__(self, n) -> None:
        self.t = [0] * 4 * n
    def inc(self, o,l,r, i, val=1):
        """ 对于i位置元素加val """
        if l==r:
            self.t[o] += val
            return
        m = (l+r)>>1
        if m>=i: self.inc(2*o, l, m, i, val)
        else: self.inc(2*o+1, m+1, r, i, val)
        self.t[o] = self.t[2*o] + self.t[2*o+1]
        
    def query(self, o,l,r, left, right):
        """ 查询 [left, right] 区间内的元素个数
        注意, 在递归过程中不需要考虑修改查询区间 [left, right] """
        if l>=left and r<=right: return self.t[o]
        m = (l+r)>>1
        sum = 0
        if m>=left: sum += self.query(2*o, l, m, left, right)
        if m+1<=right: sum += self.query(2*o+1, m+1, r, left, right)
        return sum

class Template():
    def template(self, ):
        def build(o:int, l,r) -> None:
            if l==r:
                # ...
                return 
            m = (l+r)//2
            build(o*2, l,m)
            build(o*2+1, m+1,r)
            # 维护...
        def update(o:int, l,r, L,R) -> None:
            if L<=l and r<=R:
                # 更新...
                return 
            m = (l+r)//2
            if m>=L: update(o*2, l,m, L,R)
            if m<R: update(o*2+1, m+1,r, L,R)
            # 维护...

class Solution:
    """ 6358. 更新数组后处理求和查询 #hard 题目比较复杂, 总结就是, 对于一个0/1序列, 需要实现一个函数完成 [l,r] 范围的反转操作, 并实现求和操作
限制: n 1e5; 操作次数 q 1e5
思路1: Python 直接暴力转为二进制数可以过?! 
    是一个非常大的数字
思路2: #线段树 #模版题 #题型 见 [segment-tree]
    复杂度: O(n + q logn)
[灵神](https://leetcode.cn/problems/handling-sum-queries-after-update/solution/xian-duan-shu-by-endlesscheng-vx80/)
"""
    def handleQuery(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        # 思路2: #线段树 #模版题 #题型 见 [segment-tree]
        n = len(nums1)
        cnt1 = [0] * (4 * n)        # 维护的特殊区间; 注意从1开始
        flip = [False] * (4 * n)

        def maintain(o: int) -> None:
            # 维护cnt区间, 在 build, update 时调用
            cnt1[o] = cnt1[o * 2] + cnt1[o * 2 + 1]

        def do(o: int, l: int, r: int) -> None:
            # 执行反转操作; lazy
            cnt1[o] = r - l + 1 - cnt1[o]
            flip[o] = not flip[o]

        # 初始化线段树   o,l,r=1,1,n
        def build(o: int, l: int, r: int) -> None:
            if l == r:
                cnt1[o] = nums1[l - 1]  # 注意下标从1开始
                return
            m = (l + r) // 2
            build(o * 2, l, m)
            build(o * 2 + 1, m + 1, r)
            maintain(o)

        # 反转区间 [L,R]   o,l,r=1,1,n
        def update(o: int, l: int, r: int, L: int, R: int) -> None:
            if L <= l and r <= R:
                do(o, l, r) # [l,r] 被完整包含, lazy
                return
            m = (l + r) // 2
            # lazy标记下传
            if flip[o]:
                do(o * 2, l, m)
                do(o * 2 + 1, m + 1, r)
                flip[o] = False
            if m >= L: update(o * 2, l, m, L, R)
            if m < R: update(o * 2 + 1, m + 1, r, L, R)
            maintain(o)     # 维护区间

        build(1, 1, n)
        ans, s = [], sum(nums2)
        for op, l, r in queries:
            if op == 1: update(1, 1, n, l + 1, r + 1)   # 注意idx转换
            elif op == 2: s += l * cnt1[1]
            else: ans.append(s)
        return ans


    """ 0327. 区间和的个数 #hard #题型 #线段树
给定一个数组, 要求其所有的子区间中, 区间和在 [lower, upper] 范围内的数量
限制: 数组长度 1e5, 元素大小 32bit
see [官答](https://leetcode.cn/problems/count-of-range-sum/solution/qu-jian-he-de-ge-shu-by-leetcode-solution/)
提示: 我们从小到大遍历j, 要使得 `sum[i...j] = acc[j]-acc[i-1]` 在 [lower, upper] 范围内, 需要 acc[i-1] 在 `[acc[j]-upper, acc[j]-lower]` 范围内. 
    因此需要一个DS能够插入数据, 并查询在某一范围内的元素数量. (偷懒的话可以直接调用 SortedList)
思路0: 归并排序
思路1: #线段树
    求在一个范围内的数字有多少, 显然可以用 #线段树 来做.
    另外, 本题的数字上限很大, 需要将其转为连续整数 (#离散化), 也即, 将线段树中所有出现过的数字 (包括需要查询的 left, right) 变为 0~n-1 的连续整数.
思路2: 动态增加节点的线段树
思路3: 树状数组
思路4: 平衡二叉搜索树

"""
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        """ 思路1 线段树
        改成了 Python版本, 下面的 SegTree_0 居然超时了, 重新实现了 SegTree 过"""
        # 利用哈希表将所有可能出现的整数，映射到连续的整数区间内
        preSum = list(accumulate(nums, initial=0)) 
        allNums = set(preSum)
        allNums = allNums.union(set(i-lower for i in allNums)).union(set(i-upper for i in allNums))
        allNums = sorted(list(allNums))
        kth = {j:i+1 for i,j in enumerate(allNums)}
        
        # t = SegTree(len(allNums) * 4)
        # t.build(1, 1, len(kth))
        # t.inc(1, kth[0])        # 将0映射后的值加入到线段树中 (因为假如单个数字符合要求, 也OK)
        # ans = 0
        # for s in preSum[1:]:
        #     left, right = kth[s-upper], kth[s-lower]
        #     ans += t.query(1, left, right)
        #     t.inc(1, kth[s])
        # return ans
        
        n = len(allNums)
        t = SegTree(n)      # 内部生成 4*n 的数组记录
        t.inc(1, 1, n, kth[0])
        ans = 0
        for s in preSum[1:]:
            left, right = kth[s-upper], kth[s-lower]
            ans += t.query(1, 1, n, left, right)
            t.inc(1,1,n, kth[s])
        return ans


    """ 6206. 最长递增子序列 II #hard #题型 对于给定的数组, 找到其中最长的严格递增子序列, 要求相邻元素差值不超过 k.
限制: n 1e5; k 1e5
思路1: 建立 {val: LIS} 的字典记录以val结尾的LIS 长度. 遍历过程中, 对于val, 在 [val-k,val] 范围内查询最大值.
    考虑到数据范围, 可以采用 #线段树.
    技巧: 由于我们线段树的定义从节点1开始, 下面注释部分要避免出现区间非法! 为此, 我们可以将数字整体shift一下.
拓展: 若本题的数据范围在 1e9, 则需要采用 #动态开点线段树. 
参见 [灵神](https://leetcode.cn/problems/longest-increasing-subsequence-ii/solution/zhi-yu-xian-duan-shu-pythonjavacgo-by-en-p1gz/)
"""
    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        # 思路1: 线段树. 注意下面因为「线段树从1开始」导致的边界情况.
        # 线段树框架
        # u = max(nums)
        u = max(nums) + 1  # 对于num进行shift, 从而避免下面注释部分的判断.
        mx = [0] * (u*4)
        def modify(o,l,r,i,val):
            # 修改 a[i] = val
            if l==r: mx[o]=val; return
            m = (l+r)//2
            if i<=m: modify(o*2,l,m,i,val)
            else: modify(o*2+1,m+1,r,i,val)
            mx[o] = max(mx[o*2], mx[o*2+1])
        def query(o,l,r,L,R):
            # 查询 max(a[L:R+1])
            if L<=l and r<=R: return mx[o]
            res = 0
            m = (l+r)//2
            if L<=m: res = query(o*2,l,m,L,R)
            if R>m: res = max(res, query(o*2+1,m+1,r,L,R))
            return res
        
        # for x in nums:
        #     # 注意, 线段树从 1 开始!!!
        #     if x==1: 
        #         modify(1,1,u,1,1)       # 都是正数, 次数长度一定为1
        #     else: 
        #         res = 1 + query(1,1,u,max(1,x-k),x-1)     # 这里的 x-1 应该 >= 1
        #         modify(1,1,u,x,res)
        for x in nums:
            x += 1
            res = 1 + query(1,1,u,max(1,x-k),x-1)
            modify(1,1,u,x,res)
        return mx[1] # 对于线段树, 最大值就是根节点.
    

    """ 1964. 找出到每个位置为止最长的有效障碍赛跑路线 #hard #DP
问题定义: 给定一个序列, 对于其中的每一个值, 计算以其结尾的递增序列的最大长度
思路1: #线段树
    我们用一个哈希表记录num结尾的递增序列的最大长度
    这样, 对于每一个元素, 我们需要查询「小于等于当前元素的数字中, 长度最大的那一个」. 因此可以用线段树来解决
思路2: #DP
    基本和 0300 「最长递增子序列」完全一致.
    核心是: dp[i] 记录长度为 i+1 的序列中, 结尾元素的最小值
"""
    def longestObstacleCourseAtEachPosition(self, obstacles: List[int]) -> List[int]:
        # 注意不能简单用单调栈: 例如 `[5,1,5,5,1,3,4,5,1,4]` 的最后一个值应该是 5 ([1,1,3,4,4]), 而单调栈因为要保证倒数第二个1, 会得到 4
        
        n = len(obstacles)
        # 离散化
        nums = list(set(obstacles))
        nums.sort()
        num2idx = {v:i+1 for i,v in enumerate(nums)}
        obstacles = [num2idx[v] for v in obstacles]
        
        """ 定义线段树, 注意长度为所有数字(离散化之后)的数量 *4
        这里的 seg 为统计每个数字结尾的递增序列的最大长度的哈希表
        segMax 为统计每个数字结尾的递增序列的最大长度的线段树 """
        ll = len(num2idx)
        seg = defaultdict(int)
        segMax = [0] * 4*ll
        def update(idx, val, o=1, l=1,r=ll):
            if l==r:
                seg[idx] = max(seg[idx], val)
                segMax[o] = seg[idx]
                return
            m = (l+r)//2
            if m >= idx: update(idx, val, 2*o, l, m)
            else: update(idx, val, 2*o+1, m+1, r)
            # seg[o] = seg[2*o] + seg[2*o+1]
            segMax[o] = max(segMax[2*o], segMax[2*o+1])
        def query(L, R, o=1, l=1, r=ll):
            # 查询区间 [L, R] 的最大值
            if L <= l and r <= R: return segMax[o]
            # from Coplit 居然如此简洁
            if R < l or r < L: return 0
            return max(query(L, R, 2*o, l, (l+r)//2), query(L, R, 2*o+1, (l+r)//2+1, r))
            # m = (l+r)//2
            # ans = 0
            # if m>=L: ans = max(ans, query(L, R, 2*o, l, m))
            # if m+1<=R: ans = max(ans, query(L, R, 2*o+1, m+1, r))
            # return ans
        
        ans = [0] * n
        for i,height in enumerate(obstacles):
            # 注意这里的查询更新逻辑: 每次查询height一下的最长递增序列; 然后+1, 并进行更新
            hisHeight = query(1, height)
            ans[i] = hisHeight + 1
            update(height, hisHeight+1)
        return ans

    """ 2213. 由单个字符重复的最长子字符串 #hard #线段树
给定一个长n的字符串, 每次操作中, 对某一位置的元素修改为另一字符, 问每次操作后字符串中有的最长重复子字符串的长度.
限制: n 12e5, 操作次数 k 1e5
思路1: 采用 #线段树 维护「pre, suf, mx」表示前缀/后缀 和 区间内的最长连续字符数量.
    如何初始化? 假设递归函数 `build(o: int, l: int, r: int)` 初始化 [l,r] 区间. 1) 边界: l==r; 2) 当处理好两个子区间后, 用一个 `maintain(o: int, l: int, r: int)` 为更新父区间o的属性.
    如何实现更新操作? 假设 `update(o: int, l: int, r: int, i: int)` 将i个字符进行替换. 1) 边界: l==r; 2) 当处理好两个子区间后, 同样需要用一个 `maintain(o: int, l: int, r: int)` 为更新父区间o的属性 —— 复用上面的那个函数.
[灵神](https://leetcode.cn/problems/longest-substring-of-one-repeating-character/solution/by-endlesscheng-qpbw/)
"""
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        s = list(s)
        n = len(s)
        # 距离 [l,r] 区间的最大连续前缀/后缀/最大连续字符数量
        pre, suf, mx = [0]*(4*n), [0]*(4*n), [0]*(4*n)
        def build(o,l,r):
            # 构建线段树过程
            if l==r:        # 边界
                pre[o] = suf[o] = mx[o] = 1
                return
            m = (l+r)//2    # 分治
            build(o*2,l,m)
            build(o*2+1,m+1,r)
            # 更新o节点自身
            maintain(o,l,r)
        def update(o,l,r, i):
            # 更新第i个字符
            if l==r:        # 边界
                # pre[o] = suf[o] = mx[o] = 1 # 本来就是1
                return
            m = (l+r)//2
            # 更新包含i的那个子区间
            if i<=m: update(o*2,l,m,i)
            else: update(o*2+1,m+1,r,i)
            # 更新o节点自身
            maintain(o,l,r)
        def maintain(o,l,r):
            # 两子节点属性已正确, 更新o节点的属性
            # init
            pre[o] = pre[o*2]; suf[o] = suf[o*2+1]
            mx[o] = max(mx[o*2],mx[o*2+1])
            # 
            m = (l+r)//2
            # if s[m]==s[m+1]:    # 只有当中间的两个字符相同的时候, 才会被更新.
            # 注意字符串位置从 0开始
            if s[m-1]==s[m]:
                mx[o] = max(mx[o], suf[o*2]+pre[o*2+1])
                if pre[o*2]==m-l+1: pre[o] += pre[o*2+1]
                if suf[o*2+1]==r-m: suf[o] += suf[o*2]
        build(1,1,n)
        ans = []
        for c,i in zip(queryCharacters, queryIndices):
            s[i] = c
            update(1,1,n,i+1)   # 始终需要注意idx差距1
            ans.append(mx[1])
        return ans




""" 0729. 我的日程安排表 I #medium
给定一组左开右闭的区间表示课程. 对于一个课程序列, 依次判断是否会与之前的产生冲突 (不冲突的就加入课程集合).
思路1: 维护一个有序的列表, 二分判断当前课程是否会与之前的冲突.
    时间复杂度: 由于插入操作, 复杂度为 O(n^2).
    [官答](https://leetcode.cn/problems/my-calendar-i/solution/wo-de-ri-cheng-an-pai-biao-i-by-leetcode/) 解法1就是暴力 O(n^2).
    Python 可以用 SortedList, 在对数时间实现插入 (应该是平衡树?), 见思路2.
思路2: #平衡树
    官答还用了二叉树来存储时序关系的课程, 但最坏情况还是 O(n^2). 在JAVA中直接调用 `TreeMap `, 而Python手写一个平衡树超纲了.

"""
class MyCalendar:
    # 维护有序列表, 直接调包
    def __init__(self):
        from sortedcontainers import SortedList
        self.cal = SortedList()

    def book(self, start: int, end: int) -> bool:
        idx = self.cal.bisect_right((start, end))
        if idx>0 and self.cal[idx-1][1]>start: return False
        if idx<len(self.cal) and self.cal[idx][0]<end: return False
        self.cal.add((start, end))
        return True

""" 0731. 我的日程安排表 II
相较于 0729, 这里的限制是三个课程不能同时进行, 也即重叠时间不能超过2.
注意判断两个区间是否有交集的方法: 对于 [start, end] 和 [i,j] 两个区间, 它们存在交集的条件为 `start<j and end>i`.
思路1: 暴力法
    用两个数组分别存储已有的课程和重复的时间片段. 暴力遍历
    [here](https://leetcode.cn/problems/my-calendar-ii/solution/wo-de-ri-cheng-an-pai-biao-ii-by-leetcode/)
"""

class MyCalendarTwo:
    """ 思路1: 用两个数组分别存储已有的课程和重复的时间片段. 暴力遍历
    [here](https://leetcode.cn/problems/my-calendar-ii/solution/wo-de-ri-cheng-an-pai-biao-ii-by-leetcode/) """
    def __init__(self):
        # from sortedcontainers import SortedList
        self.cal = []
        self.dupCal = []

    def book(self, start: int, end: int) -> bool:
        # 检查是否有三重重复
        for i,j in self.dupCal:
            if start<j and end>i: return False
        # 检查是否与已有课程重复.
        for i,j in self.cal:
            if start<j and end>i: self.dupCal.append((max(start,i), min(end,j)))
        self.cal.append((start, end))
        return True


sol = Solution()
result = [
#     testClass("""["MyCalendar", "book", "book", "book"]
# [[], [10, 20], [15, 25], [20, 30]]"""),
#     testClass("""["MyCalendar","book","book","book","book","book","book","book","book","book","book"]
# [[],[48,50],[0,6],[6,13],[8,13],[15,23],[49,50],[45,50],[29,34],[3,12],[38,44]]"""),

    # sol.countRangeSum(nums = [-2,5,-1], lower = -2, upper = 2),
    # sol.countRangeSum([-3,1,2,-2,2,-1],-3,-1),
    sol.longestRepeating(s = "babacc", queryCharacters = "bcb", queryIndices = [1,3,3]),
    sol.longestRepeating(s = "abyzz", queryCharacters = "aa", queryIndices = [2,1]),
]
for r in result:
    print(r)
