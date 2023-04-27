## jQuery

- 作用
    - 消除浏览器差异：你不需要自己写冗长的代码来针对不同的浏览器来绑定事件，编写AJAX等代码；
    - 简洁的操作DOM的方法：写`$('#test')`肯定比`document.getElementById('test')`来得简洁；
    - 轻松实现动画、修改CSS等各种操作。
- `$.fn.jquery` 查看版本
- `$` 符号
    - `$`是著名的jQuery符号。实际上，jQuery把所有功能全部封装在一个全局变量`jQuery`中，而`$`也是一个合法的变量名，它是变量`jQuery`的别名
    - `$`本质上就是一个函数，但是函数也是对象，于是`$`除了可以直接调用外，也可以有很多其他属性。

### 选择器

- 选择器是jQuery的核心。一个选择器写出来类似`$('#dom-id')`。
- 返回 jQuery 对象. jQuery对象类似数组，它的每个元素都是一个引用了DOM节点的对象。
    - 找不到时返回 `[]`, 因此 jQuery的选择器不会返回`undefined`或者`null`
- jQuery对象和DOM对象之间可以互相转化
    - 例如, 对于 `var div = $('#abc');` jQuery 对象
    - `var divDom = div.get(0);` 转为 DOM 对象.
    - `var another = $(divDom);` 将 DOM 对象转为 jQuery 对象
- 通常情况下你不需要获取DOM对象，直接使用jQuery对象更加方便
- 按ID查找, `#`
    - `var div = $('#abc');` 查找 `<div id="abc">`
- tag, 直接写 tag 名称
    - `var ps = $('p');` 返回所有 `<p>` 节点
    - `ps.length` 返回查找到的数量
- class, `.`
    - `var a = $('.red');` 所有节点包含`class="red"`都将返回, 也匹配 `<p class="green red">...</p>`
    - 查找多个 class: `var a = $('.red.green');`
- 属性, `[...="..."]`
    - `var email = $('[name=email]');`
    - 当属性的值包含空格等特殊字符时，需要用双引号括起来
    - 按属性查找还可以使用前缀查找或者后缀查找
    - `var icons = $('[class^="icon-"]');`
- 组合查找
    - `var emailInput = $('input[name=email]');` 筛选 name属性为 email 的 input 节点
- 多项选择器 `,`
    - `$('p.red,p.green');` 筛选 class 包含 red或green 的 p 节点
    - 要注意的是，选出来的元素是按照它们在HTML中出现的顺序排列的，而且不会有重复元素。例如，`<p class="red green">`不会被上面的`$('p.red,p.green')`选择两次。

```js
/* ID */
// 查找<div id="abc">:
var div = $('#abc');

/* tag */
var ps = $('p'); // 返回所有<p>节点
ps.length; // 数一数页面有多少个<p>节点

/* class */
var a = $('.red'); // 所有节点包含`class="red"`都将返回
// 例如:
// <div class="red">...</div>
// <p class="green red">...</p>

var a = $('.red.green'); // 注意没有空格！
// 符合条件的节点：
// <div class="red green">...</div>
// <div class="blue green red">...</div>

/* 属性 */
var email = $('[name=email]'); // 找出<??? name="email">
var passwordInput = $('[type=password]'); // 找出<??? type="password">
var a = $('[items="A B"]'); // 找出<??? items="A B">

// 按照前后缀匹配
var icons = $('[name^=icon]'); // 找出所有name属性值以icon开头的DOM
// 例如: name="icon-1", name="icon-2"
var names = $('[name$=with]'); // 找出所有name属性值以with结尾的DOM
// 例如: name="startswith", name="endswith"

// 这个方法尤其适合通过class属性查找，且不受class包含多个名称的影响
var icons = $('[class^="icon-"]'); // 找出所有class包含至少一个以`icon-`开头的DOM
// 例如: class="icon-clock", class="abc icon-home"

/* 组合查找 */
var emailInput = $('input[name=email]'); // 不会找出<div name="email">
// 根据tag和class来组合查找也很常见：
var tr = $('tr.red'); // 找出<tr class="red ...">...</tr>

/* $('p.red,p.green'); */
$('p,div'); // 把<p>和<div>都选出来
$('p.red,p.green'); // 把<p class="red">和<p class="green">都选出来
```

#### 层级选择器

- 层级选择器（Descendant Selector）
    - 用 `` 空格隔开, 具有层级关系的两个节点
    - 例如, `$('form[name=upload] input');` 筛选 name为upload 表单下的 input 节点
    - 也可以多层, `$('form.test p input');`
- 子选择器（Child Selector）
    - 限制为父子关系 `>`
    - `$('ul.lang>li.lang-javascript');`

##### 过滤器（Filter）

- 过滤器一般不单独使用，它通常附加在选择器上，帮助我们更精确地定位元素
    - `:` 后加筛选条件
    - `first-child, last-child, nth-child(2), nth-child(even)`
    - 例如 `$('ul.lang li:nth-child(odd)');` 选出序号为奇数的元素
- `:visible`, `:hidden` 选出可见的或隐藏的元素
    - 例如 `$('div:visible');`

针对表单元素，jQuery还有一组特殊的选择器：

- `:input`：可以选择`<input>`，`<textarea>`，`<select>`和`<button>`；
- `:file`：可以选择`<input type="file">`，和`input[type=file]`一样；
- `:checkbox`：可以选择复选框，和`input[type=checkbox]`一样；
- `:radio`：可以选择单选框，和`input[type=radio]`一样；
- `:focus`：可以选择当前输入焦点的元素，例如把光标放到一个`<input>`上，用`$('input:focus')`就可以选出；
- `:checked`：选择当前勾上的单选框和复选框，用这个选择器可以立刻获得用户选择的项目，如`$('input[type=radio]:checked')`；
- `:enabled`：可以选择可以正常输入的 `<input>`、`<select>` 等，也就是没有灰掉的输入；
- `:disabled`：和`:enabled`正好相反，选择那些不能输入的。

#### 查找和过滤

可以对 jQuery 进一步执行查找

- 最常见的查找是在某个节点的所有子节点中查找，使用`find()`方法，它本身又接收一个任意的选择器
    - `var dy = ul.find('.dy');` 在 ul 这个 jQuery 对象的子节点中查找 class 为 dy 的节点
- 如果要从当前节点开始向上查找，使用`parent()`方法
- 对于位于同一层级的节点，可以通过`next()`和`prev()`方法
    - 它们和 parent 方法都可以传入筛选条件, 若不符合则返回空 jQuery 对象

过滤

- `filter()`方法可以过滤掉不符合选择器条件的节点
    - 也可以传入一个函数，要特别注意函数内部的`this`被绑定为DOM对象，不是jQuery对象
- `map()`方法把一个jQuery对象包含的若干DOM节点转化为其他对象
- `irst()`、`last()`和`slice()`方法可以返回一个新的jQuery对象，把不需要的DOM节点去掉

```js
var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
langs.filter(function () {
    return this.innerHTML.indexOf('S') === 0; // 返回S开头的节点
}); // 拿到Swift, Scheme

var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
var arr = langs.map(function () {
    return this.innerHTML;
}).get(); // 用get()拿到包含string的Array：['JavaScript', 'Python', 'Swift', 'Scheme', 'Haskell']

var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
var js = langs.first(); // JavaScript，相当于$('ul.lang li:first-child')
var haskell = langs.last(); // Haskell, 相当于$('ul.lang li:last-child')
var sub = langs.slice(2, 4); // Swift, Scheme, 参数和数组的slice()方法一致

```

### 操作 DOM

- 一个jQuery对象可以包含0个或任意个DOM对象，它的方法实际上会作用在对应的每个DOM节点上。
- jQuery对象的所有方法都返回一个jQuery对象（可能是新的也可能是自身），这样我们可以进行链式调用，非常方便
- 修改文本
    - jQuery对象的`text()`和`html()`方法分别获取节点的文本和原始HTML文本
- 修改 CSS
    - style 属性: `css` 方法
        - 调用jQuery对象的`css('name', 'value')`方法
        - `$('#test-css li.dy>span').css('background-color', '#ffd351').css('color', 'red');` 设置相应节点的 background-color, color 两个CSS属性
        - 为了和JavaScript保持一致，CSS属性可以用`'background-color'`和`'backgroundColor'`两种格式。
    - class 属性
        - `hasClass(), addClass(), removeClass()`

```js
var div = $('#test-div');
div.css('color'); // '#000033', 获取CSS属性
div.css('color', '#336699'); // 设置CSS属性
div.css('color', ''); // 清除CSS属性

var div = $('#test-div');
div.hasClass('highlight'); // false， class是否包含highlight
div.addClass('highlight'); // 添加highlight这个class
div.removeClass('highlight'); // 删除highlight这个class
```

### 事件

- 鼠标事件
    - `click`: 鼠标单击时触发；
    - dblclick：鼠标双击时触发；
    - `mouseenter`：鼠标进入时触发；
    - mouseleave：鼠标移出时触发；
    - mousemove：鼠标在DOM内部移动时触发；
    - `hover`：鼠标进入和退出时触发两个函数，相当于mouseenter加上mouseleave。
- 键盘事件
    - 键盘事件仅作用在当前焦点的DOM上，通常是`<input>`和`<textarea>`。
    - `keydown`：键盘按下时触发；
    - keyup：键盘松开时触发；
    - `keypress`：按一次键后触发。
- 其他事件
    - `focus`：当DOM获得焦点时触发；
    - `blur`：当DOM失去焦点时触发；
    - `change`：当`<input>`、`<select>`或`<textarea>`的内容改变时触发；
    - `submit`：当`<form>`提交时触发；
    - `ready`：当页面被载入并且DOM树完成初始化后触发。
        - `ready`仅作用于`document`对象。由于`ready`事件在DOM完成初始化后触发，且只触发一次，所以非常适合用来写其他的初始化代码

#### ready

- 比如, 要在 head 里设置 DOM 的某个事件监听, 由于 DOM 还没有初始化, 是找不到的
- 因此需要 `$(document).on('ready', function () {})` 设置当页面初始化之后再来绑定事件
    - 例如绑定到一个 form 节点上设置 submit 后要执行的 `$('#testForm).on('submit', function () {})`
- 由于 ready 事件非常普遍, 可以简写
    - `$(document).ready(f)`
    - 甚至直接 `$(f)`, 也即, 在 `$()` 中传入回调函数
- 可以反复绑定事件处理函数，它们会依次执行

```js
// $(document).on('ready', function () {
// $(document).ready(function () {
$(document).ready(function () {
    // on('submit', function)也可以简化:
    $('#testForm).submit(function () {
        alert('submit!');
    });
});
```

#### 事件参数

- 有些事件，如`mousemove`和`keypress`，我们需要获取鼠标位置和按键的值，否则监听这些事件就没什么意义了。所有事件都会传入`Event`对象作为参数，可以从`Event`对象上获取到更多的信息

```js
// 设置当鼠标在 testMouseMoveDiv 这一节点中移动时, 捕捉鼠标位置并显示
// 注意回调函数接受了 Event 对象
$(function () {
    $('#testMouseMoveDiv').mousemove(function (e) {
        $('#testMouseMoveSpan').text('pageX = ' + e.pageX + ', pageY = ' + e.pageY);
    });
});
```

#### 取消绑定

- 要取消绑定一个特定的回调函数, `off('click', function)`
- `off('click')`一次性移除已绑定的`click`事件的所有处理函数
- 无参数调用`off()`一次性移除已绑定的所有类型的事件处理函数

#### 事件触发条件

- 事件的触发总是由用户操作引发的
- 因此, 用代码修改的时候无法触发
- `trigger()` 方法
    - 有些时候，我们希望用代码触发事件
    - 可以用 `trigger('change')` 触发
    - 或者是简写, 无参数的`change()`方法来触发 change 事件

```js
// 绑定事件, 监听用户输入
var input = $('#test-input');
input.change(function () {
    console.log('changed...');
});

var input = $('#test-input');
input.val('change it!'); // 这样通过 js 修改无法触发事件
// 下面手动触发
input.trigger('change') // or
input.change(); // 触发change事件
```

例子: 对于一组 checkbox, 利用 jQuery 事件监听 实现一个「全选/全不选」选项, 以及「反选」, 需要注意各个选项之间的逻辑关系

### 动画

[here](https://www.liaoxuefeng.com/wiki/1022910821149312/1023023579162208)

### AJAX

- 可以通过 `$.ajax(url, settings)` 处理 AJAX 请求
    - settings 中的选项包括 `method, contentType, data, headers, dataType` 等
    - 通过 `done, fail, always` 方法来进行类似 Promise 的处理
- 对于常用的请求, 可以简写成 `$.get(rul, paras)` `$.post(url, paras)`
    - `$.getJSON(url, paras)` 快速通过GET获取一个JSON对象
- jQuery的AJAX完全封装的是JavaScript的AJAX操作，所以它的安全限制和前面讲的用JavaScript写AJAX完全一样
    - 如果需要使用JSONP，可以在`ajax()`中设置`jsonp: 'callback'`

jQuery在全局对象`jQuery`（也就是`$`）绑定了`ajax()`函数，可以处理AJAX请求。`ajax(url, settings)`函数需要接收一个URL和一个可选的`settings`对象，常用的选项如下：

- async：是否异步执行AJAX请求，默认为`true`，千万不要指定为`false`；
- method：发送的Method，缺省为`'GET'`，可指定为`'POST'`、`'PUT'`等；
- contentType：发送POST请求的格式，默认值为`'application/x-www-form-urlencoded; charset=UTF-8'`，也可以指定为`text/plain`、`application/json`；
- data：发送的数据，可以是字符串、数组或object。如果是GET请求，data将被转换成query附加到URL上，如果是POST请求，根据contentType把data序列化成合适的格式；
- headers：发送的额外的HTTP头，必须是一个object；
- dataType：接收的数据格式，可以指定为`'html'`、`'xml'`、`'json'`、`'text'`等，缺省情况下根据响应的`Content-Type`猜测。

jQuery的jqXHR对象类似一个Promise对象，我们可以用链式写法来处理各种回调

- `.done`
- `.fail`
- `.always`

```js
function ajaxLog(s) {
    var txt = $("#test-response-text");
    txt.val(txt.val() + "\n" + s);
}
$("#test-response-text").val("");

// 返回的是 xhr 对象
var jqxhr = $.ajax("/api/categories", {
    dataType: "json",
})
    .done(function (data) {
        ajaxLog("成功, 收到的数据: " + JSON.stringify(data));
    })
    .fail(function (xhr, status) {
        ajaxLog("失败: " + xhr.status + ", 原因: " + status);
    })
    .always(function () {
        ajaxLog("请求完成: 无论成功或失败都会调用");
    });
```

- 对常用的AJAX操作，jQuery提供了一些辅助方法
    - get
        - 第二个参数如果是object，jQuery自动把它变成query string然后加到URL后面
        - 这样我们就不用关心如何用URL编码并构造一个query string了。
    - post
        - 传入的第二个参数默认被序列化为`application/x-www-form-urlencoded`
        - 作为POST的body被发送
    - getJSON

```js
var jqxhr = $.get('/path/to/resource', {
    name: 'Bob Lee',
    check: 1
});
// 实际的 URL 是 /path/to/resource?name=Bob%20Lee&check=1

var jqxhr = $.post('/path/to/resource', {
    name: 'Bob Lee',
    check: 1
});
// 构造成 name=Bob%20Lee&check=1 作为POST的body被发送

var jqxhr = $.getJSON('/path/to/resource', {
    name: 'Bob Lee',
    check: 1
}).done(function (data) {
    // data已经被解析为JSON对象了
});
```

### 插件

我们得出编写一个jQuery插件的原则：

1. 给 `$.fn` 绑定函数，实现插件的代码逻辑；
2. 插件函数最后要 `return this;` 以支持链式调用；
3. 插件函数要有默认值，绑定在 `$.fn.<pluginName>.defaults` 上；
   1. 通过 `$.extend(target, obj1, obj2, ...)` 来合并后续 obj 的属性到 target 中
4. 用户在调用时可传入设定值以便覆盖默认值。

```js
$.fn.highlight = function (options) {
    // 合并默认值和用户设定值:
    var opts = $.extend({}, $.fn.highlight.defaults, options);
    this.css('backgroundColor', opts.backgroundColor).css('color', opts.color);
    return this;
}
// 设定默认值:
$.fn.highlight.defaults = {
    color: '#d85030',
    backgroundColor: '#fff8de'
}

// 用户自行设置默认值
$.fn.highlight.defaults.color = '#659f13';
$.fn.highlight.defaults.backgroundColor = '#f2fae3';
// 调用
$('#test-highlight p:first-child span').highlight();
// 调用的时候也支持传入 opt
$('#test-highlight p:last-child span').highlight({
    color: '#dd1144'
});
```

若要对于特定的元素进行拓展, 可以用 `filter` 方法进行过滤
