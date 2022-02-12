"use strict";

/* XMLHttpRequest */
function testXMLHttpRequest() {
    function success(text) {
        var textarea = document.getElementById("test-response-text");
        textarea.value = text;
    }
    function fail(code) {
        var textarea = document.getElementById("test-response-text");
        textarea.value = "Error code: " + code;
    }

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        // 状态发生变化时，函数被回调
        if (request.readyState === 4) {
            // 成功完成
            // 判断响应结果
            if (request.status === 200) {
                // // 成功，通过responseText拿到响应的文本:
                return success(request.responseText);
            } else {
                // 失败，根据响应码判断失败原因:
                return fail(request.status);
            }
        } else {
            // HTTP请求还在继续...
        }
    };
    // 发送请求:
    // request.open("GET", "/api/categories");
    request.open("GET", "http://www.sina.com.cn/");
    request.send();
    // alert("请求已发送，请等待响应...");
}

/* JSONP */
function refreshPrice(data) {
    var p = document.getElementById("test-jsonp");
    p.innerHTML =
        "当前价格：" +
        data["0000001"].name +
        ": " +
        data["0000001"].price +
        "；" +
        data["1399001"].name +
        ": " +
        data["1399001"].price;
}
function getPrice() {
    var js = document.createElement("script"),
        head = document.getElementsByTagName("head")[0];
    // 提前写好 callback !!
    js.src =
        "http://api.money.126.net/data/feed/0000001,1399001?callback=refreshPrice";
    head.appendChild(js);
}

/* 一个 CORS 例子 */
function getWeather() {
    // ERR: net::ERR_SSL_VERSION_OR_CIPHER_MISMATCH
    let url = "https://www.apiopen.top/weatherApi?city=";
    // let url = "https://api.apiopen.top/getImages";
    let city = document.getElementById("city");
    // 获取要查询的城市
    let newURL = url + city.value;
    console.log(newURL);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                return successWeather(xhr.responseText);
            } else {
                alert("失败！");
            }
        }
    };
    xhr.open("POST", newURL);
    xhr.send();
}
function getImage() {
    let url = "https://api.apiopen.top/getImages";
    // 获取要查询的城市
    let imageId = document.getElementById("imageId");
    console.log(url);
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                return successImage(xhr.responseText, imageId.value);
            } else {
                alert("失败！");
            }
        }
    };
    xhr.open("POST", url);
    xhr.send();
}

function successImage(data, id) {
    let image = document.getElementById("imageInfo");
    var imageInfo = JSON.parse(data);
    if (imageInfo.code === 200) {
        var url = imageInfo.result[id].img;
        // 图片跨域也失败了 !
        image.innerHTML =
            `图片ID：${id} + ；图片URL：${url}` + "<br>" + `<img src=${url}>`;
    } else {
        image.innerText = imageInfo.msg;
    }
}

function successWeather(data) {
    let weather = document.getElementById("weatherInfo");
    let weatherInfo = JSON.parse(data);
    if (weatherInfo.code === 200) {
        weather.innerHTML =
            "查询成功" +
            "<br>" +
            "当前城市：" +
            weatherInfo.data.city +
            "<br>" +
            "当前温度：" +
            weatherInfo.data.wendu +
            "<br>" +
            "气温：" +
            "最" +
            weatherInfo.data.forecast[0].high +
            "，最" +
            weatherInfo.data.forecast[0].low +
            "<br>" +
            "天气：" +
            weatherInfo.data.forecast[0].type +
            "<br>" +
            "风向：" +
            weatherInfo.data.forecast[0].fengxiang +
            weatherInfo.data.forecast[0].fengli +
            "<br>" +
            "注意：" +
            weatherInfo.data.ganmao;
    } else {
        weather.innerText = weatherInfo.msg;
    }
}

// testXMLHttpRequest();
