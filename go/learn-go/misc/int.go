package main

import (
	"fmt"
	"math"
	"unsafe"
)

/* 范围
int8: -128 ~ 127
int16: -32768 ~ 32767
int32: -2147483648 ~ 2147483647
int64: -9223372036854775808 ~ 9223372036854775807
uint8: 0 ~ 255
uint16: 0 ~ 65535
uint32: 0 ~ 4294967295
uint64: 0 ~ 18446744073709551615 */

// from Go语言-int类型取值范围 https://blog.csdn.net/dshf_1/article/details/105403862
func intLimit() {
    // 输出各int类型的取值范围
    fmt.Println("各int类型的取值范围为：")
    fmt.Println("int8:", math.MinInt8, "~", math.MaxInt8)
    fmt.Println("int16:", math.MinInt16, "~", math.MaxInt16)
    fmt.Println("int32:", math.MinInt32, "~", math.MaxInt32)
    fmt.Println("int64:", math.MinInt64, "~", math.MaxInt64)
    fmt.Println()
    
    // n是自动推导类型
    n := 1234567890
    fmt.Printf("n := 1234567890 的默认类型为：%T\n", n)
    fmt.Printf("int类型的字节数为：")
    fmt.Println(unsafe.Sizeof(n))
    fmt.Printf("\n")
 
    // 初始化一个32位整型值
    var a int32 = 987654321
 
    fmt.Println("var a int32 = 987654321")
    // 输出变量的十六进制形式和十进制值
    fmt.Printf("int32: 十六进制为0x%x，十进制为%d\n", a, a)
 
    // 将a转换为int8类型, 发生数值截断
    b := int8(a)
    // 输出变量的十六进制形式和十进制值
    fmt.Printf("int8: 十六进制为0x%x，十进制为%d\n", b, b)
 
    // 将a转换为int16类型, 发生数值截断
    c := int16(a)
    // 输出变量的十六进制形式和十进制值
    fmt.Printf("int16: 十六进制为0x%x，十进制为%d\n", c, c)
 
    // 将a转换为int64类型
    d := int64(a)
    // 输出变量的十六进制形式和十进制值
    fmt.Printf("int64: 十六进制为0x%x，十进制为%d\n", d, d)
}