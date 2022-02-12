// client test:

const WebSocket = require("ws");

let count = 0;

let ws = new WebSocket("ws://127.0.0.1:3000/ws/chat");

ws.on("open", function () {
    console.log(`[CLIENT] open()`);
    ws.send("Hello!");
});

ws.on("message", function (message) {
    console.log(`[CLIENT] Received: ${message}`);
    count++;
    if (count > 3) {
        ws.send("Goodbye!");
        ws.close();
    } else {
        setTimeout(() => {
            ws.send(`Hello, I'm Mr No.${count}!`);
        }, 1000);
    }
});
