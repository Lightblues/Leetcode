/*
主文件
这里实现了搜索
引用的三个文件分别检查了 现有索引、简单搜索、搜索特定关键词
*/

// index.js
const express = require('express');
const elasticsearch = require('elasticsearch');
const fs = require('fs');
const app = express();

const PORT = 5000;
const verify = require('./verify');
const searchData = require('./search')
const searchTerm = require('./search_term')

const client = new elasticsearch.Client({
    host: '127.0.0.1:9200',
    log: 'error'
});

client.ping({ requestTimeout: 30000 }, error => {
    if (error) {
        console.error('elasticsearch cluster is down!');
    } else {
        console.log('Everything is OK');
    }
});

const bulkIndex = (index, type, data) => {
    let bulkBody = [];
    data.forEach( item => {
        bulkBody.push({
            index: {
                _index: index,
                _type: type,
                _id: item.id
            }
        });
        bulkBody.push(item);
    });

    client.bulk({body: bulkBody})
        .then( response => {
            let errCount = 0;
            response.items.forEach(item => {
                if (item.index && item.index.error) {
                    console.log(++errCount, item.index.error);
                }
            });
            console.log(
                `Successfully indexed ${data.length - errCount} out of ${data.length} items`
            );
        })
        .catch(console.err);
}

const indexData = async () => {
    const twitterRaw = await fs.readFileSync("./data.json");
    const twitters = JSON.parse(twitterRaw);
    console.log(`${twitters.length} items parsed form data file`);
    bulkIndex("twitter2", "_doc", twitters);
};

// 这里好像不应该用异步？如何顺序执行？
(async () => {
    // await indexData();
    // await verify();
    await searchData();
    // await searchTerm();
})();


// app.listen(PORT, function() {
//     console.log('Server is running on PORT:', PORT);
//     console.log(`http://localhost:${PORT}`)
// });
