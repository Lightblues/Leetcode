
## 函数

- 参数
    - `function foo(a, b, ...rest) {}`; `arguments` 对象; 值传递, 对象引用是值
- 变量作用域
    - 变量提升; 全局作用域; 申明块级作用域 let, const
- Function 构造器
    - `var myFunction = new Function("a", "b", "return a * b");`
- 解构赋值: 类似Python中的序列解包
    - 对象的解构赋值. 别名; 嵌套; 默认值; 在函数传参时使用
- 对象的方法
    - this 关键词
    - apply, call(). `Math.max.apply(null, [3, 5, 4]);`
- 高阶函数
    - forEach
    - map, reduce
    - filter
    - sort. `sort((firstEl, secondEl) => { /* ... */ } )` 注意返回 -1,0,1 负数表示优先级高
    - every
    - find, findIndex
- 函数闭包: 返回一个新的函数
    - 作用: 1. 可以像 class 一样定义私有变量; 2. 可以封装新的函数
- 箭头函数: 主要区别在于对于 this 的指向进行了一定修复, 其内部的 this 是词法作用域, 由上下文确定
- generator 生成器: 类似 Python
    - 作用: 1. 可以记录过程中变量, 完成 object 采用实现的任务; 2. 更重要的是, 可以把异步回调代码变成“同步”代码

## 标准对象

- `number`、`string`、`boolean`、`function` 和 `undefined`
- 包装对象, `Number, Boolean, String`; 注意用 new 来创建的话将返回一个对象
- 转为数字 `parseInt(), parseFloat()`
- 所有 JavaScript 数据类型都有 valueOf() 和 toString() 方法
- 判断
    - 是否为 array `Array.isArray(arr)`
    - 是否为 null `myVar === null` (null 类型为 object)
    - 是否存在 `typeof myVar === 'undefined'`
- Date
    - `var now = new Date();`
    - Date 对象的方法: getFullYear, getMonth, getDate, getDay, getHours, getMinutes, getSeconds, getMilliseconds
        - getTime 返回时间戳
    - now 方法返回时间戳 `Date.now()`
    - parse 方法: `var d = Date.parse('2015-06-24T19:49:22.875+08:00');`
- RegExp
    - `/正则表达式/`, 表达式内的 `\` 符号不需要转义, 若用 new 创建输入的字符串需要转义
    - 标志: g 全局 (记录 lastIndex 再次运行回往后匹配), i 忽略大小写, m 多行
    - test
    - `exec` 匹配失败返回 null, 成功则返回 Array, 其中第一个为完整匹配, 后面是分组
    - 默认贪婪匹配, 加 `?` 非贪婪, 例如 `var re = /^(\d+?)(0*)$/;` 第二组匹配最后的 0
    - 正则基础
        - `*, +, ?, {n}, {n,m}` 限制长度
- JSON
    - 序列化: `JSON.stringify()`, 第二个参数为对 key, value 进行处理的函数, 第三个参数指定输出个数
        - 还可以通过指定 object 的 `toJSON` 方法自定义输出对象内容
    - 反序列化: `JSON.parse('{"name":"小明","age":14}')`

### 字符串

- length,
- indexOf(), lastIndexOf(), search,
- slice(), substring(), substr(),
- replace(),
- toUpperCase(), toLowerCase(),
- concat(),
- trim(),
- charAt(), charCodeAt(),
- split()

### Number

- toString(2/10/16), toExponential(), toFixed(), toPrecision(),
- valueOf(),
- MAX_VALUE, MIN_VALUE, NEGATIVE_INFINITY, NaN, POSITIVE_INFINITY

## 面向对象编程

- js 中通过原型（prototype）来实现面向对象编程 OOM
- 一个对象的 `__proto__` 属性 指向其原型
- 一个构造函数及其所构造出来的对象满足关系 `foo.__proto__ === Foo.prototype` , 这里的 foo 通过 `new Foo()` 构造.
- 构造函数
    - 使用 `new` 关键字创建;
    - 为了避免冗余, 不应该在构造函数中定义方法, 而应该定义在其原型上, 例如 `Student.prototype.func = ...`
- 注意区分:
    - `prototype` 是函数独有的属性
    - `__proto__` 和 `constructor` 是对象的属性; 但是由于 JS 中函数也是一种对象，所以函数也拥有
- 不应该操作 `__proto__` 属性
- 如何实现继承 (实现构造函数)? 由于还需要引入构造函数的 prototype, 需要利用一个无关的空函数 new 一个原型对象, 然后调整继承链
- class 关键词
    - 语法: `class Student {}`
        - `class`的定义包含了构造函数 `constructor`和定义在原型对象上的方法（注意没有`function`关键字）
    - 继承: `class PrimaryStudent extends Student {}`; 记得在 constructor 函数中调用父类的构造方法 `super(name);` super 就是父类的构造函数

## 浏览器

- 浏览器对象
    - window,
    - nevigator, 浏览器信息.
        - 属性: appName, appVersion, language, platform, userAgent
        - 注意 navigator 的信息可以很容易地被用户修改，所以JavaScript读取的值不一定是正确的
    - screen, 属性有 width, height, colorDepth
    - location, 当前 URL信息
        - `href` 完整 URL
        - `protocol`, `host`, `port`, `pathname`; 以及 `search`, `hash`
    - history 避免使用
- document; 操作对象
    - title (对应 html)
    - cookie
    - 方法:
        - `getElementById, getElementsByTagName, getElementsByClassName`
        - `querySelector()` 和 `querySelectorAll()`
    - 节点属性
        - innerHTML, innerText, id
        - parentNode, chilren (注意 rrray.from() 转为列表), firstElementChild, lastElementChild
        - setAttribute 方法, 例如 `setAttribute('type', 'text/css')`
    - 插入
        - 插入子节点 `appendChild`
            - `document.createElement('p')`, 并修改 innerText 等属性
        - 插入到指定位置 `parentElement.insertBefore(newElement, referenceElement);`
    - 删除
        - `parent.removeChild(parent.children[0])`
- 操作表单
- 操作文件
- AJAX
    - Asynchronous JavaScript and XML, 用JavaScript执行异步网络请求
    - XMLHttpRequest
        - `var request = new XMLHttpRequest();` 创建了`XMLHttpRequest`对象后，要先设置`onreadystatechange`的回调函数。在回调函数中，通常我们只需通过`readyState === 4`判断请求是否完成，如果已完成，再根据`status === 200`判断是否是一个成功的响应
        - `XMLHttpRequest`对象的`open()`方法有3个参数，第一个参数指定是`GET`还是`POST`，第二个参数指定URL地址，第三个参数指定是否使用异步，默认是`true`，所以不用写
        - 最后 `request.send();`
    - JSONP, 参见 [说说JSON和JSONP，也许你会豁然开朗，含jQuery用例](https://www.cnblogs.com/dowinning/archive/2012/04/19/json-jsonp-jquery.html)
    - CORS全称 `Cross-Origin Resource Sharing` ，是HTML5规范定义的如何跨域访问资源
- Promise
    - `setTimeout(callback, 1000);`
    - 语法:
        - `var p1 = new Promise(test);` 新建 Promise 对象, 其中回调函数 `function test(resolve, reject) {}` 是我们主要关心的函数逻辑,
            - 其中 resolve, reject 分别是执行成功或失败之后的操作, 不关心
        - `var p2 = p1.then(function (result) {})`. 这里 `then` 中传入的就是上面的 resolve
        - `var p3 = p2.catch(function (reason) {})`. 其中 `catch` 传入的是 reject
        - 可以串联写成 `new Promise(test).then(resolve).catch(reject)` 的形式
    - 作用: Promise最大的好处是在异步执行的流程中，把执行代码和处理结果的代码清晰地分离了
    - 串行: `job1.then(job2).then(job3).catch(handleError);` 其中 job1,2,3 都是 Promise 对象
    - 并行
        - `Promise.all([p1, p2])` 全部执行, 输出(then 的输入) 也是一个 Array
        - `Promise.race([p1, p2])` 哪个先返回就执行哪个
- Canvas

## jQuery

- `$` 符号: 是 `jQuery`的别名
- 选择器: `$('#dom-id')`
    - 返回 jQuery 对象. 找不到也不返回 undefined 而是类似 `[]`
    - 相互转化: 对于 `var div = $('#abc');` 这一 jQuery 对象, 可以 `var divDom = div.get(0);` 转为 DOM 对象; `var another = $(divDom);` 将 DOM 对象转为 jQuery 对象
    - 选择语法:
        - tag 直接写 tag 名称 `var ps = $('p');`
        - id 用`#id`, class 用 `$('.red.green')` 可以写多个;
        - 属性 `$('[name=email]')`
            - 前缀或后缀匹配 `$('[class^="icon-"]')`
        - 组合查找 `$('input[name=email]');`
        - 多项选择器, `,`, 例如 `$('p.red,p.green');`
        - 层次选择 `$('form[name=upload] input');`
        - 子选择器限制为父子关系 `$('ul.lang>li.lang-javascript');`
    - 过滤
        - `:` 后加筛选条件
        - `first-child, last-child, nth-child(2), nth-child(even)`
        - visible, hidden, 如 `$('div:visible');`
        - 表单选择器
            - :input, :file, :checkbox, :radio, :focus, :checked, :enabled/disabled
- 操作 DOM
    - 修改文本: jQuery对象的`text()`和`html()`方法
    - 修改 CSS
        - 直接写改 style 可以用 `css('name', 'value')` 方法
        - 或者修改 class 可以 `hasClass(), addClass(), removeClass()`
- 事件
    - 绑定表单提交 `$('#testForm).on('submit', function () {})`
    - 对于 DOM ready 后绑定, `$(document).on('ready', function () {})` 可以简写为 `$(document).ready(f)` 或者直接 `$(f)`
    - 要取消绑定一个特定的回调函数, `off('click', function)`
    - 事件触发条件: `trigger('change')` 或者 简写成无参数的`change()`方法 (模拟用户改动 input 文字)
- AJAX
    - 可以通过 `$.ajax(url, settings)` 处理 AJAX 请求
        - settings 中的选项包括 `method, contentType, data, headers, dataType` 等
        - 通过 `done, fail, always` 方法来进行类似 Promise 的处理
    - 对于常用的请求, 可以简写成 `$.get(rul, paras)` `$.post(url, paras)`
        - `$.getJSON(url, paras)` 快速通过GET获取一个JSON对象
- jQuery 插件
    - 给 `$.fn` 绑定函数，实现插件的代码逻辑
    - 插件函数要有默认值，绑定在 `$.fn.<pluginName>.defaults` 上
        - 通过 `$.extend(target, obj1, obj2, ...)` 来合并后续 obj 的属性到 target 中

## 错误处理

- `try ... catch(e) ... finally`
- `e instanceof TypeError` 判断错误类型; `e.message`
- `throw new Error('输入错误');`
- 异步错误处理: 错误的处理应该在回调函数内部实现

## underscore

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

## Node

- CommonJS 规范
    - `const greet = require('./hello');`
    - `module.exports = variable;`
- Node 对象
    - global
        - 判断环境: `if (typeof(window) === 'undefined')` 则是 node 环境
    - process
        - 如果我们响应`exit`事件，可以 `process.on('exit', function (code) {}`
- fs 模块
    - 异步读取
        - `fs.readFile('sample.txt', 'utf-8', function (err, data) {})`
    - 同步读取
        - 没有回调函数 `var data = fs.readFileSync('sample.txt', 'utf-8');`
    - Buffer
        - 当读取二进制文件时，不传入文件编码时，回调函数的`data`参数将返回一个`Buffer`对象
        - 与字符串转换: `data.toString('utf-8')` 和 `Buffer.from(text, 'utf-8')`
    - stat 方法
        - `fs.stat()`，它返回一个`Stat`对象
        - 属性: `isFile, isDirectory`, `size`, `birthtime, mtime`
- stream 模块
    - 读取
        - `var rs = fs.createReadStream('sample.txt', 'utf-8');`
        - 流是一个对象，我们只需要响应流的事件就可以了：`data` 事件表示流的数据已经可以读取了，`end` 事件表示这个流已经到末尾了，没有数据可以读取了，`error` 事件表示出错了
        - `rs.on('data', function (chunk) {...}`
    - pipe
        - 在Node.js中，`Readable`流有一个`pipe()`方法, 可以进行复制. `rs.pipe(ws);`
- http 模块
    - 提供的`request`和`response`对象
    - 创建 `var server = http.createServer(function (request, response) {}`
    - 端口监听 `server.listen(8080);`
    - `url` 模块: 通过`parse()` 将一个字符串解析为一个`Url`对象
- crypto 模块
    - hash, Hmac, AES, Diffie-Hellman, RSA

## Web 开发

- 如何运行?
    - 直接 node. `node app.js`
    - npm `npm start`. 需要在 `package.json` 中的 scripts 定义对应的 start 命令 (也是 node)
    - VSCode 中运行, 或配置 debug
- koa
    - koa middleware
        - `app.use(async (ctx, next) => {}` (每个async函数是 middleware)
        - 参数`ctx`是由koa传入的封装了request和response的变量，我们可以通过它访问request和response，`next`是koa传入的将要处理的下一个异步函数
    - `koa-router` 处理 URL
        - 使用`router.get('/path', async fn)`来注册一个GET请求。
        - 可以在请求路径中使用带变量的`/hello/:name`，变量可以通过`ctx.params.name`访问。
    - `koa-bodyparser` 解析 body
        - `app.use(bodyParser());`
        - 解析参数，把解析后的参数绑定到`ctx.request.body`中
    - Middleware
        - 代码重构. 例如对于 URL处理的代码放在同一个 controllers 文件夹中, 用专门写一个函数扫描`controllers`目录和创建`router`
- Nunjucks: 模板引擎
    - 作用: 特殊字符转义, 格式化, if, for 等逻辑
    - 对于 Python 中 jinja2 的 js 实现
    - 使用很方便: `var s = env.render('hello.html', { name: 'Tom' });`
    - block, 继承 `extends`
- mysql
    - sequelize, mysql2 包
    - 创建 sequelize 对象实例, 然后定义模型 (数据库表)
    - 操作
        - `create` 插入数据
        - `findAll` 查询
            - 对查询到的实例调用 `save, destory`
- mocha: 单元测试
    - 如何执行测试?
        - 方法一 `node_modules\mocha\bin\mocha`
        - 方法二，在 `package.json` 中添加 scripts `"test": "mocha"`, 然后 `npm test` 即可
        - 方法三，配置 VS Code, `.vscode/launch.json`, 定义 `"program": "${workspaceRoot}/node_modules/mocha/bin/mocha"` 以及 `"type": "node",` —— 其实就是运行 `node node_modules/mocha/bin/mocha`
    - assert 包: `const assert = require('assert');`
    - 如果要测试同步函数，我们传入无参数函数即可
        - `it(' description', function () {}`
        - 然后在其中 assert 判断即可
    - 如果要测试异步函数，我们要传入的函数需要带一个参数，通常命名为`done`
        - `it(' description', function (done) {}`
        - 然后在其中运行代测试的函数 f
        - 手动调用`done()`表示测试成功，`done(err)`表示测试出错
    - 对于 async 函数, 更方便的是直接将其转化为同步函数测试
        - 例如, 传入 `async () => { assert.strictEqual(await f(), groundTruth) }`
    - Http 测试: `supertest` 包
        - `request = require('supertest')`
        - 使用 `let res = await request(server).get('/');` 构造一个GET请求，发送给koa的应用，然后获得响应
        - 可以手动检查响应对象，例如，`res.body`，还可以利用`supertest`提供的`expect()`更方便地断言响应的HTTP代码、返回内容和HTTP头。断言HTTP头时可用使用正则表达式
- WebSocket
    - ws 协议
    - koa 和 ws 包可以共用一个端口, 比如默认的 3000. 因为 koa 实际上调用 Node标准http模块创建的 http.Server 监听的, 只是把响应函数注册到了其中, ws 也一样, 因此可以用一个端口, 根据协议不同分别由 koa 和 ws 处理.
    - 如何识别用户身份?
        - 总体而言, cookie 是一个服务端和客户端相互配合的过程. 服务器创建 cookie, 浏览器保存并在之后的请求中附加 cookie; 若要建立 ws 链接也用 cookie 即可.
    - 案例: 聊天室. 服务器维护一组 ws 连接, 每当收到一条消息之后, 广播到所有连接.
- REST
    - 获取资源用 GET, 新建、更新、删除 分别用 POST, PUT, DELETE 请求, 内容放在 body 中 (`Content-Type` 为 `application/json`)

## MVVM

- MVVM 的核心思路: 关注Model的变化，让MVVM框架去自动更新DOM的状态.
- ViewModel 负责把Model的数据同步到View显示出来，还负责把View的修改同步回Model
- 优势: 处理前端逻辑比较复杂的页面, 但是不适合展示数据的页面, 例如需要 SEO (Search Engine Optimization) 的页面
- Vue
    - 语法
        - `var vm = new Vue({})` 其中 `el` 指定绑定节点, `data` 定义了数据/模型
    - Vue 单向绑定: v-text
    - Vue 双向绑定
        - `<form id="vm" v-on:submit.prevent="register">`
    - 同步DOM结构: v-for
        - 注意, 可以监听数组的 `splice`、`push`、`unshift` 等方法调用, 但不能监听数组整体的赋值
    - 集成 API: `vue-resource` 包
        - 可以给VM对象加上一个`$resource`属性
        - `that.$resource('/api/todos').get().then(function (resp){}, function (resp){})`
