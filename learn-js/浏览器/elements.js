function taskGet() {
    /* 1. 采用 get */
    // 选择<p>JavaScript</p>:
    var js = document.getElementById("test-p");

    // 选择<p>Python</p>,<p>Ruby</p>,<p>Swift</p>:
    var div = document.getElementById("test-div");
    var arr1 = div.getElementsByClassName("c-red c-green")[0];
    //   console.log(arr1);
    var arr = arr1.getElementsByTagName("p");

    // 选择<p>Haskell</p>:
    // var arr2 = div.getElementsByClassName("c-green")[0];
    var green = div.lastElementChild;
    // console.log(green);
    var haskell = green.lastElementChild;

    /* 2. 用selector */
    js = document.querySelector("#test-p");
    // 选择 class 为 c-red c-green 的元素, 的所有 p 子节点
    arr = document.querySelectorAll("#test-div .c-red.c-green p");
    // 选择 id 为 test-div 元素的最后一个 div 子节点, 的最后一个 p 子节点
    haskell = document.querySelector("#test-div div:last-child p:last-child");

    // 测试:
    if (!js || js.innerText !== "JavaScript") {
        alert("选择JavaScript失败!");
    } else if (
        !arr ||
        arr.length !== 3 ||
        !arr[0] ||
        !arr[1] ||
        !arr[2] ||
        arr[0].innerText !== "Python" ||
        arr[1].innerText !== "Ruby" ||
        arr[2].innerText !== "Swift"
    ) {
        console.log("选择Python,Ruby,Swift失败!");
    } else if (!haskell || haskell.innerText !== "Haskell") {
        console.log("选择Haskell失败!");
    } else {
        console.log("测试通过!");
    }
}

function update() {
    // 1. 修改 innerHTML
    // 获取<p id="p-id">...</p>
    var p = document.getElementById("p-id");
    // 设置文本为abc:
    p.innerHTML = "ABC"; // <p id="p-id">ABC</p>
    // 设置HTML:
    p.innerHTML = 'ABC <div><span style="color:red">RED</span></div> XYZ';
    // <p>...</p>的内部结构已修改

    // // 2. 修改 innerText
    // // 获取<p id="p-id">...</p>
    // var p = document.getElementById("p-id");
    // // 设置文本:
    // p.innerText = '<script>alert("Hi")</script>';
    // // HTML被自动编码，无法设置一个<script>节点:
    // // <p id="p-id">&lt;script&gt;alert("Hi")&lt;/script&gt;</p>
}

function updateCSS() {
    // CSS
    // 获取<p id="p-id">...</p>
    var p = document.getElementById("p-id");
    // 设置CSS:
    p.style.color = "#ff0000";
    p.style.fontSize = "20px";
    p.style.paddingTop = "2em";
}

function taskUpdate() {
    // 获取<p>javascript</p>节点:
    var js = document.querySelector("#test-js");

    // 修改文本为JavaScript:
    js.innerText = "JavaScript";

    // 修改CSS为: color: #ff0000, font-weight: bold
    js.style.color = "#Ff0000";
    js.style.fontWeight = "bold";

    // 测试:
    if (
        js &&
        js.parentNode &&
        js.parentNode.id === "test-div" &&
        js.id === "test-js"
    ) {
        if (js.innerText === "JavaScript") {
            if (
                js.style &&
                js.style.fontWeight === "bold" &&
                (js.style.color === "red" ||
                    js.style.color === "#ff0000" ||
                    js.style.color === "#f00" ||
                    js.style.color === "rgb(255, 0, 0)")
            ) {
                console.log("测试通过!");
            } else {
                console.log("CSS样式测试失败!");
            }
        } else {
            console.log("文本测试失败!");
        }
    } else {
        console.log("节点测试失败!");
    }
}

function insert() {
    // 移动原有的 node
    var js = document.getElementById("js"),
        list = document.getElementById("list");
    list.appendChild(js);

    // 新建
    var haskell = document.createElement("p");
    haskell.id = "haskell";
    haskell.innerText = "Haskell";
    list.appendChild(haskell);
}

function taskInsert() {
    // sort list:
    /* 方案一: 直接对children排序再导入 */
    var list = document.getElementById("test-list");
    // 1.1 指定比较函数
    // var sorted = Array.from(list.children).sort((a, b) =>
    //     a.innerText < b.innerText ? -1 : 1
    // );
    // 1.2 使用 localeCompare
    var sorted = Array.from(list.children).sort((a, b) =>
        a.innerText.localeCompare(b.innerText)
    );
    for (let e of sorted) {
        list.appendChild(e);
    }

    /* 方案二: 先提取文本，对文本排序再逐一写入 */
    var list = Array.from(document.getElementById("test-list").children);
    var sorted = list.map((e) => e.innerText).sort();
    list.map((element, index) => {
        element.innerText = sorted[index];
    });

    // 测试:
    (function () {
        var arr,
            i,
            t = document.getElementById("test-list");
        if (t && t.children && t.children.length === 5) {
            arr = [];
            for (i = 0; i < t.children.length; i++) {
                arr.push(t.children[i].innerText);
            }
            if (
                arr.toString() ===
                ["Haskell", "JavaScript", "Python", "Ruby", "Scheme"].toString()
            ) {
                console.log("测试通过!");
            } else {
                console.log("测试失败: " + arr.toString());
            }
        } else {
            console.log("测试失败!");
        }
    })();
}

function taskRemove() {
    var related = ["JavaScript", "HTML", "CSS"];
    var parent = document.getElementById("test-list");
    var list = Array.from(parent.children);
    // 注意, 这里遍历 parent.children 会出错? 因为 children 返回的不是 Array 类型
    for (let e of list) {
        if (!related.includes(e.innerText)) {
            console.log("remove", e.innerText);
            parent.removeChild(e);
        }
    }
}

// taskGet();
// update();
// taskUpdate();
// insert();
// taskInsert();
// taskRemove();
