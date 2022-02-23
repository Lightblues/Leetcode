/*
 * @lc app=leetcode.cn id=17 lang=golang
 *
 * [17] 电话号码的字母组合
 */

// @lc code=start
func letterCombinations(digits string) []string {
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
// @lc code=end

