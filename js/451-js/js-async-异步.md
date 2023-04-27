还是实习的时候写的 js 异步笔记.

## 异步

参见知乎文 [最后谈一次 JavaScript 异步编程](https://zhuanlan.zhihu.com/p/24444262) 讲得比较清楚。

### Node.js 事件循环

通常，在大多数浏览器中，每个浏览器选项卡都有一个事件循环，以使每个进程都隔离开，并避免使用无限的循环或繁重的处理来阻止整个浏览器的网页。
该环境管理多个并发的事件循环，例如处理 API 调用。 Web 工作进程也运行在自己的事件循环中。
主要需要关心代码会在单个事件循环上运行，并且在编写代码时牢记这一点，以避免阻塞它。

#### 阻塞事件循环

任何花费太长时间才能将控制权返回给事件循环的 JavaScript 代码，都会阻塞页面中任何 JavaScript 代码的执行，甚至阻塞 UI 线程，并且用户无法单击浏览、滚动页面等。
JavaScript 中几乎所有的 I/O 基元都是非阻塞的。 网络请求、文件系统操作等。 被阻塞是个异常，这就是 JavaScript 如此之多基于回调（最近越来越多基于 promise 和 async/await）的原因。

#### 调用堆栈

调用堆栈是一个 LIFO 队列（后进先出）。
事件循环不断地检查调用堆栈，以查看是否需要运行任何函数。
当执行时，它会将找到的所有函数调用添加到调用堆栈中，并按顺序执行每个函数。

#### 消息队列

```js
const bar = () => console.log('bar')

const baz = () => console.log('baz')

const foo = () => {
  console.log('foo')
  setTimeout(bar, 0)
  baz()
}

foo()
```

当调用 setTimeout() 时，浏览器或 Node.js 会启动定时器。 当定时器到期时（在此示例中会立即到期，因为将超时值设为 0），则回调函数会被放入“消息队列”中。

在消息队列中，用户触发的事件（如单击或键盘事件、或获取响应）也会在此排队，然后代码才有机会对其作出反应。 类似 `onLoad` 这样的 DOM 事件也如此。

事件循环会赋予调用堆栈优先级，它首先处理在调用堆栈中找到的所有东西，一旦其中没有任何东西，便开始处理消息队列中的东西。

我们不必等待诸如 `setTimeout`、fetch、或其他的函数来完成它们自身的工作，因为它们是由浏览器提供的，并且位于它们自身的线程中。 例如，如果将 `setTimeout` 的超时设置为 2 秒，但不必等待 2 秒，等待发生在其他地方。

#### ES6 作业队列

ECMAScript 2015 引入了作业队列的概念，Promise 使用了该队列（也在 ES6/ES2015 中引入）。 这种方式会尽快地执行异步函数的结果，而不是放在调用堆栈的末尾。

在当前函数结束之前 resolve 的 Promise 会在当前函数之后被立即执行。

### process.nextTick()

当尝试了解 Node.js 事件循环时，其中一个重要的部分就是 process.nextTick()。
每当事件循环进行一次完整的行程时，我们都将其称为一个滴答。
当将一个函数传给 process.nextTick() 时，则指示引擎在当前操作结束（在下一个事件循环滴答开始之前）时调用此函数：

```js
process.nextTick(() => {
  //做些事情
})
```

事件循环正在忙于处理当前的函数代码。
当该操作结束时，JS 引擎会运行在该操作期间传给 `nextTick` 调用的所有函数。

这是可以告诉 JS 引擎异步地（在当前函数之后）处理函数的方式，但是尽快执行而不是将其排入队列。
调用 `setTimeout(() => {}, 0)` 会在下一个滴答结束时执行该函数，比使用 `nextTick()`（其会优先执行该调用并在下一个滴答开始之前执行该函数）晚得多。
当要确保在下一个事件循环迭代中代码已被执行，则使用 `nextTick()`。

### setImmediate()

当要异步地（但要尽可能快）执行某些代码时，其中一个选择是使用 Node.js 提供的 `setImmediate()` 函数：

```js
setImmediate(() => {
  //运行一些东西
})
```

作为 setImmediate() 参数传入的任何函数都是在事件循环的下一个迭代中执行的回调。

`setImmediate()` 与 `setTimeout(() => {}, 0)`（传入 0 毫秒的超时）、`process.nextTick()` 有何不同？

* 传给 `process.nextTick()` 的函数会在事件循环的当前迭代中（当前操作结束之后）被执行。 这意味着它会始终在 `setTimeout` 和 `setImmediate` 之前执行。
* 延迟 0 毫秒的 `setTimeout()` 回调与 `setImmediate()` 非常相似。 执行顺序取决于各种因素，但是它们都会在事件循环的下一个迭代中运行。

### JavaScript 定时器

#### setTimeout()

当编写 JavaScript 代码时，可能希望延迟函数的执行。

这就是 setTimeout 的工作。 指定一个回调函数以供稍后执行，并指定希望它稍后运行的时间（以毫秒为单位）的值：

```js
setTimeout(() => {
  // 2 秒之后运行
}, 2000)

setTimeout(() => {
  // 50 毫秒之后运行
}, 50)

//传入参数
const myFunction = (firstParam, secondParam) => {
  // 做些事情
}

// 2 秒之后运行
setTimeout(myFunction, 2000, firstParam, secondParam)
```

##### 零延迟

如果将超时延迟指定为 `0`，则回调函数会被尽快执行（但是是在当前函数执行之后）。

```js
setTimeout(() => {
  console.log('后者 ')
}, 0)

console.log(' 前者 ')
```

会打印 `前者 后者`。

通过在调度程序中排队函数，可以避免在执行繁重的任务时阻塞 CPU，并在执行繁重的计算时执行其他函数。

#### setInterval()

`setInterval` 是一个类似于 `setTimeout` 的函数，不同之处在于：它会在指定的特定时间间隔（以毫秒为单位）一直地运行回调函数，而不是只运行一次：

```js
setInterval(() => {
  // 每 2 秒运行一次
}, 2000)
```

上面的函数每隔 2 秒运行一次，除非使用 `clearInterval` 告诉它停止（传入 `setInterval` 返回的间隔定时器 id）。

通常在 `setInterval` 回调函数中调用 `clearInterval`，以使其自行判断是否应该再次运行或停止。 例如，此代码会运行某些事情，除非 `App.somethingIWait` 具有值 `arrived`：

```js
const interval = setInterval(() => {
  if (App.somethingIWait === 'arrived') {
    clearInterval(interval)
    return
  }
  // 否则做些事情
}, 100)
```

然而，由于网络等因素的影响，可能会出现这些任务执行事件不一致的问题。此时调用 setInterval() 是不合适的。
为了避免这种情况，可以在回调函数完成时安排要被调用的递归的 setTimeout：

```js
const myFunction = () => {
  // 做些事情

  setTimeout(myFunction, 1000)
}

setTimeout(myFunction, 1000)
```

`setTimeout` 和 `setInterval` 可通过[定时器模块](http://nodejs.cn/api/timers.html)在 Node.js 中使用。

Node.js 还提供 `setImmediate()`（相当于使用 `setTimeout(() => {}, 0)`），通常用于与 Node.js 事件循环配合使用。

### JavaScript 异步编程与回调

JavaScript 默认情况下是同步的，并且是单线程的。 这意味着代码无法创建新的线程并且不能并行运行。
但是 JavaScript 诞生于浏览器内部，一开始的主要工作是响应用户的操作，例如 `onClick`、`onMouseOver`、`onChange`、`onSubmit` 等。 使用同步的编程模型该如何做到这一点？

答案就在于它的环境。 浏览器通过提供一组可以处理这种功能的 API 来提供了一种实现方式。

更近点，Node.js 引入了非阻塞的 I/O 环境，以将该概念扩展到文件访问、网络调用等。

#### 回调

你不知道用户何时单击按钮。 因此，为点击事件定义了一个事件处理程序。 该事件处理程序会接受一个函数，该函数会在该事件被触发时被调用：

```js
document.getElementById('button').addEventListener('click', () => {
  //被点击
})
```

这就是所谓的回调。

**回调是一个简单的函数，会作为值被传给另一个函数，并且仅在事件发生时才被执行**。 之所以这样做，是因为 JavaScript 具有顶级的函数，这些函数可以被分配给变量并传给其他函数（称为高阶函数）。

通常会将所有的客户端代码封装在 `window` 对象的 `load` 事件监听器中，其仅在页面准备就绪时才会运行回调函数：

```js
window.addEventListener('load', () => {
  //window 已被加载。
  //做需要做的。
})
```

回调无处不在，不仅在 DOM 事件中。
一个常见的示例是使用定时器。

```js
setTimeout(() => {
  // 2 秒之后运行。
}, 2000)
```

XHR 请求也接受回调，在此示例中，会将一个函数分配给一个属性，该属性会在发生特定事件（在该示例中，是请求状态的改变）时被调用：

```js
const xhr = new XMLHttpRequest()
xhr.onreadystatechange = () => {
  if (xhr.readyState === 4) {
    xhr.status === 200 ? console.log(xhr.responseText) : console.error('出错')
  }
}
xhr.open('GET', 'http://nodejs.cn')
xhr.send()
```

#### 处理回调中的错误

如何处理回调的错误？ 一种非常常见的策略是使用 Node.js 所采用的方式：任何回调函数中的第一个参数为错误对象（即错误优先的回调）。

如果没有错误，则该对象为 `null`。 如果有错误，则它会包含对该错误的描述以及其他信息。

#### 回调的问题

回调适用于简单的场景！

但是，每个回调都可以添加嵌套的层级，并且当有很多回调时，代码就会很快变得非常复杂：

```js
window.addEventListener('load', () => {
  document.getElementById('button').addEventListener('click', () => {
    setTimeout(() => {
      items.forEach(item => {
        //你的代码在这里。
      })
    }, 2000)
  })
})
```

这只是一个简单的 4 个层级的代码，但还有更多层级的嵌套，这很不好。

从 ES6 开始，JavaScript 引入了一些特性，可以帮助处理异步代码而不涉及使用回调：**Promise（ES6）和 Async/Await（ES2017）**。

### Promise

Promise 通常被定义为 **最终会变为可用值的代理**。
Promise 是一种处理异步代码（而不会陷入[回调地狱](http://callbackhell.com/)）的方式。
多年来，promise 已成为语言的一部分（在 ES2015 中进行了标准化和引入），并且最近变得更加集成，在 ES2017 中具有了 **async** 和 **await**。

**异步函数** 在底层使用了 promise，因此了解 promise 的工作方式是了解 `async` 和 `await` 的基础。

当 promise 被调用后，它会以**处理中状态**开始。 这意味着调用的函数会继续执行，而 promise 仍处于处理中直到解决为止，从而为调用的函数提供所请求的任何数据。
被创建的 promise 最终会以**被解决状态**或**被拒绝状态**结束，并在完成时调用相应的回调函数（传给 `then` 和 `catch`）。

除了自己的代码和库代码，标准的现代 Web API 也使用了 promise，例如：

* Battery API
* Fetch API
* Service Worker

#### 创建 promise

Promise API 公开了一个 Promise 构造函数，可以使用 `new Promise()` 对其进行初始化：

```js
let done = true

const isItDoneYet = new Promise((resolve, reject) => {
  if (done) {
    const workDone = '这是创建的东西'
    resolve(workDone)
  } else {
    const why = '仍然在处理其他事情'
    reject(why)
  }
})

const checkIfItsDone = () => {
    isItDoneYet
        .then(ok => {
            console.log(ok)
        })
        .catch(err => {
            console.error(err)
        })
}

checkIfItsDone()
```

如你所见，promise 检查了 `done` 全局常量，如果为真，则 promise 进入**被解决**状态（因为调用了 `resolve` 回调）；否则，则执行 `reject` 回调（将 promise 置于被拒绝状态）。 如果在执行路径中从未调用过这些函数之一，则 promise 会保持处理中状态。
使用 `resolve` 和 `reject`，可以向调用者传达最终的 promise 状态以及该如何处理。 在上述示例中，只返回了一个字符串，但是它可以是一个对象，也可以为 `null`。 由于已经在上述的代码片段中创建了 promise，因此它已经开始执行。

运行 `checkIfItsDone()` 会指定当 `isItDoneYet` promise 被解决（在 `then` 调用中）或被拒绝（在 `catch` 调用中）时执行的函数。

一个更常见的示例是一种被称为 Promisifying 的技术。 这项技术能够使用经典的 JavaScript 函数来接受回调并使其返回 promise：

```js
const fs = require('fs')

const getFile = (fileName) => {
  return new Promise((resolve, reject) => {
    fs.readFile(fileName, (err, data) => {
      if (err) {
        reject(err)  // 调用 `reject` 会导致 promise 失败，无论是否传入错误作为参数，
        return        // 且不再进行下去。
      }
      resolve(data)
    })
  })
}

getFile('/etc/passwd')
.then(data => console.log(data))
.catch(err => console.error(err))
```

### 链式 promise

```js
const status = response => {
  if (response.status >= 200 && response.status < 300) {
    return Promise.resolve(response)
  }
  return Promise.reject(new Error(response.statusText))
}

const json = response => response.json()

fetch('/todos.json')
  .then(status)    // 注意，`status` 函数实际上在这里被调用，并且同样返回 promise，
  .then(json)      // 这里唯一的区别是的 `json` 函数会返回解决时传入 `data` 的 promise，
  .then(data => {  // 这是 `data` 会在此处作为匿名函数的第一个参数的原因。
    console.log('请求成功获得 JSON 响应', data)
  })
  .catch(error => {
    console.log('请求失败', error)
  })
```

【关于 fetch，参见 <https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch>】

在此示例中，调用 `fetch()` 从域根目录中的 `todos.json` 文件中获取 TODO 项目的列表，并创建一个 promise 链。

运行 `fetch()` 会返回一个[响应](https://fetch.spec.whatwg.org/#concept-response)，该响应具有许多属性，在属性中引用了：

* `status`，表示 HTTP 状态码的数值。
* `statusText`，状态消息，如果请求成功，则为 `OK`。

`response` 还有一个 `json()` 方法，该方法会返回一个 promise，该 promise 解决时会传入已处理并转换为 JSON 的响应体的内容。

因此，考虑到这些前提，发生的过程是：链中的第一个 promise 是我们定义的函数，即 `status()`，它会检查响应的状态，如果不是成功响应（介于 200 和 299 之间），则它会拒绝 promise。

此操作会导致 promise 链跳过列出的所有被链的 promise，且会直接跳到底部的 `catch()` 语句（记录`请求失败`的文本和错误消息）。

如果成功，则会调用定义的 `json()` 函数。 由于上一个 promise 成功后返回了 `response` 对象，因此将其作为第二个 promise 的输入。

### async, await

JavaScript 在很短的时间内从回调发展到了 promise（ES2015），且自 ES2017 以来，异步的 JavaScript 使用 async/await 语法甚至更加简单。
异步函数是 promise 和生成器的组合，基本上，它们是 promise 的更高级别的抽象。 而 async/await 建立在 promise 之上。
这是一个 async/await 的简单示例，用于异步地运行函数：

```js
const doSomethingAsync = () => {
  return new Promise(resolve => {
    setTimeout(() => resolve('做些事情'), 3000)
  })
}

const doSomething = async () => {
  console.log(await doSomethingAsync())
}

console.log('之前')
doSomething()
console.log('之后')
```

打印内容

```text
之前
之后
做些事情 // 3 秒之后
```

#### async

在任何函数之前加上 `async` 关键字意味着该函数会返回 promise。
即使没有显式地这样做，它也会在内部使它返回 promise。

```js
const aFunction = async () => {
  return '测试'
}
aFunction().then(alert) // 这会 alert '测试'

// 等价于
const aFunction = () => {
  return Promise.resolve('测试')
}
aFunction().then(alert) // 这会 alert '测试'
```

#### 代码更容易阅读

相较于使用普通的 promise 或者回调，代码看上去更简单。
例如，下面用 promise 获取并解析 JSON

```js
const getFirstUserData = () => {
  return fetch('/users.json') // 获取用户列表
    .then(response => response.json()) // 解析 JSON
    .then(users => users[0]) // 选择第一个用户
    .then(user => fetch(`/users/${user.name}`)) // 获取用户数据
    .then(userResponse => userResponse.json()) // 解析 JSON
}

getFirstUserData()
```

改成 await/async 的格式

```js
const getFirstUserData = async () => {
  const response = await fetch('/users.json') // 获取用户列表
  const users = await response.json() // 解析 JSON
  const user = users[0] // 选择第一个用户
  const userResponse = await fetch(`/users/${user.name}`) // 获取用户数据
  const userData = await userResponse.json() // 解析 JSON
  return userData
}

getFirstUserData()
```

#### 多个异步函数串联

异步函数可以很容易地链接起来，并且语法比普通的 promise 更具可读性：

```js
const promiseToDoSomething = () => {
  return new Promise(resolve => {
    setTimeout(() => resolve('做些事情'), 10000)
  })
}

const watchOverSomeoneDoingSomething = async () => {
  const something = await promiseToDoSomething()
  return something + ' 查看'
}

const watchOverSomeoneWatchingSomeoneDoingSomething = async () => {
  const something = await watchOverSomeoneDoingSomething()
  return something + ' 再次查看'
}

watchOverSomeoneWatchingSomeoneDoingSomething().then(res => {
  console.log(res)
})
```

结果为

```text
做些事情 查看 再次查看
```
