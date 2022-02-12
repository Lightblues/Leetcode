"use strict";

function testWindow() {
  // 可以调整浏览器窗口大小试试:
  console.log(
    "window inner size: " + window.innerWidth + " x " + window.innerHeight
  );
  console.log(window.outerWidth + " x " + window.outerHeight);
}

function testLocation() {
  if (confirm("重新加载当前页" + location.href + "?")) {
    location.reload();
  } else {
  }
  //   跳转
  // location.assign("."); // 设置一个新的URL地址
}

function testDocument() {
  // 获取文档的标题
  console.log(document.title);

  var menu = document.getElementById("drink-menu");
  console.log(menu);
  var drinks = document.getElementsByTagName("dt");
  var i, s;
  s = "提供的饮料:";
  for (i = 1; i < drinks.length; i++) {
    s += drinks[i].innerHTML + " ";
  }
  console.log(s);
}

// testWindow();
// testLocation();
// testDocument();
