# LeetCode 刷题记录


有时间重新刷一遍! 整理一下

### DP

[编辑距离](https://github.com/labuladong/fucking-algorithm/blob/master/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%E7%B3%BB%E5%88%97/%E7%BC%96%E8%BE%91%E8%B7%9D%E7%A6%BB.md) 显然用动态规划，若是要求出如何进行的编辑，则需要记录每一次转移的来源；DP 表的每一个元素可以是一个设计好的数据结构。

[排课问题](https://blog.csdn.net/GentleCP/article/details/103095884) DP+贪心

### 其他

[今日头条2017校招题目解析(一)：KMP中next数组与Trie树的应用](https://segmentfault.com/a/1190000014466075)
[面经 | 字节跳动实习算法岗（2019届）](https://zhuanlan.zhihu.com/p/86746425)
[字节跳动数据挖掘算法工程师一面（记录）](https://blog.csdn.net/jianminli2/article/details/103585066)




### 023 合并 K 个升序链表

```python
给你一个链表数组，每个链表都已经按升序排列。
请你将所有链表合并到一个升序链表中，返回合并后的链表。

输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
  1->4->5,
  1->3->4,
  2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6

输入：lists = []
输出：[]
```

【思路 1】「分治」思想，将 k 个链表合并的问题递归转化为两链表合并问题
【思路 2】采用 PriorityQueue 的结构保存节点，参见 <https://docs.python.org/3/library/heapq.html>；需要注意的是，在 `heapq` 中的元素是要能比较大小的（C++中能重载运算符就很强），所以这里记录的是 (node.val, index) ，其中 val 作为排序的优先级，而 index 表示这个元素属于哪一条链表。

#### 021 两个有序链表合并

在第一种思路中需要实现两个有序链表的合并（见👇），在 021 题中我用的循环条件是 `while l1 or l2`，这样的话在循环中的判断条件会比较复杂，而这里参考标答换成了 `while l1 and l2`，最后只会剩下 l1 或 l2 的剩余部分，或两者都为空，直接将维护的`now` 指针指向它就行了。虽然只是一个小细节，但这样写代码逻辑清楚很多。

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def printList(self):
        res = [self.val]
        now = self
        while now.next:
            now = now.next
            res.append(now.val)
        print(res)

def genNode(l):
    root = ListNode(val=l[0])
    pre = root
    for num in l[1:]:
        now = ListNode(val=num)
        pre.next = now
        pre = now
    return root


class Solution:
    # def mergeKLists(self, lists: List[ListNode]) -> ListNode:
    """
    思路一：「分治」思想，将 k 个链表合并的问题递归转化为两链表合并问题
    """
    def mergeKLists(self, lists):
        # 两个链表合并函数
        def merge2(l1, l2):
            head_pre = ListNode()   # 虚头部
            now = head_pre
            while l1 and l2:
                if l1.val < l2.val:
                    now.next = l1
                    l1 = l1.next
                else:
                    now.next = l2
                    l2 = l2.next
                now = now.next
            l = l1 if l1 else l2
            now.next = l
            return head_pre.next

        def mergeKgen(lists):
            if len(lists)==0:
                return None
            if len(lists)==1:
                return lists[0]
            k = len(lists)//2
            return merge2(mergeKgen(lists[:k]), mergeKgen(lists[k:]))

        return mergeKgen(lists)

    """
    思路二：维护一个 PriorityQueue
    """
    def mergeKLists2(self, lists):

        from heapq import heappush, heappop

        head_pre = ListNode()
        now = head_pre
        pq = []
        for i, l in enumerate(lists):
            if l:   # 可能有输入 [[]]
                heappush(pq, (l.val, i))        # 注意不能把 l 直接人进去，因为无法比较大小
        while pq:
            _, index = heappop(pq)
            l = lists[index]
            now.next = l
            now = now.next
            if l.next:
                lists[index] = l.next
                heappush(pq, (l.next.val, index))
        return head_pre.next

ls =  [[1,4,5],[1,3,4],[2,6]]
lists = [genNode(l) for l in ls]
res = Solution().mergeKLists2(lists)
res.printList()
```




### 029 两数相除

不使用乘除和 mod 运算，实现两任意整数的整除。
整数除法是 truncate 的，`truncate(-2.5) = -2`

【思路】首先考虑符号对于商数的影响：1. 两数异号则商为负（也就是决定了 👇 的`flag`）；2. 由于采用了 truncate 机制（也就是商向 0 取整），可将正数/负数的商数计算转化为两正数求商：例如 7/3=2...1, 7/(-3)=(-2)...1, (-7)/3=(-2)...(-1), (-7)/(-3)=2...(-1)。
综上，可划分成求商的符号，和计算两正数相除的商两步。

而在第二步中，若一直中被除数去减除数，相当于线性搜索，效率太低。
采用「反向二分查找」的方式，**每次将除数扩大一倍**（乘以 2 可由加法简单实现，或者是左移一位），来判断 dividend 中有多少个 2^k divisor。
另外注意到还需判断剩余部分有多少 divisor，因此要实现一个 `def div(dividend: int, divisor: int) -> int` 。
递归调用：返回结果为 `return count + div(dividend-divisor_2, divisor)`。
终止条件：`dividend < divisor`

```python
class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        # 脑回路清奇才会用加法吧……
        # if dividend<0:
        #     dividend, divisor = -dividend, -divisor
        # flag = 1
        # if divisor<0:
        #     divisor = -divisor
        #     flag = -1
        # res = 0
        # while dividend>=0:
        #     dividend -= divisor
        #     res += 1
        # return flag*(res-1)

        # 模拟 int32
        INT_MAX = 2147483647
        if dividend == -INT_MAX-1 and divisor==-1:
            return INT_MAX

        # 用 flag 表示结果正负，将两数均转化为正数
        if dividend<0:
            dividend, divisor = -dividend, -divisor
        flag = 1
        if divisor<0:
            divisor = -divisor
            flag = -1

        def div(dividend: int, divisor: int) -> int:
            if dividend < divisor:
                return 0
            count = 1
            divisor_2 = divisor # 倍增 divisor
            while dividend>divisor_2+divisor_2:
                # 从加法变为左移，运行时间从 52ms 降到 40ms
                # divisor_2 = divisor_2+divisor_2
                # count = count + count
                divisor_2 <<= 1
                count <<= 1
            return count + div(dividend-divisor_2, divisor)

        if flag>0:
            return div(dividend, divisor)
        else:
            return -div(dividend, divisor)
```

### 031 下一个排列 ***

```python
实现获取 下一个排列 的函数，算法需要将给定数字序列重新排列成字典序中下一个更大的排列。
如果不存在下一个更大的排列，则将数字重新排列成最小的排列（即升序排列）。
必须 原地 修改，只允许使用额外常数空间。

输入：nums = [1,2,3]
输出：[1,3,2]

输入：nums = [3,2,1]
输出：[1,2,3]

输入：nums = [1,1,5]
输出：[1,5,1]

输入：nums = [1]
输出：[1]
```

又是被标答折服的一次……但看了一遍之后感觉其实还行，关键是要理解这里的**数学原理**。
【思路】要看这里求解的目标有什么规律？以 [1, 2, 3] 为例，从小到大依次为：

```python
（1）[1 2 3]
（2）[1 3 2]
（3）[2 1 3]
（4）[2 3 1]
（5）[3 1 2]
（6）[3 2 1]
```

为了找到下一个排列，我们的思路是从右向左检索，看是否有两个指标可以**交换**，使得数组的字典序变大（或者若元素全部为 0-9 的数字，就是组成的数字更大）。「增大」需要满足的条件是：nums[left]<nums[right]，交换过后得到的排列是大于原排列。
但我们要得到的是大于原排列中最小的那一个，例如上面的（2）到（3），检索 [1 3 2] 之后发现左侧的 1 小于右侧的 2 于是先交换这两个元素，结果为 [2 3 1] ；交换之后，需要对 left 右侧的部分「排序」，得到最小的一个（也就是「next permutation」）。

下面的第一种自己的实现正是基于此。但还有一个重要的性质：**交换 left, right 后，[left+1:] 还是逆序的**！因此事实上不需要排序，而只要进行数组元素的逆序即可。

【感想】另外发现LeetCode 的运行时间只能大致参考，例如这里难点在于得到下一个排列，因此似乎没有涉及复杂情况。
（1）此题中，我一开始用 `is_reverse()` 来依次判断最后的 2,3,... 个元素是否逆序，整体上找到 left 相当于用了双重循环；但是其运行时间反而要比之后从数组尾部逆向找到第一个非逆序元素的改进算法更短。
（2）进一步将算法改进成标答 `nextPermutation2()` ，结果也没有明显改进。

```python
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        l = len(nums)
        def sort(start,end):
            # 对 nums[start:end] 实现原地排序
            for i in range(start, end):
                idx_min = i
                for j in range(i+1, end):
                    if nums[j]<nums[idx_min]:
                        idx_min = j
                if idx_min != i:
                    nums[i], nums[idx_min] = nums[idx_min], nums[i]
        # sort(0, len(nums))
        # print(nums)
        def is_reverse(start, end):
            # 判断 nums[start:end] 是否逆序
            for i in range(start, end-1):
                if nums[i]<nums[i+1]:
                    return False
            return True
        # print(is_reverse(1,3))

        # flag = False
        for i in range(l-2, -1, -1):
            if is_reverse(i, l):
                continue
            # 若不为逆序，找到 [i+1:] 最比 nums[i] 大的元素中最小的那一个，然后对 [i+1:] 排序
            idx = i+1
            for j in range(i+2, l):
                if nums[idx] > nums[j] > nums[i]:
                    idx = j

            nums[idx], nums[i] = nums[i], nums[idx]
            sort(i+1, l)
            return
        # 若未发生上述操作，说明已是最大的排列
        # if not flag:
        #     nums.sort()
        nums.sort()

    def nextPermutation2(self, nums: List[int]) -> None:
        l = len(nums)

        # 从后向前，找出第一个非逆序的元素
        i = l-2
        while i>=0 and nums[i]>=nums[i+1]:
            i -= 1
        """
        两种情况
        1. i>=0，此时需要在 [i+1:] 中找到大于 nums[i] 的元素中最小的那一个，设指标为 j；然后需要（1）交换 ij；（2）将 [i+1:] 逆序，此时设置 left=i+1
        2. i=-1，说明完全逆序（最大），下面的 left, right 指针为数组头尾，注意此时 left=i+1 仍满足
        """
        if i>=0: # 注意 [i+1:] 是逆序的
            j = i+1
            while j<l-1 and nums[i]<nums[j+1]:
                j += 1
            nums[j], nums[i] = nums[i], nums[j]

        # 然后需要对 [i+1:n] 部分进行所谓排序，但实际上这部分是降序的，所以进行一次反转即可
        left, right = i+1, l-1
        while left<right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
        return
```

### 032 最长有效括号 ***

```python
给你一个只包含 '(' 和 ')' 的字符串，找出最长有效（格式正确且连续）括号子串的长度。

输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"
```

【反思】这题写了三四个个小时吧，深夜思路混乱，而且在纠结的画图和混乱的代码中完全不能状态；说明刷 LeetCode 还是要找好状态。

#### 暴力查找

一开始的想法：若直接双重循环，内部循环判断最长可能序列，则复杂度为 O(n^2)。
是否要用 DP？其复杂度至少为二次方，似乎不如直接求解。

第二天写了下面这个暴力方案：果断超时了，断在一个长 15000 的序列上。

```python
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        if len(s) < 2:
            return 0
        n = len(s)
        f = lambda c: 1 if c=='(' else -1
        s_list = [f(c) for c in s]

        def next_left_parentthesis(start):
            # 从 start 开始找到第一个左括号
            # 若未找到则返回 n
            while start < n and s_list[start] == -1:
                start += 1
            return start

        def search_from_i(start):
            acc = 0
            best_len = 0
            i = start
            while i<n:
                acc += s_list[i]
                if acc == 0:
                    best_len = i-start+1
                if acc < 0:
                    return best_len
                i += 1
            return best_len

        left = next_left_parentthesis(0)
        longest = 0
        while left<n:
            longest = max(longest, search_from_i(left))
            left = next_left_parentthesis(left+1)
        return longest
```

#### 基于折线图模型

【反思】这是昨晚转的牛角尖：有效括号的条件是前序左括号数量大于右括号。因此，定义左右括号分别为 1 和 -1，则一个序列对应坐标系上的一个折线；而找最长有效序列，就是要找在坐标轴上方的最长序列。【是不是很像随机过程？】
要找到最长有效序列，就是从某一点出发（i,h），向右所有的点都在（i,j）所定义的坐标系上方，并且最后一个点与坐标轴相交，也即坐标为（j,h）。
基本思路就是这样，但由于左侧可能有多于的左括号（例如序列 `(((())`），一次从左到右的搜索可能会有遗漏。

【错误的】两次遍历的算法框架：

1. 从第一个值为 1 的点开始（left 指针），其高度为 h，向右遍历，直至遇到一个高度为 h-1 的点，就说明构成一次有效序列，记录；
    1. 若后一个节点为正（高度为 h），则继续遍历
    2. 否则后一个节点为负，此时前面的节点不可能构成比此次构成的子序列更长的有效序列。此时，从下一个为正的节点出发开始搜索（更新 left），也即转到第一行；
2. 当搜索一遍之后，可能最右侧点的高度要比 left 的高度高（height[left]<height[len(s)-1]）。此时 [left:len(s)] 之间还可能构成较长的有效序列
    1. 从 s 的末尾出发找到第一个 -1 节点（左括号），记作 right 指针，类似上面的第一次遍历进行一次从右向左的搜索。注意到由于 height[right]>height[left]，因此不会出现第一次遍历中的第二种情况。

👆算法错误之处在于，例如对于序列 12345432343，前序遍历无法删减，后续也只能找到右侧的一个峰。

【正确的思路】最后纠结了好几个小时的结果：

1. 初始化 start 为左侧起第一个左括号
2. 循环，当 start<len(nums)
    1. 记 start 的高度为 h，则 target=h-1；从左向右找到最远的高度为 target 的节点，其中不能低于 target，（若找到的话）记作 end
        1. 若找到了，注意 end 后一个点为右括号，因此从 start 到 end 的部分的最长有效序列至多为 end-start+1
        2. 若未找到，说明序列后面的点均 >=target，则从 start 开始的第一个右括号开始，寻找「最低点」，记作 p_deepest（若有多个 deepest，则为最右侧的那个）。则从 start 到 p_deepest 部分可构成一个有效序列，**并且 p_deepest 之后的点的高度均高于 deepest，因此无法与 p_deepest 前的符号匹配**。【注意到 p_deepest 后一个符号必为左括号，将其设置成新的 start，继续循环】

【复杂度】讲起来非常绕，但直接图示其实非常直观。每次找到从左括号出发的最长序列，并且能够保证这样找到的是这一段序列所能组合的最优解。
因此，最外层是一层循环遍历。其内部由于（1）需要找到是否有 end，一次遍历；（2）若没有的话要找最低点，一次遍历【下面算法中搞复杂了】，还是比较复杂。因此在复杂度最坏情况应该也在 O(n^2) 左右，但由于可能外层的遍历是「跳跃的」，因此效果要比暴力好上不少。【至少提交有结果了 hhh】

```python
        start = next_left_parentthesis(0)
        while start < n:
            target = heights[start] - 1
            # 假设 height[start]=1，则与其匹配的右括号高度为 0
            # 当若该点之后为 1，则还可能继续匹配
            """
            找到最远的高度为 target 的节点，其中不能低于 target
            """
            end = -1    # 表示未找到
            p = start+1
            while p<n:
                if heights[p]==target:
                    end = p
                elif heights[p]<target:
                    break
                p += 1

            if end!=-1:
                longest = max(end+1-start, longest)
                start = next_left_parentthesis(end)  # target 在循环头部更新
            else:
                # 说明没找到
                next_right = next_right_parentthesis(start + 1)
                if next_right == n:  # 没找到
                    return longest
                # 找其后的最低点
                deepest = min(heights[next_right:])
                p = n - 1
                while heights[p] != deepest:
                    p -= 1
                left_parentthesis = heights[start:].index(deepest) + start
                longest = max(p - left_parentthesis, longest)
                # start = next_left_parentthesis(p)
                start = p
        return longest
```

##### 找到最后一个某高度且其间高度均大于它的点

上述思路中的一个子问题也困扰良久：就是要找到序列中最后一个高度为 target，且其间所有点的高度均 >=target 的点。或者说，来连续变化情况下，找到第一个高度为 target-1 的点。
之前由于边界情况（未找到）等问题困扰，而最后发现其实很简单：
如下，`end` 初始化为 -1 表示未找到，而另外用一个指针 p 遍历，每找到一个高度为 target 的更新一次 end，而遇到 target-1 则停止。
这样 end=-1 则说明未找到。
【本质上似乎还是一个 flag，之前一个想不到太蠢了】

```python
end = -1  # 表示未找到
p = start + 1
while p < n:
    if heights[p] == target:
        end = p
    elif heights[p] < target:
        break
    p += 1
```

##### 两次遍历 ***

标答「思路 3」三次震惊我……

![-w521](media/16147360600817/16150105404456.jpg)

#### 利用栈 ***

> 通过栈，我们可以在遍历给定字符串的过程中去判断到目前为止扫描的子串的有效性，同时能得到最长有效括号的长度。
> 具体做法是我们始终保持栈底元素为当前已经遍历过的元素中「最后一个没有被匹配的右括号的下标」，这样的做法主要是考虑了边界条件的处理，栈里其他元素维护左括号的下标：

* 对于遇到的每个 ‘(’ ，我们将它的下标放入栈中
* 对于遇到的每个 ‘)’ ，我们先弹出栈顶元素表示匹配了当前右括号：
    * 如果栈为空，说明当前的右括号为没有被匹配的右括号，我们将其下标放入栈中来更新我们之前提到的「最后一个没有被匹配的右括号的下标」
    * 如果栈不为空，当前右括号的下标减去栈顶元素即为「以该右括号为结尾的最长有效括号的长度」

> 我们从前往后遍历字符串并更新答案即可。
> 需要注意的是，如果一开始栈为空，第一个字符为左括号的时候我们会将其放入栈中，这样就不满足提及的「最后一个没有被匹配的右括号的下标」，为了保持统一，我们在一开始的时候往栈中放入一个值为 -1−1 的元素。

拜服
【反思】之前 020 就用栈判断了是否为有效的括号序列，但之前想的是：入栈的都是左括号/右括号。现在回想起来，入栈的永远只有左括号，而**栈的高度恰好反映了左括号比右括号多多少**。另外没想到的是，与其只入栈没有意义的左括号符号，**栈的元素还可以用来记录该括号的位置信息**，也就是「通过栈，我们可以在遍历给定字符串的过程中去判断到目前为止扫描的子串的有效性，同时能得到最长有效括号的长度」。

```python
    def longestValidParentheses3(self, s: str) -> int:
        maxans = 0
        stack = [-1]    # 先入栈一个 -1
        for i, c in enumerate(s):
            if c == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    maxans = max(maxans, i-stack[-1])
        return maxans
```

#### DP算法

![-w516](media/16147360600817/16150104215412.jpg)

```python
    def longestValidParentheses4(self, s: str) -> int:
        dp = [0 for _ in range(len(s))]
        for i in range(1, len(s)):
            if s[i] == ')':
                if s[i-1] == '(':
                    dp[i] = (dp[i-2] if i>=2 else 0) + 2
                else:
                    if i-dp[i-1]>0 and s[i-dp[i-1]-1] == '(':
                        dp[i] = dp[i-1] + (dp[i - dp[i - 1] - 2] if i - dp[i - 1]>=2 else 0) + 2
        maxans = max(dp)
        return maxans
```

### 040 组合总和 2

#### 039 组合总和

```python
给定一个无重复元素的数组 candidates和一个目标数 target ，找出 candidates 中所有可以使数字和为 target的组合。
candidates 中的数字可以无限制重复被选取。

输入：candidates = [2,3,6,7], target = 7,
所求解集为：
[
  [7],
  [2,2,3]
]
```

【思路】DFS
这里的要求是可以重复使用数组中元素的，那么对于目前检索的 num，选取的数量 q 可以从 remainder//num 到 0 进行遍历，尝试加入并更新 remainder；然后递归检索。

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        combination = {}
        results = []

        def record():
            results.append([k for k, v in combination.items() for _ in range(v)])

        def backtrace(i, remains):
            if i == -1:
                return
            num = candidates[i]
            quiotient, _ = divmod(remains, num)

            for q in range(quiotient, -1, -1):
                new_remains = remains - q*num
                combination[num] = q
                if new_remains == 0:
                    record()
                else:
                    backtrace(i-1, new_remains)

        backtrace(len(candidates)-1, target)
        return results
```

#### 040

```python
输入: candidates = [10,1,2,7,6,1,5], target = 8,
所求解集为:
[
  [1, 7],
  [1, 2, 5],
  [2, 6],
  [1, 1, 6]
]
```

和上一题的区别是 candidates 中的数字可能重复，但只能用一次了。
也就是说每一个数字可能用到的次数有了上限。一开始想复杂了，但实际上只需要根据上一题的思路稍作改进：对于所检索的 num，选取的数量 q 从 min(remainder//num, count(num)) 到 0 进行遍历。

```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        from collections import Counter
        sorted_nums = sorted(Counter(candidates).items())
        # 记录了(num, count)元组

        combination = {}
        results = []

        def record():
            results.append([k for k, v in combination.items() for _ in range(v)])

        def backtrace(i, remains):
            if i == -1:
                return
            num, count = sorted_nums[i]
            quiotient, _ = divmod(remains, num)

            for q in range(min(quiotient, count), -1, -1):
                new_remains = remains - q * num
                combination[num] = q
                if new_remains == 0:
                    record()
                else:
                    backtrace(i - 1, new_remains)

        backtrace(len(sorted_nums) - 1, target)
        return results
```

### 041 缺失的第一个正数 ***

```python
给你一个未排序的整数数组 nums ，请你找出其中没有出现的最小的正整数。

输入：nums = [3,4,-1,1]
输出：2

输入：nums = [7,8,9,11,12]
输出：1
```

如果本题没有额外的时空复杂度要求，那么就很容易实现：

* 我们可以将数组所有的数放入哈希表，随后从 1 开始依次枚举正整数，并判断其是否在哈希表中；
* 我们可以从 1 开始依次枚举正整数，并遍历数组，判断其是否在数组中。

如果数组的长度为 N，那么第一种做法的时间复杂度为 O(N)，空间复杂度为 O(N)；第二种做法的时间复杂度为 O(N^2)，空间复杂度为 O(1)。但它们都不满足时间复杂度为 O(N)O(N) 且空间复杂度为 O(1)。

「真正」满足时间复杂度为 O(N) 且空间复杂度为 O(1) 的算法是不存在的，但是我们可以退而求其次：**利用给定数组中的空间来存储一些状态**。也就是说，如果题目给定的数组是不可修改的，那么就不存在满足时空复杂度要求的算法；但如果我们可以修改给定的数组，那么是存在满足要求的算法的。

【思路】注意这里核心是「利用给定数组中的空间来存储一些状态」。而这需要避免丢失所关心的信息。利用到的一点：由于数组长度为 n，要找到第一个缺失正数，只有数组中值为 [1,n] 的元素才是有意义的。

* 方案一：将所有出现在 [1,n] 范围内的数字「归位」，即 nums[i-1]=i；这样第二次遍历仅需顺序找到不满足此公式的数即可。主要需要处理的可能需要多次进行交换的情况，要避免死循环。
* 方案二：用负数存储信息，先将所有数变为正数，利用不在 [1,n] 范围内的正数表示无关信息。第二次循环中将数组中所有出现在范围内的数字所在坐标的数变为负数（因此要知道原本的数需要加 abs），这样就利用了原本的数组存放了需要的信息。

```python
class Solution:
    # 想法是将所有出现在 [1,n] 范围内的数字「归位」，即 nums[i-1]=i；这样第二次遍历仅需顺序找到不满足此公式的数即可。
    # 需要注意的是所更换的数字需要二次交换，即对于第 i 位的 nums[i]=num，其指向的元素 nums[num-1] 仍是在 [1,n]，则需继续交换。注意避免死循环，即若 nums[num-1]=num，则不需要进行交换
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)

        for i in range(n):
            # num = nums[i]
            # # 若是 i 位置的元素 num<=n，则要将其放到 num 位置上，也即交换；
            # # 若交换的数字 nums[num] 仍然 <= 且在另外一个位置上，需要继续交换
            # while 0<num<=n and num!=i+1:
            #     num_to_swep = nums[num-1]
            #     if num_to_swep != num-1:    # 避免循环
            #         nums[num-1], nums[i] = num, num_to_swep
            #         num = num_to_swep
            #     else:
            #         break

            # 简化成一行
            # 需要在（1）nums[i] 属于 [1,n] 范围内；（2）nums[i]与其指向位置的值不相等时进行交换。其中第二点是为了避免死循环。
            while 0<nums[i]<=n and nums[nums[i]-1] != nums[i]:
                nums[nums[i] - 1], nums[i] = nums[i], nums[nums[i]-1]
        i = 0
        while i<n:
            if nums[i] != i+1:
                break
            i += 1
        return i+1

    # 用负数表示元素存在；为此，先将所有不在 [1,n] 范围内的数变为 n+1（或其他正数）；
    # 第二次遍历，将在 [1,n] 范围内的数字所对应的列表元素变为负数；
    # 第三次，找到第一个非负的就是所求
    def firstMissingPositive2(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n):
            if nums[i] <= 0:
                nums[i] = n+1
        for i in range(n):
            if abs(nums[i]) <= n and nums[abs(nums[i])-1] > 0:
                nums[abs(nums[i]) - 1] *= -1
        for i in range(n):
            if nums[i] > 0:
                return i+1
        return n+1
```


### 053 最大子序列求和

```python
给定一个整数数组 nums，找出其中具有最大和的连续自数组，返回最大和

输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
```

#### 基于 DP

一开始想了乱七八糟的方式，结果走不通。
这种题型 DP 肯定是可解的，但一直没想到该如何设计。
或者说，如何简化问题，使得子问题的递归较为简单。
【核心思路】dp 记录「以 i 元素结尾的最大和」，然后返回 max(dp) 即可。
相应的，更新公式：`dp[i] = max(dp[i-1]+nums[i], nums[i])`，DP 的精髓即在此。

```python
class Solution:
    """
    dp 记录「以 i 元素结尾的最大和」，然后返回 max(dp) 即可
    更新公式：dp[i] = max(dp[i-1]+nums[i], nums[i])
    """
    def maxSubArray(self, nums: List[int]) -> int:
        dp = [0 for _ in range(len(nums))]
        dp[0] = nums[0]
        for i in range(1, len(nums)):
            dp[i] = max(dp[i-1]+nums[i], nums[i])
        return max(dp)
    """
    上述空间复杂度为 O(N)
    事实上由于更新 dp 过程中仅需要前一个元素即可，而 max 操作也可分步进行，因此可将其减少为 O(1)
    「滚动数组」
    """

    def maxSubArray2(self, nums: List[int]) -> int:
        pre = 0
        max_temp = nums[0]
        for num in nums:
            pre = max(pre+num, num)
            max_temp = max(max_temp, pre)
        return max_temp
```

#### 基于线段树/分治

分治思想，维护以下四个变量，更新公式还是较为显然的。

![-w427](media/16147360600817/16151766304739.jpg)

「方法二」相较于「方法一」来说，时间复杂度相同，但是因为使用了递归，并且维护了四个信息的结构体，运行的时间略长，空间复杂度也不如方法一优秀，而且难以理解。那么这种方法存在的意义是什么呢？

对于这道题而言，确实是如此的。但是仔细观察「方法二」，它不仅可以解决区间 [0, n-1][0,n−1]，还可以用于解决任意的子区间 [l,r][l,r] 的问题。如果我们把 [0, n-1][0,n−1] 分治下去出现的所有子区间的信息都用堆式存储的方式记忆化下来，即建成一颗真正的树之后，我们就可以在 O(\log n)O(logn) 的时间内求到任意区间内的答案，我们甚至可以修改序列中的值，做一些简单的维护，之后仍然可以在 O(\log n)O(logn) 的时间内求到任意区间内的答案，对于大规模查询的情况下，这种方法的优势便体现了出来。这棵树就是上文提及的一种神奇的数据结构——线段树。
