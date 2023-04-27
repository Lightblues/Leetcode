
## Node.js

!!! warning
    下面的主体是廖雪峰教程的笔记的一部分

!!! note
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

- 因为JavaScript是单线程执行，根本不能进行同步IO操作，所以，JavaScript的这一“缺陷”导致了它只能使用异步IO。
- 优势
    - 最大的优势是借助JavaScript天生的事件驱动机制加V8高性能引擎，使编写高性能Web服务轻而易举。
    - 在Node环境下，通过模块化的JavaScript代码，加上函数式编程，并且无需考虑浏览器兼容性问题，直接使用最新的ECMAScript 6标准，可以完全满足工程上的需求。
- <https://nodejs.org/zh-cn/>
- npm
    - npm其实是Node.js的包管理工具（package manager）
- Node
    - 命令行模式和Node交互模式
- [使用 VSCode 调试](https://www.liaoxuefeng.com/wiki/1022910821149312/1099503821472096)

### 模块

```js
/* hallo.js */
var s = 'Hello';

function greet(name) {
    console.log(s + ', ' + name + '!');
}

module.exports = greet;

/* main.js */
// 引入hello模块:
var greet = require('./hello');

var s = 'Michael';

greet(s); // Hello, Michael!
```

- 在使用`require()`引入模块的时候，请注意模块的相对路径。【例如，`./hello.js`】
- 如果只写模块名【如 `hello.js`】，则Node会依次在 **内置模块、全局模块和当前模块** 下查找hello.js。

#### CommonJS 规范

- 这种模块加载机制被称为CommonJS规范。在这个规范下，每个`.js`文件都是一个模块，它们内部各自使用的变量名和函数名都互不冲突，例如，`hello.js` 和 `main.js` 都申明了全局变量 `var s = 'xxx'`，但互不影响。
- 一个模块想要对外暴露变量（函数也是变量），可以用 `module.exports = variable;`，一个模块要引用其他模块暴露的变量，用 `var ref = require('module_name');` 就拿到了引用模块的变量。

#### 模块实现机制

- (浏览器中) JavaScript语言本身并没有一种模块机制来保证不同模块可以使用相同的变量名。
- 其实要实现“模块”这个功能，并不需要语法层面的支持。Node.js也并不会增加任何JavaScript语法。实现“模块”功能的奥妙就在于JavaScript是一种函数式编程语言，它支持闭包。如果我们把一段JavaScript代码用一个函数包装起来，这段代码的所有“全局”变量就变成了函数内部的局部变量。
- 模块的输出`module.exports`怎么实现？

```js
// 准备module对象:
var module = {
    id: 'hello',
    exports: {}
};
var load = function (module) {
    // 读取的hello.js代码:
    function greet(name) {
        console.log('Hello, ' + name + '!');
    }
    
    module.exports = greet;
    // hello.js代码结束
    return module.exports;
};
var exported = load(module);
// 保存module:
save(module, exported);
```

### 基本模块

因为 Node.js 是运行在服务区端的 JavaScript 环境，服务器程序和浏览器程序相比，最大的特点是没有浏览器的安全限制了，而且，服务器程序必须能接收网络请求，读写文件，处理二进制内容，所以，Node.js内置的常用模块就是为了实现基本的服务器功能。这些模块在浏览器环境中是无法被执行的，因为它们的底层代码是用C/C++在Node.js运行环境中实现的。

#### Node 模块基础

- global
    - JavaScript有且仅有一个全局对象，在浏览器中，叫`window`对象。而在Node.js环境中，也有唯一的全局对象，叫`global`，这个对象的属性和方法也和浏览器环境的`window`不同
    - `global.console`
- process
    - `process`也是Node.js提供的一个对象，它代表当前Node.js进程。
    - JavaScript程序是由事件驱动执行的单线程模型，Node.js也不例外。Node.js不断执行响应事件的JavaScript函数，直到没有任何响应事件的函数可以执行时，Node.js就退出了。
    - 如果我们想要在下一次事件响应中执行代码，可以调用`process.nextTick()`
    - Node.js进程本身的事件就由`process`对象来处理。如果我们响应`exit`事件，可以 `process.on('exit', function (code) {}`
- 判断 js 执行环境
    - 常用的方式就是根据浏览器和Node环境提供的全局变量名称来判断
    - `if (typeof(window) === 'undefined')` 则是 node 环境

```js
> global.console
Console {
  log: [Function: bound ],
  info: [Function: bound ],
  warn: [Function: bound ],
  error: [Function: bound ],
  dir: [Function: bound ],
  time: [Function: bound ],
  timeEnd: [Function: bound ],
  trace: [Function: bound trace],
  assert: [Function: bound ],
  Console: [Function: Console] }
```

```js
> process === global.process;
true
> process.version;
'v5.2.0'
> process.platform;
'darwin'
> process.arch;
'x64'
> process.cwd(); //返回当前工作目录
'/Users/michael'
> process.chdir('/private/tmp'); // 切换当前工作目录
undefined
> process.cwd();
'/private/tmp'
```

```js
// test.js

// process.nextTick()将在下一轮事件循环中调用:
process.nextTick(function () {
    console.log('nextTick callback!');
});
console.log('nextTick was set!');
```

```js
// 程序即将退出时的回调函数:
process.on('exit', function (code) {
    console.log('about to exit with code: ' + code);
});
```

```js
// 判断JavaScript执行环境
if (typeof(window) === 'undefined') {
    console.log('node.js');
} else {
    console.log('browser');
}
```

#### fs 模块

- Node.js内置的`fs`模块就是文件系统模块，负责读写文件。
- 和所有其它JavaScript模块不同的是，`fs` 模块同时提供了异步和同步的方法。
- 异步读取
    - `fs.readFile('sample.txt', 'utf-8', function (err, data) {})`
    - 第二个参数: 文件编码
    - 异步读取时，传入的回调函数接收两个参数，当正常读取时，`err`参数为`null`，`data`参数为读取到的String。当读取发生错误时，`err`参数代表一个错误对象，`data`为`undefined`。这也是Node.js标准的回调函数：第一个参数代表错误信息，第二个参数代表结果。
    - 当读取二进制文件时，不传入文件编码时，回调函数的`data`参数将返回一个`Buffer`对象。在Node.js中，`Buffer`对象就是一个包含零个或任意个字节的数组（注意和Array不同）。
        - Buffer 对象可以和 String 转换,
        - `data.toString('utf-8')` 和 `Buffer.from(text, 'utf-8')`
- 同步读取
    - `var data = fs.readFileSync('sample.txt', 'utf-8');`
    - 不传入回调函数, 直接返回
    - 如果同步读取文件发生错误，则需要用`try...catch`捕获该错误
- 写文件
    - `fs.writeFile('output.txt', data, function (err) {})`
    - `writeFile()`的参数依次为文件名、数据和回调函数。如果传入的数据是String，默认按UTF-8编码写入文本文件，如果传入的参数是`Buffer`，则写入的是二进制文件。回调函数由于只关心成功与否，因此只需要一个`err`参数。
    - `fs.writeFileSync('output.txt', data);`
- stat
    - 如果我们要获取文件大小，创建时间等信息，可以使用`fs.stat()`，它返回一个`Stat`对象，能告诉我们文件或目录的详细信息
    - 属性:
        - `isFile, isDirectory`,
        - `size`
        - `birthtime, mtime`

##### 异步读文件

按照JavaScript的标准，异步读取一个文本文件的代码如下：

```js
var fs = require('fs');

fs.readFile('sample.txt', 'utf-8', function (err, data) {
    if (err) {
        console.log(err);
    } else {
        console.log(data);
    }
});
```

异步读取时，传入的回调函数接收两个参数，当正常读取时，`err`参数为`null`，`data`参数为读取到的String。当读取发生错误时，`err`参数代表一个错误对象，`data`为`undefined`。这也是Node.js标准的回调函数：第一个参数代表错误信息，第二个参数代表结果。后面我们还会经常编写这种回调函数。

- 当读取二进制文件时，不传入文件编码时，回调函数的`data`参数将返回一个 `Buffer` 对象。在Node.js中，`Buffer`对象就是一个包含零个或任意个字节的 **数组** （注意和Array不同）。
- `Buffer`对象可以和String作转换

```js
// Buffer -> String
var text = data.toString('utf-8');
console.log(text);

// String -> Buffer
var buf = Buffer.from(text, 'utf-8');
console.log(buf);
```

##### 同步读文件

- 除了标准的异步读取模式外，`fs`也提供相应的同步读取函数。同步读取的函数和异步函数相比，多了一个`Sync`后缀，并且不接收回调函数，函数直接返回结果。
- 可见，原异步调用的回调函数的`data`被函数直接返回，函数名需要改为`readFileSync`，其它参数不变。
- 如果同步读取文件发生错误，则需要用`try...catch`捕获该错误

```js
try {
    var data = fs.readFileSync('sample.txt', 'utf-8');
    console.log(data);
} catch (err) {
    // 出错了
}
```

##### 异步还是同步

- 在`fs`模块中，提供同步方法是为了方便使用。那我们到底是应该用异步方法还是同步方法呢？
- 由于Node环境执行的JavaScript代码是服务器端代码，所以，绝大部分需要在服务器运行期反复执行业务逻辑的代码，**必须使用异步代码**，否则，同步代码在执行时期，服务器将停止响应，因为JavaScript只有一个执行线程。
- 服务器启动时如果需要读取配置文件，或者结束时需要写入到状态文件时，可以使用同步代码，因为这些代码只在启动和结束时执行一次，不影响服务器正常运行时的异步执行。

#### stream 模块

- `stream` 是Node.js提供的又一个仅在服务端可用的模块，目的是支持“流”这种数据结构。
- 流的特点是数据是有序的，而且必须依次读取，或者依次写入，不能像Array那样随机定位。
- 在Node.js中，流也是一个对象，我们只需要响应流的事件就可以了：`data`事件表示流的数据已经可以读取了，`end`事件表示这个流已经到末尾了，没有数据可以读取了，`error`事件表示出错了。
    - `var rs = fs.createReadStream('sample.txt', 'utf-8');`
    - 要注意，`data`事件可能会有多次，每次传递的`chunk`是流的一部分数据。
- 写入: 要以流的形式写入文件，只需要不断调用`write()`方法 (可以传入字符串或 Buffer)，最后以`end()`结束
    - `var ws1 = fs.createWriteStream('output1.txt', 'utf-8');`
- 所有可以读取数据的流都继承自`stream.Readable`，所有可以写入的流都继承自`stream.Writable`。
- pipe
    - 就像可以把两个水管串成一个更长的水管一样，两个流也可以串起来。一个`Readable`流和一个`Writable`流串起来后，所有的数据自动从`Readable`流进入`Writable`流，这种操作叫`pipe`。
    - 在Node.js中，`Readable`流有一个`pipe()`方法, 可以进行复制
    - `rs.pipe(ws);`
    - 默认情况下，当`Readable`流的数据读取完毕，`end`事件触发后，将自动关闭`Writable`流。如果我们不希望自动关闭`Writable`流，需要传入参数 `readable.pipe(writable, { end: false });`

```js
/* 从文件流读取文本内容 */
var fs = require('fs');

// 打开一个流:
var rs = fs.createReadStream('sample.txt', 'utf-8');

rs.on('data', function (chunk) {
    console.log('DATA:')
    console.log(chunk);
});

rs.on('end', function () {
    console.log('END');
});

rs.on('error', function (err) {
    console.log('ERROR: ' + err);
});
```

以流的形式写入文件

```js
var fs = require('fs');

var ws1 = fs.createWriteStream('output1.txt', 'utf-8');
ws1.write('使用Stream写入文本数据...\n');
ws1.write('END.');
ws1.end();

var ws2 = fs.createWriteStream('output2.txt');
ws2.write(new Buffer('使用Stream写入二进制数据...\n', 'utf-8'));
ws2.write(new Buffer('END.', 'utf-8'));
ws2.end();
```

pipe

```js
var fs = require('fs');

var rs = fs.createReadStream('sample.txt');
var ws = fs.createWriteStream('copied.txt');

rs.pipe(ws);
```

#### http 模块

- 要理解Web服务器程序的工作原理，首先，我们要对HTTP协议有基本的了解。如果你对HTTP协议不太熟悉，先看一看 [HTTP协议简介](http://www.liaoxuefeng.com/wiki/1016959663602400/1017804782304672)。
- 要开发HTTP服务器程序，从头处理TCP连接，解析HTTP是不现实的。这些工作实际上已经由Node.js自带的`http`模块完成了。应用程序并不直接和HTTP协议打交道，而是操作`http`模块提供的`request`和`response`对象。
    - `request`对象封装了HTTP请求，我们调用`request`对象的属性和方法就可以拿到所有HTTP请求的信息；
    - `response`对象封装了HTTP响应，我们操作`response`对象的方法，就可以把HTTP响应返回给浏览器。
- `var server = http.createServer(function (request, response) {}` (直接去看示例代码)
- 然后设置监听 `server.listen(8080);`
- 其他模块
    - 解析URL需要用到Node.js提供的`url`模块，它使用起来非常简单，通过`parse()` 将一个字符串解析为一个`Url`对象
    - 处理本地文件目录需要使用Node.js提供的`path`模块，它可以方便地构造目录

用Node.js实现一个HTTP服务器程序非常简单。我们来实现一个最简单的Web程序`hello.js`，它对于所有请求，都返回`Hello world!`：

```js
// 导入http模块:
var http = require('http');

// 创建http server，并传入回调函数:
var server = http.createServer(function (request, response) {
    // 回调函数接收request和response对象,
    // 获得HTTP请求的method和url:
    console.log(request.method + ': ' + request.url);
    // 将HTTP响应200写入response, 同时设置Content-Type: text/html:
    response.writeHead(200, {'Content-Type': 'text/html'});
    // 将HTTP响应的HTML内容写入response:
    response.end('<h1>Hello world!</h1>');
});

// 让服务器监听8080端口:
server.listen(8080);

console.log('Server is running at http://127.0.0.1:8080/');
```

- 让我们继续扩展一下上面的Web程序。我们可以设定一个目录，然后让Web程序变成一个文件服务器。要实现这一点，我们只需要解析`request.url`中的路径，然后在本地找到对应的文件，把文件内容发送出去就可以了。
- 解析URL需要用到Node.js提供的`url`模块，它使用起来非常简单，通过`parse()`将一个字符串解析为一个`Url`对象

```js
var url = require('url');

console.log(url.parse('http://user:pass@host.com:8080/path/to/file?query=string#hash'));
```

结果为

```js
Url {
  protocol: 'http:',
  slashes: true,
  auth: 'user:pass',
  host: 'host.com:8080',
  port: '8080',
  hostname: 'host.com',
  hash: '#hash',
  search: '?query=string',
  query: 'query=string',
  pathname: '/path/to/file',
  path: '/path/to/file?query=string',
  href: 'http://user:pass@host.com:8080/path/to/file?query=string#hash' }
```

我们实现一个文件服务器`file_server.js`：

```js
var
    fs = require('fs'),
    url = require('url'),
    path = require('path'),
    http = require('http');

// 从命令行参数获取root目录，默认是当前目录:
var root = path.resolve(process.argv[2] || '.');

console.log('Static root dir: ' + root);

// 创建服务器:
var server = http.createServer(function (request, response) {
    // 获得URL的path，类似 '/css/bootstrap.css':
    var pathname = url.parse(request.url).pathname;
    // 获得对应的本地文件路径，类似 '/srv/www/css/bootstrap.css':
    var filepath = path.join(root, pathname);
    // 获取文件状态:
    fs.stat(filepath, function (err, stats) {
        if (!err && stats.isFile()) {
            // 没有出错并且文件存在:
            console.log('200 ' + request.url);
            // 发送200响应:
            response.writeHead(200);
            // 将文件流导向response:
            fs.createReadStream(filepath).pipe(response);
        } else {
            // 出错了或者文件不存在:
            console.log('404 ' + request.url);
            // 发送404响应:
            response.writeHead(404);
            response.end('404 Not Found');
        }
    });
});

server.listen(8080);

console.log('Server is running at http://127.0.0.1:8080/');
```

- 没有必要手动读取文件内容。由于`response`对象本身是一个`Writable Stream`，直接用`pipe()`方法就实现了自动读取文件内容并输出到HTTP响应。

#### crypto 模块

- crypto模块的目的是为了提供通用的加密和哈希算法。用纯JavaScript代码实现这些功能不是不可能，但速度会非常慢。Nodejs用C/C++实现这些算法后，通过cypto这个模块暴露为JavaScript接口，这样用起来方便，运行速度也快。
- hash
    - `const hash = crypto.createHash('md5');` 可以是 md5, sha1, sha256, sha512
    - 可以任意次 `hash.update('Hello, world!');`. 默认字符串编码为`UTF-8`，也可以传入Buffer
    - 得到 hash 值 `hash.digest('hex')`
- Hmac 算法也是一种 hash 算法, 不同的是需要一个密钥
    - `const hmac = crypto.createHmac('sha256', 'secret-key');`
- AES
    - AES是一种常用的对称加密算法，加解密都用同一个密钥.
    - 包括 aes192, aes-128-ecb, aes-256-cbc 等
    - `const cipher = crypto.createCipher('aes192', key);`
    - `const decipher = crypto.createDecipher('aes192', key);`
- Diffie-Hellman
    - DH算法是一种密钥交换协议，它可以让双方在不泄漏密钥的情况下协商出一个密钥来
    - `crypto.createDiffieHellman`
- RSA
    - RSA算法是一种非对称加密算法，即由一个私钥和一个公钥构成的密钥对，通过私钥加密，公钥解密，或者通过公钥加密，私钥解密
    - 当小明给小红发送信息时，可以用小明自己的私钥加密，小红用小明的公钥解密，也可以用小红的公钥加密，小红用她自己的私钥解密，这就是非对称加密。相比对称加密，非对称加密只需要每个人各自持有自己的私钥，同时公开自己的公钥，不需要像AES那样由两个人共享同一个密钥。
    - 使用私钥加密 `let enc_by_prv = crypto.privateEncrypt(prvKey, Buffer.from(message, 'utf8'));` 返回的是 Buffer
    - 使用公钥解密 `let dec_by_pub = crypto.publicDecrypt(pubKey, enc_by_prv);`
    - RSA加密的原始信息必须小于Key的长度。那如何用RSA加密一个很长的消息呢？实际上，RSA并不适合加密大数据，而是先生成一个随机的AES密码，用AES加密原始信息，然后用RSA加密AES口令，这样，实际使用RSA时，给对方传的密文分两部分，一部分是AES加密的密文，另一部分是RSA加密的AES口令。对方用RSA先解密出AES口令，再用AES解密密文，即可获得明文。

```js
/* 封装 AES 函数便于使用 */
const crypto = require('crypto');

function aesEncrypt(data, key) {
    const cipher = crypto.createCipher('aes192', key);
    var crypted = cipher.update(data, 'utf8', 'hex');
    crypted += cipher.final('hex');
    return crypted;
}

function aesDecrypt(encrypted, key) {
    const decipher = crypto.createDecipher('aes192', key);
    var decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

var data = 'Hello, this is a secret message!';
var key = 'Password!';
var encrypted = aesEncrypt(data, key);
var decrypted = aesDecrypt(encrypted, key);

console.log('Plain text: ' + data);
console.log('Encrypted text: ' + encrypted);
console.log('Decrypted text: ' + decrypted);
```

生成RSA密钥

```bash
# 生成一个RSA密钥对
# 需要输入密码, 这个密码是用来加密RSA密钥的; 加密方式指定为AES256，生成的RSA的密钥长度是2048位
openssl genrsa -aes256 -out rsa-key.pem 2048
# 导出私钥和公钥, 需要输入之前的密码
openssl rsa -in rsa-key.pem -outform PEM -out rsa-prv.pem
openssl rsa -in rsa-key.pem -outform PEM -pubout -out rsa-pub.pem
```

### Web 开发

- 最早的软件都是运行在大型机上的，软件使用者通过“哑终端”登陆到大型机上去运行软件。后来随着PC机的兴起，软件开始主要运行在桌面上，而数据库这样的软件运行在服务器端，这种Client/Server模式简称CS架构。
- 随着互联网的兴起，人们发现，CS架构不适合Web，最大的原因是Web应用程序的修改和升级非常迅速，而CS架构需要每个客户端逐个升级桌面App，因此，Browser/Server模式开始流行，简称BS架构。
    - 在BS架构下，客户端只需要浏览器，应用程序的逻辑和数据都存储在服务器端。浏览器只需要请求服务器，获取Web页面，并把Web页面展示给用户即可。
    - 今天，除了重量级的软件如Office，Photoshop等，大部分软件都以Web形式提供。比如，新浪提供的新闻、博客、微博等服务，均是Web应用。
- Web开发也经历了好几个阶段：
    - ·CGI：由于静态Web页面无法与用户交互，比如用户填写了一个注册表单，静态Web页面就无法处理。要处理用户发送的动态数据，出现了Common Gateway Interface，简称CGI，用C/C++编写。
    - ASP/JSP/PHP：由于Web应用特点是修改频繁，用C/C++这样的低级语言非常不适合Web开发，而脚本语言由于开发效率高，与HTML结合紧密，因此，迅速取代了CGI模式。ASP是微软推出的用VBScript脚本编程的Web开发技术，而JSP用Java来编写脚本，PHP本身则是开源的脚本语言。
    - MVC：为了解决直接用脚本语言嵌入HTML导致的可维护性差的问题，Web应用也引入了Model-View-Controller的模式，来简化Web开发。ASP发展为ASP.Net，JSP和PHP也有一大堆MVC框架。
- 由于Node.js把JavaScript引入了服务器端，因此，原来必须使用PHP/Java/C#/Python/Ruby等其他语言来开发服务器端程序，现在可以使用Node.js开发了！
    - 在Node.js诞生后的短短几年里，出现了无数种Web框架、ORM框架、模版引擎、测试框架、自动化构建工具
    - 常见的Web框架包括：[Express](http://expressjs.com/)，[Sails.js](http://sailsjs.org/)，[koa](http://koajs.com/)，[Meteor](https://www.meteor.com/)，[DerbyJS](http://derbyjs.com/)，[Total.js](https://www.totaljs.com/)，[restify](http://restify.com/)……
    - ORM 框架比Web框架要少一些：[Sequelize](http://www.sequelizejs.com/)，[ORM2](http://dresende.github.io/node-orm2/)，[Bookshelf.js](http://bookshelfjs.org/)，[Objection.js](http://vincit.github.io/objection.js/)……
    - 模版引擎PK：[Jade](http://jade-lang.com/)，[EJS](http://ejs.co/)，[Swig](https://github.com/paularmstrong/swig)，[Nunjucks](http://mozilla.github.io/nunjucks/)，[doT.js](http://olado.github.io/doT/)……
    - 测试框架包括：[Mocha](http://mochajs.org/)，[Expresso](http://visionmedia.github.io/expresso/)，[Unit.js](http://unitjs.com/)，[Karma](http://karma-runner.github.io/)……
    - 构建工具有：[Grunt](http://gruntjs.com/)，[Gulp](http://gulpjs.com/)，[Webpack](http://webpack.github.io/)……

#### koa

- koa是Express的下一代基于Node.js的web框架
- 历史
    - Express是第一代最流行的web框架，它对Node.js的http进行了封装
        - 虽然Express的API很简单，但是它是基于ES5的语法，要实现异步代码，只有一个方法：回调。如果异步嵌套层次过多，代码写起来就非常难看
    - koa 1.0
        - 随着新版Node.js开始支持ES6，Express的团队又基于ES6的generator重新编写了下一代web框架koa。和Express相比，koa 1.0使用generator实现异步，代码看起来像同步的
        - 用generator实现异步比回调简单了不少，但是generator的本意并不是异步。Promise才是为异步设计的，但是Promise的写法……想想就复杂。为了简化异步代码，ES7（目前是草案，还没有发布）引入了新的关键字`async`和`await`，可以轻松地把一个function变为异步模式
    - koa2
        - koa团队并没有止步于koa 1.0，他们非常超前地基于ES7开发了koa2，和koa 1相比，koa2完全使用Promise并配合`async`来实现异步。

##### 入门

如何安装 koa 包?

- 方法一：可以用npm命令直接安装koa。 `npm install koa@2.0.0`
- 方法二：在`hello-koa`这个目录下创建一个`package.json`，这个文件描述了我们的`hello-koa`工程会用到哪些包。
    - 最重要的是在 `dependencies` 中指定 `"koa": "2.0.0"`
    - `npm install`

如何运行?

- 点击 VSCode 上的运行按钮 (可以看到调用了 node 命令)
- 直接用命令 `node app.js` 在命令行启动程序
- 或者用`npm start`启动。`npm start` 命令会让npm执行定义在 `package.json` 文件中的start对应命令.
    - 在 `scripts` 中指定 `"start": "node --use_strict app.js"`

##### koa middleware

- 核心代码
    - `app.use(async (ctx, next) => {}`
    - 每收到一个http请求，koa就会调用通过`app.use()`注册的async函数，并传入`ctx`和`next`参数。
        - 参数`ctx`是由koa传入的封装了request和response的变量，我们可以通过它访问request和response，`next`是koa传入的将要处理的下一个异步函数。
        - 由`async`标记的函数称为异步函数，在异步函数中，可以用`await`调用另一个异步函数，这两个关键字将在ES7中引入。
    - koa把很多async函数组成一个处理链，每个async函数都可以做一些自己的事情，然后用`await next()`来调用下一个async函数。我们把每个async函数称为middleware，这些middleware可以组合起来，完成很多有用的功能。

```js
/* app.js */
// 导入koa，和koa 1.x不同，在koa2中，我们导入的是一个class，因此用大写的Koa表示:
const Koa = require('koa');

// 创建一个Koa对象表示web app本身:
const app = new Koa();

// 对于任何请求，app将调用该异步函数处理请求：
app.use(async (ctx, next) => {
    await next();
    ctx.response.type = 'text/html';
    ctx.response.body = '<h1>Hello, koa2!</h1>';
});

// 在端口3000监听:
app.listen(3000);
console.log('app started at port 3000...');
```

处理链示例如下 (观察 next 函数的位置)

```js
// 可以用以下3个middleware组成处理链，依次打印日志，记录处理时间，输出HTML
app.use(async (ctx, next) => {
    console.log(`${ctx.request.method} ${ctx.request.url}`); // 打印URL
    await next(); // 调用下一个middleware
});

app.use(async (ctx, next) => {
    const start = new Date().getTime(); // 当前时间
    await next(); // 调用下一个middleware
    const ms = new Date().getTime() - start; // 耗费时间
    console.log(`Time: ${ms}ms`); // 打印耗费时间
});

app.use(async (ctx, next) => {
    await next();
    ctx.response.type = 'text/html';
    ctx.response.body = '<h1>Hello, koa2!</h1>';
});
```

##### 处理URL

- `koa-router`
    - 为了处理URL，我们需要引入`koa-router`这个middleware，让它负责处理URL映射
    - 注意, 导入的是一个函数 `const router = require('koa-router')();`
- get
    - 使用`router.get('/path', async fn)`来注册一个GET请求。
    - 可以在请求路径中使用带变量的`/hello/:name`，变量可以通过`ctx.params.name`访问。
- `koa-bodyparser`
    - post请求通常会发送一个表单，或者JSON，它作为request的body发送，但无论是Node.js提供的原始request对象，还是koa提供的request对象，都 不提供 解析request的body的功能！
    - 因此, 需要另一个 middleware `koa-bodyparser`. 用它解析参数，然后把解析后的参数，绑定到`ctx.request.body`中
    - 需要在合适的位置加上 `app.use(bodyParser());`
- post
    - `router.post('/path', async fn)`
    - 然后可以用 `ctx.request.body` 得到解析好的 request的body
- 类似的，put、delete、head请求也可以由router处理。

```js
const Koa = require('koa');

// 注意require('koa-router')返回的是函数:
const router = require('koa-router')();

const app = new Koa();

// log request URL:
app.use(async (ctx, next) => {
    console.log(`Process ${ctx.request.method} ${ctx.request.url}...`);
    await next();
});

// add url-route:
router.get('/hello/:name', async (ctx, next) => {
    var name = ctx.params.name;
    ctx.response.body = `<h1>Hello, ${name}!</h1>`;
});

router.get('/', async (ctx, next) => {
    ctx.response.body = '<h1>Index</h1>';
});

// add router middleware:
app.use(router.routes());

app.listen(3000);
console.log('app started at port 3000...');
```

```js
// 这样才能解析到 ctx.request.body !
app.use(bodyParser());
/* 写一个简单的登录表单 */
router.get('/', async (ctx, next) => {
    ctx.response.body = `<h1>Index</h1>
        <form action="/signin" method="post">
            <p>Name: <input name="name" value="koa"></p>
            <p>Password: <input name="password" type="password"></p>
            <p><input type="submit" value="Submit"></p>
        </form>`;
});

router.post('/signin', async (ctx, next) => {
    var
        name = ctx.request.body.name || '',
        password = ctx.request.body.password || '';
    console.log(`signin with name: ${name}, password: ${password}`);
    if (name === 'koa' && password === '12345') {
        ctx.response.body = `<h1>Welcome, ${name}!</h1>`;
    } else {
        ctx.response.body = `<h1>Login failed!</h1>
        <p><a href="/">Try again</a></p>`;
    }
});
```

##### Controller Middleware

- 对于不同 URL 的响应, 应该从 `app.js` 中分离出来, 也即 Controller Middleware
- 因此, 对于代码重构
    - 将处理 URL 的代码 (处理函数) 都放在一个 `controllers` 文件夹中
    - 用专门的一个 `controller.js`, 扫描`controllers`目录和创建`router`, 作为一个简单的 middleware 使用
    - 这样, `app.js`的代码得以简化.
- 经过重新整理后的工程 `url2-koa` 目前具备非常好的模块化，所有处理URL的函数按功能组存放在`controllers`目录，今后我们也只需要不断往这个目录下加东西就可以了，`app.js`保持不变。

##### Nunjucks

- 模板引擎
    - 模板引擎就是基于模板配合数据构造出字符串输出的一个组件。
- 输出HTML有几个特别重要的问题需要考虑：
    - 转义
        - 对特殊字符要转义，避免受到XSS攻击。比如，如果变量`name`的值不是`小明`，而是`小明<script>...</script>`，模板引擎输出的HTML到了浏览器，就会自动执行恶意JavaScript代码。
    - 格式化
        - 对不同类型的变量要格式化，比如，货币需要变成`12,345.00`这样的格式，日期需要变成`2016-01-01`这样的格式。
    - 简单逻辑
        - 模板还需要能执行一些简单逻辑，比如，要按条件输出内容
- Nunjucks
    - 我们选择Nunjucks作为模板引擎。Nunjucks是 Mozilla 开发的一个纯JavaScript编写的模板引擎，既可以用在Node环境下，又可以运行在浏览器端。但是，主要还是运行在Node环境下，因为浏览器端有更好的模板解决方案，例如MVVM框架。
    - 就是用 js 重新实现了 Python的模板引擎[jinja2](https://www.liaoxuefeng.com/wiki/1016959663602400/1017806952856928)

如何使用模板引擎?

- 创建引擎对象
    - `function render(view, model) {}`
    - `view`是模板的名称（又称为视图），因为可能存在多个模板，需要选择其中一个。`model`就是数据，在JavaScript中，它就是一个简单的Object。`render`函数返回一个字符串，就是模板的输出。
    - 创建`env`需要的参数可以查看文档获知。
    - 下例中, 我们用`opts.noCache || false`这样的代码给每个参数加上默认值，最后使用`new nunjucks.FileSystemLoader('views')`创建一个文件系统加载器，从`views`目录读取模板。

```js
const nunjucks = require('nunjucks');

function createEnv(path, opts) {
    var
        autoescape = opts.autoescape === undefined ? true : opts.autoescape,
        noCache = opts.noCache || false,
        watch = opts.watch || false,
        throwOnUndefined = opts.throwOnUndefined || false,
        env = new nunjucks.Environment(
            new nunjucks.FileSystemLoader('views', {
                noCache: noCache,
                watch: watch,
            }), {
                autoescape: autoescape,
                throwOnUndefined: throwOnUndefined
            });
    if (opts.filters) {
        for (var f in opts.filters) {
            env.addFilter(f, opts.filters[f]);
        }
    }
    return env;
}

var env = createEnv('views', {
    watch: true,
    filters: {
        hex: function (n) {
            return '0x' + n.toString(16);
        }
    }
});
```

- 使用就非常简单
    - 例如, 写一个简单的 html 文件, 内容为 `<h1>Hello {{ name }}</h1>`
    - 故意传入一个包含特殊符号的对象: `var s = env.render('hello.html', { name: '<script>alert("小明")</script>' });`
    - 可以看到会对于特殊字符进行转移, 这样就避免了输出恶意脚本
- 功能
    - 条件判断、循环
    - 继承
        - Nunjucks模板引擎最强大的功能在于模板的继承。仔细观察各种网站可以发现，网站的结构实际上是类似的，头部、尾部都是固定格式，只有中间页面部分内容不同。如果每个模板都重复头尾，一旦要修改头部或尾部，那就需要改动所有模板。

```html
<!-- 循环输出名字 -->
<body>
    <h3>Fruits List</h3>
    {% for f in fruits %}
    <p>{{ f }}</p>
    {% endfor %}
</body>

<!-- base.html -->
<html><body>
{% block header %} <h3>Unnamed</h3> {% endblock %}
{% block body %} <div>No body</div> {% endblock %}
{% block footer %} <div>copyright</div> {% endblock %}
</body>

<!-- extend.html -->
{% extends 'base.html' %}
{% block header %}<h1>{{ header }}</h1>{% endblock %}
{% block body %}<p>{{ body }}</p>{% endblock %}
```

##### 使用MVC

- MVC：Model-View-Controller，中文名“模型-视图-控制器”。
    - 异步函数是C：Controller，Controller负责业务逻辑，比如检查用户名是否存在，取出用户信息等等；
    - 包含变量`{{ name }}`的模板就是V：View，View负责显示逻辑，通过简单地替换一些变量，View最终输出的就是用户看到的HTML。
    - Model是用来传给View的，这样View在替换变量的时候，就可以从Model中取出相应的数据。

具体而言

- router 逻辑
    - 在 `controller` 文件夹中, 实现 `async (ctx, next) => {}` 这些异步函数, 交给 koa 进行处理
    - 这里直接写了 `ctx.render('index.html', {})`, 其中的 render 是我们定义在 ctx 上的函数, 用 nonjucks 渲染模板
- 编写 view
    - 写一个 base.html 作为骨架, 其他模板直接继承即可
- 集成 Nunjucks
    - 集成Nunjucks实际上也是编写一个middleware，这个middleware的作用是给`ctx`对象绑定一个`render(view, model)`的方法，这样，后面的Controller就可以调用这个方法来渲染模板了。
- 编写 middleware
    - 第一个middleware是记录URL以及页面执行时间
    - 第二个middleware处理静态文件
        - 如果是静态文件, 返回即可!
        - 如果不是, `next()`
    - 第三个middleware解析POST请求
    - 第四个middleware负责给`ctx`加上`render()`来使用Nunjucks
        - 注意, 这里对于每一个请求, 都需要加上 render 方法, 然后调用 `next()` (在下面的路有中决定渲染哪一个模板)
    - 最后一个middleware处理URL路由
- 开发/生产环境
    - 可以定义一个常量 `isProduction` 根据环境变量 `process.env.NODE_ENV` 判断是否为开发环境
    - 开发:
        - Nonjucks: 开发环境下，关闭缓存后，我们修改View，可以直接刷新浏览器看到效果，否则，每次修改都必须重启Node程序，会极大地降低开发效率
        - 开发环境下, 我们用 koa 处理静态文件, 而生产端直接交给 Nginx 处理
- 技巧: 拓展
    - 注意到`ctx.render`内部渲染模板时，Model对象并不是传入的model变量，而是 `ctx.response.body = env.render(view, Object.assign({}, ctx.state || {}, model || {}));`
    - 首先，`model || {}`确保了即使传入`undefined`，model也会变为默认值`{}`
    - `ctx.state || {}` 目的是为了能把一些公共的变量放入`ctx.state`并传给View
        - 例如，某个middleware负责检查用户权限，它可以把当前用户放入`ctx.state`中
        - 这样就没有必要在每个Controller的async函数中都把user变量放入model中
    - 使用 `Object.assign()` 将除了第一个参数意外的对象属性都复制到第一个参数中

建议直接看代码, 注意 koa 添加 run 函数的执行逻辑.

#### mysql

- 开源数据库
    - MySQL，大家都在用，一般错不了；
    - PostgreSQL，学术气息有点重，其实挺不错，但知名度没有MySQL高；
    - sqlite，嵌入式数据库，适合桌面和移动应用。
- 安装
    - `brew install mysql`
    - `brew services start mysql`
    - `mysql -uroot`

##### Sequelize

```js
// 如果直接使用`mysql2`包提供的接口，我们编写的代码就比较底层，例如，查询代码
connection.query('SELECT * FROM users WHERE id = ?', ['123'], function(err, rows) {
    if (err) {
        // error
    } else {
        for (let row in rows) {
            processRow(row);
        }
    }
});

// Sequelize 方式
Pet.findAll()
   .then(function (pets) {
       for (let pet in pets) {
           console.log(`${pet.id}: ${pet.name}`);
       }
   }).catch(function (err) {
       // error
   });

// 采用 async 方式
(async () => {
    // 注意 await 必须在 async 函数中使用
    var pets = await Pet.findAll();
})();
```

生成数据

```sql
-- create
create database test;
use test;

-- create & grant user
create user 'www'@'%' identified by 'www';
grant all privileges on test.* to 'www'@'%';

-- create table
create table pets (
    id varchar(50) not null,
    name varchar(100) not null,
    gender bool not null,
    birth varchar(10) not null,
    createdAt bigint not null,
    updatedAt bigint not null,
    version bigint not null,
    primary key (id)
) engine=innodb;
```

- 使用 sequelize
    - 安装 `sequelize, mysql2`
    - 第一步，创建一个sequelize对象实例
    - 第二步，定义 **模型** Pet，告诉Sequelize如何映射数据库表
        - 用 `sequelize.define()` 定义Model时，传入名称 `pet`，默认的表名就是 `pets`。第二个参数指定列名和数据类型，如果是主键，需要更详细地指定。第三个参数是额外的配置，我们传入`{ timestamps: false }`是为了关闭Sequelize的自动添加timestamp的功能。
    - 操作
        - `create` 插入数据
        - `findAll` 查询
            - 对查询到的实例调用 `save, destory`

```js
const Sequelize = require('sequelize');
const config = require('./config');
// 第一步，创建一个sequelize对象实例
var sequelize = new Sequelize(config.database, config.username, config.password, {
    host: config.host,
    dialect: 'mysql',
    pool: {
        max: 5,
        min: 0,
        idle: 30000
    }
});
// 第二步，定义模型Pet，告诉Sequelize如何映射数据库表
var Pet = sequelize.define('pet', {
    id: {
        type: Sequelize.STRING(50),
        primaryKey: true
    },
    name: Sequelize.STRING(100),
    gender: Sequelize.BOOLEAN,
    birth: Sequelize.STRING(10),
    createdAt: Sequelize.BIGINT,
    updatedAt: Sequelize.BIGINT,
    version: Sequelize.BIGINT
}, {
        timestamps: false // 关闭Sequelize的自动添加timestamp的功能
    });
```

- Model
    - 我们把通过`sequelize.define()`返回的`Pet`称为 **Model**，它表示一个数据模型。
    - 我们把通过`Pet.findAll()`返回的一个或一组对象称为Model **实例**，每个实例都可以直接通过`JSON.stringify`序列化为JSON字符串。但是它们和普通JSON对象相比，多了一些由Sequelize添加的方法，比如`save()`和`destroy()`。调用这些方法我们可以执行更新或者删除操作。
- 所以，使用Sequelize操作数据库的一般步骤就是：
    - 首先，通过某个Model对象的`findAll()`方法获取实例；
        - 注意`findAll()`方法可以接收`where`、`order`这些参数，这和将要生成的SQL语句是对应的。
    - 如果要更新实例，先对实例属性赋新值，再调用`save()`方法
    - 如果要删除实例，直接调用`destroy()`方法。

```js
// await 写法 create
(async () => {
    var dog = await Pet.create({
        id: "d-" + now,
        name: "Odie",
        gender: false,
        birth: "2008-08-08",
        createdAt: now,
        updatedAt: now,
        version: 0,
    });
    console.log("created: " + JSON.stringify(dog));
})();

/* find & save & destroy 查询, 修改, 删除 */
(async () => {
    var pets = await Pet.findAll({
        where: {
            name: "Gaffey",
        },
    });
    console.log(`find ${pets.length} pets:`);
    for (let p of pets) {
        console.log(JSON.stringify(p));
        console.log("update pet...");
        p.gender = true;
        p.updatedAt = Date.now();
        p.version++;
        await p.save();
        if (p.version === 3) {
            await p.destroy();
            console.log(`${p.name} was destroyed.`);
        }
    }
})();
```

##### 建立 Model

我们需要一个统一的模型，强迫所有Model都遵守同一个规范，这样不但实现简单，而且容易统一风格。

1. 统一主键，名称必须是`id`，类型必须是`STRING(50)`；
2. 主键可以自己指定，也可以由框架自动生成（如果为null或undefined）；
3. 所有字段默认为`NOT NULL`，除非显式指定；
4. 统一timestamp机制，每个Model必须有`createdAt`、`updatedAt`和`version`，分别记录创建时间、修改时间和版本号。其中，`createdAt`和`updatedAt`以`BIGINT`存储时间戳，最大的好处是无需处理时区，排序方便。`version`每次修改时自增。

因此, 我们定义一个 `defineModel` 函数, 制实现上述规则。

- Sequelize在创建、修改Entity时会调用我们指定的函数，这些函数通过`hooks`在定义Model时设定。我们在`beforeValidate`这个事件中根据是否是`isNewRecord`设置主键（如果主键为`null`或`undefined`）、设置时间戳和版本号。

```js
/* 调用形式 */
db.defineModel('users', {
    email: {
        type: db.STRING(100),
        unique: true
    },
    passwd: db.STRING(100),
    name: db.STRING(100),
    gender: db.BOOLEAN
});

/* 我们定义一个 `defineModel` 函数, 制实现上述规则。 */
function defineModel(name, attributes) {
    var attrs = {};
    for (let key in attributes) {
        let value = attributes[key];
        if (typeof value === 'object' && value['type']) {
            value.allowNull = value.allowNull || false;
            attrs[key] = value;
        } else {
            attrs[key] = {
                type: value,
                allowNull: false
            };
        }
    }
    attrs.id = {
        type: ID_TYPE,
        primaryKey: true
    };
    attrs.createdAt = {
        type: Sequelize.BIGINT,
        allowNull: false
    };
    attrs.updatedAt = {
        type: Sequelize.BIGINT,
        allowNull: false
    };
    attrs.version = {
        type: Sequelize.BIGINT,
        allowNull: false
    };
    return sequelize.define(name, attrs, {
        tableName: name,
        timestamps: false,
        hooks: {
            beforeValidate: function (obj) {
                let now = Date.now();
                if (obj.isNewRecord) {
                    if (!obj.id) {
                        obj.id = generateId();
                    }
                    obj.createdAt = now;
                    obj.updatedAt = now;
                    obj.version = 0;
                } else {
                    obj.updatedAt = Date.now();
                    obj.version++;
                }
            }
        }
    });
}
```

- 我们其实不需要创建表的SQL，因为Sequelize提供了一个`sync()`方法，可以自动创建数据库。
    - 这个功能在开发和生产环境中没有什么用，但是在测试环境中非常有用。测试时，我们可以用`sync()`方法自动创建出表结构，而不是自己维护SQL脚本。这样，可以随时修改Model的定义，并立刻运行测试。
    - 开发环境下，首次使用`sync()`也可以自动创建出表结构，避免了手动运行SQL的问题。

```js
/* 暴露 sync 函数 */
module.exports = {
    sync: () => {
        // only allow create ddl in non-production environment:
        if (process.env.NODE_ENV !== "production") {
            sequelize.sync({ force: true });
        } else {
            throw new Error(
                "Cannot sync() when NODE_ENV is set to 'production'."
            );
        }
    },
};

/* init-db.js */
const model = require('./model.js');
model.sync();
console.log('init db ok.');
```

#### mocha

- mocha是JavaScript的一种单元测试框架，既可以在浏览器环境下运行，也可以在Node.js环境下运行。
- 特点
    - 既可以测试简单的JavaScript函数，又可以测试异步代码，因为异步是JavaScript的特性之一；
    - 可以自动运行所有测试，也可以只运行特定的测试；
    - 可以支持before、after、beforeEach和afterEach来编写初始化代码。

如何执行测试?

- 方法一 `node_modules\mocha\bin\mocha`
- 方法二，我们在`package.json`中添加npm命令
    - 在 scripts 中添加 `"test": "mocha"`
    - 然后 `npm test` 即可
- 方法三，我们在VS Code中创建配置文件`.vscode/launch.json`
    - `"program": "${workspaceRoot}/node_modules/mocha/bin/mocha"`
    - `"type": "node",`
    - 其实就是运行了 `node node_modules/mocha/bin/mocha` !

##### 编写测试

```js
const assert = require('assert');
const sum = require('../hello');

describe('#hello.js', () => {
    describe('#sum()', () => {
        before(function () {
            console.log('before:');
        });

        after(function () {
            console.log('after.');
        });

        beforeEach(function () {
            console.log('  beforeEach:');
        });

        afterEach(function () {
            console.log('  afterEach.');
        });

        it('sum() should return 0', () => {
            assert.strictEqual(sum(), 0);
        });

        it('sum(1) should return 1', () => {
            assert.strictEqual(sum(1), 1);
        });
    });
});
```

##### 异步测试

- 如果要测试同步函数，我们传入无参数函数即可
    - `it(' description', function () {}`
    - 然后在其中 assert 判断即可
- 如果要测试异步函数，我们要传入的函数需要带一个参数，通常命名为`done`
    - `it(' description', function (done) {}`
    - 然后在其中运行代测试的函数 f
    - 手动调用`done()`表示测试成功，`done(err)`表示测试出错
- 对于 async 函数, 更方便的是直接将其转化为同步函数测试
    - 例如, 传入 `async () => { assert.strictEqual(await f(), groundTruth) }`

```js
// 如果要测试同步函数，我们传入无参数函数即可
it('test sync function', function () {
    // sycnFunc()
    assert(true);
});

// 如果要测试异步函数，我们要传入的函数需要带一个参数，通常命名为`done`
it('test async function', function (done) {
    // 要测试的异步函数, 例如这里的 fs.readFile
    fs.readFile('filepath', function (err, data) {
        // 测试异步函数需要在函数内部手动调用`done()`表示测试成功，`done(err)`表示测试出错。
        if (err) {
            done(err);
        } else {
            done();
        }
    });
});

// 对于 await 函数
// 0. 可以用 try...catch 测试
it('#async with done', (done) => {
    (async function () {
        try {
            let r = await hello();
            assert.strictEqual(r, 15);
            done();
        } catch (err) {
            done(err);
        }
    })();
});
// 1. 更方便的, 就是直接把async函数当成同步函数来测试
it('#async function', async () => {
    let r = await hello();
    assert.strictEqual(r, 15);
});
```

##### Http 测试

- 从 `app.js` 中分离直接运行 (listen) 的代码, 令其只负责创建`app`实例，并不监听端口
    - 从而可以在测试中导入 app 然后 `let server = app.listen(9900);`
- 利用 `supertest` 简化 HTTP assertions
    - `request = require('supertest')`
    - 使用 `let res = await request(server).get('/');` 构造一个GET请求，发送给koa的应用，然后获得响应
    - 可以手动检查响应对象，例如，`res.body`，还可以利用`supertest`提供的`expect()`更方便地断言响应的HTTP代码、返回内容和HTTP头。断言HTTP头时可用使用正则表达式
        - 例如 `.expect('Content-Type', /text\/html/)` 可用成功匹配到`Content-Type`为`text/html`、`text/html; charset=utf-8`等值。

参见 <https://www.npmjs.com/package/supertest> 中的 macha 部分

```js
// app-test.js

const
    request = require('supertest'),
    app = require('../app');

describe('#test koa app', () => {

    let server = app.listen(9900);

    describe('#test server', () => {

        it('#test GET /', async () => {
            let res = await request(server)
                .get('/')
                .expect('Content-Type', /text\/html/)
                .expect(200, '<h1>Hello, world!</h1>');
        });

        it('#test GET /path?name=Bob', async () => {
            let res = await request(server)
                .get('/path?name=Bob')
                .expect('Content-Type', /text\/html/)
                .expect(200, '<h1>Hello, Bob!</h1>');
        });
    });
});
```

#### WebSocket

- WebSocket是 HTML5 新增的协议，它的目的是在浏览器和服务器之间建立一个不受限的双向通信的通道，比如说，服务器可以在任意时刻发送消息给浏览器。
    - HTTP协议是一个请求－响应协议，请求必须先由浏览器发给服务器，服务器才能响应这个请求，再把数据发送给浏览器。换句话说，浏览器不主动请求，服务器是没法主动发数据给浏览器的。
- 也能实现, 但是效率低. 比如用轮询或者Comet。
    - 轮询是指浏览器通过JavaScript启动一个定时器，然后以固定的间隔给服务器发请求，询问服务器有没有新消息。这个机制的缺点一是实时性不够，二是频繁的请求会给服务器带来极大的压力。
    - Comet本质上也是轮询，但是在没有消息的情况下，服务器先拖一段时间，等到有消息了再回复。这个机制暂时地解决了实时性问题，但是它带来了新的问题：以多线程模式运行的服务器会让大部分线程大部分时间都处于挂起状态，极大地浪费服务器资源。另外，一个HTTP连接在长时间没有数据传输的情况下，链路上的任何一个网关都可能关闭这个连接，而网关是我们不可控的，这就要求Comet连接必须定期发一些ping数据表示连接“正常工作”。
- 为什么WebSocket连接可以实现全双工通信而HTTP连接不行呢？实际上HTTP协议是建立在TCP协议之上的，TCP协议本身就实现了全双工通信，但是HTTP协议的请求－应答机制限制了全双工通信。WebSocket连接建立以后，其实只是简单规定了一下：接下来，咱们通信就不使用HTTP协议了，直接互相发数据吧。
    - 安全的WebSocket连接机制和HTTPS类似。首先，浏览器用`wss://xxx`创建WebSocket连接时，会先通过HTTPS创建安全的连接，然后，该HTTPS连接升级为WebSocket连接，底层通信走的仍然是安全的SSL/TLS协议。
- 服务器
    - 由于WebSocket是一个协议，服务器具体怎么实现，取决于所用编程语言和框架本身。Node.js本身支持的协议包括TCP协议和HTTP协议，要支持WebSocket协议，需要对Node.js提供的HTTPServer做额外的开发。已经有若干基于Node.js的稳定可靠的WebSocket实现，我们直接用npm安装使用即可。

##### ws 协议

```js
GET ws://localhost:3000/ws/chat HTTP/1.1
Host: localhost
Upgrade: websocket
Connection: Upgrade
Origin: http://localhost:3000
Sec-WebSocket-Key: client-random-string
Sec-WebSocket-Version: 13
```

该请求和普通的HTTP请求有几点不同：

1. GET请求的地址不是类似`/path/`，而是以`ws://`开头的地址；
2. 请求头`Upgrade: websocket`和`Connection: Upgrade`表示这个连接将要被转换为WebSocket连接；
3. `Sec-WebSocket-Key`是用于标识这个连接，并非用于加密数据；
4. `Sec-WebSocket-Version`指定了WebSocket的协议版本。

服务器的响应:

```js
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: server-random-string
```

该响应代码`101`表示本次连接的HTTP协议即将被更改，更改后的协议就是`Upgrade: websocket`指定的WebSocket协议。

##### 案例: 编写聊天室

##### 如何共用端口

koa通过3000端口响应HTTP，我们要新加的WebSocketServer还能否使用3000端口？可以!

- 实际上，3000端口并非由koa监听，而是koa调用Node标准的http模块创建的http.Server监听的。koa只是把响应函数注册到该http.Server中了。类似的，WebSocketServer也可以把自己的响应函数注册到http.Server中，这样，同一个端口，根据协议，可以分别由koa和ws处理
- 把WebSocketServer绑定到同一个端口的关键代码是先获取koa创建的`http.Server`的引用，再根据`http.Server`创建WebSocketServer

```js
// koa app的listen()方法返回http.Server:
let server = app.listen(3000);

// 创建WebSocketServer:
let wss = new WebSocketServer({
    server: server
});
```

###### 如何识别用户身份: cookie

!!! note
    总结: 总体而言, cookie 是一个服务端和客户端相互配合的过程. (以这个案例为准, `/singin` 页面进行登陆, `/` 页面为聊天室)

    1. 浏览器请求 `/`, 初始的时候还没有 cookie, koa 进行判断, 将页面重定向到 `/signin`;
    2. 用户填写身份信息, 发送 post 请求;
    3. 服务器生成 cookie (下面的 "POST /signin" 对应的函数), 重定向回 `/` 聊天页面 (这里不考虑用户信息出错的情况)
    4. 浏览器再次请求 `/`, 此时发送的是带有 cookie 的, koa 验证 cookie (在 middleware 中注册了 parseUser 函数), 成功后渲染页面发送给浏览器 ('GET /' 对应的函数)
    5. 在 `/` 页面中包含了建立 ws 连接的代码, 浏览器发起 ws 连接请求 `new WebSocket('ws://localhost:3000/ws/chat')` (在 `room.html` 模板中)
    6. 服务器验证 cookie (在响应 'connection' 的时候调用 parseUser), 建立连接
    7. 然后, 浏览器和服务器之间的发送消息就通过这条建立好的 ws 连接来通信了!

- 在koa应用中，可以很容易地认证用户，例如，通过session或者cookie，但是，在响应WebSocket请求时，如何识别用户身份？
- 一个简单可行的方案是把用户登录后的身份写入Cookie，在koa中，可以使用middleware解析Cookie，把用户绑定到`ctx.state.user`上。
- WS请求也是标准的HTTP请求，所以，服务器也会把Cookie发送过来，这样，我们在用WebSocketServer处理WS请求时，就可以根据Cookie识别用户身份。
- 处理逻辑
    - 在 koa 中, (在 middleware 注册 parseUser 函数), 将 cookie 保存在 `ctx.state` 中. 由于处理的都是 http 请求, 可以容易得到
    - 而对于 ws, 我们需要在初始建立 connection 的时候创建 cookie, 然后绑定到 WebSocket对象 上.

```js
/* server 新用户登陆, 构造 user 对象, 生成 base64 编码的 cookie —— 然后发送给浏览器
controller/signin.js */
    "POST /signin": async (ctx, next) => {
        index++;
        let name = ctx.request.body.name || "路人甲";
        let user = {
            id: index,
            name: name,
            image: index % 10,
        };
        let value = Buffer.from(JSON.stringify(user)).toString("base64");
        console.log(`Set cookie value: ${value}`);
        ctx.cookies.set("name", value);
        ctx.response.redirect("/"); // 重定向回首页
    },
/* controller/index.js */
    'GET /': async (ctx, next) => {
        let user = ctx.state.user;
        if (user) {
            ctx.render('room.html', {
                user: user
            });
        } else {
            ctx.response.redirect('/signin');
        }
    }

/* 识别用户身份的逻辑
传入的 obj 可以是 1. cookie 字符串; 2. request 对象 */
function parseUser(obj) {
    if (!obj) {
        return;
    }
    console.log('try parse: ' + obj);
    let s = '';
    if (typeof obj === 'string') {
        s = obj;
    } else if (obj.headers) {
        let cookies = new Cookies(obj, null);
        s = cookies.get('name');
    }
    if (s) {
        try {
            let user = JSON.parse(Buffer.from(s, 'base64').toString());
            console.log(`User: ${user.name}, ID: ${user.id}`);
            return user;
        } catch (e) {
            // ignore
        }
    }
}

// 在koa的middleware中，我们很容易识别用户
app.use(async (ctx, next) => {
    ctx.state.user = parseUser(ctx.cookies.get('name') || '');
    await next();
});

// 在WebSocketServer中，就需要响应`connection`事件，然后识别用户
wss.on('connection', function (ws) {
    // ws.upgradeReq是一个 (http) request对象:
    let user = parseUser(ws.upgradeReq);
    if (!user) {
        // Cookie不存在或无效，直接关闭WebSocket:
        ws.close(4001, 'Invalid user');
    }
    // 识别成功，把user绑定到该 WebSocket 对象:
    ws.user = user;
    // 绑定WebSocketServer对象:
    ws.wss = wss;
});
```

浏览器

```js
/* room.html */
/* 初始化页面的时候, 和服务器建立 ws 连接, 设置 onmessage 监听逻辑 */
    var ws = new WebSocket('ws://localhost:3000/ws/chat');

    ws.onmessage = function(event) {
        var data = event.data;
        console.log(data);
        var msg = JSON.parse(data);
        if (msg.type === 'list') {
            vmUserList.users = msg.data;
        } else if (msg.type === 'join') {
            addToUserList(vmUserList.users, msg.user);
            addMessage(vmMessageList.messages, msg);
        } else if (msg.type === 'left') {
            removeFromUserList(vmUserList.users, msg.user);
            addMessage(vmMessageList.messages, msg);
        } else if (msg.type === 'chat') {
            addMessage(vmMessageList.messages, msg);
        }
    };

/* 拦截消息发送这个表单 (id为 form-chat), 使用 ws 进行发送消息 */
    $('#form-chat').submit(function (e) {
        e.preventDefault();
        var input = $(this).find('input[type=text]');
        var text = input.val().trim();
        console.log('[chat] ' + text);
        if (text) {
            input.val('');
            ws.send(text);
        }
    });
```

###### 聊天室逻辑

- 我们要对每个创建成功的WebSocket绑定`message`、`close`、`error`等事件处理函数。对于聊天应用来说，每收到一条消息，就需要把该消息广播到所有WebSocket连接上。
- 处理逻辑:
    - 某个WebSocket收到消息, 广播到所有连接

###### 页面端

- 聊天室页面可以划分为左侧会话列表和右侧用户列表两部分
- 在聊天室应用中, DOM需要动态更新，因此，状态管理是页面逻辑的核心。
    - 为了简化状态管理，我们用 `Vue` 控制左右两个列表

紧接着，创建WebSocket连接，响应服务器消息，并且更新会话列表和用户列表

```js
// 为了建立 ws 连接, 发送的还是 http 请求, 
var ws = new WebSocket('ws://localhost:3000/ws/chat');

ws.onmessage = function(event) {
    var data = event.data;
    console.log(data);
    var msg = JSON.parse(data);
    if (msg.type === 'list') {
        vmUserList.users = msg.data;
    } else if (msg.type === 'join') {
        addToUserList(vmUserList.users, msg.user);
        addMessage(vmMessageList.messages, msg);
    } else if (msg.type === 'left') {
        removeFromUserList(vmUserList.users, msg.user);
        addMessage(vmMessageList.messages, msg);
    } else if (msg.type === 'chat') {
        addMessage(vmMessageList.messages, msg);
    }
};
```

###### 配置反向代理

- 如果网站配置了反向代理，例如Nginx，则HTTP和WebSocket都必须通过反向代理连接Node服务器。
    - HTTP的反向代理非常简单，但是要正常连接WebSocket，代理服务器必须支持WebSocket协议。
    - Nginx 为例, 官方博客：[Using NGINX as a WebSocket Proxy](https://www.nginx.com/blog/websocket-nginx/)

#### REST

- 自从Roy Fielding博士在2000年他的博士论文中提出[REST](http://zh.wikipedia.org/wiki/REST)（Representational State Transfer）风格的软件架构模式后，REST就基本上迅速取代了复杂而笨重的SOAP，成为Web API的标准了。
- 编写API有什么好处呢？
    - 由于API就是把Web App的功能全部封装了，所以，通过API操作数据，可以极大地把前端和后端的代码隔离，使得后端代码易于测试，前端代码编写更简单。
    - 此外，如果我们把前端页面看作是一种用于展示的客户端，那么API就是为客户端提供数据、操作数据的接口。
        - **这种设计可以获得极高的扩展性**。例如，当用户需要在手机上购买商品时，只需要开发针对iOS和Android的两个客户端，通过客户端访问API，就可以完成通过浏览器页面提供的功能，而后端代码基本无需改动。

##### 编写 REST API

- 编写REST API，实际上就是编写处理HTTP请求的async函数，不过，REST请求和普通的HTTP请求有几个特殊的地方：
    - REST请求仍然是标准的HTTP请求，但是，除了GET请求外，POST、PUT等请求的body是JSON数据格式，请求的`Content-Type` 为 `application/json`
    - REST响应返回的结果是JSON数据格式，因此，响应的 `Content-Type`也是`application/json`。
- REST规范定义了资源的通用访问格式，虽然它不是一个强制要求，但遵守该规范可以让人易于理解。
    - 获取资源, 使用 GET
        - 资源还可以按层次组织
        - 当我们只需要获取部分数据时，可通过参数限制返回的结果集
    - 新建一个Product使用POST请求，JSON数据包含在body中
    - 更新一个Product使用PUT请求
    - 删除一个Product使用DELETE请求

```js
GET /api/products // 获取所有商品
GET /api/products/123/reviews
GET /api/products/123/reviews?page=2&size=10&sort=time // 返回第2页评论，每页10项，按时间排序

POST /api/products // 新建, JSON 数据放在 body中

PUT /api/products/123 // 更新

DELETE /api/products/123
```

在koa中处理REST请求是非常简单的。`bodyParser()`这个middleware可以解析请求的JSON数据并绑定到`ctx.request.body`上，输出JSON时我们先指定`ctx.response.type = 'application/json'`，然后把JavaScript对象赋值给`ctx.response.body`就完成了REST请求的处理。

##### 开发 REST API

- 使用REST虽然非常简单，但是，设计一套合理的REST框架却需要仔细考虑很多问题。
- 问题一：如何组织URL
    - 在实际工程中，一个Web应用既有REST，还有MVC，可能还需要集成其他第三方系统。如何组织URL？
    - 一个简单的方法是通过固定的前缀区分。例如，`/static/`开头的URL是静态资源文件，类似的，`/api/`开头的URL就是REST API，其他URL是普通的MVC请求。
- 问题二：如何统一输出REST
    - 注意到, 服务端每次返回的都是一个 json 内容, 需要固定设置 `ctx.response.type = 'application/json';`
    - 回忆我们集成Nunjucks模板引擎的方法：通过一个middleware给`ctx`添加一个`render()`方法，Controller就可以直接使用`ctx.render('view', model)`来渲染模板，不必编写重复的代码。
    - 类似的，我们也可以通过一个middleware给`ctx`添加一个`rest()`方法
- 问题三：如何处理错误
    - 第一，当REST API请求出错时，我们如何返回错误信息？
        - 类似403，404，500等错误，这些错误实际上是HTTP请求可能发生的错误. 服务端不用管
    - 第二，当客户端收到REST响应后，如何判断是成功还是错误？
        - 返回错误信息, 一个JSON字符串
- 问题四：如何定义错误码
    - 相较于用数字, 不如直接用字符串, 即设定 `"code": "错误代码",` 和 `"message": "错误描述信息"`
    - 例如, 一个错误代码可以是 `auth:bad_password`
- 问题五：如何返回错误
    - 一个直观的想法是 (在控制流程的各个部分) 调用`ctx.rest()`
    - 更好的方式是异步函数直接用`throw`语句抛出错误，让middleware去处理错误
    - 下面实现一个 restify 中间层: 仅仅处理前缀为 `/api/` 的请求, 对于其他请求直接 next
        - 绑定 `ctx.rest()` 方法 (问题二：如何统一输出REST)
        - 用 `try...catch` 统一处理错误 (在 controller 部分直接抛出错误即可).
        - 受益于async/await语法，我们在middleware中可以直接用`try...catch`捕获异常。如果是callback模式，就无法用`try...catch`捕获，代码结构将混乱得多。

```js
module.exports = {
    APIError: function (code, message) {
        this.code = code || "internal:unknown_error";
        this.message = message || "";
    },
    restify: (pathPrefix) => {
        // REST API前缀，默认为/api/:
        pathPrefix = pathPrefix || "/api/";
        return async (ctx, next) => {
            // 是否是REST API前缀?
            if (ctx.request.path.startsWith(pathPrefix)) {
                // 绑定rest()方法:
                console.log(
                    `Process API ${ctx.request.method} ${ctx.request.url}...`
                );
                ctx.rest = (data) => {
                    ctx.response.type = "application/json";
                    ctx.response.body = data;
                };
                try {
                    await next();
                } catch (e) {
                    console.log("Process API error...");
                    ctx.response.status = 400;
                    ctx.response.type = "application/json";
                    ctx.response.body = {
                        code: e.code || "internal:unknown_error",
                        message: e.message || "",
                    };
                }
            } else {
                // 这里仅处理 /api 开头的请求, 对于其他的请求, 直接 next 跳过
                await next();
            }
        };
    },
};
```

#### MVVM

- [MVVM](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)是Model-View-ViewModel的缩写。
- 用JavaScript在浏览器中操作HTML，经历了若干发展阶段：
    - 第一阶段，直接用JavaScript操作DOM节点，使用浏览器提供的原生API
    - 第二阶段，由于原生API不好用，还要考虑浏览器兼容性，jQuery横空出世
    - 第三阶段，MVC模式，需要服务器端配合，JavaScript可以在前端修改服务器渲染后的数据
- MVVM 的核心思路: 关注Model的变化，让MVVM框架去自动更新DOM的状态，从而把开发者从操作DOM的繁琐步骤中解脱出来！
- MVVM
    - MVVM最早由微软提出来，它借鉴了桌面应用程序的MVC思想，在前端页面中，把Model用纯JavaScript对象表示，View负责显示，两者做到了最大限度的分离。
    - 把Model和View关联起来的就是ViewModel。ViewModel负责把Model的数据同步到View显示出来，还负责把View的修改同步回Model。
    - ViewModel如何编写？需要用JavaScript编写一个通用的ViewModel，这样，就可以复用整个MVVM模型了。
- 如果是用jQuery实现修改DOM节点, 需要先定位出 DOM 节点, 然后修改其内容; 然而, 在 MVVM 中, 我们不关心DOM结构, 只关心数据是怎么存储的 —— 例如作为 js 对象, 因此直接在代码中修改对象值即可, DOM 同步修改!
    - 例如, 对于 `var person = {name: 'Bart'}`, 我们把变量`person`看作Model，把HTML某些DOM节点看作View，并假定它们之间被关联起来了。
    - 通过改变JavaScript对象的状态，会导致DOM结构作出对应的变化
- 著名的 MVVM 框架
    - [Angular](https://angularjs.org/)：Google出品，名气大，但是很难用；
    - [Backbone.js](http://backbonejs.org/)：入门非常困难，因为自身API太多；
    - [Ember](http://emberjs.com/)：一个大而全的框架，想写个Hello world都很困难。
    - 最佳选择是[尤雨溪](http://weibo.com/p/1005051761511274)大神开发的MVVM框架：[Vue.js](http://vuejs.org/)

```js
/* 第一阶段 */
var dom = document.getElementById('name');
dom.innerHTML = 'Homer';
dom.style.color = 'red';

/* 第二阶段 */
$('#name').text('Homer').css('color', 'red');
```

##### Vue 单向绑定

- 在Vue中，可以直接写`{{ name }}`绑定某个属性。如果属性关联的是对象，还可以用多个`.`引用，例如，`{{ address.zipcode }}`。
- 另一种是把指令写在HTML节点的属性上，它会被Vue解析，该节点的文本内容会被绑定为Model的指定属性，注意不能再写双花括号`{{ }}`。
    - `<p>Hello, <span v-text="name"></span>!</p>`

要特别注意的是，在 `<head>` 内部编写的JavaScript代码，需要用jQuery把MVVM的初始化代码推迟到页面加载完毕后执行，否则，直接在 `<head>` 内执行MVVM代码时，DOM节点尚未被浏览器加载，初始化将失败。

来看创建一个 VM 的核心代码:

- `el` 指定了要把Model绑定到哪个DOM根节点上，语法和jQuery类似。这里的`'#vm'`对应ID为`vm`的一个`<div>`节点
    - 在该节点以及该节点内部，就是Vue可以操作的View。Vue可以自动把Model的状态映射到View上，但是不能操作View范围之外的其他DOM节点。

```js
<html>
<head>
<!-- 引用jQuery -->
<script src="/static/js/jquery.min.js"></script>
<!-- 引用Vue -->
<script src="/static/js/vue.js"></script>

<script>
// 初始化代码:
$(function () {
    var vm = new Vue({
        el: '#vm',
        data: {
            name: 'Robot',
            age: 15
        }
    });
    window.vm = vm;
});
</script>

</head>

<body>
    <div id="vm">
        <p>Hello, {{ name }}!</p>
        <p>You are {{ age }} years old!</p>
    </div>
</body>
<html>
```

下面来看一个解析用户输入, 执行命令的代码:

- 用 jQuery 得到输入内容
- 通过 `new Function(...)` 解析代码字符串

将该函数绑定到页面上的一个 button 即可.

```js
function executeJs() {
    try {
        var code = $('#code').val();
        var fn = new Function('var vm = window.vm;\n' + code);
        fn();
    } catch (e) {}
    return false;
}
```

##### Vue 双向绑定

- 双向绑定, 即用户更新了View，Model的数据也自动被更新
- 什么情况下用户可以更新View呢？填写表单就是一个最直接的例子。当用户填写表单时，View的状态就被更新了，如果此时MVVM框架可以自动更新Model的状态，那就相当于我们把Model和View做了双向绑定
- 双向绑定最大的好处是我们不再需要用jQuery去查询表单的状态，而是直接获得了用JavaScript对象表示的Model。

###### 处理事件

- 当用户提交表单时，传统的做法是响应`onsubmit`事件，用jQuery获取表单内容，检查输入是否有效，最后提交表单，或者用AJAX提交表单。
- 现在，获取表单内容已经不需要了，因为双向绑定直接让我们获得了表单内容，并且获得了合适的数据类型。
- 响应`onsubmit`事件也可以放到VM中。我们在`<form>`元素上使用指令
    - `<form id="vm" v-on:submit.prevent="register">`
    - 其中，`v-on:submit="register"`指令就会自动监听表单的`submit`事件，并调用`register`方法处理该事件。使用`.prevent`表示阻止事件冒泡，这样，浏览器不再处理`<form>`的`submit`事件。
        - 补充: 1、prevent是preventDefault,阻止标签默认行为，有些标签有默认行为，例如a标签的跳转链接属性href等。 2、submit点击默认行为是提交表单，这里并不需要它提交，只需要执行register方法，故阻止为妙。 3、stop是stopPropagation，阻止事件冒泡，点击哪个元素，就只响应这个元素，父级就不会响应了
    - 因为我们指定了事件处理函数是`register`，所以需要在创建VM时添加一个`register`函数
        - 在`register()`函数内部，我们可以用AJAX把JSON格式的Model发送给服务器，就完成了用户注册的功能。

```js
// 在 VM 中定义的 register 函数
var vm = new Vue({
    el: '#vm',
    data: {
        ...
    },
    methods: {
        register: function () {
            // 显示JSON格式的Model:
            alert(JSON.stringify(this.$data));
            // AJAX POST...
        }
    }
});
```

##### 同步DOM结构: v-for

- 除了简单的单向绑定和双向绑定，MVVM还有一个重要的用途，就是让Model和DOM的结构保持同步。
- `v-for`指令把数组和一组`<li>`元素绑定了。在`<li>`元素内部，用循环变量`t`引用某个属性，例如，`{{ t.name }}`。这样，我们只关心如何更新Model，不关心如何增删DOM节点，大大简化了整个页面的逻辑。
- 需要注意的是，Vue之所以能够监听Model状态的变化，是因为JavaScript语言本身提供了[Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)或者[Object.observe()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/observe)机制来监听对象状态的变化。但是，对于数组元素的赋值，却没有办法直接监听
    - `vm.todos[0] = {}` 这样的赋值无法被监听/同步修改, Vue无法更新View
    - 而应该这样修改 `vm.todos[0].name = 'New name';`
    - 或者，通过`splice()`方法，删除某个元素后，再添加一个元素，达到“赋值”的效果
        - `vm.todos.splice(index, 1, {});`
        - Vue可以监听数组的 `splice`、`push`、`unshift` 等方法调用

##### 集成 API

- 上一节中的 TODO 仅仅是在浏览器, 我们需要跟服务端同步.
- 如果要把这个简单的TODO应用变成一个用户能使用的Web应用，我们需要解决几个问题：
  1. 用户的TODO数据应该从后台读取；
  2. 对TODO的增删改必须同步到服务器后端；
  3. 用户在View上必须能够修改TODO。
- 第1个和第2个问题都是和API相关的。只要我们实现了合适的API接口，就可以在MVVM内部更新Model的同时，通过API把数据更新反映到服务器端，这样，用户数据就保存到了服务器端，下次打开页面时就可以读取TODO列表。
    - 实现 API
        - GET /api/todos：返回所有TODO列表；
        - POST /api/todos：创建一个新的TODO，并返回创建后的对象；
        - PUT /api/todos/:id：更新一个TODO，并返回更新后的对象；
        - DELETE /api/todos/:id：删除一个TODO。
    - 准备好API后，在Vue中，我们如何把Model的更新 **同步到服务器端**？
        - 一是直接用jQuery的AJAX调用REST API，不过这种方式比较麻烦。
        - 第二个方法是使用[vue-resource](https://github.com/vuejs/vue-resource)这个针对Vue的扩展，它可以给VM对象加上一个`$resource`属性，通过`$resource`来方便地操作API。
- 如何实现修改?
    - 用`contenteditable="true"` 让DOM节点变成可编辑的，用`v-on:blur="update(t, 'name', $event)"`在编辑结束时调用`update()`方法并传入参数，特殊变量`$event`表示DOM事件本身。

```js
<div id="vm">
    <h3>{{ title }}</h3>
    <ol>
        <li v-for="t in todos">
            <dl>
                <dt contenteditable="true" v-on:blur="update(t, 'name', $event)">{{ t.name }}</dt>
                <dd contenteditable="true" v-on:blur="update(t, 'description', $event)">{{ t.description }}</dd>
                <dd><a href="#0" v-on:click="remove(t)">Delete</a></dd>
            </dl>
        </li>
    </ol>
</div>
```

###### vue-resource

使用: `<script src="https://cdn.jsdelivr.net/vue.resource/1.0.3/vue-resource.min.js"></script>`

```js
var vm = new Vue({
    el: '#vm',
    data: {
        title: 'TODO List',
        todos: []
    },
    // 创建后执行 init 函数
    created: function () {
        this.init();
    },
    methods: {
        init: function () {
            var that = this;
            that.$resource('/api/todos').get().then(function (resp) {
                // 调用API成功时调用json()异步返回结果:
                resp.json().then(function (result) {
                    // 更新VM的todos:
                    that.todos = result.todos;
                });
            }, function (resp) {
                // 调用API失败:
                alert('error');
            });

        create: function (todo) {
            var that = this;
            that.$resource('/api/todos').save(todo).then(function (resp) {
                resp.json().then(function (result) {
                    that.todos.push(result);
                });
            }, showError);
        },
        update: function (todo, prop, e) {
            ...
        },
        remove: function (todo) {
            ...
        }
        }
    }
});
```

##### 在线电子表格

- 首先，我们定义Model的结构，它的主要数据就是一个二维数组，每个单元格用一个JavaScript对象表示
    - 定义第一行 header `{ row: 0, col: 0, text: '' },`
    - 从第二行开始为数据 `{ row: 1, col: 1, text: '' },`
    - 记录当前活动单元格 (`selectedRowIndex, selectedColIndex`)
- 紧接着，我们就可以把Model的结构映射到一个`<table>`上
- 用Vue把Model和View关联起来，这个电子表格的原型已经可以运行了！

```js
data: {
    title: 'New Sheet',
    header: [ // 对应首行 A, B, C...
        { row: 0, col: 0, text: '' },
        { row: 0, col: 1, text: 'A' },
        { row: 0, col: 2, text: 'B' },
        { row: 0, col: 3, text: 'C' },
        ...
        { row: 0, col: 10, text: 'J' }
    ],
    rows: [
        [
         { row: 1, col: 0, text: '1' },
         { row: 1, col: 1, text: '' },
         { row: 1, col: 2, text: '' },
            ...
         { row: 1, col: 10, text: '' },
        ],
        [
         { row: 2, col: 0, text: '2' },
         { row: 2, col: 1, text: '' },
         { row: 2, col: 2, text: '' },
            ...
         { row: 2, col: 10, text: '' },
        ],
        ...
        [
         { row: 10, col: 0, text: '10' },
         { row: 10, col: 1, text: '' },
         { row: 10, col: 2, text: '' },
            ...
         { row: 10, col: 10, text: '' },
        ]
    ],
    selectedRowIndex: 0, // 当前活动单元格的row
    selectedColIndex: 0 // 当前活动单元格的col
}
```

```html
<table id="sheet">
    <thead>
        <tr>
            <th v-for="cell in header" v-text="cell.text"></th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="tr in rows">
            <td v-for="cell in tr" v-text="cell.text"></td>
        </tr>
    </tbody>
</table>
```

- 下一步，我们想在单元格内输入一些文本. 需要判断: 首行和首列不能编辑
    - 首行对应的是`<th>`，默认是不可编辑的，首列对应的是第一列的`<td>`，所以，需要判断某个`<td>`是否可编辑，我们用`v-bind`指令给某个DOM元素绑定对应的HTML属性
    - 在Model中给每个单元格对象加上`contentEditable`属性，就可以决定哪些单元格可编辑。
    - `<td v-for="cell in tr" v-bind:contenteditable="cell.contentEditable" v-text="cell.text"></td>`
- 最后，给`<td>`绑定click事件，记录当前活动单元格的row和col，再绑定blur事件，在单元格内容编辑结束后更新Model
    - <td v-for="cell in tr" v-on:click="focus(cell)" v-on:blur="change" ...></td>

```js
var vm = new Vue({
    ...
    methods: {
        focus: function (cell) {
            this.selectedRowIndex = cell.row;
            this.selectedColIndex = cell.col;
        },
        change: function (e) {
            // change事件传入的e是DOM事件
            var
                rowIndex = this.selectedRowIndex,
                colIndex = this.selectedColIndex,
                text;
            if (rowIndex > 0 && colIndex > 0) {
                text = e.target.innerText; // 获取td的innerText
                this.rows[rowIndex - 1][colIndex].text = text;
            }
        }
    }
});
```

- 总结 MVVM 适用范围
    - 从几个例子我们可以看到，MVVM最大的优势是编写前端逻辑非常复杂的页面，尤其是需要大量DOM操作的逻辑，利用MVVM可以极大地简化前端页面的逻辑。
    - 对于以展示逻辑为主的页面，例如，新闻，博客、文档等，不能使用MVVM展示数据，因为这些页面需要被搜索引擎索引，而搜索引擎无法获取使用MVVM并通过API加载的数据。
    - 所以，需要SEO（Search Engine Optimization）的页面，不能使用MVVM展示数据。不需要SEO的页面，如果前端逻辑复杂，就适合使用MVVM展示数据，例如，工具类页面，复杂的表单页面，用户登录后才能操作的页面等等。
