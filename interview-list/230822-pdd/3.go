package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	var n int
	fmt.Scanf("%d\n", &n)
	for i := 0; i < n; i++ {
		var N, M int
		fmt.Scanf("%d %d\n", &N, &M)
		arr := make([]int, N)
		for j := 0; j < N; j++ {
			fmt.Scanf("%d", &arr[j])
		}
		fmt.Printf("%d\n", maxMatch(arr, M))
	}
}


func maxMatch(arr []int, m int) int {
	mod2cnt := make(map[int]map[int]int)
	mod2sum := make(map[int]int)
	for _, x := range arr {
		if _, ok := mod2cnt[x%m]; !ok {
			mod2cnt[x%m] = make(map[int]int)
		}
		mod2cnt[x%m][x] += 1
		mod2sum[x%m] += 1
	}
	ans := 0
	used := make(map[int]bool)
	for x, cnt := range mod2cnt {
		if used[m-x] {
			continue
		}
		used[x], used[m-x] = true, true
		if x == 0 {
			for _, v := range cnt {
				ans += v / 2
			}
			continue
		}
		if _, ok := mod2cnt[m-x]; !ok {
			ans += getPairs(cnt)
			continue
		}
		cnt2 := mod2cnt[m-x]
		acc1, acc2 := mod2sum[x], mod2sum[m-x]
		mn, mx := acc1, acc2
		if acc1 > acc2 {
			mn, mx = acc2, acc1
		}
		ans += mn + min(getPairs(cnt), (mx-mn)/2)
	}
	return ans
}

func getPairs(cnt map[uint8]int) int {
	pairs := 0
	for _, v := range cnt {
		pairs += v / 2
	}
	return pairs
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
func max(a, b int) int {
	if a >= b {
		return a
	}
	return b
}