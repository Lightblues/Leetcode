function testSetTimeout() {
    function callback() {
        console.log("Done");
    }
    console.log("before setTimeout()");
    setTimeout(callback, 1000); // 1秒钟后调用callback函数
    console.log("after setTimeout()");
}

/* Promise 示例 */
function testPromise() {
    // 清除log:
    var logging = document.getElementById("test-promise-log");
    while (logging.children.length > 1) {
        logging.removeChild(logging.children[logging.children.length - 1]);
    }
    // 输出log到页面:
    function log(s) {
        var p = document.createElement("p");
        p.innerHTML = s;
        logging.appendChild(p);
    }

    /* callback 函数, 注意参数为两个函数为 resolve 和 reject, 分别在 then 和 catch 中传入 */
    new Promise(function (resolve, reject) {
        log("start new Promise...");
        var timeOut = Math.random() * 2;
        log("set timeout to: " + timeOut + " seconds.");
        setTimeout(function () {
            if (timeOut < 1) {
                log("call resolve()...");
                resolve("200 OK");
            } else {
                log("call reject()...");
                reject("timeout in " + timeOut + " seconds.");
            }
        }, timeOut * 1000);
    })
        .then(function (r) {
            log("Done: " + r);
        })
        .catch(function (reason) {
            log("Failed: " + reason);
        });
    log("=== Next things here ===");
}

/* job1.then(job2).then(job3).catch(handleError); */
function testPromiseStack() {
    var logging = document.getElementById("test-promise2-log");
    while (logging.children.length > 1) {
        logging.removeChild(logging.children[logging.children.length - 1]);
    }

    function log(s) {
        var p = document.createElement("p");
        p.innerHTML = s;
        logging.appendChild(p);
    }

    // 0.5秒后返回input*input的计算结果:
    function multiply(input) {
        return new Promise(function (resolve, reject) {
            log("calculating " + input + " x " + input + "...");
            setTimeout(resolve, 500, input * input);
        });
    }
    // 0.5秒后返回input+input的计算结果:
    function add(input) {
        return new Promise(function (resolve, reject) {
            log("calculating " + input + " + " + input + "...");
            setTimeout(resolve, 500, input + input);
        });
    }
    var p = new Promise(function (resolve, reject) {
        log("start new Promise...");
        resolve(123);
    });

    p.then(multiply)
        .then(add)
        .then(multiply)
        .then(add)
        .then(function (result) {
            log("Got value: " + result);
        });
}

/* Promise.race([p1, p2]) */
function testPromiseRace() {
    var p1 = new Promise(function (resolve, reject) {
        // 这里 setTimeout 第三个参数以后是, Additional arguments which are passed through to the function specified by `function`.
        // from https://developer.mozilla.org/en-US/docs/Web/API/setTimeout
        setTimeout(resolve, 500, "P1");
    });
    var p2 = new Promise(function (resolve, reject) {
        setTimeout(resolve, 600, "P2");
    });
    Promise.race([p1, p2]).then(function (result) {
        console.log(result);
    });
}

/* 我们把上一节的AJAX异步执行函数转换为Promise对象，看看用Promise如何简化异步处理 */
// ajax函数将返回Promise对象:
function ajax(method, url, data) {
    var request = new XMLHttpRequest();
    return new Promise(function (resolve, reject) {
        request.onreadystatechange = function () {
            if (request.readyState === 4) {
                if (request.status === 200) {
                    resolve(request.responseText);
                } else {
                    reject(request.status);
                }
            }
        };
        request.open(method, url);
        request.send(data);
    });
}
function testAJAX() {
    var log = document.getElementById("test-promise-ajax-result");
    var p;
    // p = ajax("GET", "http://www.baidu.com");
    p = ajax("GET", "/test.json");

    p.then(function (text) {
        log.innerText = text;
    }).catch(function (status) {
        log.innerText = `Error: ${status}`;
    });
}

// testSetTimeout();

// 这些在 html 中响应
// testPromise();
// testPromiseStack()
// testAJAX()

// testPromiseRace();
