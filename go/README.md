
## 分类小结

总结一下每道题的思路:

### DP

- 5 最长回文子字符串, `中`
  - 解法四 `DP`, 时间复杂度 O(n^2), 空间复杂度 O(n^2)
  - 解法三 `中心扩散` 法, 时间复杂度 O(n^2), 空间复杂度 O(1)
  - 解法二 `滑动窗口`, 时间复杂度 O(n^2), 空间复杂度 O(1)
  - 解法一 Manacher's algorithm, 时间复杂度 O(n), 空间复杂度 O(n)
- 22 生成所有指定长度的括号对, `中`
  - 解法一 DFS, O(2^n), O(n)
  - `模拟`: 根据记录的数量模拟每一步合法的括号
- 32 最长合法的括号序列 `难`
  - 注意需要记录的其实是「上一个没有被匹配的右括号的下标」
  - 解法一 `栈`, 这里初始化栈底为 -1 并在扫描过程中保证栈不为空, O(n), O(n)
  - 解法二 `双指针` O(n), O(1), 算是对栈方法提升了空间消耗 —— 注意每次需要记录的实际上只有「上一个没有被匹配的右括号的下标」, 因此只需要再配合两个计数器分别记录左右括号出现的数量, 从而判断当前序列是否合法即可; 注意到会忽略 `(()` 这样的终止条件,因此还要从右往左扫描一遍.
- 42 接雨水 `难`
  - 本题是想求针对每个 i，找到它左边最大值 leftMax，右边的最大值 rightMax，然后 `min(leftMax，rightMax)` 为能够接到水的高度
  - 解法一 `扫描`, O(n), O(n), 两次遍历分别记录每个 index 的左右最大值;
  - 解法二 `双指针`, O(n), O(1), 若用双指针一次遍历, 这里维护「全局」的左右最大值 `maxLeft, maxRight`, 需要对于每个 index(遍历的左右指针) 都是合理的, 这里通过控制左右指针的移动 (每次移动较高的那一个) 来更新左右最大值.
- 45 跳跃游戏 `中`
  - 解法一: `贪心/模拟`, O(n), O(1). 注意到, 由于可选择当前位置条约的步数, 因此**可达的最远位置之前的所有格子一定也可达**, 因此可考虑贪心. 扫描步数数组, 维护当前能够到达最大下标的位置, 记为能到达的最远边界, 如果扫描过程中到达了最远边界, 更新边界并将跳跃次数 + 1.
- 53 最大子数组和 `易`, 但个人觉得算 `中`
  - 解法一 `DP`, O(n), O(n), 设计 `dp[i]` 是所有以 i 结尾的区间和的最大值, 状态转移方程是 `dp[i] = nums[i] + dp[i-1] (dp[i-1] > 0), dp[i] = nums[i] (dp[i-1] ≤ 0)`.
  - 解法二 `模拟`, O(n), O(1), 注意到这里实际用到的只是 dp[i-1] —— 事实上可以改写转移方程 `dp[i] = max{dp[i-1], 0} + nums[i]`, 迭代过程中维护这个数字即可
- 55 跳跃游戏, 判断是否可达 `易`
  - 关联 45, 顺序扫描即可, 记录可达的最远距离, 若扫描位置超过该 maxRight 则说明不可达
- 62 矩形到达另一个叫的路径数量, 杨辉三角
- 63 增加 obstacle
- 64 矩形每个坐标有对应数字, 求最小路径 `易` 以上几题都是基本的 DP; 需要注意的是可能可以用节省内存 (但面试/做题时候应该不用考虑). 另外注意64题可以直接在输入矩阵上计算.
- 70 爬楼梯, O(n)
  - 每次一步或两步, 问爬n阶楼梯有几种方式, 递推公式 `dp[i]=dp[i-1]+dp[i-2]` —— 正是斐波那契数列
  - 也可以用 `滚动数组` 节省空间; 公式 `f,g = g, f+g`
- 91 对字母用数字 1-26 编码, 问给定一个数字字符串的解码数量
  - 需要特殊考虑的是0, 要注意 "06" 是不合法的.
  - DP递推公式: `dp[i] += dp[i-1]` (当 1 ≤ s[i-1 : i] ≤ 9)；`dp[i] += dp[i-2]` (当 10 ≤ s[i-2 : i] ≤ 26)
  - 这题和上面的都可以考虑 `哨兵` 的思想, 避免起始的边界情况
- 95 给定一个数字生成所有的元素为1-n的 BST’s (binary search trees) `中` 但个人觉得挺难的 `structure`
  - 这里函数定义是 `func generateTrees(n int) []*TreeNode`, 只需要返回node指针即可.
  - 思路其实比较简单: 注意到对于**二叉搜索树**, 一个节点左边的数均小于该节点; 此题场景下, 递归 `func generateBSTrees(start, end int) []*TreeNode` 即可; 
  - 要注意终止条件, 这里可以设置为 `start>end`
- 96 求上面二叉树的数量
  - 在上一题思路下就很简单了: 递推公式 `dp[i] = dp[0] * dp[n-1] + dp[1] * dp[n-2] + …… + dp[n-1] * dp[0]`

### math

- 2 两数相加, 形式为逆序链表. `中`
  - 定义了基本的 `ListNode` 结构, 并定义 `List2Ints, IntsList` 实现数组和链表的方便转换.
- 7 反转32位整数 `中`
  - 这题主要的限制是在要防止 32位 sign int 溢出, 讨巧的思路可以用更长的整数类型/字符串来保存. 「标准」思路应该是每次 `*10` 之前进行检查 (或者说, 和 `math.MinInt32/10` 进行比较) 防止溢出.
- 9 Palindrome 回文数
  - 同样可以采用 1. 反转数字; 2. 转为数组; 3. 转为字符串等方式.
  - 直接反转可能溢出 (虽然此时必然不是回文数); 思路是「反转整数长度的一半」(即循环条件 `x>rev`), 最后的判断条件: 若 x 为回文数且长度为偶数, 则 `x==rev`; 若为奇数, 则 `x==rev/10`
- 12, 13 罗马数字转阿拉伯数字
  - 就是所使用的基数不用, 累计即可
- 60 Permutation-Sequence 找出以一定的数字作为元素的排列中的第 k 个 `难`
  - 思路一 也即官方的 [缩小问题规模](https://leetcode-cn.com/problems/permutation-sequence/solution/di-kge-pai-lie-by-leetcode-solution/); 其实也可理解为贪婪剪枝的 DFS?
    - 使用 go 来实现的时候没有 Python 中好用的 `math.perm` 函数, 方便的类型转换等. 解答中用到的一些技巧值得学习. 例如, 1. 构造了 factorial 来实现 Python 中的 math.perm; 2. 用 valid 数组标记还没有用过的数字
    - 重点还是要明确公式: `a_i=(k-1)mod(n-1)!+1`
  - 反过来的问题: 对于给定的排列确定其为顺序第几个?
    - 公式 `k=sum(order_i*(n-1)!)+1`, 其中的 order_i 是在 序列 `a_i+1...a_n` 中小于 a_i 的元素数量
- 29 整除 `中`
  - 思路一 类似二分查找, 每次将除数 `*2` 找到小于等于被除数的最大的那一个, 迭代终止条件是 `dividend<divisor`, 即不断减去除数的倍数之后, 剩余的部分小于除数
  - 思路二 `倍增法` 实际上在除数递增的过程中即可将被除数相减, 当增大到接近被除数之后再不断 `/2`, 终止条件是因子 `cnt==0`, 也即 `dividend<divisor`

### binary search 二分查找

总结了二分查找的注意点:

- 循环退出条件，注意是 low <= high，而不是 low < high。
- mid 的取值，mid := low + (high-low)»1
- low 和 high 的更新。low = mid + 1，high = mid - 1。

```go
func binarySearchMatrix(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + (high-low)>>1
  if nums[mid] == target {
   return mid
  } else if nums[mid] > target {
   high = mid - 1
  } else {
   low = mid + 1
  }
 }
 return -1
}
```

四个基本的变种

```go
// 二分查找第一个与 target 相等的元素，时间复杂度 O(logn)
func searchFirstEqualElement(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + ((high - low) >> 1)
  if nums[mid] > target {
   high = mid - 1
  } else if nums[mid] < target {
   low = mid + 1
  } else {
   if (mid == 0) || (nums[mid-1] != target) { // 找到第一个与 target 相等的元素
    return mid
   }
   high = mid - 1
  }
 }
 return -1
}

// 二分查找最后一个与 target 相等的元素，时间复杂度 O(logn)
func searchLastEqualElement(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + ((high - low) >> 1)
  if nums[mid] > target {
   high = mid - 1
  } else if nums[mid] < target {
   low = mid + 1
  } else {
   if (mid == len(nums)-1) || (nums[mid+1] != target) { // 找到最后一个与 target 相等的元素
    return mid
   }
   low = mid + 1
  }
 }
 return -1
}

// 二分查找第一个大于等于 target 的元素，时间复杂度 O(logn)
func searchFirstGreaterElement(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + ((high - low) >> 1)
  if nums[mid] >= target {
   if (mid == 0) || (nums[mid-1] < target) { // 找到第一个大于等于 target 的元素
    return mid
   }
   high = mid - 1
  } else {
   low = mid + 1
  }
 }
 return -1
}

// 二分查找最后一个小于等于 target 的元素，时间复杂度 O(logn)
func searchLastLessElement(nums []int, target int) int {
 low, high := 0, len(nums)-1
 for low <= high {
  mid := low + ((high - low) >> 1)
  if nums[mid] <= target {
   if (mid == len(nums)-1) || (nums[mid+1] > target) { // 找到最后一个小于等于 target 的元素
    return mid
   }
   low = mid + 1
  } else {
   high = mid - 1
  }
 }
 return -1
}
```

- 35 搜索插入位置
  - 基本的「在有序数组中找到最后一个比 target 小的元素」这一变种
- 69 实现 sqrt
  - 解法二 `牛顿法`, 即求 `f(x)=x^2-n` 的零点
