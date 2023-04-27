package main

import (
	"container/heap"
	"fmt"
	"math"
	"sort"
)

// ===================funcs ===================================
func min(a,b int) int{
    if a<b{return a}
    return b
}
func max(a,b int)int{
    if a>b{return a}
    return b
}

// ListNode 列表结构
type ListNode struct {
    Val int
    Next *ListNode
}

// =================== problems ===================================
/* 23. 合并K个升序链表 */
// type Item struct {
//     val int
//     node *ListNode
// }
// type ItemHeap []Item

// func (h ItemHeap) Len() int { return len(h) }
// func (h ItemHeap) Less(i, j int) bool { 
//     return h[i].val < h[j].val
// }
// func (h ItemHeap) Swap(i, j int) {
//     h[i], h[j] = h[j], h[i]
// }
// func (h *ItemHeap) Push(val int) {
//     *h = append(*h, Item{val, nil})
// }
// func (h *ItemHeap) Pop() interface{} {
//     old := *h
//     n := len(old)
//     x := old[n-1]
//     *h = old[:n-1]
//     return x
// }
// func mergeKLists(lists []*ListNode) *ListNode {
//     h := &ItemHeap{}
//     for _, l := range lists {
//         heap.Push(h, Item{l.Val, l})
//     }
//     res := ListNode{0, nil}
//     for {
//         item := heap.Pop(h).(Item)
//     }
//     return res.Next
// }


// TODO go 语言语法
// https://leetcode-cn.com/problems/merge-k-sorted-lists/solution/go-zi-dai-zui-xiao-dui-by-zhaoyongjie-frgs/
type minHeap []* ListNode

func (h minHeap) Len() int { return len(h) }
func (h minHeap) Less(i, j int) bool { return h[i].Val < h[j].Val }
func (h minHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *minHeap) Push(x interface{}) {
    *h = append(*h, x.(*ListNode))
}
func (h *minHeap) Pop() interface{} {
    old := *h
    n := len(old) 
    x := old[n-1]
    *h = old[:n-1]
    return x
}
func mergeKLists(lists []*ListNode) *ListNode {
    h := new(minHeap)
    // h := minHeap{}
    for _, l := range lists {
        if l!=nil {
            heap.Push(h, l)
        }
    }
    // dummyHead := ListNode{}
    dummyHead := new(ListNode)
    pre := dummyHead
    for h.Len() >0{
        tmp := heap.Pop(h).(*ListNode)
        if tmp.Next != nil {
            heap.Push(h, tmp.Next)
        }
        pre.Next = tmp
        pre = pre.Next
    }
    return dummyHead.Next
}


/* 2089. 找出数组排序后的目标下标
排序, 输出对应的index */
func targetIndices(nums []int, target int) []int {
    sort.Ints(nums)
    results := []int{}
    for i:=0; i<len(nums); i++ {
        if nums[i] == target {
            results = append(results, i)
        }
    }
    return results
}
func f2089(){
    fmt.Println(targetIndices([]int{1,2,5,2,3}, 2))
}

/* 2090. 半径为 k 的子数组平均值
输入：nums = [7,4,3,9,1,8,5,2,6], k = 3
输出：[-1,-1,-1,5,4,4,-1,-1,-1]
解释：
- avg[0]、avg[1] 和 avg[2] 是 -1 ，因为在这几个下标前的元素数量都不足 k 个。
- 中心为下标 3 且半径为 3 的子数组的元素总和是：7 + 4 + 3 + 9 + 1 + 8 + 5 = 37 。
  使用截断式 整数除法，avg[3] = 37 / 7 = 5 。
- 中心为下标 4 的子数组，avg[4] = (4 + 3 + 9 + 1 + 8 + 5 + 2) / 7 = 4 。
- 中心为下标 5 的子数组，avg[5] = (3 + 9 + 1 + 8 + 5 + 2 + 6) / 7 = 4 。
- avg[6]、avg[7] 和 avg[8] 是 -1 ，因为在这几个下标后的元素数量都不足 k 个。

输入：nums = [100000], k = 0
输出：[100000]
解释：
- 中心为下标 0 且半径 0 的子数组的元素总和是：100000 。
  avg[0] = 100000 / 1 = 100000 。

输入：nums = [8], k = 100000
输出：[-1]
解释：
- avg[0] 是 -1 ，因为在下标 0 前后的元素数量均不足 k 。 */
func getAverages(nums []int, k int) []int {
    result := make([]int, len(nums))
    for i:=0; i<len(nums); i++ {
        result[i] = -1
    }
    if len(nums)>=2*k+1{
        temp := 0
        for i:=0; i<2*k+1; i++{
            temp += nums[i]
        }
        for i:=k; i<len(nums)-k; i++{
            result[i] = temp / (2*k+1)
            if i+k+1<len(nums){
                temp = temp + nums[i+k+1] - nums[i-k]
            }
        }
    }
    return result
}
func f2090(){
    fmt.Println(getAverages([]int{7,4,3,9,1,8,5,2,6}, 3))
}

/* 2091. 从数组中移除最大值和最小值
从前或者从后面开始移除, 计算最小移除次数
 */
func minimumDeletions(nums []int) int {
    minIndex, maxIndex := 0, 0
    for i:=0; i<len(nums); i++{
        if nums[i] > nums[maxIndex]{
            maxIndex = i
        }
        if nums[i] < nums[minIndex]{
            minIndex = i
        }
    }
    // minL, minR := minIndex+1, len(nums)-minIndex
    // maxL, maxR := maxIndex+1, len(nums)-maxIndex
    // if minL<=minR && maxL<=maxR {
    //     return max(minL, maxL)
    // } else if minR<=minL && maxR<=maxL {
    //     return max(minR, maxR)
    // }
    // return min(minL, minR) + min(maxL, maxR)

    i1, i2 := min(minIndex, maxIndex), max(minIndex, maxIndex)
    r1, r2, r3 := i2+1, len(nums)-i1, i1+1+len(nums)-i2
    result := min(r1, r2)
    return min(result, r3)
}
func f2091(){
    fmt.Println(minimumDeletions([]int{-1,-53,93,-42,37,94,97,82,46,42,-99,56,-76,-66,-67,-13,10,66,85,-28}))
}

/* 2092. 找出知晓秘密的所有专家
Python
 */


/* 1155. 掷骰子的N种方法
这里有 d 个一样的骰子，每个骰子上都有 f 个面，分别标号为 1, 2, ..., f。
我们约定：掷骰子的得到总点数为各骰子面朝上的数字的总和。
如果需要掷出的总点数为 target，请你计算出有多少种不同的组合情况（所有的组合情况总共有 f^d 种），
模 10^9 + 7 后返回。

输入：d = 2, f = 6, target = 7
输出：6

输入：d = 30, f = 30, target = 500
输出：222616187

更新公式: dp[d][target] = dp[d-1][target-1] + ... + dp[d-1][target-f]
  */
func numRollsToTarget(n int, k int, target int) int {
    // 确保 target>=n, 可解
    if n>target {return 0}
    dp := make([]int, target+1)
    // 边界!!
    for i:=1; i<=min(target, k); i++ {
        dp[i] = 1
    }
    for i:=2; i<=n; i++ {
        for j :=target; j>=1; j-- {
            tmp := 0
            for jj:=1; jj<=k; jj++{
                if j-jj<0 {break}
                tmp += dp[j-jj]
                tmp %= int(math.Pow(10,9))+7
            }
            dp[j] = tmp
        }
    }
    return dp[target]
}
func f1155(){
    fmt.Println(
        numRollsToTarget(2,6,7),
        numRollsToTarget(1,2,3),
        numRollsToTarget(30,30,500),
    )
}

/* 1392. 最长的前缀和后缀相同

see https://leetcode-cn.com/problems/longest-happy-prefix/solution/zui-chang-kuai-le-qian-zhui-by-leetcode-solution/*/


// =================== main ===================================
func main() {
    // f2091()
    f1155()
}