package main

import (
	"fmt"
	"math"
	"math/bits"
	"sort"
	"strconv"
	"strings"
)

// TreeNode node type
type TreeNode struct {
	Val int
	Left *TreeNode
	Right *TreeNode
}

/* 0017.Letter-Combinations-of-a-Phone-Number/
Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent.
给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。
Input: "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].*/
var letterMap = []string{
	" ",    //0
	"",     //1
	"abc",  //2
	"def",  //3
	"ghi",  //4
	"jkl",  //5
	"mno",  //6
	"pqrs", //7
	"tuv",  //8
	"wxyz", //9
}
// 解法一 DFS
func letterCombinations(digits string) []string {
	if len(digits)==0{
        return []string{}
    }
	results := []string{}

	var findCombination func(digits *string, index int, s string)
	findCombination = func(digits *string, index int, s string) {
		if index==len(*digits) {
			results = append(results, s)
			return
		}
		letterMapped := letterMap[(*digits)[index]-'0']
		for _, letter := range letterMapped {
			findCombination(digits, index+1, s+string(letter))	// char 2 string
		}
	}
	findCombination(&digits, 0, "")
	return results
}
// 非递归? 写不来
// func letterCombinations2(digits string)[]string {
// 	if len(digits)==0{
//         return []string{}
//     }
// 	results := []string{}
// 	tmp := ""
// 	for _, digit := range digits {
// 		letterMapped := letterMap[digit-'0']
// 		for _,letter := range letterMapped {
// 			tmp += string(letter)
// 		}
// 	}
// 	return results
// }
// 解法三 回溯（参考回溯模板，类似DFS）
func letterCombinations3(digits string)[]string {
	if len(digits)==0{
        return []string{}
    }
	results := []string{}
	var backtraking func(res string, digits string)
	backtraking = func(res string, digits string) {
		if digits == ""{
			results = append(results, res)
			return
		}
		k := digits[0]		// char
		digits = digits[1:]
		letterMapped := letterMap[k-'0']
		for _,letter := range letterMapped {
			backtraking(res+string(letter), digits)
		}
	}
	backtraking("", digits)
	return results
}

func f17(){
	fmt.Println(letterCombinations("23"))
}

/* 0037.Sudoku-Solver/ */
type position struct {
	x int
	y int
}
func solveSudoku(board [][]byte) {
	positions := []position{}
	isSuccess := false
	for i := 0; i < len(board); i++ {
		for j := 0; j < len(board[0]); j++ {
			if board[i][j] == '.' {
				positions = append(positions, position{i,j})
			}
		}
	}
	putSudoku(&board, positions, 0, &isSuccess)
}
func putSudoku(board *[][]byte, pos []position, index int, succ *bool) {
	if *succ {
		return
	}
	if index==len(pos){
		*succ = true
		return
	}
	for i := 1; i < 10; i++ {
		if checkSudoku(board, pos[index], i) {
			(*board)[pos[index].x][pos[index].y] = byte(i)+'0'
			putSudoku(board, pos, index+1, succ)
			if *succ {	// 若找到一个解则直接返回
				return
			}
		}
		(*board)[pos[index].x][pos[index].y] = '.'		// 恢复, 回溯

	}
}
func checkSudoku(board *[][]byte, pos position, val int) bool {
	// 判断横行是否有重复数字
	for i:=0; i<len((*board)[0]); i++ {
		if (*board)[pos.x][i]!='.' && (*board)[pos.x][i] == byte(val)+'0' {
			return false
		}
	}
	// 判断竖行是否有重复数字
	for i:=0; i<len((*board)); i++ {
		if (*board)[i][pos.y]!='.' && int((*board)[i][pos.y]-'0')==val {
			return false
		}
	}
	// 判断九宫格是否有重复数字
	initX, initY := pos.x-pos.x%3, pos.y-pos.y%3
	for i:=initX; i<initX+3;i++{
		for j:=initY; j<initY+3; j++{
			if (*board)[i][j]!='.' && int((*board)[i][j]-'0')==val{
				return false
			}
		}
	}
	return true
}
func f37(){
	// 
}

/* 0039.Combination-Sum/
给定一个无重复元素的数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合。
candidates 中的数字可以无限制重复被选取。 
Input: candidates = [2,3,5], target = 8,
A solution set is:
[
  [2,2,2,2],
  [2,3,3],
  [3,5]
] */
func combinationSum(candidates []int, target int) [][]int {
	c, res := []int{}, [][]int{}
	sort.Ints(candidates)
	findcombinationSum(candidates, target, 0, c, &res)
	return res
}
func findcombinationSum(candidates []int, target int, index int, c []int, res *[][]int) {
	if target<0 {return}
	if target==0 {
		*res = append(*res, append([]int{}, c...))
		return
	}
	for i:=index; i<len(candidates); i++ {
		if candidates[i]>target {break}
		c = append(c, candidates[i])
		findcombinationSum(candidates, target-candidates[i], i, c, res)
		c = c[:len(c)-1]
	}
}
func f39(){
	fmt.Println(combinationSum([]int{2,3,5}, 8))
}

/* 0040.Combination-Sum-II/
给定一个数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合
Input: candidates = [2,5,2,1,2], target = 5,
A solution set is:
[
  [1,2,2],
  [5]
] */
func combinationSum2(candidates []int, target int) [][]int {
	sort.Ints(candidates)
	tmp, res := []int{}, [][]int{}
	findCombinationSum(candidates, target, 0, tmp, &res)
	return res
}
func findCombinationSum(nums []int, target int, index int, tmp []int, res *[][]int) {
	if target == 0 {
		*res = append(*res, append([]int{}, tmp...))
		return
	}
	for i:=index; i<len(nums); i++ {
		if nums[i] > target {break}
		if i>index && nums[i]==nums[i-1]{	// 这里是去重的关键逻辑,本次不取重复数字，下次循环可能会取重复数字
			continue
		}
		tmp = append(tmp, nums[i])
		findCombinationSum(nums, target-nums[i], i+1, tmp, res)
		tmp = tmp[:len(tmp)-1]
	}
}
func f40(){
	fmt.Println(combinationSum2([]int{2,5,2,1,2}, 5))
}
/* 0046.Permutations/
给定一个没有重复数字的序列，返回其所有可能的全排列。 */
func permute(nums []int) [][]int {
	result := [][]int{}
	now := make([]int, len(nums))
	used := make([]bool, len(nums))		// 用一个列表记录该位置是否被用过
	var dfs func(index int)
	dfs = func(index int) {
		if index == len(nums) {
			tmp := append([]int{}, now...)
			result = append(result, tmp)
			return
		}
		for i:=0; i<len(nums); i++ {
			if !used[i] {
				now[index] = nums[i]
				used[i] = true
				dfs(index+1)
				used[i] = false
				// now = now[:index]
			}
		}
	}
	dfs(0)
	return result
}
func f46(){
	fmt.Println(permute([]int{1,2,3}))
}

/* /0047.Permutations-II/
这一题是第 46 题的加强版，第 46 题中求数组的排列，数组中元素不重复，但是这一题中，数组元素会重复，所以需要最终排列出来的结果需要去重。 */
func permuteUnique(nums []int) [][]int {
	sort.Ints(nums)
	now, used, result := make([]int, len(nums)), make([]bool, len(nums)), [][]int{}
	var dfs func(index int)
	dfs = func(index int) {
		if index==len(nums) {
			result = append(result, append([]int{}, now...))
			return
		}
		for i:=0; i<len(nums); i++ {
			if !used[i] {
				// 去重逻辑: 前一个相同的数字没有用到, 则这一个不考虑
				if i>0 && nums[i-1]==nums[i] && !used[i-1] { 
					continue 
				}
				now[index] = nums[i]
				used[i] = true
				dfs(index+1)
				used[i] = false
			}
		}
	}
	dfs(0)
	return result
}
func f47(){
	fmt.Println(permuteUnique([]int{1,1,2}))
}

/* 0051.N-Queens/
Given an integer n, return all distinct solutions to the n-queens puzzle.
Input: 4
Output: [
 [".Q..",  // Solution 1
  "...Q",
  "Q...",
  "..Q."],

 ["..Q.",  // Solution 2
  "Q...",
  "...Q",
  ".Q.."]
]
Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above. */
func solveNQueens(n int) [][]string {
	// col, dia1, dia2 记录列和两个对角线的位置是否被占用
	// row 记录每一行所放的 queen 位置
	col, dia1, dia2, row, res := make([]bool, n), make([]bool, 2*n-1), make([]bool, 2*n-1), []int{}, [][]string{}
	putQueen(n, 0, &col, &dia1, &dia2, &row, &res)
	return res
}
// 尝试在一个n皇后问题中, 摆放第index行的皇后位置
func putQueen(n, index int, col, dia1, dia2 *[]bool, row *[]int, res *[][]string) {
	if index==n{
		*res = append(*res, generateBoard(row))
		return
	}
	for i:=0; i<n; i++ {
		if !(*col)[i] && !(*dia1)[index+i] && !(*dia2)[index-i+n-1] {
			*row = append(*row, i)
			(*col)[i] = true
			(*dia1)[index+i] = true
			(*dia2)[index-i+n-1] = true
			putQueen(n, index+1, col, dia1, dia2, row, res)
			(*col)[i] = false
			(*dia1)[index+i] = false
			(*dia2)[index-i+n-1] = false
			*row = (*row)[:len(*row)-1]
		}
	}
}
func generateBoard(row *[]int) []string {
	result := make([]string, len(*row))
	tmp := ""
	for j:=0;j<len(*row);j++ {
		tmp += "."
	}
	for index,r := range *row {
		t := []byte(tmp)
		t[r] = 'Q'
		result[index] = string(t)
	}
	return result
}
func f51(){
	fmt.Println(solveNQueens(4))
}

/* 0052.N-Queens-II/ 只要返回数量 */
func totalNQueens(n int) int {
	col, dia1, dia2 := make([]bool, n), make([]bool, 2*n-1), make([]bool, 2*n-1)
	rows := []int{}
	result := 0
	dfsTotalNQueen(n, 0, &col, &dia1, &dia2, &rows, &result)
	return result
}
func dfsTotalNQueen(n, index int, col, dia1, dia2 *[]bool, rows *[]int, result *int) {
	if index==n{
		*result++
		return
	}
	for i := 0; i < n; i++ {
		if !(*col)[i] && !(*dia1)[i+index] && !(*dia2)[i-index+n-1] {
			*rows = append(*rows, i)
			(*col)[i] = true
			(*dia1)[i+index] = true
			(*dia2)[i-index+n-1] = true
			dfsTotalNQueen(n, index+1, col, dia1, dia2, rows, result)
			(*col)[i] = false
			(*dia1)[i+index] = false
			(*dia2)[i-index+n-1] = false
			*rows = (*rows)[:len(*rows)-1]
		}
	}
}
func f52(){
	fmt.Println(totalNQueens(4))
}

/* 0077.Combinations/
Given two integers n and k, return all possible combinations of k numbers out of 1 … n.
Input: n = 4, k = 2
Output:
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
] */
func combine(n int, k int) [][]int {
	// used := make([]bool, n)
	record := []int{}
	result := [][]int{}
	dfsCombine(n,k,0,0, &record, &result)
	return result
}
func dfsCombine(n, k, index, last int, record *[]int, result *[][]int){
	if index==k{
		*result = append(*result, append([]int{}, (*record)...))
		return
	}
	for i:=last+1; i<n+1; i++{
		(*record) = append(*record, i)
		dfsCombine(n,k,index+1, i, record, result)
		*record = (*record)[:len(*record)-1]
	}
}
func f77(){
	fmt.Println(combine(4,2))
}

/* /0078.Subsets/
Given a set of distinct integers, nums, return all possible subsets (the power set).
Input: nums = [1,2,3]
Output:
[
  [3],
  [1],
  [2],
  [1,2,3],
  [1,3],
  [2,3],
  [1,2],
  []
] */
func subsets(nums []int) [][]int {
	tmp := []int{}
	result := [][]int{}
	dfsSubsets(0, &nums, &tmp, &result)
	return result
}
func dfsSubsets(index int, nums, tmp *[]int, result *[][]int){
	if index==len(*nums){
		*result = append(*result, append([]int{}, *tmp...))
		return
	}
	*tmp = append(*tmp, (*nums)[index])
	dfsSubsets(index+1, nums, tmp, result)
	*tmp = (*tmp)[:len(*tmp)-1]
	dfsSubsets(index+1, nums, tmp, result)
}
func f78(){
	fmt.Println(subsets([]int{1,2,3}))
}

/* 0090.Subsets-II/ `中`
Given a collection of integers that might contain duplicates, nums, return all possible subsets (the power set).
Input: [1,2,2]
Output:
[
  [2],
  [1],
  [1,2,2],
  [2,2],
  [1,2],
  []
]*/
func subsetsWithDup(nums []int) [][]int {
	sort.Ints(nums)		// 排序
	tmp, result := []int{}, [][]int{}
	dfsSubsetsWithDup(0, false, &nums, &tmp, &result)
	return result
}
// 其中 lastUsed 标记上一个元素是否被用到, 当 1. 前后元素相同; 2. 上一个元素未被用到的时候, 应该跳过
func dfsSubsetsWithDup(index int, lastUsed bool, nums, tmp *[]int, result *[][]int){
	if index==len(*nums) {
		*result = append(*result, append([]int{}, *tmp...))
		return
	}
	dfsSubsetsWithDup(index+1, false, nums, tmp, result)
	if index>0 && (*nums)[index-1]==(*nums)[index] && !lastUsed {return}	// 跳过
	*tmp = append(*tmp, (*nums)[index])
	dfsSubsetsWithDup(index+1, true, nums, tmp,result)
	*tmp = (*tmp)[:len(*tmp)-1]
}
func f90(){
	fmt.Println(subsetsWithDup([]int{1,1,2}))
}

/* 0079.Word-Search/ 
board =
[
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]

Given word = "ABCCED", return true.
Given word = "SEE", return true.
Given word = "ABCB", return false. */
func exist(board [][]byte, word string) bool {
	directions := [][]int{
		{-1,0},
		{1,0},
		{0,-1},
		{0,1},
	}
	visited := make([][]bool, len(board))
	for i := 0; i < len(visited); i++ {
		visited[i] = make([]bool, len(board[0]))
	}
	m,n := len(board), len(board[0])
	var dfs func(x,y,remainLen int) bool
	dfs = func(x,y,remainLen int) bool{
		if remainLen == 0 { return true }
		for i:=0;i<len(directions);i++ {
			nx,ny := x+directions[i][0], y+directions[i][1]
			if nx>=0 && ny>=0 && nx<m && ny<n && !visited[nx][ny] && board[nx][ny]==word[len(word)-remainLen] {
				visited[nx][ny] = true
				if dfs(nx,ny,remainLen-1) {
					return true
				}
				visited[nx][ny] = false
			}
		}
		return false
	}
	for i:=0; i<m; i++ {
		for j:=0; j<n; j++ {
			// 改进: 可以将这个判断放到 dfs 最前面
			if board[i][j] == word[0] {
				visited[i][j] = true
				if dfs(i,j,len(word)-1) {
					return true
				}
				visited[i][j] = false
			}
		}
	}
	return false
}
func f79(){
	// [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
	// "ABCB"
	fmt.Println(exist(
		[][]byte{
			{'A','B','C','E'},
			{'S','F','C','S'},
			{'A','D','E','E'},
		}, "ABCB"))
}

/* 0089.Gray-Code/
The gray code is a binary numeral system where two successive values differ in only one bit.
Given a non-negative integer n representing the total number of bits in the code, print the sequence of gray code. A gray code sequence must begin with 0. 
Input: 2
Output: [0,1,3,2]
Explanation:
00 - 0
01 - 1
11 - 3
10 - 2

For a given n, a gray code sequence may not be uniquely defined.
For example, [0,2,3,1] is also a valid gray code sequence.

00 - 0
10 - 2
11 - 3
01 - 1

Input: 0
Output: [0]
Explanation: We define the gray code sequence to begin with 0.
             A gray code sequence of n has size = 2n, which for n = 0 the size is 20 = 1.
             Therefore, for n = 0 the gray code sequence is [0].

生成方式: 
1. 直接排列. 以二进制为0值的格雷码为第零项，第一项改变最右边的位元，第二项改变右起第一个为1的位元的左边位元，第三、四项方法同第一、二项，如此反复，即可排列出n个位元的格雷码。
2. 镜像排列. n位元的格雷码可以从n-1位元的格雷码以上下镜射后加上新位元的方式快速的得到，如右图所示一般。

观察 1-4 位 Gray码, 结合 wiki, 可以看到, 
1. n位Gray码的前 2**(n-1) 位正是 n-1 位 Gray码. 
2. Gray码最大的数字是 10000 
3. 上面两种方式生成的顺序是一致的 */

// 解法一 递归方法，时间复杂度和空间复杂度都较优
// https://zh.wikipedia.org/wiki/%E6%A0%BC%E9%9B%B7%E7%A0%81
func grayCode(n int) []int {
	res := []int{}
	tmp := make([]int, n)
	genGrayCode(1<<n, 0, &tmp, &res)
	return res
}
func genGrayCode(n, step int, num *[]int, res *[]int) {
	// if n==0 {return}		// 这里的 n 其实没啥用, 下面的 index 判断即可
	*res = append(*res, binary2int(*num))
	if step%2 == 0 {
		(*num)[len(*num)-1] = flapGrayCode((*num)[len(*num)-1])
	} else {
		index := len(*num) - 1
		for ; index>=0; index-- {
			if (*num)[index] == 1 { break }
		}
		if index == 0 { return }	// 终止条件, Gray 编码的最大数字是 1000 的形式
		(*num)[index-1] = flapGrayCode((*num)[index-1])
	}
	genGrayCode(n-1, step+1, num, res)
}
func flapGrayCode(n int) int {
	//翻转二进制
	if n==0 {return 1}
	return 0
}
func binary2int(num []int) int {
	// 二进制转数字
	res := 0
	rad := 1
	for i:=len(num)-1; i>=0; i-- {
		res += num[i] * rad
		rad <<= 1
	}
	return res
}

// 方式二, 镜像翻转
func grayCode2(n int) []int {
	res := []int{0}
	for i:=0; i<n; i++ {
		for j:=len(res)-1; j>=0; j-- {
			res = append(res, res[j]+1<<i)
		}
	}
	return res
}
func f89(){
	fmt.Println(grayCode2(3))		// [0 1 3 2 6 7 5 4]
}

/* 0093.Restore-IP-Addresses/
Given a string containing only digits, restore it by returning all possible valid IP address combinations.
Input: "25525511135"
Output: ["255.255.11.135", "255.255.111.35"] */
func restoreIPAddresses(s string) []string {
	result := []string{}
	ips := []int{}
	dfsRestoreIPAddresses(s, 0, ips, &result)
	return result
}
func dfsRestoreIPAddresses(s string, index int, ip []int, result *[]string) {
	if index == len(s) {
		if len(ip) == 4 {
			*result = append(*result, convertIPToString(ip))
		}
		return
	}
	if index==0 {
		num,_ := strconv.Atoi(string(s[0]))	// string(char) 转为 string·
		ip = append(ip, num)
		dfsRestoreIPAddresses(s, index+1, ip, result)
	} else {
		num, _ := strconv.Atoi(string(s[index]))
		next := ip[len(ip)-1] * 10 + num
		if next<=255 && ip[len(ip)-1]!=0 {		// 注意IP中无法出现 01 这种
			ip[len(ip)-1] = next
			dfsRestoreIPAddresses(s, index+1, ip, result)
			ip[len(ip)-1] /= 10
		}
		if len(ip)<4 {
			ip = append(ip, num)
			dfsRestoreIPAddresses(s, index+1, ip, result)
			// ip = ip[:len(ip)-1]
		}
	}
}
func convertIPToString(ip []int) string {
	res := strconv.Itoa(ip[0])
	for i:=1; i<len(ip); i++ {
		res += "." + strconv.Itoa(ip[i])
	}
	return res
}
func f93(){
	fmt.Println(restoreIPAddresses("25525511135"))
}

/* 0095.Unique-Binary-Search-Trees-II/
给定一个整数 n，生成所有由 1 … n 为节点所组成的二叉搜索树。
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
   2     1         2                 3 */
func generateTrees(n int) []*TreeNode {
	return dfsGenTrees(1,n)
}
func dfsGenTrees(start, end int) []*TreeNode {
	// 返回由 [s,e] 构成的所有 BST
	trees := []*TreeNode{}
	if start>end {
		trees = append(trees, nil)
		return trees
	}
	for i := start; i<=end; i++ {
		left := dfsGenTrees(start, i-1)
		right := dfsGenTrees(i+1, end)
		for _,l := range left{
			for _,r := range right{
				root := &TreeNode{i, l, r}
				trees = append(trees, root)
			}
		}
	}
	return trees
}

/* 0127.Word-Ladder/
Given two words (beginWord and endWord), and a dictionary’s word list, find the length of shortest transformation sequence from beginWord to endWord, such that:

Only one letter can be changed at a time.
Each transformed word must exist in the word list. Note that beginWord is not a transformed word.

Input:
beginWord = "hit",
endWord = "cog",
wordList = ["hot","dot","dog","lot","log","cog"]

Output: 5

Explanation: As one shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog",
return its length 5. 
https://leetcode-cn.com/problems/word-ladder/solution/dan-ci-jie-long-by-leetcode-solution/*/
func ladderLength(beginWord string, endWord string, wordList []string) int {
	word2id := map[string]int{}
	wordNum := 0
	beginInWords, endInWords := false, false
	for _,word := range wordList {
		if beginWord == word {beginInWords = true}
		if endWord == word {endInWords = true}
		word2id[word] = wordNum
		wordNum++
	}
	if !endInWords {return 0}	// 若 end 不在字典中, 返回 0
	if !beginInWords {
		word2id[beginWord] = wordNum
		wordNum++
	}
	// edge
	edges := make([][]int, len(word2id))
	for i,w1 := range wordList {
		for j,w2 :=range wordList[i+1:]{
			if i==j {continue}
			if ladderHasEdge(w1,w2) {
				id1, id2 := word2id[w1], word2id[w2]
				edges[id1] = append(edges[id1], id2)
				edges[id2] = append(edges[id2], id1)
			}
		}
	}
	if !beginInWords {
		for _,w := range wordList {
			if ladderHasEdge(w, beginWord) {
				id1,id2 := word2id[beginWord],word2id[w]
				edges[id1] = append(edges[id1], id2)
				edges[id2] = append(edges[id2], id1)
			}
		}
	}
	// BFS
	inf := math.MaxInt32
	dist := make([]int, len(word2id))
	for i := range dist {
		dist[i] = inf
	}
	begin, end := word2id[beginWord], word2id[endWord]
	dist[begin] = 0
	queue := []int{begin}
	for len(queue) > 0 {
		u := queue[0]
		queue = queue[1:]
		if u==end {
			return dist[u] + 1
		}
		for _,v := range edges[u] {
			if dist[v] == inf {
				// 仅当第一次遍历到 v 节点时才加入 queue
				dist[v] = dist[u] + 1
				queue = append(queue, v)
			}
		}
	}
	return 0 // 说明无法到达
}
func ladderHasEdge(s1, s2 string) bool {
	count := 0
	for i:=0; i<len(s1); i++ {
		if s1[i]!=s2[i] {
			count++
			if count > 1{return false}
		}
	}
	if count == 1{return true}
	return false
}
// 优化建图, 虚拟节点
func ladderLength1(beginWord string, endWord string, wordList []string) int {
    wordID := map[string]int{}
    graph := [][]int{}
    addWord := func(word string) int {
        id, has := wordID[word]
        if !has {
            id = len(wordID)
            wordID[word] = id
            graph = append(graph, []int{})
        }
        return id
    }
    addEdge := func(word string) int {
        id1 := addWord(word)
        s := []byte(word)
		// 虚拟节点
        for i, b := range s {
            s[i] = '*'
            id2 := addWord(string(s))
            graph[id1] = append(graph[id1], id2)
            graph[id2] = append(graph[id2], id1)
            s[i] = b
        }
        return id1
    }

    for _, word := range wordList {
        addEdge(word)
    }
    beginID := addEdge(beginWord)
    endID, has := wordID[endWord]
    if !has {
        return 0
    }

    const inf int = math.MaxInt64
    dist := make([]int, len(wordID))
    for i := range dist {
        dist[i] = inf
    }
    dist[beginID] = 0
    queue := []int{beginID}
    for len(queue) > 0 {
        v := queue[0]
        queue = queue[1:]
        if v == endID {
            return dist[endID]/2 + 1
        }
        for _, w := range graph[v] {
            if dist[w] == inf {
                dist[w] = dist[v] + 1
                queue = append(queue, w)
            }
        }
    }
    return 0
}
func f127(){
	fmt.Println(ladderLength(
		"hit", "cog", []string{"hot","dot","dog","lot","log","cog"},
	))
}

/* 0126.Word-Ladder-II/
给出上一题中的所有路径 Given two words (beginWord and endWord), and a dictionary’s word list, find all shortest transformation sequence(s) from beginWord to endWord
Input:
beginWord = "hit",
endWord = "cog",
wordList = ["hot","dot","dog","lot","log","cog"]

Output:
[
  ["hit","hot","dot","dog","cog"],
  ["hit","hot","lot","log","cog"]
]*/
// 这里的实现更简洁清晰 https://books.halfrost.com/leetcode/ChapterFour/0100~0199/0126.Word-Ladder-II/ 
func findLadders(beginWord string, endWord string, wordList []string) [][]string {
	// nodes
	numWords := 0
	word2id := map[string]int{}
	id2word := map[int]string{}
	beginInWords, endInWords := false, false
	for _,w := range wordList {
		if w == beginWord {beginInWords=true}
		if w == endWord {endInWords=true}
		word2id[w] = numWords
		id2word[numWords] = w
		numWords++
	}
	if !endInWords {return [][]string{}}
	if !beginInWords {
		word2id[beginWord] = numWords
		id2word[numWords] = beginWord
		numWords++
	}
	// edges
	edges := make([][]int, numWords)
	for i,w1 := range wordList {
		for _,w2 := range wordList[i+1:] {
			// if i==j {continue;}
			if ladderHasEdge(w1,w2) {
				id1, id2 := word2id[w1], word2id[w2]
				edges[id1] = append(edges[id1], id2)
				edges[id2] = append(edges[id2], id1)
			}
		}
	}
	if !beginInWords {
		for _,w := range wordList {
			if ladderHasEdge(w, beginWord) {
				id1, id2 := word2id[w], word2id[beginWord]
				edges[id1] = append(edges[id1], id2)
				edges[id2] = append(edges[id2], id1)
			}
		}
	}
	// dfs
	find := false
	begin, end := word2id[beginWord], word2id[endWord]
	// queue := []int{begin}
	pathRecord := [][]int{
		{begin},
	}
	tmpPathRecord := [][]int{}
	result := [][]string{}
	// 记录节点是否被访问过
	inf := math.MaxInt32
	dist := make([]int, len(word2id))
	for i := range dist {
		dist[i] = inf
	}
	dist[begin] = 0

	// 用一个 queLen 来记录是否遍历完当前层
	queLen := 1
	for len(pathRecord) > 0 {
		queLen--
		// 每次都遍历完一整层, 用 tmpQueue 记录下一层
		// u := queue[0]
		// queue = queue[1:]
		path := pathRecord[0]
		pathRecord = pathRecord[1:]
		u := path[len(path)-1]
		// if u==end {
		// 	find = true
		// 	result = append(result, ladderConvertPath(path, &id2word))
		// } else {
		
		for _,v := range edges[u] {
			newPath := append(append([]int{}, path...), v)
			if v==end {
				find = true
				result = append(result, ladderConvertPath(&newPath, &id2word))
			} else {
				if !(dist[v]<dist[u]+1) {
					// 不重复(剪枝)的关键: 只有当前层搜索到同一个之前未搜索过的节点的时候才加入序列. 当然不加其实也不会死循环
					dist[v] = dist[u]+1
					// tmpQueue = append(tmpQueue, v)
					tmpPathRecord = append(tmpPathRecord, newPath)
				}
			}
		}
		// 进入下一层
		if queLen==0{
			// 如果找到了直接退出下一层遍历
			if find {
				return result
			}
			// queue = tmpQueue
			pathRecord = tmpPathRecord
			queLen = len(tmpPathRecord)
			tmpPathRecord = [][]int{}
		}
	}
	return [][]string{}
}
func ladderConvertPath(path *[]int, id2word *map[int]string) []string {
	result := []string{}
	for _,id := range *path {
		result = append(result, (*id2word)[id])
	}
	return result
}
func f126(){
	fmt.Println(findLadders(
		"hit", "cog", []string{"hot","dot","dog","lot","log","cog"},
	))
}

/* 0131.Palindrome-Partitioning/ 
Given a string s, partition s such that every substring of the partition is a palindrome.
Return all possible palindrome partitioning of s.
Input: "aab"
Output:
[
  ["aa","b"],
  ["a","a","b"]
]*/
func partition9(s string) [][]string {
	return dfsPartition(s)
}
// 会重复 DFS s[i:j], 复杂度很高, 会超时
func dfsPartition(s string) [][]string {
	result := [][]string{}
	if len(s) == 1 {
		return append(result, []string{s})
	}
	if isPalindrome(s){
		result = append(result, []string{s})
	}
	for index:=1; index<=len(s)-1; index++ {
		left, right := s[:index], s[index:]
		lResult := dfsPartition(left)
		rResult := dfsPartition(right)
		for _,l := range lResult {
			for _,r := range rResult {
				// result = append(result, append(l, r...)) 
				//这个会出错?
				tmp := append([]string{}, l...)
				tmp = append(tmp, r...)
				result = append(result, tmp)
			}
		}
	}
	return removeDup(&result)
}
// 去重 字符串列表
func removeDup(strings *[][]string) [][]string {
	result := [][]string{}
	records := map[string]bool{}
	for _,ss:=range *strings {
		record := ""
		for _,s:=range ss{
			record += "-"+s
		}
		if !records[record] {
			records[record] = true
			result = append(result, ss)
		}
	}
	return result
}
func isPalindrome(s string) bool {
	for l,r:=0,len(s)-1; l<r; {
		if s[l]!=s[r] {return false}
		l++; r--
	}
	return true
}
// https://leetcode-cn.com/problems/palindrome-partitioning/solution/fen-ge-hui-wen-chuan-by-leetcode-solutio-6jkv/
func partition(s string) [][]string {
	// dp := make([]bool, len(s))

	tmp := []string{}
	result := [][]string{}
	dfsPartition2(&s, 0, &tmp, &result)
	return result
}
func dfsPartition2(s *string, index int, tmp *[]string, result *[][]string){
	if index==len(*s) {
		*result = append(*result, append([]string{}, (*tmp)...))
		return
	}
	for j:=index; j<len(*s); j++ {
		if isPalindrome((*s)[index:j+1]) {
			*tmp = append(*tmp, (*s)[index:j+1])
			dfsPartition2(s, j+1, tmp, result)
			*tmp = (*tmp)[:len(*tmp)-1]
		}
	}
}
func partition3(s string) [][]string {
	dp := make([][]bool, len(s))
	for i := range s{
		dp[i] = make([]bool, len(s))
	}
	// 注意这里的 DP 递归形式, `dp[i][j] = s[i]==s[j] && dp[i+1][j-1]`
	for i:=len(s)-1; i>=0; i-- {
		for j:=0; j<len(s); j++ {
			if j<=i {
				dp[i][j] = true
			} else {
				if s[i]==s[j] && dp[i+1][j-1] {
					dp[i][j] = true
				}
			}
		}
	}

	tmp := []string{}
	result := [][]string{}
	dfsPartition3(&s, 0, &tmp, &result, &dp)
	return result
}
func dfsPartition3(s *string, index int, tmp *[]string, result *[][]string, dp *[][]bool){
	if index==len(*s) {
		*result = append(*result, append([]string{}, (*tmp)...))
		return
	}
	for j:=index; j<len(*s); j++ {
		// if isPalindrome((*s)[index:j+1]) {
		if (*dp)[index][j]{
			*tmp = append(*tmp, (*s)[index:j+1])
			dfsPartition3(s, j+1, tmp, result, dp)
			*tmp = (*tmp)[:len(*tmp)-1]
		}
	}
}
func f131(){
	// fmt.Println(partition("aab"))
	fmt.Println(partition3("cbbbcc"))
	fmt.Println(partition3("dddddddddddd"))
}

/* 0212.Word-Search-II/
Input: 
board = [
  ['o','a','a','n'],
  ['e','t','a','e'],
  ['i','h','k','r'],
  ['i','f','l','v']
]
words = ["oath","pea","eat","rain"]

Output: ["eat","oath"]
和 79 题一样, 不过是变成了一组 words*/
func findWords(board [][]byte, words []string) []string {
	directions := [][]int{
		{-1,0},
		{1,0},
		{0,-1},
		{0,1},
	}
	result := []string{}
	for _, word := range words {
		if findWord(word, &board, &directions) {
			result = append(result, word)
		}
	}
	return result
}
func findWord(word string, board *[][]byte, directions *[][]int) bool {
	m, n := len(*board), len((*board)[0])
	visited := make([][]bool, m)
	for i:=0;i<m;i++ {visited[i] = make([]bool, n)}
	for x:=0; x<m; x++{
		for y:=0; y<n; y++{
			if (*board)[x][y] == word[0] {
				visited[x][y] = true
				if dfsFindWord(word, board, directions, 1, &visited, x,y,m,n) {
					return true
				}
				visited[x][y]= false
			}
		}
	}
	return false
}
func dfsFindWord(word string, board *[][]byte, directions *[][]int, index int, visited *[][]bool, x,y, m,n int) bool {
	if index==len(word) {
		return true
	}
	for _,d := range *directions{
		nx,ny := x+d[0], y+d[1]
		if isValidFindWord(nx,ny,m,n) && !(*visited)[nx][ny] && (*board)[nx][ny]==word[index] {
			(*visited)[nx][ny] = true
			if dfsFindWord(word, board, directions, index+1, visited, nx,ny,m,n){
				return true
			}
			// Note 如果没找到, 应该将 visited 复原
			(*visited)[nx][ny] = false
		}
	}
	return false
}
func isValidFindWord(x,y,m,n int)bool{
	return x>=0 && x<m && y>=0 && y<n
}

// Trie 记录所有代搜索的 word
type Trie struct {
	children [26]*Trie
	word string
}
// Insert 插入词表中的 word
func (t *Trie)Insert(s string){
	node := t
	for _,ch := range s{
		ch -= 'a'
		if node.children[ch] == nil{
			node.children[ch] = &Trie{}
		}
		node = node.children[ch]
	}
	node.word = s
}
// 方式2: 采用 Trie 记录所有代搜索的 word, 然后从 board 每个点出发尝试匹配 Trie
func findWords2(board [][]byte, words []string) []string {
	directions := []struct{ x, y int }{
		{-1,0},
		{1,0},
		{0,-1},
		{0,1},
	}
	t := &Trie{}
	for _,word := range words {
		t.Insert(word)
	}
	m,n := len(board), len(board[0])
	seen := map[string]bool{}
	var dfs func(node *Trie, x,y int)
	dfs = func(node *Trie, x,y int) {
		ch := board[x][y]
		node = node.children[ch-'a']
		if node==nil {return}
		if node.word != "" {seen[node.word]=true}

		// 防止 DFS 过程中重复一个位置
		board[x][y] = '#'
		for _,d := range directions{
			nx,ny := x+d.x, y+d.y
			if nx>=0 && nx<m && ny>=0 && ny<n && board[nx][ny]!='#' {
				dfs(node, nx, ny)
			}
		}
		board[x][y] = ch
	}

	for x := range board{
		for y:= range board[0]{
			dfs(t, x,y)
		}
	}
	result := []string{}
	for word := range seen {
		result = append(result, word)
	}
	return result
}

func f212(){
	fmt.Println(findWords2([][]byte{
		{'o','a','a','n'},
		{'e','t','a','e'},
		{'i','h','k','r'},
		{'i','f','l','v'},
	}, []string{"oath","pea","eat","rain", "aaao"}))
}

/* 0216.Combination-Sum-III/
Find all possible combinations of k numbers that add up to a number n, given that only numbers from 1 to 9 can be used and each combination should be a unique set of numbers.

Input: k = 3, n = 9
Output: [[1,2,6], [1,3,5], [2,3,4]] */
func combinationSum3(k int, n int) [][]int {
	result := [][]int{}
	tmp := []int{}
	dfsCombinationSum3(1, n, k, &tmp, &result)
	return result
}
func dfsCombinationSum3(begin, remain, remainK int, tmp *[]int, result *[][]int) {
	if remainK==1 {
		if remain<10 && remain>=begin {
			*tmp = append(*tmp, remain)
			*result = append(*result, append([]int{}, (*tmp)...))
			*tmp = (*tmp)[:len(*tmp)-1]
			return
		}
	}
	for d:=begin; d<10; d++ {
		if remain>begin {
			*tmp = append(*tmp, d)
			dfsCombinationSum3(d+1, remain-d, remainK-1, tmp, result)
			*tmp = (*tmp)[:len(*tmp)-1]
		}
	}
}
func f216(){
	fmt.Println(combinationSum3(3,9))
}

/* 301. Remove Invalid Parentheses 
Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.
Return all the possible results. You may return the answer in any order.
Example 1:

Input: s = "()())()"
Output: ["(())()","()()()"]
Example 2:

Input: s = "(a)())()"
Output: ["(a())()","(a)()()"]
Example 3:

Input: s = ")("
Output: [""]
*/
func removeInvalidParentheses(s string) []string {
	countL, countR := 0, 0
	countRemoveL, countRemoveR := 0, 0
	for _, ch := range s {
		if ch=='(' {
			countL++
		} else if ch==')' {
			if countR == countL {
				countRemoveR++
			} else {
				countR++
			}
		}
	}
	countRemoveL = countL-countR
	// if countRemoveL+countRemoveR == len(s) {
	// 	return []string{""}
	// }
	result := []string{}
	tmp := ""
	dfsRemoveInvalidParentheses(tmp, s, 0, &result, countRemoveL, countRemoveR, 0,0)
	resultFilter := map[string]bool{}
	for _,ss := range result {
		resultFilter[ss] = true
	}
	result = []string{}
	for ss := range resultFilter {
		result = append(result, ss)
	}
	return result
}
func dfsRemoveInvalidParentheses(tmp, s string, index int, result *[]string, countRemoveL, countRemoveR int, countL, countR int){
	if index==len(s) {
		if countL==countR && countRemoveR==0 && countRemoveL==0{
			*result = append(*result, tmp)
		}
		return
	}
	ch := s[index]
	if ch=='(' {
		dfsRemoveInvalidParentheses(tmp+"(", s, index+1, result, countRemoveL, countRemoveR, countL+1, countR)
		if countRemoveL>0 {
			dfsRemoveInvalidParentheses(tmp, s, index+1, result, countRemoveL-1, countRemoveR, countL, countR)
		}
	} else if ch==')' {
		if countL>countR {
			dfsRemoveInvalidParentheses(tmp+")", s, index+1, result, countRemoveL, countRemoveR, countL, countR+1)
		}
		if countRemoveR>0 {
			dfsRemoveInvalidParentheses(tmp, s, index+1, result, countRemoveL, countRemoveR-1, countL, countR)
		}
	} else {
		dfsRemoveInvalidParentheses(tmp+string(ch), s, index+1, result, countRemoveL, countRemoveR, countL, countR)
	}
}
func f301(){
	fmt.Println(removeInvalidParentheses("()())()"))
	fmt.Println(removeInvalidParentheses("(a)())()"))
	fmt.Println(removeInvalidParentheses(")(n"))
}


/* 0306.Additive-Number/
Given a string containing only digits '0'-'9', write a function to determine if it’s an additive number.

Input: "112358"
Output: true 
Explanation: The digits can form an additive sequence: 1, 1, 2, 3, 5, 8. 
             1 + 1 = 2, 1 + 2 = 3, 2 + 3 = 5, 3 + 5 = 8
Input: "199100199"
Output: true 
Explanation: The additive sequence is: 1, 99, 100, 199. 
             1 + 99 = 100, 99 + 100 = 199*/
func isAdditiveNumber(num string) bool {
	if len(num) < 3 {return false;}
	// 遍历生成 第 1,2 个数字
	for firstEnd:=0; firstEnd<len(num)/2; firstEnd++ {
		if firstEnd>0 && num[0]=='0' {return false }
		first,_ := strconv.Atoi(num[:firstEnd+1])
		for secondEnd:=firstEnd+1; secondEnd<len(num); secondEnd++ {
			if secondEnd>firstEnd+1 && num[secondEnd]=='0' {return false}
			second,_:= strconv.Atoi(num[firstEnd+1:secondEnd+1])
			if recCheckAdditive(num, first, second, secondEnd+1) {
				return true
			}
		}
	}
	return false
}
func recCheckAdditive(num string, x1, x2, index int) bool{
	if index == len(num) {return true}
	nextStr := strconv.Itoa(x1+x2)
	if strings.HasPrefix(num[index:], nextStr){
		return recCheckAdditive(num, x2, x2+x1, index+len(nextStr))
	}
	return false
}
func f306(){
	fmt.Println(isAdditiveNumber("199100199"))
}


/* 0357.Count-Numbers-with-Unique-Digits/
Given a non-negative integer n, count all numbers with unique digits, x, where 0 ≤ x < 10n.

Input: 2
Output: 91 
Explanation: The answer should be the total numbers in the range of 0 ≤ x < 100, 
             excluding 11,22,33,44,55,66,77,88,99
*/
// 暴力打表法
func countNumbersWithUniqueDigits1(n int) int {
	res := []int{1, 10, 91, 739, 5275, 32491, 168571, 712891, 2345851, 5611771, 8877691}
	if n >= 10 {
		return res[10]
	}
	return res[n]
}
func countNumberWithUniqueDigits(n int) int {
	if n>10 {return 0}
	if n==0 { return 1 }
	result, tmp, availableDigits := 10, 9, 9
	for ; n>1; n-- {
		tmp *= availableDigits
		availableDigits--
		result += tmp
	}
	return result
}
func f357(){
	fmt.Println(countNumberWithUniqueDigits(3))
}

/* 0401.Binary-Watch/
二进制手表顶部有 4 个 LED 代表小时（0-11），底部的 6 个 LED 代表分钟（0-59）。每个 LED 代表一个 0 或 1，最低位在右侧。
给定一个非负整数 n 代表当前 LED 亮着的数量，返回二进制表所有可能的时间。 

Input: n = 1
Return: ["1:00", "2:00", "4:00", "8:00", "0:01", "0:02", "0:04", "0:08", "0:16", "0:32"]*/
func readBinaryWatch(turnedOn int) []string {
	hourBases := []int{1,2,4,8}
	minBases := []int{1,2,4,8,16,32}
	result := []string{}
	for i:=0; i<=turnedOn; i++ {
		avaHours, avaMins := []int{}, []int{}
		dfsAvailableDigits(&hourBases, 0, i, 0, &avaHours)
		dfsAvailableDigits(&minBases, 0, turnedOn-i, 0, &avaMins)
		for _,hour := range avaHours {
			if hour>11 {continue}
			for _,min := range avaMins {
				if min>59 {continue}
				result = append(result, convertBinaryEatch(hour, min))
			}
		}
	}
	return result
}
func convertBinaryEatch(hour, min int) string {
	minStr := ""
	if min<10 {
		minStr += "0" + strconv.Itoa(min)
	} else {
		minStr += strconv.Itoa(min)
	}
	return strconv.Itoa(hour)+ ":" + minStr
}
func dfsAvailableDigits(bases *[]int, index, turnedOn, tmp int, result *[]int){
	if turnedOn > len(*bases) {
		return
	}
	if turnedOn==0 {
		*result = append(*result, tmp)
		return
	}
	for i:=index; i<len(*bases); i++ {
		dfsAvailableDigits(bases, i+1, turnedOn-1, tmp+(*bases)[i], result)
	}
}
// https://leetcode-cn.com/problems/remove-invalid-parentheses/solution/shan-chu-wu-xiao-de-gua-hao-by-leetcode-9w8au/
func readBinaryWatch1(turnedOn int) []string {
	result := []string{}
	for hour :=uint64(0); hour<=11; hour++ {
		for min:=uint64(0); min<=59 ;min++ {
			if bits.OnesCount64(hour) + bits.OnesCount64(min) == turnedOn {
				result = append(result, fmt.Sprintf("%d:%02d", hour, min))
			}
		}
	}
	return result
}
func readBinaryWatch2(turnedOn int) []string {
	result := []string{}
	for i:=0; i<1024; i++ {
		hour, min := i>>6, i&63 
		if hour<12 && min<60 && bits.OnesCount64(uint64(i))==turnedOn {
			result = append(result, fmt.Sprintf("%d:%02d", hour, min))
		}
	}
	return result
}
func f401(){
	// fmt.Println(readBinaryWatch1(1));
	fmt.Println(readBinaryWatch2(1))
}

/* 0473.Matchsticks-to-Square/
现在已知小女孩有多少根火柴，请找出一种能使用所有火柴拼成一个正方形的方法。不能折断火柴，可以把火柴连接起来，并且每根火柴都要用到。输入为小女孩拥有火柴的数目，每根火柴用其长度表示。输出即为是否能用所有的火柴拼成正方形。

Input: matchsticks = [1,1,2,2,2]
Output: true
Explanation: You can form a square with length 2, one side of the square came two sticks with length 1.*/
func makesquare(matchsticks []int) bool {
	sort.Ints(matchsticks)
	sum := 0
	for _, i := range matchsticks {
		sum += i
	}
	if sum % 4 != 0 {return false}
	target := sum/4
	used := make([]bool, len(matchsticks))
	return dfsMakeSquare(&matchsticks, &used, target, target, len(matchsticks)-1, len(matchsticks))
}
func dfsMakeSquare(sticks *[]int, used *[]bool, target, tmp, index, remain int) bool {
	// remain 记录还有多少火柴
	if remain==0 {return true}
	// 为了剪枝, 从大到小遍历
	for i:= index; i>=0; i-- {
		if (*sticks)[i] > tmp || (*used)[i] {
			continue
		} else {
			(*used)[i] = true
			if (*sticks)[i] == tmp {
				// 找满了一条边, 从头开始遍历
				result := dfsMakeSquare(sticks, used, target, target, len(*sticks)-1, remain-1)
				if result {return true}
			} else {
				result := dfsMakeSquare(sticks, used, target, tmp-(*sticks)[i], i-1, remain-1)
				if result {return true}
			}
			(*used)[i] = false
			
		}
	}
	return false
}
func f473(){
	// fmt.Println(makesquare([]int{1,1,2,2,2}))
	fmt.Println(makesquare([]int{5,5,5,5,4,4,4,4,3,3,3,3}))
}

/* 0491.Increasing-Subsequences/
Given an integer array, your task is to find all the different possible increasing subsequences of the given array, and the length of an increasing subsequence should be at least 2.

Input: [4, 6, 7, 7]
Output: [[4, 6], [4, 7], [4, 6, 7], [4, 6, 7, 7], [6, 7], [6, 7, 7], [7,7], [4,7,7]]

输入：nums = [4,4,3,2,1]
输出：[[4,4]]

这一题和第 78 题和第 90 题是类似的题目。第 78 题和第 90 题是求所有子序列，这一题在这两题的基础上增加了非递减和长度大于 2 的条件。需要注意的两点是，原数组中元素可能会重复，最终结果输出的时候需要去重。最终结果输出的去重用 map 处理，数组中重复元素用 DFS 遍历搜索。在每次 DFS 中，用 map 记录遍历过的元素，保证本轮 DFS 中不出现重复的元素，递归到下一层还可以选择值相同，但是下标不同的另外一个元素。外层循环也要加一个 map，这个 map 是过滤每组解因为重复元素导致的重复解，经过过滤以后，起点不同了，最终的解也会不同。*/

// 方式二 和90代码完全一样. see https://leetcode-cn.com/problems/increasing-subsequences/solution/di-zeng-zi-xu-lie-by-leetcode-solution/
func findSubsequences(nums []int) [][]int {
	tmp, result := []int{}, [][]int{}
	dfsFindSubsequences(0, math.MinInt32, &nums, &tmp, &result)
	return result
}
func dfsFindSubsequences(index, lastNum int, nums, tmp *[]int, result *[][]int) {
	if index==len(*nums) {
		if len(*tmp)>= 2{
			*result = append(*result, append([]int{}, (*tmp)...))
		}
		return
	}
	// 递归情况1: 加入当前元素
	if (*nums)[index]>=lastNum {
		*tmp = append(*tmp, (*nums)[index])
		dfsFindSubsequences(index+1, (*nums)[index], nums, tmp, result)
		*tmp = (*tmp)[:len(*tmp)-1]
	}
	// 递归情况2: 不加入当前元素
	// 为了避免重复, 当前要加入的数字和 tmp 中上一个数字相同时, 不遍历
	if (*nums)[index]!=lastNum {
		dfsFindSubsequences(index+1, lastNum, nums, tmp, result)
	}
}
func f491(){
	fmt.Println(findSubsequences([]int{4, 6, 7, 7}))
}
func main() {
	// f357()
	// f401()
	// f473()
	f491()
}
