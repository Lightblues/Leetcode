"use strict";

function testStandardObject() {
  typeof new Number(123); // 'object'
  new Number(123) === 123; // false

  typeof new Boolean(true); // 'object'
  new Boolean(true) === true; // false

  typeof new String("str"); // 'object'
  new String("str") === "str"; // false
}

function testDate() {
  var now = new Date();
  now; // Wed Jun 24 2015 19:49:22 GMT+0800 (CST)
  now.getFullYear(); // 2015, 年份
  now.getMonth(); // 5, 月份，注意月份范围是0~11，5表示六月
  now.getDate(); // 24, 表示24号
  now.getDay(); // 3, 表示星期三
  now.getHours(); // 19, 24小时制
  now.getMinutes(); // 49, 分钟
  now.getSeconds(); // 22, 秒
  now.getMilliseconds(); // 875, 毫秒数
  now.getTime(); // 1435146562875, 以number形式表示的时间戳
}

function dateParse() {
  var d = Date.parse("2015-06-24T19:49:22.875+08:00");
  console.log(d); // 1435146562875
  d = Date.parse("2021-2-9");
  var date = new Date(d);
  console.log(date);
}

function dateGetTime() {
  var d = new Date(1435146562875);
  var dLocal = d.toLocaleString(); // '2015/6/24 下午7:49:22'，本地时间（北京时区+8:00），显示的字符串与操作系统设定的格式有关
  var dUTC = d.toUTCString(); // 'Wed, 24 Jun 2015 11:49:22 GMT'，UTC时间，与本地时间相差8小时
  console.log(dLocal);
  console.log(dUTC);
}

function testRegExp() {
  // test
  var re = /^\d{3}\-\d{3,8}$/;
  console.log(re.test("010-12345"));

  //   exec, 返回一个列表, 第一个元素为完成匹配, 后面为分组的值; 若不匹配则返回null
  var re = /^(\d{3})-(\d{3,8})$/;
  re.exec("010-12345"); // ['010-12345', '010', '12345']
  re.exec("010 12345"); // null
}

function reEmail() {
  var re = /^[\w\d\.]+@\w+\.\w+$/;

  // 测试:
  var i,
    success = true,
    should_pass = [
      "someone@gmail.com",
      "bill.gates@microsoft.com",
      "tom@voyager.org",
      "bob2015@163.com",
    ],
    should_fail = [
      "test#gmail.com",
      "bill@microsoft",
      "bill%gates@ms.com",
      "@voyager.org",
    ];
  for (i = 0; i < should_pass.length; i++) {
    if (!re.test(should_pass[i])) {
      console.log("测试失败: " + should_pass[i]);
      success = false;
      break;
    }
  }
  for (i = 0; i < should_fail.length; i++) {
    if (re.test(should_fail[i])) {
      console.log("测试失败: " + should_fail[i]);
      success = false;
      break;
    }
  }
  if (success) {
    console.log("测试通过!");
  }
}

function reEmailV2() {
  // 版本二可以验证并提取出带名字的Email地址：
  var re = /^<([\w\ ]+)> ([\w\d\.]+@\w+\.\w+)$/;

  var r = re.exec("<Tom Paris> tom@voyager.org");
  console.log(r);
  if (
    r === null ||
    r.toString() !==
      ["<Tom Paris> tom@voyager.org", "Tom Paris", "tom@voyager.org"].toString()
  ) {
    console.log("测试失败!");
  } else {
    console.log("测试成功!");
  }
}

function testJson() {
  // 3. 自定义
  var xiaoming = {
    name: "小明",
    age: 14,
    gender: true,
    height: 1.65,
    grade: null,
    "middle-school": '"W3C" Middle School',
    skills: ["JavaScript", "Java", "Python", "Lisp"],
    toJSON: function () {
      return {
        // 只输出name和age，并且改变了key：
        Name: this.name,
        Age: this.age,
      };
    },
  };
  var s = JSON.stringify(xiaoming, ["Age"], "\t");
  console.log(s);

  delete xiaoming.toJSON;
  s = JSON.stringify(xiaoming, null, 4);
  console.log(s);
}

function getJSON() {
  var url =
    "https://api.openweathermap.org/data/2.5/forecast?q=Beijing,cn&appid=800f49846586c3ba6e7052cfc89af16c";
  $.getJSON(url, function (data) {
    var info = {
      city: data.city.name,
      weather: data.list[0].weather[0].main,
      time: data.list[0].dt_txt,
    };
    console.log(JSON.stringify(info, null, "  "));
  });
}

// dateParse();
// dateGetTime();
// testRegExp();
// reEmailV2();
// testJson();
getJSON();
