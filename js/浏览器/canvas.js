"use strict";

window.loadStockData = function (r) {
    var NUMS = 30,
        data = r.data;
    if (data.length > NUMS) {
        data = data.slice(data.length - NUMS);
    }
    data = data.map(function (x) {
        return {
            date: x[0],
            open: x[1],
            close: x[2],
            high: x[3],
            low: x[4],
            vol: x[5],
            change: x[6],
        };
    });
    window.drawStock(data);
};

window.drawStock = function (data) {
    var canvas = document.getElementById("stock-canvas"),
        width = canvas.width,
        height = canvas.height,
        ctx = canvas.getContext("2d"),
        colWidth = canvas.width / 30 / 1.5, // 矩形宽
        start, // 中心线起始位置
        spacing, // 中心线间隔
        max = data.map((x) => x.high).sort()[data.length - 1], // 最高价
        min = data.map((x) => x.low).sort()[0], // 最低价
        unitLen = canvas.height / (max - min), // 单位价格区间长度对应的坐标长度
        bottom = canvas.height; // 底部

    // 限制宽度和高度
    if (colWidth > 10) {
        colWidth = 10;
    }
    if (unitLen > 1) {
        bottom = (1 / unitLen) * bottom; // 使图像靠上
        unitLen = 1;
    }

    start = colWidth / 2;
    spacing = colWidth * 1.5;
    console.log(JSON.stringify(data[0])); // {"date":"20150602","open":4844.7,"close":4910.53,"high":4911.57,"low":4797.55,"vol":62374809900,"change":1.69}
    ctx.clearRect(0, 0, width, height);
    // ctx.fillText('Test Canvas', 10, 10);

    for (let i = 0; i < data.length; i++) {
        // 绘制中心线
        var path = new Path2D();
        let coord = start + spacing * i; // 中心线坐标
        path.moveTo(coord, bottom - (data[i].low - min) * unitLen);
        path.lineTo(coord, bottom - (data[i].high - min) * unitLen);
        ctx.strokeStyle = "black";
        ctx.stroke(path);

        // 绘制矩形
        let higher, lower;
        if (data[i].open < data[i].close) {
            ctx.fillStyle = "red";
            higher = data[i].close;
            lower = data[i].open;
        } else {
            ctx.fillStyle = "green";
            higher = data[i].open;
            lower = data[i].close;
        }
        ctx.fillRect(
            coord - colWidth / 2,
            bottom - (higher - min) * unitLen,
            colWidth,
            (higher - lower) * unitLen
        );
    }
};

function testDraw() {
    // 加载最近30个交易日的K线图数据:
    var js = document.createElement("script");
    js.src =
        "http://img1.money.126.net/data/hs/kline/day/history/2015/0000001.json?callback=loadStockData&t=" +
        Date.now();
    document.getElementsByTagName("head")[0].appendChild(js);
}
