package main

import (
	"fmt"
	// 这里的 gopl.io 在 go.mod 中定义
	"gopl.io/ch6/geometry"
)

func testConst() {
	type Currency int
	// 用 iota 来定义一些常量
	const (
		USD Currency = iota // 美元
		EUR                 // 欧元
		GBP                 // 英镑
		RMB                 // 人民币
	)
	// 按照 idx:value 的形式初始化数组
	symbol := [...]string{EUR: "€", GBP: "￡", RMB: "￥", USD: "$"}
	fmt.Println(RMB, symbol[RMB]) // "3 ￥"

	r := [...]int{99: -1}
	fmt.Println(len(r)) // "[99 -1]"
}

func main() {
	perim := geometry.Path{{X: 1, Y: 1}, {X: 5, Y: 1}, {X: 5, Y: 4}, {X: 1, Y: 1}}
	fmt.Println(geometry.Path.Distance(perim)) // "12", standalone function
	fmt.Println(perim.Distance())              // "12", method of geometry.Path

	testConst()
}
