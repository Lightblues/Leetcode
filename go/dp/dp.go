package main

import (
	"fmt"
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



func main(){
	f55()
}