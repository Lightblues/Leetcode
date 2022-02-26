## js

js 标准内置对象参见 <https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects>

- Array
    - 属性: length
    - 常见方法:
        - 头尾添加 push, pop, unshift, shift
        - 遍历 forEach
        - 复制/子集 slice
        - 查找 indexOf
        - 通过索引删除 splice
    - 其他方法
        - reverse 翻转
        - concat 拼接
        - sort 排序
        - `join("")` 类似Python中的 `"".join([])`
- Map
    - 属性: size
    - 方法:
        - has, get, set, delete, clear
        - keys, values, entries
        - forEach

排序

- 注意 js 中的 sort 方法是原地操作, 也返回排序后的结果

数组

- 复制: 1. arr.slice() 方法; 2. map, filter 辅助实现; 3. `[...arr]` 语法进行复制; 4. `_.clone` ; 5. JSON 进行 stringify, parse 进行深复制.

### underscore

- 提供了一套完善的函数式编程的接口，让我们更方便地在JavaScript中实现函数式编程
- Collections: 集合类是指Array和Object
    - 当作用于Object时，传入的函数为`function (value, key)`
    - map
    - every, some
    - max, min
    - groupBy 把集合的元素按照key归类，key由传入的函数返回
    - shuffle, sample
- Array
    - first, last
    - flatten
    - zip, unzip
    - object
        - `_.object(names, scores);` 以 names 数组作为key scores 数组作为value
    - `range`
        - `_.range(0, 30, 5);` 从0开始小于30，步长5
- Functions
    - bind
    - `partial`
        - `var cube = _.partial(Math.pow, _, 3);` 计算三次方, 其中 `_` 占位符
    - `memorize`
    - once
    - delay
- Object
    - `keys`, allKeys
    - values
    - mapObject
    - invert 调换 key, value
    - `extend`, extendOwn 把多个object的key-value合并到第一个object并返回; 后者获取属性时忽略从原型链继承下来的属性
    - clone 浅复制
    - `isEqual` 深度比较
- Chaining
    - _.chain([1, 4, 9, 16, 25]).map(Math.sqrt).value()

## Go

### 类型转换

```go
directions := [][]int{
  {-1,0},
  {1,0},
  {0,-1},
  {0,1},
}
[][]byte{
  {'A','B','C','E'},
  {'S','F','C','S'},
  {'A','D','E','E'},
}
```

### 传递 值拷贝 vs 指针

典型的问题是遍历二叉树, 例如 113题(找到二叉树路径和为目标值的所有路径), 需要维护一个历史的path.

- go中将slice作为参数传递/赋值(Python中将list作为参数传递也类似), 传递的还是类似指针的类型; 因此相较于值拷贝, 内存开销会小一点.
- 因此, 在对于这个类型进行修改的时候, 需要注意对于外层变量的影响

#### go语言中的slice 传递 & 复制

- go中的slice本质上还是包括了len, cap 属性的一个指针, 可表示为 `[3/5]0xc42003df10`, 传递给函数是浅复制(**仍然指向源slice的底层数组**), 若在函数内进行了修改
    - 若函数内部对slice进行扩容，扩容时生成了一个新的底层数组, 两个 slice 的内存指向就不同了, 不会影响外层slice
    - 若没有进行扩容, 修改了底层数组, 则外层同样引用这一底层数组的slice会被改变
- **复制** slice
    - 可以使用 cope 函数, `copy(s2, s1)` 将s1复制到s2, 若s1较长会被截断, 较短则复制s1那部分(s2后面的部分不变, len也不变); 函数返回成功复制的数量
    - 或者是字面量 `append([]int{}, s1...)`

### 全局变量 vs 传参

参见 113 题(找到二叉树路径和为目标值的所有路径).

- 对于 `pathSum(root *TreeNode, targetSum int) [][]int` 这样的问题
    - **传参**, 递归函数 `pathSumRec(node *TreeNode, sum int, paths *[][]int, tmp []int)`; 这里用了指针 `paths [][]int{}`, 因为初始化的 `[][]int{}` 类型长度为0, 若在函数内部进行 append, 会因为进行了扩容而开辟一个新的内存, 从而无法修改到外层的 slice
    - **全局变量+内部函数**, 在函数内部定义 `var dfs func(root *TreeNode, target int)`, 从而直接修改全局变量, 从而避免了外部定义一个函数, 需要考虑的传参问题

之所以会有这样的困扰, 因为之前没看过 go 的内部函数语法; 从实际应用上来看, 「全局变量+内部函数」的方式无疑更简单和优雅.
