function testSelector() {
    var selected = null;
    selected = $("#para-1");
    selected = $(".color-red.color-green");
    selected = $("#para-1,.color-red.color-green");
    selected = $("[class^=color-]");
    selected = $("input[name=name]");
    selected = $("input[name=name],input[name=email]");
    // 高亮结果:
    if (!(selected instanceof jQuery)) {
        return console.log("不是有效的jQuery对象!");
    }
    $("#test-jquery").find("*").css("background-color", "");
    selected.css("background-color", "#ffd351");
}

function taskForm() {
    var json = null;
    json = {};
    // 利用和表单元素相关的特殊选择器
    // 理解filter和map的机制
    $("#test-form :input")
        .not("button")
        .filter(function () {
            //console.log(this.type);
            return this.type !== "radio" || this.checked;
        })
        .map(function () {
            json[this.name] = this.value;
            return true;
        });

    json = JSON.stringify(json);

    // 显示结果:
    if (typeof json === "string") {
        console.log(json);
    } else {
        console.log("json变量不是string!");
    }
}

/* 例子: 对于一组 checkbox, 利用 jQuery 事件监听 实现一个「全选/全不选」选项, 以及「反选」, 需要注意各个选项之间的逻辑关系

绑定合适的事件处理函数，实现以下逻辑：

当用户勾上“全选”时，自动选中所有语言，并把“全选”变成“全不选”；
当用户去掉“全不选”时，自动不选中所有语言；
当用户点击“反选”时，自动把所有语言状态反转（选中的变为未选，未选的变为选中）；
当用户把所有语言都手动勾上时，“全选”被自动勾上，并变为“全不选”；
当用户手动去掉选中至少一种语言时，“全不选”自动被去掉选中，并变为“全选”。 */
function testCheckbox() {
    var form = $("#test-form-2"),
        langs = form.find("[name=lang]"),
        selectAll = form.find("label.selectAll :checkbox"),
        selectAllLabel = form.find("label.selectAll span.selectAll"),
        deselectAllLabel = form.find("label.selectAll span.deselectAll"),
        invertSelect = form.find("a.invertSelect");

    // 重置初始化状态:
    form.find("*").show().off();
    form.find(":checkbox").prop("checked", false).off();
    deselectAllLabel.hide();
    // 拦截form提交事件:
    form.off().submit(function (e) {
        e.preventDefault();
        alert(form.serialize());
    });

    /* 筛选逻辑: 1. 当没有全部勾选时, 显示「全选」, 点击后变为「全不选」; 2. 全部勾选时显示「全不选」, 点击后改变 */
    selectAll.click(() => {
        if (selectAllLabel.is(":visible")) {
            deselectAllLabel.show();
            selectAllLabel.hide();
            langs.prop(`checked`, true);
        } else {
            deselectAllLabel.hide();
            selectAllLabel.show();
            langs.prop("checked", false);
        }
    });
    /* 监听各个子选项. 根据条件判断 selectAll 应该显示什么 */
    langs.change(() => {
        if (langs.get().every((lang) => lang.checked)) {
            selectAll.prop("checked", true);
            deselectAllLabel.show();
            selectAllLabel.hide();
        } else {
            selectAll.prop("checked", false);
            deselectAllLabel.hide();
            selectAllLabel.show();
        }
    });
    /* 反选逻辑: 反转 checked, 然后触发 langs.change() */
    invertSelect.click(() => {
        langs.each(function () {
            // 注意, 当使用箭头函数时, this 指向的 window !
            // 这里的 this 是 DOM 对象，不是 jQuery 对象
            // console.log(this);
            // console.log(this.checked);
            // $(this) 将 this 转为 jQuery 对象.
            // 要修改 checked 状态, 1. 可以用 回调函数; 2. 直接利用 DOM 的 checked 属性.
            $(this).prop("checked", !this.checked);
            // $(this).prop("checked", (x, y) => !y);
        });
        langs.change();
    });
}
// ready 后执行
$(testCheckbox);

function testAjax() {
    function ajaxLog(s) {
        var txt = $("#test-response-text");
        txt.val(txt.val() + "\n" + s);
    }
    $("#test-response-text").val("");
    // ajaxLog("test");

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

    console.log(jqxhr);
}

/* 拓展 jQuery 函数
filter 针对特定元素的扩展 */
$.fn.external = function () {
    // return返回的each()返回结果，支持链式调用:
    return this.filter("a").each(function () {
        // 注意: each()内部的回调函数的this绑定为DOM本身!
        var a = $(this);
        var url = a.attr("href");
        if (
            url &&
            (url.indexOf("http://") === 0 || url.indexOf("https://") === 0)
        ) {
            a.attr("href", "#0")
                .removeAttr("target")
                .append(' <i class="uk-icon-external-link"></i>')
                .click(function () {
                    if (confirm("你确定要前往" + url + "？")) {
                        window.open(url);
                    }
                });
        }
    });
};
function testJqueryExtends() {
    $("#test-external a").external();
}
