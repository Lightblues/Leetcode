module.exports = {
    APIError: function (code, message) {
        this.code = code || "internal:unknown_error";
        this.message = message || "";
    },
    restify: (pathPrefix) => {
        // REST API前缀，默认为/api/:
        pathPrefix = pathPrefix || "/api/";
        return async (ctx, next) => {
            // 是否是REST API前缀?
            if (ctx.request.path.startsWith(pathPrefix)) {
                // 绑定rest()方法:
                console.log(
                    `Process API ${ctx.request.method} ${ctx.request.url}...`
                );
                ctx.rest = (data) => {
                    ctx.response.type = "application/json";
                    ctx.response.body = data;
                };
                try {
                    await next();
                } catch (e) {
                    console.log("Process API error...");
                    ctx.response.status = 400;
                    ctx.response.type = "application/json";
                    ctx.response.body = {
                        code: e.code || "internal:unknown_error",
                        message: e.message || "",
                    };
                }
            } else {
                // 这里仅处理 /api 开头的请求, 对于其他的请求, 直接 next 跳过
                await next();
            }
        };
    },
};
