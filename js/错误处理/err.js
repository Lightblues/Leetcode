function testError() {
    var r1,
        r2,
        s = null;
    try {
        r2 = 1;
        r1 = s.length; // 此处应产生错误
        r2 = 100; // 该语句不会执行
    } catch (e) {
        console.log("出错了：" + e);
    } finally {
        console.log("finally");
    }
    console.log("r1 = " + r1); // r1应为undefined
    console.log("r2 = " + r2); // r2应为undefined
}

function testOn() {
    var $btn = $("#calc");

    // 取消已绑定的事件:
    $btn.off("click");

    $btn.click(function () {
        try {
            var x = parseFloat($("#x").val()),
                y = parseFloat($("#y").val()),
                r;
            if (isNaN(x) || isNaN(y)) {
                throw new Error("输入有误");
            }
            r = x + y;
            alert("计算结果：" + r);
        } catch (e) {
            alert("输入有误！", e);
        }
    });
}

// testError();
$(testOn);
