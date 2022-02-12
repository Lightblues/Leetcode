"use strict";

// alert
// var s = "Hello World";
// alert(s);

function useStrict() {
  // 不加 var 会报错
  var abc = "Hello, world";
  console.log(abc);
}

function typeOf() {
  console.log(typeof 43);
  console.log(67 instanceof Number);
}

function stringTest() {
  var s = `这是一个
多行
字符串`;
  console.log(s);

  //   ASCII
  s = "\x4156"; // 完全等同于 'A'
  s += "\u4e2d\u6587"; // 完全等同于 '中文'
  console.log(s);

  var name = "小明";
  var age = 20;
  s = `你好, ${name}, 你今年${age}岁了!`;
  console.log(s);
}

function stringManipulate() {
  var s = "Hello, world!";
  var lower = s.toLowerCase();
  console.log(s, lower);

  var substring = s.substring(1, 3);
  console.log(substring, "\n", s.substring(5));

  var index = s.indexOf("o");
  console.log(index);
}

function arrayShift() {
  var a = [1, 2];
  a.unshift("a", "b");
  a.push([1, 2]);
  var first = a.shift();
  console.log(first);
  console.log(a);
}

function objectBasic() {
  var xiaohong = {
    name: "小红",
    "middle-school": "No.1 Middle School",
  };

  xiaohong["middle-school"]; // 'No.1 Middle School'
  xiaohong["name"]; // '小红'
  xiaohong.name; // '小红'
  console.log(xiaohong["middle-school"]);
}

function controlIf() {
  var height = parseFloat(prompt("请输入身高(m):"));
  var weight = parseFloat(prompt("请输入体重(kg):"));
  var bmi = weight / (height * height);
  console.log(bmi);
}

function controlFor() {
  for (var i = 1; i <= 10; i++) {
    console.log(i);
  }
}

function controlForIn(params) {
  var o = {
    name: "Jack",
    age: 20,
    city: "Beijing",
  };
  for (var key in o) {
    console.log(key, o[key]);
  }

  //   Array 也是对象
  var a = ["A", 56, null];
  for (var i in a) {
    console.log(i, typeof i); // '0', '1', '2'
    console.log(a[i], typeof a[i]); // 'A', 'B', 'C'
  }
}

function testMap() {
  var m = new Map();
  m.set("name", "小明");
  m.set(1, "A");
  m.set(NaN, "B");
  m.set(null, undefined);
  console.log(m);
  console.log(m.get(null));

  // init, 只能用 Array 初始化 Map, 无法用 object
  var o = {
    1: "A",
    s2: "B",
  };
  var ll = [];
  for (var key in o) {
    ll.push([key, o[key]]);
  }
  var m1 = new Map(ll);
  console.log(m1);
  //   in 判断无效
  console.log(1 in o, "1" in o);
  console.log(1 in m1, "1" in m1);
}

function testSet() {
  var arr = [1, 2, 3, 3, "3"];
  var s = new Set(arr);
  console.log(s); // Set {1, 2, 3, "3"}
  console.log(s.has(1)); // true
  console.log(1 in s); // false
  console.log(1 in arr);
}

function testIterable() {
  var a = ["A", "B", "C"];
  var s = new Set(["A", "B", "C"]);
  var m = new Map([
    [1, "x"],
    [2, "y"],
    [3, "z"],
  ]);
  for (var x of a) {
    // 遍历Array
    console.log(x);
  }
  for (var x of s) {
    // 遍历Set
    console.log(x);
  }
  for (var x of m) {
    // 遍历Map
    console.log(x[0] + "=" + x[1]);
  }
}

function testIterableOf() {
  // 当我们手动给Array对象添加了额外的属性后，for ... in 循环将带来意想不到的意外效果
  var a = ["A", "B", "C"];
  a.name = "Hello";
  a.push(1);
  console.log(a);
  for (var x in a) {
    console.log(x); // '0', '1', '2', 'name'
  }
  // 此时用 for...of 就只会循环集合本身的元素
  for (var x of a) {
    console.log(x); // 'A', 'B', 'C'
  }
}

function testForEach() {
  // forEach Array
  var a = ["A", "B", "C"];
  a.forEach(function (element, index, array) {
    // element: 指向当前元素的值
    // index: 指向当前索引
    // array: 指向Array对象本身
    console.log(element + ", index = " + index);
  });
  // Set
  var s = new Set(["A", "B", "C"]);
  s.forEach(function (element, sameElement, set) {
    console.log(element, sameElement, set);
  });
  //Map
  var m = new Map([
    [1, "x"],
    [2, "y"],
    [3, "z"],
  ]);
  m.forEach(function (value, key, map) {
    console.log(key, value);
  });

  // 函数调用的参数可以多于设定数量
  var a = ["A", "B", "C"];
  a.forEach(function (element) {
    console.log(element);
  });
}

// useStrict();
// stringTest();
// stringManipulate();
// arrayShift();
// objectBasic();
// controlIf();
// controlFor();
// controlForIn();
// testMap();
// testSet();
// testIterable();
// testIterableOf();
testForEach();
