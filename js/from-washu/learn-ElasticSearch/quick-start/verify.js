/*
通过 elasticsearch 的方法来把我们的录入的数据读出来
*/

const elasticsearch = require('elasticsearch');

const client = new elasticsearch.Client({
    host: "localhost:9200",
    log: 'error'
});

function indices() {
    return client.cat.indices({v: true})
        .then(console.log)
        .catch( err => {
            console.error(`Error connection to the es client ${err}`)
        });
}


module.exports = function verify() {
    console.log(`elasticsearch indices information: `);
    indices();
}
