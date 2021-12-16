package main

import (
	"fmt"
	"sort"
)

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





func main() {
	f47()
}
