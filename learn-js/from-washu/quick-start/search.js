/*
搜索
*/

const elasticsearch = require('elasticsearch');

const client = new elasticsearch.Client({
    host: "localhost:9200",
    log: 'error'
});

// 两个参数：1 index 名称；2 查询的 DSL body
function search(index, body) {
    return client.search( {index: index, body: body} );
}

module.exports = function searchData() {
    let body = {
        size: 4,
        from: 0,
        query: {
            match_all: {}
        }
    };

    search('twitter2', body)
        .then(results => {
            console.log(`found ${results.hits.total} items in ${results.took}ms`);
            console.log(`returned twitters:`);
            results.hits.hits.forEach(
                (hit, index) => console.log(hit._source)
            );
        })
        .catch(console.error);
}
