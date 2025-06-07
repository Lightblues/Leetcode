

## 环境配置
1. 编辑器, vscode; 插件: ESLint、Prettier
2. 数据结构实现: 链表; 二叉树; 栈/队列;
3. 算法模板: 双指针; DFS; BFS; 
    1. memory 机制 (DP)
4. js 特性
    1. 浮点精度问题: 0.1 + 0.2 !== 0.3（用 toFixed(2) 处理）
    2. === 与 == 的区别: 严格使用前者
5. LeetCode 环境
    1. Node.js 22.14.0; --harmony 标记来启用 ES6 新特性
    2. 包含 lodash.js 库 [github](https://lodash.com/)
    3. 相关包: [priority-queue](https://github.com/datastructures-js/priority-queue), [queue](https://github.com/datastructures-js/queue/), [deque](https://github.com/datastructures-js/deque)

参考 [BaffinLee/leetcode-javascript](https://github.com/BaffinLee/leetcode-javascript) 🌟

## ES6（ECMAScript 2015）
参见 [ECMAScript 6 入门](https://es6.ruanyifeng.com/) by @阮一峰

特性
1. 变量声明：let & const `let y = 20;`
2. 箭头函数：`const add = (x, y) => x + y;`
    1. 相较于ES5的 `[1,6,3,8].filter(function(n){ return n>5; });`, 
    2. 可以简化为 `[1,6,3,8].filter(n => n>5);`
3. 模板字符串 ```const msg = `Hello ${name}!\n今天是：${new Date().toLocaleDateString()}`;```
4. 解构赋值
    1. 数组解构 `const [first, , third] = [1, 2, 3];`
        1. 交换变量, 相较于ES5 `var tmp = a; a = b; b = tmp;`
        2. 可以简化为 `[b, a] = [a, b];`
    2. 对象解构 `const { name, age } = user;`
    3. 函数参数解构 `function greet({ name, age }) {...};`
5. 类（Class）
    1. 方法 (自动绑定原型)
    2. 静态方法
    3. 继承
6. 模块化（Modules）​​`import { PI, circleArea } from './math.js';`
7. Promise 异步处理​
    1. 配合 async/await（ES2017）
8. 扩展运算符（Spread）
    1. 数组拓展 `const combined = [...arr1, ...arr2];`
    2. 对象拓展 `const merged = { ...obj1, ...obj2 };`
    3. 函数参数拓展 `function sum(...numbers) { return numbers.reduce((a, b) => a + b); };`
        1. 可以 `const nums = [1,2,3]; sum(...nums);` 也可以 `sum(1,2,3);`
        2. 或者是基本定义 `function sum(x, y, z) { return x + y + z; }`
9. 新数据结构 ​Map/Set​

## Lodash 包
[github](https://github.com/lodash/lodash); [doc](https://lodash.com/docs/) #Lodash 简化数组、对象、数字、字符串等数据类型的操作

数组
```js
import { chunk, difference, flattenDeep } from 'lodash';

chunk([1, 2, 3, 4], 2); // → [[1,2], [3,4]]
difference([2, 1], [2, 3]); // → [1]
flattenDeep([1, [2, [3]]]); // → [1, 2, 3]
```

对象
```js
import { get, set, merge, omit } from 'lodash';

const obj = { a: { b: 2 } };
get(obj, 'a.b'); // → 2 (安全访问嵌套属性)
set(obj, 'a.c', 3); // → { a: { b: 2, c: 3 } }
merge({a: 1}, {b: 2}); // → {a:1, b:2} (深度合并)
omit({a:1, b:2}, ['a']); // → {b:2} (排除属性)
```

函数
```js
import { throttle, debounce, memoize } from 'lodash';

// 节流：每200ms最多触发一次
const throttledResize = throttle(() => console.log('Resize'), 200);

// 防抖：停止输入300ms后触发
const debouncedSearch = debounce(searchAPI, 300);

// 缓存结果
const fibonacci = memoize(n => n <= 1 ? n : fibonacci(n-1) + fibonacci(n-2));
```

类型检查
```js
_.isObject({}); // true
_.isNil(null); // true
_.isEmpty([]); // true
_.random(5, 10); // 生成5-10间的随机数
_.times(3, () => 'hi'); // → ['hi', 'hi', 'hi']
```

集合操作
```js
_.map([1, 2], n => n * 2); // → [2, 4]
_.filter([1, 2, 3], n => n > 1); // → [2, 3]
_.groupBy(['a', 'bb', 'c'], 'length'); // → {1: ['a','c'], 2: ['bb']}
```

深度操作
```js
_.cloneDeep({ a: [1] }); // 深拷贝
_.isEqual({a:1}, {a:1}); // 深度比较 → true
```
