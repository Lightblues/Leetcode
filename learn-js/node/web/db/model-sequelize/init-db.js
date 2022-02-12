// require('babel-core/register')({
//     presets: ['stage-3']
// });

const model = require("./model.js");
try {
    model.sync();

    console.log("init db ok.");
    process.exit(0);
} catch (e) {
    console.log(e);
}
