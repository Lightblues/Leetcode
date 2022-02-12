const crypto = require("crypto");

// aes192，aes-128-ecb，aes-256-cbc
function aesEncrypt(data, key) {
    const cipher = crypto.createCipher("aes192", key);
    var crypted = cipher.update(data, "utf8", "hex");
    crypted += cipher.final("hex");
    return crypted;
}

function aesDecrypt(encrypted, key) {
    const decipher = crypto.createDecipher("aes192", key);
    var decrypted = decipher.update(encrypted, "hex", "utf8");
    decrypted += decipher.final("utf8");
    return decrypted;
}

const data = "Hello, this is a secret message!";
const key = "Password!";
var encrypted = aesEncrypt(data, key);
var decrypted = aesDecrypt(encrypted, key);

console.log("Plain text: " + data);
console.log("Encrypted text: " + encrypted);
console.log("Decrypted text: " + decrypted);
