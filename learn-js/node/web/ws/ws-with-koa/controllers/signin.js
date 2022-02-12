// sign in:

var index = 0;

module.exports = {
    "GET /signin": async (ctx, next) => {
        let names = "甲乙丙丁戊己庚辛壬癸";
        let name = names[index % 10];
        ctx.render("signin.html", {
            name: `路人${name}`,
        });
    },

    /* 新用户登陆, 构造 user 对象, 生成 base64 编码的 cookie */
    "POST /signin": async (ctx, next) => {
        index++;
        let name = ctx.request.body.name || "路人甲";
        let user = {
            id: index,
            name: name,
            image: index % 10,
        };
        let value = Buffer.from(JSON.stringify(user)).toString("base64");
        console.log(`Set cookie value: ${value}`);
        ctx.cookies.set("name", value);
        ctx.response.redirect("/"); // 重定向回首页
    },

    "GET /signout": async (ctx, next) => {
        ctx.cookies.set("name", "");
        ctx.response.redirect("/signin");
    },
};
