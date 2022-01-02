package main

// 尝试把超时的 Python 代码修改为 Go, 没写完
func maximumInvitations(favorite []int) int {
	beLoved := make([][]int, len(favorite))
	for i:=0; i<len(favorite); i++ {
		beLoved[i] = []int{}
	}
	possibleStart := map[int]bool{}
	for i,ll := range beLoved {
		if len(ll)>0{
			possibleStart[i] = true
		}
	}
	findCircles := func (start int) []int {
		nodes := map[int]bool{}
		nodes[start] = true
		now := favorite[start]
		for now != start {
			if nodes[now] {
				return []int{}
			}
			nodes[now] = true
			now = favorite[now]
		}
		result := []int{}
		for n := range nodes {
			result = append(result, n)
		}
		return result
	}
	circles := [][]int{}
	for len(possibleStart) > 0 {
		for s := range possibleStart {
			rr := findCircles(s)
			if len(rr) > 0 {
				circles = append(circles, rr)
				for node := range rr {
					delete(possibleStart, node)
				}
			} else {
				delete(possibleStart, s)
			}
			break
		}
	}

	dfsFindChain := func (x , chainLen int) int {
		if len(beLoved[x]) > 0 {
			results := []int{}
			for _,lover := range beLoved[x]{
				results = append(results, dfsFindChain(lover, chainLen+1))
			}
			return max(results)
		}
		return chainLen
	}

	circles2 := [][]int{}
	results := []int{}
	for _, c := range circles{
		if len(c) > 2 {
			results = append(results, len(c))
		} else {
			circles2 = append(circles2, c)
		}
	}
	cumsum2 := 0
	for _, pair := range circles2 {
		for _,person := range pairs {
			pass
		}
	}
}

func max(nums []int) int {
	maxx := 0
	for num := range nums {
		if num>maxx {
			maxx = num
		}
	}
	return maxx
}