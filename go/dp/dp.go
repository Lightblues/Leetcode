package main

import (
	"container/heap"
	"fmt"
	"math"
	"sort"
)

func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func max(x,y int)int{
	if x>y{
		return x
	}
	return y
}

// TreeNode 定义的二叉树节点
type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

// Tree2Postorder 把 二叉树 转换成 postorder 的切片
func Tree2Postorder(root *TreeNode) []int {
	if root == nil {
		return nil
	}

	if root.Left == nil && root.Right == nil {
		return []int{root.Val}
	}

	res := Tree2Postorder(root.Left)
	res = append(res, Tree2Postorder(root.Right)...)
	res = append(res, root.Val)

	return res
}



/* 0005.Longest-Palindromic-Substring/
Given a string s, return the longest palindromic substring in s.

Input: s = "babad"
Output: "bab"
Note: "aba" is also a valid answer.
*/
// 解法四 DP, 时间复杂度 O(n^2), 空间复杂度 O(n^2)
func longestPalindromic(s string) string {
	dp := make([][]bool, len(s))
	res := ""
	for i:=0; i<len(s); i++ {
		dp[i] = make([]bool, len(s))
	}
	for i:=len(s)-1; i>=0; i--{		// 注意这里DP递归公式, 遍历i的顺序
		for j:=i; j<len(s);j++{
			dp[i][j] = s[i]==s[j] && (j-i<3 ||dp[i+1][j-1])
			if dp[i][j] && len(res)<j-i+1 {
				res = s[i:j+1]
			}
		}
	}
	return res
}
// 解法三 中心扩散法, 时间复杂度 O(n^2), 空间复杂度 O(1)
func longestPalindromic1(s string) string {
	res := ""
	for i:=0; i<len(s); i++{
		res = maxPalindromic(s,i,i,res)
		res = maxPalindromic(s, i,i+1, res)
	}
	return res
}
func maxPalindromic(s string,i,j int, res string) string{
	sub:=""
	for i>=0 && j<len(s) && s[i]==s[j]{
		sub = s[i:j+1]
		i--
		j++
	}
	if len(sub) > len(res){
		return sub
	}
	return res
}
// 解法二 滑动窗口, 时间复杂度 O(n^2), 空间复杂度 O(1)
func longestPalindromic2(s string) string {
	if len(s) == 0{
		return ""
	}
	left, right, pl, pr := 0,0,0,0
	for left < len(s){
		// 先将right移动到相同字符最右边
		for right+1<len(s) && s[right+1]==s[left]{
			right++
		}
		// 两边拓展
		for left-1>=0 && right+1<len(s) && s[left-1]==s[right+1]{
			right++
			left--
		}
		if right-left>pr-pl{
			pr, pl = right, left
		}
		// 重制 right left
		left = (right+left)/2+1
		right = left
	}
	return s[pl:pr+1]
}
// 解法一 Manacher's algorithm, 时间复杂度 O(n), 空间复杂度 O(n)
func longestPalindromic3(s string) string {
	if len(s) < 2 {
		return s
	}
	newS := make([]rune, 0)
	newS = append(newS, '#')
	for _, c := range s {
		newS = append(newS, c)
		newS = append(newS, '#')
	}
	// dp[i]:    以预处理字符串下标 i 为中心的回文半径(奇数长度时不包括中心)
	// maxRight: 通过中心扩散的方式能够扩散的最右边的下标
	// center:   与 maxRight 对应的中心字符的下标
	// maxLen:   记录最长回文串的半径
	// begin:    记录最长回文串在起始串 s 中的起始下标
	dp, maxRight, center, maxLen, begin := make([]int, len(newS)), 0, 0, 1, 0
	for i := 0; i < len(newS); i++ {
		if i < maxRight {
			// 这一行代码是 Manacher 算法的关键所在
			dp[i] = min(maxRight-i, dp[2*center-i])
		}
		// 中心扩散法更新 dp[i]
		left, right := i-(1+dp[i]), i+(1+dp[i])
		for left >= 0 && right < len(newS) && newS[left] == newS[right] {
			dp[i]++
			left--
			right++
		}
		// 更新 maxRight, 它是遍历过的 i 的 i + dp[i] 的最大者
		if i+dp[i] > maxRight {
			maxRight = i + dp[i]
			center = i
		}
		// 记录最长回文子串的长度和相应它在原始字符串中的起点
		if dp[i] > maxLen {
			maxLen = dp[i]
			begin = (i - maxLen) / 2 // 这里要除以 2 因为有我们插入的辅助字符 #
		}
	}
	return s[begin : begin+maxLen]
}
func f5(){
	s := "babad"
	fmt.Println(longestPalindromic3(s))
}

/* 0022.Generate-Parentheses/
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

For example, given n = 3, a solution set is:
[
  "((()))",
  "(()())",
  "(())()",
  "()(())",
  "()()()"
]
*/
// 这道题实际上不需要判断括号是否匹配的问题. 因为在 DFS 回溯的过程中, 会让 ( 和 ) 成对的匹配上的. 
// O(2^n), O(n)
func generateParentheses(n int) []string {
	if n==0 {
		return []string{}
	}
	res := []string{}
	// 深度优先搜索, 传参：左右括号剩余的数量, 当前生成的序列
	findGenerateParenttheses(n, n, "", &res)
	return res
}
func findGenerateParenttheses(lnum, rnum int, s string, res *[]string){
	// 终止条件
	if lnum==0 && rnum==0 {
		*res = append(*res, s)
	}
	// 相较于解法2的判断, 这里的判断逻辑就简化了很多 —— DFS思想
	if lnum>0 {
		findGenerateParenttheses(lnum-1, rnum, s+"(", res)
	}
	if rnum>0 && rnum>lnum {
		findGenerateParenttheses(lnum, rnum-1, s+")", res)
	}
}
// 自己此前的逻辑, 其实也是 DFS, 只是条件判断不同
func generateParentheses1(n int) []string {
	res := []string{}
	findGenerateParenttheses1("", &res, 0, 0, n)
	return res
}
func findGenerateParenttheses1(s string, res *[]string, lnum, rnum, n int){
	// 这里区分了 1. 终止；2. 仅能添加）；3. 仅能添加（；4. 左右括号均能添加四种情况
	if lnum==n && rnum==n {
		*res = append(*res, s)
	} else if lnum==n {
		findGenerateParenttheses1(s+")", res, lnum, rnum+1, n)
	} else if lnum==rnum {
		findGenerateParenttheses1(s+"(", res, lnum+1, rnum, n)
	} else {
		findGenerateParenttheses1(s+"(", res, lnum+1, rnum, n)
		findGenerateParenttheses1(s+")", res, lnum, rnum+1, n)
	}
}
func f6(){
	fmt.Println(generateParentheses1(3))
}

/* 0032.Longest-Valid-Parentheses/
Input: s = ")()())"
Output: 4
Explanation: The longest valid parentheses substring is "()()".
*/
func longestValidParenthesesTry(s string) int {
	// 这里理解错了,  "()()" 应该算 4
	res, stack := 0, []int{}
	for i:=0; i<len(s);i++ {
		if s[i] == '(' {
			stack = append(stack, i)
		} else {
			if len(stack) > 0 {
				res = max(res, i - stack[len(stack)-1]+1)
				stack = stack[:len(stack)-1]
			}
		}
	}
	return res
}
// 解法一 栈, O(n), O(n)
func longestValidParentheses(s string) int {
	res, stack := 0, []int{-1}
	// stack 记录可能的合法序列之前的 index, 因此初始化为 -1；然后每遇到一个 `(` 入栈记录, 每遇到一个 `)` 先弹出再计算长度. 
	// 需要注意的是, 若弹出后栈空, 则应该入栈 `)` 因为可能是下一个合法序列之前的 index
	for i:=0; i<len(s); i++ {
		if s[i] == '(' {
			stack = append(stack, i)
		} else {
			stack = stack[:len(stack)-1]
			if len(stack) > 0 {
				res = max(res, i - stack[len(stack)-1])
			} else if len(stack) == 0{
				stack = append(stack, i)
			}
		}
	}
	return res
}
// 解法二 双指针 O(n), O(1)
/* 
在栈的方法中, **实际用到的元素仅仅是栈底的上一个没有被匹配的右括号的下标**. 因此这里用 `mostLeft` 记录这个index, 
然后分别记录左右括号出现的数量, 1. 相等时计算长度；2. 左数量少于右数量时重制. 
注意这样 `(()` 这样的终止情况不会计算到, 因此需要从右往左再来一遍. 
*/
func longestValidParentheses2(s string) int{
	cLeft, cRight, res, mostLeft := 0, 0, 0, -1
	for i:=0; i<len(s); i++ {
		if s[i] =='(' {
			cLeft ++
		} else {
			cRight ++
		}
		if cLeft == cRight {
			res = max(res, i-mostLeft)
		} else if cLeft<cRight {
			cLeft, cRight = 0,0
			mostLeft = i
		}
	}
	cLeft, cRight, mostRight := 0, 0, len(s)
	for i:=len(s)-1; i>=0; i--{
		if s[i] =='(' {
			cLeft ++
		} else {
			cRight ++
		}
		if cLeft == cRight {
			res = max(res, mostRight-i)
		} else if cLeft>cRight {
			cLeft, cRight = 0,0
			mostRight = i
		}
	}
	return res
}
func f32(){
	println(longestValidParentheses2(")()())"))
}


/* 0042.Trapping-Rain-Water/ 接雨水
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.
结合画图理解
Input: [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6 

抽象一下，本题是想求针对每个 i，找到它左边最大值 leftMax，右边的最大值 rightMax，然后 min(leftMax，rightMax) 为能够接到水的高度。*/
// 扫描两遍, 分别求每个位置的左右最大, 即可得到可接水高度
func trap(height []int) int {
	// 左右分别扫描一遍, 得到每个位置可接水高度
	record := make([]int, len(height))
	minH := 0
	for i,h := range height{
		minH = max(h, minH)
		record[i] = minH
	}
	minH  = 0
	for i:=len(height)-1; i>=0; i--{
		minH = max(height[i], minH)
		record[i] = min(record[i], minH)
	}
	// 累计
	result := 0
	for i:=1; i<len(height); i++{
		result += record[i]-height[i]
	}
	return result
}
// 解法一 双指针
// 若用双指针一次遍历, 这里记录的左右最大值 maxLeft, maxRight, 需要对于每个 index(遍历的左右指针) 都是合理的, 这里通过控制左右指针的移动 (每次移动较高的那一个) 来更新左右最大值.
func trap2(height []int) int {
	left, right, maxLeft, maxRight, result := 0,len(height)-1,0,0,0
	maxLR := 0
	for left < right {
		maxLR = max(maxLeft, maxRight)
		if height[left] < height[right]{
			if height[left] < maxLR {
				result += maxLR-height[left]
			} 
			if height[left] > maxLeft{
				maxLeft = height[left]
			}
			left++
		} else {
			if height[right] < maxLR {
				result += maxLR-height[right]
			}
			if height[right] > maxRight{
				maxRight = height[right]
			}
			right--
		}
	}
	return result
}
func f42(){
	fmt.Println(trap2([]int{0,1,0,2,1,0,1,3,2,1,2,1}))
}

/* 0045.Jump-Game-II/
Given an array of non-negative integers nums, you are initially positioned at the first index of the array.
Each element in the array represents your maximum jump length at that position.
Your goal is to reach the last index in the minimum number of jumps.
You can assume that you can always reach the last index.
Input: nums = [2,3,1,1,4]
Output: 2
Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index. 
*/
/* 解法0 暴力, O(n^2)
对于每次能够达到的index, 更新其最小步数 */
func jumpGameTwo (nums []int) int {
	records := make([]int, len(nums))
	for i:=0; i<len(nums); i++ {
		for j:=1; j<=nums[i] && i+j<len(nums); j++ {
			if records[i+j] == 0{
				records[i+j] = records[i]+1
			} else{
				records[i+j] = min(records[i+j], records[i]+1)
			}
		}
	}
	return records[len(nums)-1]
}
// 解法一: 贪心, O(n), O(1)
/* 注意到, 由于可选择当前位置条约的步数, 因此可达的最远位置之前的所有格子一定也可达, 因此可以顺序扫描搜索. 
要求找到最少跳跃次数, 顺理成章的会想到用贪心算法解题. 扫描步数数组, 维护当前能够到达最大下标的位置, 记为能到达的最远边界, 如果扫描过程中到达了最远边界, 更新边界并将跳跃次数 + 1. 
因此, 这里维护 maxRight 可达最远的位置, 并用 currMaxRight, step 记录当前步数可达最远的位置 */
func jumpGame(nums []int) int{
	if len(nums) == 1{
		return 0
	}
	step, maxRight, currMaxRight := 0,0,0
	for i,num := range nums {
		if i+num > maxRight{
			maxRight = i+num
			// 终止条件: 最远可达超过了 nums 长度
			if maxRight >= len(nums)-1{
				return step+1
			}
		}
		if i == currMaxRight {
			// 题目中假设均可达, 这里判断不可达返回 -1
			if maxRight <= i{
				return -1
			}
			// 到了当前 step 可达的最远位置,需要更新 currMaxRight
			step ++
			currMaxRight = maxRight
		}
	}
	return step
}
func f45(){
	println(jumpGame([]int{2,1,0,1,4}))
}

/* 0053.Maximum-Subarray/
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

Input: [-2,1,-3,4,-1,2,1,-5,4],
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.*/
// 解法一 DP, O(n), O(n)
func maximumSubarray(nums[]int) int{
	if len(nums)==1{
		return nums[0]
	}
	dp:=make([]int, len(nums))
	dp[0] = nums[0]
	res:= nums[0]
	for i:=1; i<len(nums); i++ {
		if dp[i-1]>0 {
			dp[i] = dp[i-1] + nums[i]
		} else {
			dp[i] = nums[i]
		}
		res = max(res, dp[i])
	}
	return res
}
// 解法二 模拟
func maximumSubarray2(nums []int) int {
	if len(nums)==1{return nums[0]}
	result, dp := nums[0], 0
	for i:=0; i<len(nums); i++{
		dp = max(dp, 0) + nums[i]
		result = max(result, dp)
	}
	return result
}
func f53(){
	fmt.Println(maximumSubarray2([]int{-2,1,-3,4,-1,2,1,-5,4}))
}

/* 0055.Jump-Game/
判断是否可达 
顺序扫描即可, 记录可达的最远距离, 若扫描位置超过该 maxRight 则说明不可达 */
func canJump(nums []int) bool {
	n := len(nums)
	if n == 0 {
		return false
	}
	if n == 1 {
		return true
	}
	maxRight := 0
	for i, num := range nums {
		if i > maxRight {
			return false
		}
		if i+num > maxRight{
			maxRight = i+num
			if maxRight >= n-1{
				return true
			}
		}
	}
	return true
}
func f55(){
	fmt.Println(canJump([]int{3,2,1,1,4}))
}


/* 0062.Unique-Paths/
一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为“Start” ）。机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。问总共有多少条不同的路径？
Input: m = 3, n = 2
Output: 3
Explanation:
From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Right -> Down
2. Right -> Down -> Right
3. Down -> Right -> Right */
func uniquePaths(m int, n int) int {
	dp := make([][]int, m)
	// for i:=0; i<m; i++ {
	// 	dpLine := make([]int, n)
	// 	for j:= 0; j<n ; j++{
	// 		if i==0 || j==0 {
	// 			dpLine[j] = 1
	// 		} else {
	// 			dpLine[j] = dpLine[j-1] + dp[i-1][j]
	// 		}
	// 		dp[i] = dpLine
	// 	}
	// }
	// 先初始化矩阵,这样写起来更规范一点
	for i:=0; i<m; i++ {
		dp[i] = make([]int, n)
	}
	for i:=0; i<m; i++{
		for j:=0;j<n; j++{
			if i==0 || j==0{
				dp[i][j] = 1
			} else {
				dp[i][j] = dp[i-1][j] + dp[i][j-1]
			}
		}
	}
	return dp[m-1][n-1]
}
func f62(){
	fmt.Println(uniquePaths(7,3))
}

/* 0063.Unique-Paths-II/
加了 obstacles
Input:
[
  [0,0,0],
  [0,1,0],
  [0,0,0]
]
Output: 2
Explanation:
There is one obstacle in the middle of the 3x3 grid above.
There are two ways to reach the bottom-right corner:
1. Right -> Right -> Down -> Down
2. Down -> Down -> Right -> Right */
func uniquePathsWithObstacles(obstacleGrid [][]int) int {
	// 边界条件 [[1]]
	if len(obstacleGrid) == 0 || obstacleGrid[0][0] == 1 {
		return 0
	}
	m, n := len(obstacleGrid), len(obstacleGrid[0])
	dp := make([][]int, m)
	for i:=0; i<m; i++ {
		dp[i] = make([]int, n)
	}
	dp[0][0] = 1
	for i:= 1; i<m; i++ {
		if dp[i-1][0] != 0 && obstacleGrid[i][0]==0{
			dp[i][0] = 1
		}
	}
	for j:=1; j<n; j++{
		if dp[0][j-1]!=0 && obstacleGrid[0][j]==0{
			dp[0][j] = 1
		}
	}
	for i:=1; i<m; i++{
		for j:=1;j<n; j++{
			if obstacleGrid[i][j] ==0{
				dp[i][j] = dp[i-1][j]+dp[i][j-1]
			}
		}
	}
	return dp[m-1][n-1]
}
func f63(){
	fmt.Println(uniquePathsWithObstacles([][]int{
		{0,0,0},		// 这里可以省略类型 []int
		{0,1,0},
		{0,0,0},
	}))
}

/* 0064.Minimum-Path-Sum/
Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right which minimizes the sum of all numbers along its path.
Input:
[
  [1,3,1],
  [1,5,1],
  [4,2,1]
]
Output: 7
Explanation: Because the path 1→3→1→1→1 minimizes the sum. */
// 解法二 最原始的方法，辅助空间 O(n^2)
func minPathSum1(grid [][]int) int {
	m, n := len(grid), len(grid[0])
	dp := make([][]int, m)
	for i:=0; i<m; i++ {
		dp[i] = make([]int, n)
	}
	dp[0][0] = grid[0][0]
	for i:= 1; i<m; i++ {
		dp[i][0] = dp[i-1][0] + grid[i][0]
	}
	for j:=1; j<n; j++{
		dp[0][j] = dp[0][j-1] + grid[0][j]
	}
	for i:=1; i<m; i++{
		for j:=1;j<n; j++{
			dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
		}
	}
	return dp[m-1][n-1]
}
// 解法一 原地 DP，无辅助空间
// 这一题最简单的想法就是用一个二维数组来 DP，当然这是最原始的做法。由于只能往下和往右走，只需要维护 2 列信息就可以了，从左边推到最右边即可得到最小的解。更近一步，可以直接在原来的数组中做原地 DP，空间复杂度为 0 。
func minPathSum(grid [][]int) int {
	m, n := len(grid), len(grid[0])
	for i := 1; i < m; i++ {
		grid[i][0] += grid[i-1][0]
	}
	for j := 1; j < n; j++ {
		grid[0][j] += grid[0][j-1]
	}
	for i := 1; i < m; i++ {
		for j := 1; j < n; j++ {
			grid[i][j] += min(grid[i-1][j], grid[i][j-1])
		}
	}
	return grid[m-1][n-1]
}
func f64(){
	fmt.Println(minPathSum1([][]int{
		{1,3,1},
		{1,5,1},
		{4,2,1},
	}))
}

/* 0070.Climbing-Stairs/
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？注意：给定 n 是一个正整数
Input: 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step */
// 注意递推公式: dp[i] = dp[i-2] + dp[i-1]
// 这一题求解的值就是 **斐波那契数列**。
func climbStairs(n int) int {
	dp := make([]int, n+1)
	dp[0], dp[1] = 1, 1
	for i:=2; i<=n; i++{
		dp[i] = dp[i-1]+dp[i-2]
	}
	return dp[n]
}
// 解法二 滚动数组
// 实际上需要的就是最近的两个
func climbStairs2(n int) int {
    // dp := [2]int{1, 1}
    // for i := 2; i <= n; i++ {
    //     dp[i%2] = dp[0] + dp[1]
    // }
    // return dp[n%2]
	f, g := 1,1
	for i:=0; i<n; i++{
		f,g = g, f+g
	}
	return f
}
func f70(){
	fmt.Println(climbStairs2(4))
}

/* 0091.Decode-Ways/
将字母进行了编码
'A' -> 1
'B' -> 2
...
'Z' -> 26 
Given a non-empty string containing only digits, determine the total number of ways to decode it.

Input: "226"
Output: 3
Explanation: It could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

要注意 "06" 是不合法的. 
DP递推公式: dp[i] += dp[i-1] (当 1 ≤ s[i-1 : i] ≤ 9)；dp[i] += dp[i-2] (当 10 ≤ s[i-2 : i] ≤ 26)
*/
func numDecodings(s string) int {
	n:=len(s)
	dp := make([]int, n+1)
	// 哨兵, 或者理解为, 空字符串只有一种方式
	dp[0] = 1
	for i:=1; i<=n; i++{
		if s[i-1]!='0' {
			dp[i] += dp[i-1]
		}
		if i>1 && s[i-2]!='0' && 10*(s[i-2]-'0')+(s[i-1]-'0')<=26 {
			dp[i] += dp[i-2]
		}
	}
	return dp[n]
}
func f91(){
	fmt.Println(numDecodings("226"))
}

/* 0095.Unique-Binary-Search-Trees-II/
Given an integer n, generate all structurally unique BST’s (binary search trees) that store values 1 … n.
Input: 3
Output:
[
  [1,null,3,2],
  [3,2,null,1],
  [3,1,null,null,2],
  [2,1,3],
  [1,null,2,null,3]
]
Explanation:
The above output corresponds to the 5 unique BST's shown below:

   1         3     3      2      1
    \       /     /      / \      \
     3     2     1      1   3      2
    /     /       \                 \
   2     1         2                 3
 */

 /**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func generateTrees(n int) []*TreeNode {
	if n==0 {
		return []*TreeNode{}
	}
	return generateBSTrees(1, n)
}
func generateBSTrees(start, end int) []*TreeNode{
	// 生成包括了 start到end 的所有BST
	tree := []*TreeNode{}
	if start>end {
		tree = append(tree, nil)	// nil 初始化 空对象
	}
	for i:=start; i<=end; i++ {
		// 遍历过程: 分别迭代生成左右子树, 然后拼接起来
		left := generateBSTrees(start, i-1)
		right := generateBSTrees(i+1, end)
		for _,l := range left{
			for _,r := range right{
				root := &TreeNode{Val: i, Left: l, Right: r}
				tree = append(tree, root)
			}
		}
	}
	return tree
}
func f95(){
	tree := generateTrees(3)
	for i:=0; i<len(tree);i++{
		t:= tree[i]
		fmt.Println((Tree2Postorder(t)))
	}
}

/* 0096.Unique-Binary-Search-Trees/
Given n, how many structurally unique BST’s (binary search trees) that store values 1 … n?
Input: 3
Output: 5
Explanation:
Given n = 3, there are a total of 5 unique BST's:

   1         3     3      2      1
    \       /     /      / \      \
     3     2     1      1   3      2
    /     /       \                 \
   2     1         2                 3 */
func numTrees(n int) int{
	dp := make([]int, n+1)
	dp[0] = 1
	for i:=1; i<=n; i++ {
		for j:=0; j<i; j++ {
			dp[i] += dp[j] * dp[i-j-1]
		}
	}
	return dp[n]
}
func f96(){
	fmt.Println(numTrees(3), numTrees(4))
}

/* 0097.Interleaving-String/ 交错字符串
Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.
An interleaving of two strings s and t is a configuration where they are divided into non-empty substrings such that:
s = s1 + s2 + ... + sn
t = t1 + t2 + ... + tm
|n - m| <= 1
The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ... 

两个字符串能否在不改变顺序的情况下, 拼接组成第目标字符串
Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: true

Follow up: Could you solve it using only O(s2.length) additional memory space? */
// 解法一 DP
func isInterleave(s1 string, s2 string, s3 string) bool {
	m, n := len(s1), len(s2)
	if len(s3) != m+n{
		return false
	}
	dp := make([][]bool, m+1)
	for i:=0; i<=m; i++{
		dp[i] = make([]bool, n+1)
	}
	dp[0][0] = true
	for i:=1; i<=m; i++{
		dp[i][0] = s1[:i] == s3[:i]
	}
	for j:=1;j<=n;j++{
		dp[0][j] = s2[:j]==s3[:j]
	}
	for i:=1; i<=m; i++{
		for j:=1;j<=n;j++{
			dp[i][j] = dp[i-1][j]&&s1[i-1]==s3[i+j-1] || dp[i][j-1]&&s2[j-1]==s3[i+j-1]
		}
	}
	return dp[m][n]
}
// 优化空间 滚动数组
func isInterleave2(s1, s2, s3 string) bool {
	m, n := len(s1), len(s2)
	if len(s3) != m+n{
		return false
	}
	dp := make([]bool, n+1)
	for j:=0; j<=n; j++{
		dp[j] = s2[:j]==s3[:j]
	}
	for i:=1; i<=m; i++{
		dp[0] = s1[:i]==s3[:i]
		for j:=1;j<=n;j++{
			dp[j] = dp[j]&&s1[i-1]==s3[i+j-1] || dp[j-1]&&s2[j-1]==s3[i+j-1]
		}
	}
	return dp[n]
}
func f97(){
	fmt.Println(isInterleave2("aabcc", "dbbca", "aadbbcbcac"))
}

/* 0115.Distinct-Subsequences/
给定一个字符串 s 和一个字符串 t ，计算在 s 的子序列中 t 出现的个数。字符串的一个 子序列 是指，通过删除一些（也可以不删除）字符且不干扰剩余字符相对位置所组成的新字符串。（例如，“ACE” 是 “ABCDE” 的一个子序列，而 “AEC” 不是）题目数据保证答案符合 32 位带符号整数范围。

Input: s = "rabbbit", t = "rabbit"
Output: 3
Explanation:
As shown below, there are 3 ways you can generate "rabbit" from S.
rabbbitrabbbitrabbbit
 */
func numDistinct(s string, t string) int {
	m,n := len(s), len(t)
	dp := make([][]int,m+1)
	for i:=0; i<=m; i++ {
		dp[i] = make([]int, n+1)
	}
	for i:=0; i<=m; i++ {
		dp[i][0] = 1
	}
	for i:=1; i<=m; i++ {
		for j:=1; j<=n; j++ {
			if s[i-1]==t[j-1] {
				dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
			} else {
				dp[i][j] = dp[i-1][j]
			}
		}
	}
	return dp[m][n]
}
func f115(){
	fmt.Println(numDistinct("rabbbit", "rabbit"))
}

/* 118. Pascal’s Triangle #
给定一个非负整数 numRows，生成杨辉三角的前 numRows 行。在杨辉三角中，每个数是它左上方和右上方的数的和。

Input: 5
Output:
[
     [1],
    [1,1],
   [1,2,1],
  [1,3,3,1],
 [1,4,6,4,1]
]*/
func generate(numRows int) [][]int {
	result := [][]int{}
	row := []int{1}
	result = append(result, []int{1})
	for i:=1; i<numRows; i++ {
		tmp := []int{1}
		lastNum := row[0]
		for j:=1; j<len(row);j++ {
			tmp = append(tmp, lastNum+row[j])
			lastNum = row[j]
		}
		tmp = append(tmp,1)
		result = append(result, tmp[:])
		row = tmp[:]
	}
	return result
}
func f118(){
	fmt.Println(generate(4))
}

/* 0119.Pascals-Triangle-II/
给定一个非负索引 k，其中 k ≤ 33，返回杨辉三角的第 k 行。 */
func getRow(rowIndex int) []int {
	row := []int{1}
	for i:=1; i<rowIndex; i++ {
		tmp := []int{1}
		lastNum := row[0]
		for j:=0; j<len(row);j++ {
			tmp = append(tmp, lastNum+row[j])
			lastNum = row[j]
		}
		tmp = append(tmp,1)
		row = tmp[:]
	}
	return row
}
func f119(){
	fmt.Println(getRow(3))
}

/* 0120.Triangle/
给定一个三角形，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上。
[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
The minimum path sum from top to bottom is 11 (i.e., 2 + 3 + 5 + 1 = 11).
 */
func minimumTotal(triangle [][]int) int {
	min := func(a,b int) int{if a < b {return a}; return b}
	m := len(triangle)
	for i:=1; i<m; i++ {
		triangle[i][0] += triangle[i-1][0]
		for j:=1; j<i; j++ {
			triangle[i][j] += min(triangle[i-1][j-1], triangle[i-1][j])
		}
		triangle[i][i] += triangle[i-1][i-1]
	}
	result := math.MaxInt32
	for i:=0; i<m; i++ {
		result = min(result, triangle[m-1][i])
	}
	return result
}
func f120(){
	t := [][]int{
		{2},
		{3,4},
		{6,5,7}, 
		{4,1,8,3},
	}
	fmt.Println(minimumTotal(t))
}

/* 0121.Best-Time-to-Buy-and-Sell-Stock/
一次买卖的最大利润
Input: [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
             Not 7-1 = 6, as selling price needs to be larger than buying price. */
func maxProfit(prices []int) int {
	minNow := math.MaxInt32
	result := 0
	for _,price := range prices {
		result = max(result, price-minNow)
		minNow = min(minNow, price)
	}
	return result
}
func f121(){
	fmt.Println(maxProfit([]int{7,1,5,3,6,4}))
}

/* 0122.Best-Time-to-Buy-and-Sell-Stock-II/
 */
func maxProfit2(prices []int) int {
	result := 0
	for i:=1; i<len(prices); i++ {
		if prices[i]>prices[i-1] {
			result += prices[i]-prices[i-1]
		}
	}
	return result
}
func f122(){fmt.Println(maxProfit2([]int{7,1,5,3,6,4}))}

/* 0152.Maximum-Product-Subarray/
给定一个整数数组 nums ，找出一个序列中乘积最大的连续子序列（该序列至少包含一个数）。

Input: [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6. */
func maxProduct(nums []int) int {
	// 对于 0 进行了考虑, 想歪了
	return 0
	// result := math.MinInt32
	// tmpMax := math.MinInt32
	// tmpMin := math.MaxInt32
	// for _,num := range nums {
	// 	if num>0 {
	// 		tmpMax = max(tmpMax, tmpMax*num)
	// 		tmpMin = min(tmpMin, tmpMin*num)
	// 	} else if num<0{
	// 		tmpMax = max(tmpMax, tmpMin*num)
	// 		tmpMin = min(tmpMin, tmpMax*num)
	// 	} else {
	// 		tmpMax = math.MinInt32
	// 		tmpMin = math.MaxInt32
	// 	}
	// 	result = max(result, tmpMax)
	// }
	// return max(result, tmpMax)
}
// 需要维护当前最大和最小, see https://leetcode-cn.com/problems/maximum-product-subarray/solution/cheng-ji-zui-da-zi-shu-zu-by-leetcode-solution/
func maxProduct2(nums []int) int {
	minNow, maxNow, result := nums[0], nums[0], nums[0]
	for i := 1; i < len(nums); i++ {
		if nums[i] < 0 {
			minNow, maxNow = maxNow, minNow
		}
		maxNow = max(nums[i], maxNow*nums[i])
		minNow = min(nums[i], minNow*nums[i])
		result = max(result, maxNow)
	}
	return result
}
func f152(){
	fmt.Println(maxProduct2([]int{2,3,-1,4}))
}

/* 0174.Dungeon-Game/ 
用一个矩阵表示每个房间的 HP 损失(获得), 要求从左上角走到右下角的最小 HP
不同与最短路径和, 要求每一个状态时刻的 HP 都为正数.
采用 DP, 注意要从终点向前遍历. [因为不知道往后的路径需要消耗多少 HP, 因此不满足「无后效性」]

输入: [[-2,-3,3],[-5,-10,1],[10,30,-5]]
输出: 7

https://leetcode-cn.com/problems/dungeon-game/solution/di-xia-cheng-you-xi-by-leetcode-solution/  
*/
func calculateMinimumHP(dungeon [][]int) int {
	max := func(a,b int) int{if a>b {return a}; return b;}
	min := func(a,b int) int{if a>b {return b}; return a;}
	m,n := len(dungeon), len(dungeon[0])
	// dp := make([]int, n)
	// nowHP := make([]int,n)
	// for j:=0;j<n;j++{
	// 	if j==0 {
	// 		if dungeon[0][0] >= 0 {
	// 			dp[0] = 1
	// 			nowHP[0] = 1+dungeon[0][0]
	// 		} else {
	// 			dp[0] = -dungeon[0][0]+1
	// 			nowHP[0] = 1
	// 		}
	// 	} else {
	// 		if dungeon[0][j] + nowHP[j-1] > 0 {
	// 			dp[j] = dp[j-1]
	// 			nowHP[j] = nowHP[j-1]+dungeon[0][j]
	// 		} else {
	// 			dp[j] = dp[j-1] + 1-(nowHP[j-1]+dungeon[0][j])
	// 			nowHP[j] = 1
	// 		}
	// 	}
	// }
	// for i:=1;i<m; i++ {
	// 	if nowHP[0]+dungeon[i][0]>0 {
	// 		// dp[0]
	// 		nowHP[0]  += dungeon[i][0]
	// 	}
	// 	for j:=1;j<n;j++ {
	// 		dungeon[i][j] += max(dungeon[i][j-1], dungeon[i-1][j])
	// 	}
	// }
	// return dp[n-1]

	dp := make([][]int, m)
	for i:=0; i<m; i++ {
		dp[i] = make([]int, n)
	}
	dp[m-1][n-1] = max(1, 1-dungeon[m-1][n-1])
	for i:=m-2; i>=0; i-- {
		dp[i][n-1] = max(1, dp[i+1][n-1]-dungeon[i][n-1])
	}
	for j:=n-2; j>=0; j-- {
		dp[m-1][j] = max(1, dp[m-1][j+1]-dungeon[m-1][j])
	}
	for i:=m-2; i>=0; i-- {
		for j:=n-2; j>=0; j-- {
			dp[i][j] = max(1, min(dp[i][j+1], dp[i+1][j])-dungeon[i][j])
		}
	}
	return dp[0][0]
}
func f174(){
	fmt.Println(calculateMinimumHP([][]int{
		{-2,-3,3}, 
		{-5,-10,1},
		{10,30,-5},
	}))
}

/* 0198.House-Robber/
你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。
给定一个代表每个房屋存放金额的非负整数数组，计算你在不触动警报装置的情况下，能够偷窃到的最高金额。

Input: [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
             Total amount you can rob = 2 + 9 + 1 = 12.*/
func rob198(nums []int) int {
	if len(nums)==1{return nums[0]}
	max := func(a,b int) int {if a>b {return a}; return b}
	dp1, dp2 := nums[0], max(nums[0], nums[1])
	for i:=2;i<len(nums);i++ {
		dp1, dp2 = dp2, max(dp2, dp1+nums[i])
	}
	return dp2
}

/* 0213.House-Robber-II/
这个地方所有的房屋都围成一圈，这意味着第一个房屋和最后一个房屋是紧挨着的。 */
func rob213(nums []int) int {
	if len(nums)==1 {return nums[0]}
	max := func(a,b int) int {if a>b {return a}; return b}
	n := len(nums)
	return max(rob198(nums[:n-1]), rob198(nums[1:]))
}



/* 0264.Ugly-Number-II/
Given an integer n, return the nth ugly number.

Ugly number is a positive number whose prime factors only include 2, 3, and/or 5.

Input: n = 10
Output: 12
Explanation: [1, 2, 3, 4, 5, 6, 8, 9, 10, 12] is the sequence of the first 10 ugly numbers.*/
func nthUglyNumber(n int) int {
	uglyNumbers := []int{1}
	p2, p3, p5 := 0, 0, 0
	for len(uglyNumbers) < n {
		x2, x3, x5 := uglyNumbers[p2]*2, uglyNumbers[p3]*3, uglyNumbers[p5]*5
		xx := min(min(x2, x3), x5)
		uglyNumbers = append(uglyNumbers, xx)
		// 注意可能有重复, 例如 2*3, 3*2 因此不是 else if 
		if xx == x2 {
			p2++
		}
		if xx == x3 {
			p3++
		} 
		if xx == x5 {
			p5++
		}
	}
	return uglyNumbers[n-1]
}
// 方法二: heap
type hp struct { sort.IntSlice }
func (h *hp) Push(v interface{}) {h.IntSlice = append(h.IntSlice, v.(int))}
func (h *hp) Pop() interface{} {
	a := h.IntSlice;
	v := a[len(a)-1];
	h.IntSlice = a[:len(a)-1];
	return v
}
func nthUglyNumber2(n int) int {
	h := &hp{sort.IntSlice{1}}
	seen := map[int]struct{}{1:{}}
	for i:=1; ; i++ {
		x := heap.Pop(h).(int)
		if i ==n {
			return x
		}
		for _,f := range []int{2,3,5} {
			next := x*f
			if _,has := seen[next]; !has {
				heap.Push(h, next)
				seen[next] = struct{}{}
			}
		}
	}
}

func f264(){
	fmt.Println(nthUglyNumber2(10))
}

/* 0279.Perfect-Squares/
判断一个数最少是多少个完全平方数之和

Input: n = 12
Output: 3
Explanation: 12 = 4 + 4 + 4.

方法一：动态规划 */
func numSquares(n int) int {
	// isSquare := func(x int) bool {
	// 	r := int(math.Sqrt(float64(x)))
	// 	return x==r*r
	// }
	min := func(a,b int)int{if a<b {return a}; return b}
	dp := make([]int, n+1)
	dp[1] = 1
	for i:=2; i<=n; i++ {
		minn := math.MinInt64
		for j:=1; j*j<=i; j++ {
			minn = min(minn, dp[i-j*j])
		}
		// 当 i 为平方数, 例如为 4 时, minn=dp[0]=0
		dp[i] = minn+1
	}
	return dp[n]
}

/* 0300.Longest-Increasing-Subsequence/
Given an unsorted array of integers, find the length of longest increasing subsequence.

Input: [10,9,2,5,3,7,101,18]
Output: 4 
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.*/
func lengthOfLIS(nums []int) int {
	max := func (a,b int)int { if a>b { return a}; return b}
	dp := make([]int, len(nums))
	dp[0] = 1
	// dp[i] 为以第 i 个元素结果为 LIS 长度, 因此注意返回的不是最后一个元素
	result := 0
	for i:=1;i<len(nums);i++ {
		maxx := 0
		for j:=0;j<i; j++ {
			if nums[j]<nums[i] {
				maxx = max(maxx, dp[j])
			}
		}
		dp[i] = maxx+1
		result = max(result, dp[i])
	}
	return result
}
// 方法二：贪心 + 二分查找
func lengthOfLIS2(nums []int) int {
	// d[i] 记录长度为 i+1 的IS 的最小结尾元素
	d := []int{}
	for _,num := range nums {
		if len(d)==0 || d[len(d)-1] < num {
			d = append(d, num)
		} else {
			// 目标: 找到最后一个 <num 的元素, 更新该元素后面一个位置
			// 下面的错误写法中, 可能遇到 最后出现 len(d)=0 && pos=0 有问题
			// l,r,pos := 0,len(d)-1,0
			// for l<=r {
			// 	mid := (l+r) >> 1
			// 	if d[mid]<num {
			// 		pos = mid
			// 		l = mid+1
			// 	} else {
			// 		r = mid-1
			// 	}
			// }
			// d[pos+1] = num
			
			// 这里将 pos 记录为最早的 >num 的元素, 避免了问题
			l,r,pos := 0, len(d)-1, len(d)-1
			for l<=r{
				mid := (l+r)>>1
				if d[mid]>=num{
					pos = mid
					r = mid-1
				} else {
					l = mid+1
				}
			}
			d[pos] = num
		}
	}
	return len(d)
}

func f300(){
	fmt.Println(lengthOfLIS2([]int{1,3,6,7,9,4,10,5,6}))
	fmt.Println(lengthOfLIS2([]int{10,9,2,5,3,7,101,18}))
}


/* 0309.Best-Time-to-Buy-and-Sell-Stock-with-Cooldown/
买卖股票, 有 Cooldown 即卖出后第二天不能直接买入
Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete as many transactions as you like (ie, buy one and sell one share of the stock multiple times) with the following restrictions:

You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).
After you sell your stock, you cannot buy stock on next day. (ie, cooldown 1 day)

Input: [1,2,3,0,2]
Output: 3 
Explanation: transactions = [buy, sell, cooldown, buy, sell]*/
func maxProfit309(prices []int) int {

}


func main(){
	// f97()
	// f115()
	// f118()
	// f119()
	// f120()
	// f121()
	// f122()
	// f152()
	// f174()
	// f264()
	f300()
}