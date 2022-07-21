package main

import (
	"fmt"
	// "popcount"
	"math/bits"

	"github.com/tmthrgd/go-popcount"
)

func testCount() {
	// c := popcount.CountBytes([]int{2, 3})
	c := bits.OnesCount(3)
	fmt.Println(c)

	c = popcount.CountBytes(3)
	fmt.Print(c)
}

func main() {
	testCount()
}
